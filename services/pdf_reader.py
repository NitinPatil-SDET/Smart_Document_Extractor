"""
PDF reader module for extracting text from PDF documents.
"""

import pdfplumber
import fitz
import io
import tempfile
from pathlib import Path
from typing import Optional
from utils.logger import logger
from utils.helpers import clean_text

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None


class PDFReader:
    """
    Handle PDF file reading and text extraction.
    """
    
    def __init__(self):
        """Initialize PDF reader."""
        self.logger = logger
    
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from PDF file using multiple methods for robustness.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text or None if failed
        """
        try:
            pdf_file = Path(pdf_path)
            
            if not pdf_file.exists():
                self.logger.error(f"PDF file not found: {pdf_path}")
                return None
            
            if not pdf_file.suffix.lower() == '.pdf':
                self.logger.error(f"File is not a PDF: {pdf_path}")
                return None
            
            self.logger.info(f"Extracting text from: {pdf_path}")
            
            # Try extraction with pdfplumber first
            text = self._extract_with_pdfplumber(pdf_path)
            
            # If pdfplumber fails, try PyMuPDF
            if not text or len(text.strip()) == 0:
                self.logger.warning("pdfplumber extraction returned empty, trying PyMuPDF")
                text = self._extract_with_pymupdf(pdf_path)
            
            if not text or len(text.strip()) == 0:
                self.logger.error("Failed to extract text from PDF with all methods")
                return None
            
            # Clean extracted text
            cleaned_text = clean_text(text)
            
            self.logger.info(f"Successfully extracted text. Length: {len(cleaned_text)} characters")
            
            return cleaned_text
            
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {e}")
            return None

    def extract_text_from_upload(self, file_name: str, file_bytes: bytes) -> Optional[str]:
        """Extract text from an uploaded PDF, text file, or image."""
        suffix = Path(file_name).suffix.lower()

        try:
            if suffix == ".txt":
                return clean_text(file_bytes.decode("utf-8", errors="replace"))

            if suffix in {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}:
                if Image is None or pytesseract is None:
                    self.logger.error("Image extraction requires Pillow and pytesseract")
                    return None
                text = pytesseract.image_to_string(Image.open(io.BytesIO(file_bytes)))
                return clean_text(text)

            if suffix == ".pdf":
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temporary_file:
                    temporary_file.write(file_bytes)
                    temporary_path = temporary_file.name
                try:
                    return self.extract_text_from_pdf(temporary_path)
                finally:
                    Path(temporary_path).unlink(missing_ok=True)

            self.logger.error(f"Unsupported document type: {suffix}")
            return None
        except Exception as e:
            self.logger.error(f"Error extracting uploaded document: {e}")
            return None
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """
        Extract text using pdfplumber library.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                self.logger.info(f"PDF has {total_pages} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num} ---\n{page_text}"
                    except Exception as e:
                        self.logger.warning(f"Error extracting page {page_num} with pdfplumber: {e}")
                        continue
            
            return text
            
        except Exception as e:
            self.logger.error(f"pdfplumber extraction failed: {e}")
            return ""
    
    def _extract_with_pymupdf(self, pdf_path: str) -> str:
        """
        Extract text using PyMuPDF library as fallback.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            pdf_document = fitz.open(pdf_path)
            total_pages = len(pdf_document)
            self.logger.info(f"PyMuPDF: PDF has {total_pages} pages")
            
            for page_num in range(total_pages):
                try:
                    page = pdf_document[page_num]
                    page_text = page.get_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                except Exception as e:
                    self.logger.warning(f"Error extracting page {page_num + 1} with PyMuPDF: {e}")
                    continue
            
            pdf_document.close()
            return text
            
        except Exception as e:
            self.logger.error(f"PyMuPDF extraction failed: {e}")
            return ""
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get information about PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with PDF information
        """
        try:
            pdf_file = Path(pdf_path)
            
            info = {
                "filename": pdf_file.name,
                "file_size_kb": pdf_file.stat().st_size / 1024,
                "pages": 0
            }
            
            with pdfplumber.open(pdf_path) as pdf:
                info["pages"] = len(pdf.pages)
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting PDF info: {e}")
            return {"error": str(e)}
