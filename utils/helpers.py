"""
Helper utilities for Smart Document Extractor.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from utils.logger import logger


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace and special characters.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special control characters but keep useful ones
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def save_uploaded_file(uploaded_file, upload_dir: str = "uploads") -> Optional[Path]:
    """
    Save uploaded file to disk.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        upload_dir: Directory to save uploads
        
    Returns:
        Path to saved file or None if failed
    """
    try:
        upload_path = Path(upload_dir)
        upload_path.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_path / uploaded_file.name
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        logger.info(f"File saved: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Failed to save uploaded file: {e}")
        return None


def safe_json_loads(json_string: str) -> Optional[Dict[str, Any]]:
    """
    Safely load JSON string with error handling.
    
    Args:
        json_string: JSON string to parse
        
    Returns:
        Parsed dictionary or None if invalid JSON
    """
    try:
        # Remove common markdown artifacts
        json_string = json_string.strip()
        if json_string.startswith("```"):
            json_string = json_string.split("```")[1]
            if json_string.startswith("json"):
                json_string = json_string[4:]
        if json_string.endswith("```"):
            json_string = json_string[:-3]
        
        json_string = json_string.strip()
        
        # Parse JSON
        data = json.loads(json_string)
        
        if not isinstance(data, dict):
            logger.warning("Loaded JSON is not a dictionary")
            return None
        
        logger.debug("JSON parsed successfully")
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        return None


def validate_extraction_result(data: Dict[str, Any], required_fields: list) -> bool:
    """
    Validate that extraction result contains all required fields.
    
    Args:
        data: Extracted data dictionary
        required_fields: List of required field names
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    for field in required_fields:
        if field not in data:
            logger.warning(f"Missing field in extraction result: {field}")
            return False
    
    return True


def to_tabular_records(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert column-oriented extraction data into one dictionary per row.

    Scalar field extraction remains a single row. Column lists are expanded
    only when all list-valued fields have the same length.
    """
    if not isinstance(data, dict):
        return []

    list_values = {
        key: value for key, value in data.items()
        if isinstance(value, list)
    }

    if not list_values:
        return [data]

    lengths = {len(value) for value in list_values.values()}
    if len(lengths) != 1:
        return [data]

    row_count = lengths.pop()
    if row_count == 0:
        return []

    records = []
    for row_index in range(row_count):
        record = {}
        for key, value in data.items():
            record[key] = value[row_index] if isinstance(value, list) else value
        records.append(record)

    return records


def ensure_directory(directory: str) -> Path:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object for the directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path
