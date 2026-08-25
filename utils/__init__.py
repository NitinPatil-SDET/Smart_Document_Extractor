"""
Utilities package for Smart Document Extractor.
"""

from utils.logger import setup_logger, logger
from utils.helpers import (
    clean_text,
    save_uploaded_file,
    safe_json_loads,
    validate_extraction_result,
    ensure_directory
)
from utils.prompts import (
    SYSTEM_PROMPT,
    build_extraction_prompt,
    build_retry_prompt
)

__all__ = [
    'setup_logger',
    'logger',
    'clean_text',
    'save_uploaded_file',
    'safe_json_loads',
    'validate_extraction_result',
    'ensure_directory',
    'SYSTEM_PROMPT',
    'build_extraction_prompt',
    'build_retry_prompt'
]
