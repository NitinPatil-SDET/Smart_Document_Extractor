"""LLM-based document field extractor using the Groq OpenAI-compatible API."""

import requests
import json
from typing import Dict, List, Optional, Any
from utils.logger import logger
from utils.helpers import safe_json_loads
from utils.prompts import build_extraction_prompt, build_retry_prompt, SYSTEM_PROMPT


class DocumentExtractor:
    """
    Extract document fields using the Groq chat completions API.
    """
    
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 300):
        """
        Initialize document extractor.
        
        Args:
            base_url: Base URL of the Groq OpenAI-compatible API
            api_key: Groq API key
            model: LLM model name to use
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.logger = logger
        self.max_retries = 3
    
    def check_connection(self) -> bool:
        """
        Check if the Groq API is accessible and the API key is valid.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            self.logger.info("Groq API is accessible")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Groq API connection failed: {e}")
            return False
    
    def check_model_available(self) -> bool:
        """
        Check if specified model is available in Groq.
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                models = [m.get("id", "") for m in data.get("data", [])]

                if self.model in models:
                    self.logger.info(f"Model {self.model} is available")
                    return True
            
            self.logger.warning(f"Model {self.model} not found. Available models: {models}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking model availability: {e}")
            return False
    
    def extract_fields(self, pdf_text: str, fields: List[str]) -> Optional[Dict[str, Any]]:
        """
        Extract specified fields from PDF text using LLM.
        
        Args:
            pdf_text: Extracted text from PDF
            fields: List of field names to extract
            
        Returns:
            Dictionary with extracted fields or None if failed
        """
        if not pdf_text or not fields:
            self.logger.error("PDF text or fields list is empty")
            return None
        
        self.logger.info(f"Extracting {len(fields)} fields from PDF")
        
        # Build prompt
        prompt = build_extraction_prompt(pdf_text, fields)
        
        # Try extraction with retries
        for attempt in range(1, self.max_retries + 1):
            self.logger.info(f"Extraction attempt {attempt}/{self.max_retries}")
            
            response_text = self._call_groq(prompt)
            
            if response_text is None:
                if attempt < self.max_retries:
                    self.logger.warning(f"Attempt {attempt} failed, retrying...")
                    continue
                else:
                    self.logger.error("All extraction attempts failed")
                    return None
            
            # Parse JSON response
            extracted_data = safe_json_loads(response_text)
            
            if extracted_data is not None:
                # Validate result
                if self.validate_json(extracted_data, fields):
                    self.logger.info("Extraction successful")
                    return extracted_data
            
            # If validation failed and we have retries left, try again with retry prompt
            if attempt < self.max_retries:
                self.logger.warning(f"Invalid JSON response, retry attempt {attempt}")
                prompt = build_retry_prompt(pdf_text, fields, response_text or "")
                continue
        
        self.logger.error("Failed to extract valid JSON after all attempts")
        return None
    
    def validate_json(self, data: Dict[str, Any], fields: List[str]) -> bool:
        """
        Validate extracted JSON has required structure.
        
        Args:
            data: Extracted data dictionary
            fields: List of expected field names
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(data, dict):
            self.logger.error("Extracted data is not a dictionary")
            return False
        
        # Check if all required fields are present
        for field in fields:
            if field not in data:
                self.logger.error(f"Missing field in extraction: {field}")
                return False
        
        self.logger.debug("JSON validation passed")
        return True
    
    def _call_groq(self, prompt: str) -> Optional[str]:
        """
        Call Groq's OpenAI-compatible chat completions API.
        
        Args:
            prompt: The prompt to send to LLM
            
        Returns:
            LLM response text or None if failed
        """
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                choices = result.get("choices", [])
                response_text = (
                    choices[0].get("message", {}).get("content", "").strip()
                    if choices else ""
                )
                
                if response_text:
                    self.logger.debug(f"Groq response received: {len(response_text)} characters")
                    return response_text
                else:
                    self.logger.warning("Empty response from Groq")
                    return None
            else:
                self.logger.error(f"Groq API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error("Groq request timeout")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Groq request failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error calling Groq: {e}")
            return None
    
    def retry_extraction(self, pdf_text: str, fields: List[str], 
                        previous_response: str) -> Optional[Dict[str, Any]]:
        """
        Retry extraction with improved prompt after failure.
        
        Args:
            pdf_text: Extracted text from PDF
            fields: List of field names to extract
            previous_response: The invalid response to learn from
            
        Returns:
            Dictionary with extracted fields or None if failed
        """
        self.logger.info("Starting retry extraction with enhanced prompt")
        
        # Build retry prompt
        prompt = build_retry_prompt(pdf_text, fields, previous_response)
        
        # Call Ollama
        response_text = self._call_groq(prompt)
        
        if response_text is None:
            self.logger.error("Retry extraction failed")
            return None
        
        # Parse and validate
        extracted_data = safe_json_loads(response_text)
        
        if extracted_data and self.validate_json(extracted_data, fields):
            self.logger.info("Retry extraction successful")
            return extracted_data
        
        self.logger.error("Retry extraction did not produce valid JSON")
        return None
