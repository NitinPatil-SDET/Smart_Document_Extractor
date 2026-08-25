"""
Prompt templates for LLM extraction engine.
"""

SYSTEM_PROMPT = """You are an expert banking document extraction engine.

Your responsibility is to identify requested fields from document content.

Rules:
1. Return ONLY valid JSON in response - nothing else
2. No markdown, no code blocks, no explanations
3. No extra text before or after JSON
4. Keep exact values as they appear in the document
5. Use null if a field is missing or not found
6. Perform semantic matching (e.g., 'Applicant Name' matches 'Customer Name')
7. Return empty string "" if value exists but is unclear

Example semantic mappings:
- Applicant Name, Borrower Name, Name -> Customer Name
- LAN, Loan Account Number -> Loan Number
- Loan Value, Amount Sanctioned, Principal -> Amount
- Account No, Account Number -> Account Number
- IFSC Code, Bank Code -> IFSC Code
- PAN Number, PAN -> PAN

CRITICAL: Always return VALID JSON. If unsure about a value, use null instead of guessing.
For table fields such as Date, Description, Withdrawals, Deposits, and Balance,
return each field as an array with one value per transaction, in document order.
All table field arrays must have the same length. Do not return a stringified array."""

def build_extraction_prompt(pdf_text: str, fields: list) -> str:
    """
    Build the extraction prompt for LLM.
    
    Args:
        pdf_text: Extracted text from PDF
        fields: List of field names to extract
        
    Returns:
        Formatted prompt string
    """
    fields_str = "\n".join([f"- {field}" for field in fields])
    
    prompt = f"""Extract the following fields from the provided document text.

Fields to extract:
{fields_str}

Document text:
{pdf_text}

Return ONLY a valid JSON object with these fields as keys. Use null for missing values.
When the requested fields are table columns, return arrays with one item per table row,
keeping values aligned by row and preserving the document order. Do not return arrays
as strings. Do not include any explanation or text outside the JSON."""
    
    return prompt


def build_retry_prompt(pdf_text: str, fields: list, previous_response: str) -> str:
    """
    Build a retry prompt when initial extraction failed.
    
    Args:
        pdf_text: Extracted text from PDF
        fields: List of field names to extract
        previous_response: The invalid response from previous attempt
        
    Returns:
        Formatted retry prompt string
    """
    fields_str = "\n".join([f"- {field}" for field in fields])
    
    prompt = f"""The previous extraction attempt returned invalid JSON. 
Please try again and return ONLY valid JSON with no additional text.

Fields to extract:
{fields_str}

Document text:
{pdf_text}

Return a valid JSON object. Example format:
{{"field1": "value1", "field2": null, "field3": "value3"}}

Do not include any text outside the JSON object."""
    
    return prompt
