"""
Smart Document Extractor - Production-Ready Application
A complete banking document field extraction system using LLM.
"""

import streamlit as st
import os
import truststore
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional, Dict, List, Any

truststore.inject_into_ssl()
load_dotenv(override=True)

from services.pdf_reader import PDFReader
from services.llm_extractor import DocumentExtractor
from services.excel_generator import ExcelGenerator
from utils.helpers import ensure_directory, to_tabular_records
from utils.logger import logger


# Page configuration
st.set_page_config(
    page_title="Smart Document Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #1f77b4;
            margin-bottom: 30px;
        }
        .section-header {
            color: #e8eef8;
            font-size: 1.3em;
            font-weight: bold;
            min-height: 42px;
            display: flex;
            align-items: center;
            margin-top: 8px;
            margin-bottom: 10px;
            border-bottom: 2px solid #9aa9bd;
            padding-bottom: 10px;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .error-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .info-box {
            background-color: #e1f3f5;
            border: 1px solid #a8d9df;
            color: #123b45;
            font-size: 1.05rem;
            font-weight: 600;
            line-height: 1.6;
            padding: 16px 20px;
            border-radius: 4px;
            margin: 10px 0;
        }
        [data-testid="stSidebarCollapseButton"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'uploaded_file_path' not in st.session_state:
    st.session_state.uploaded_file_path = None
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = None
if 'extraction_result' not in st.session_state:
    st.session_state.extraction_result = None
if 'excel_output_path' not in st.session_state:
    st.session_state.excel_output_path = None
if 'template_bytes' not in st.session_state:
    st.session_state.template_bytes = None
if 'template_columns' not in st.session_state:
    st.session_state.template_columns = []
if 'extracted_records' not in st.session_state:
    st.session_state.extracted_records = []


def initialize_services(base_url: str, api_key: str, model_name: str, timeout: int) -> tuple:
    """
    Initialize all services.
    
    Args:
        base_url: Base URL of the Groq API
        api_key: Groq API key
        model_name: Name of LLM model
        timeout: API request timeout in seconds
        
    Returns:
        Tuple of (pdf_reader, extractor, excel_generator)
    """
    pdf_reader = PDFReader()
    extractor = DocumentExtractor(
        base_url=base_url,
        api_key=api_key,
        model=model_name,
        timeout=timeout
    )
    excel_generator = ExcelGenerator()
    
    return pdf_reader, extractor, excel_generator


def validate_groq_connection(extractor: DocumentExtractor) -> bool:
    """
    Validate Groq connection and model availability.
    
    Args:
        extractor: DocumentExtractor instance
        
    Returns:
        True if validation passed, False otherwise
    """
    if not extractor.api_key:
        st.error("GROQ_API_KEY is missing. Add it to your .env file or environment.")
        return False

    if not extractor.check_connection():
        st.markdown("""
            <div class="error-box">
                ❌ <strong>Groq API Not Accessible</strong><br>
                Check GROQ_API_KEY and GROQ_BASE_URL.
            </div>
        """, unsafe_allow_html=True)
        return False
    
    if not extractor.check_model_available():
        st.markdown(f"""
            <div class="warning-box">
                ⚠️ <strong>Model '{extractor.model}' Not Found</strong><br>
                Please pull the model first with:<br>
                <code>GROQ_MODEL={extractor.model}</code>
            </div>
        """, unsafe_allow_html=True)
        return False
    
    return True


def display_results(extraction_result: Dict[str, Any]) -> None:
    """
    Display extraction results in various formats.
    
    Args:
        extraction_result: Dictionary with extracted data
    """
    st.markdown('<div class="section-header">📊 Data Table</div>',
                unsafe_allow_html=True)

    import pandas as pd
    records = to_tabular_records(extraction_result)
    df = pd.DataFrame(records).fillna("N/A")
    st.dataframe(df, use_container_width=True)


# Main application
def main():
    """Main Streamlit application entry point."""
    st.markdown(
        '<h1 class="main-header">📄 Smart Document Extractor</h1>',
        unsafe_allow_html=True
    )
    st.markdown("""
        <div class="info-box">
            Extract banking document fields intelligently using AI.<br>
            Upload a document, map the results to your Excel template, and download the completed file.
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("## ⚙️ Configuration")
    base_url = st.sidebar.text_input(
        "Groq Base URL",
        value=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
        help="OpenAI-compatible base URL for Groq"
    )
    model_name = st.sidebar.text_input(
        "LLM Model Name",
        value=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        help="Name of the Groq model to use"
    )
    api_key = os.getenv("GROQ_API_KEY", "")
    timeout = int(os.getenv("GROQ_TIMEOUT", "300"))

    ensure_directory("outputs")
    ensure_directory("logs")
    pdf_reader, extractor, excel_generator = initialize_services(
        base_url, api_key, model_name, timeout
    )
    groq_available = validate_groq_connection(extractor)

    document_column, fields_column = st.columns([1, 1], gap="large")
    with document_column:
        st.markdown('<div class="section-header">📄 Upload PDF/Image/Text</div>',
                    unsafe_allow_html=True)
        document_file = st.file_uploader(
            "Select a document",
            type=["pdf", "png", "jpg", "jpeg", "tiff", "bmp", "txt"],
            label_visibility="collapsed",
        )

        st.markdown('<div class="section-header">📑 Upload Output Excel Template</div>',
                    unsafe_allow_html=True)
        template_file = st.file_uploader(
            "Select an Excel template",
            type=["xlsx", "xlsm"],
            label_visibility="collapsed",
        )

    with fields_column:
        st.markdown('<div class="section-header">🏷️ Enter Fields to Extract</div>',
                    unsafe_allow_html=True)
        fields_input = st.text_area(
            "Enter field names (one per line)",
            value="Customer Name\nLoan Number\nAmount\nPAN Number\nIFSC Code",
            height=150,
            label_visibility="collapsed",
            help="List the fields you want to extract from the document",
        )

    submit_clicked = st.button(
        "✅ Submit", use_container_width=True, disabled=not groq_available
    )

    if submit_clicked:
        if document_file is None:
            st.error("Please upload a document before submitting.")
        else:
            fields_list = [field.strip() for field in fields_input.splitlines() if field.strip()]
            if not fields_list:
                st.error("Please enter at least one field to extract.")
            else:
                with st.spinner("Reading document and extracting fields..."):
                    pdf_text = pdf_reader.extract_text_from_upload(
                        document_file.name, document_file.getvalue()
                    )
                    extraction_result = (
                        extractor.extract_fields(pdf_text, fields_list)
                        if pdf_text else None
                    )

                if not pdf_text:
                    st.error("Could not extract content from the uploaded document.")
                elif not extraction_result:
                    st.error("Could not extract the requested fields from the document.")
                else:
                    st.session_state.pdf_text = pdf_text
                    st.session_state.extraction_result = extraction_result
                    st.session_state.extracted_records = to_tabular_records(extraction_result)
                    st.session_state.excel_output_path = excel_generator.generate_excel(
                        extraction_result
                    )
                    st.session_state.template_bytes = None
                    st.session_state.template_columns = []

                    if template_file is not None:
                        template_bytes = template_file.getvalue()
                        template_columns = excel_generator.get_template_columns(template_bytes)
                        if template_columns:
                            st.session_state.template_bytes = template_bytes
                            st.session_state.template_columns = template_columns
                        else:
                            st.warning("The uploaded template could not be read. The default Excel is available.")

                    st.success("Document processed successfully. Your default Excel file is ready.")

    if st.session_state.extraction_result:
        st.markdown('<div class="section-header">📊 Extracted Data Preview</div>',
                    unsafe_allow_html=True)
        display_results(st.session_state.extraction_result)

        if st.session_state.excel_output_path:
            st.markdown('<div class="section-header">💾 Download Default Excel</div>',
                        unsafe_allow_html=True)
            with open(st.session_state.excel_output_path, "rb") as output_file:
                st.download_button(
                    "📥 Download Default Excel",
                    data=output_file.read(),
                    file_name=Path(st.session_state.excel_output_path).name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

        if st.session_state.template_columns:
            st.markdown('<div class="section-header">🔗 Optional Field Mapping</div>',
                        unsafe_allow_html=True)
            extracted_fields = list(st.session_state.extraction_result.keys())
            mapping = {}
            for template_column in st.session_state.template_columns:
                selected_field = st.selectbox(
                    f"{template_column} ← Extracted field",
                    ["-- Select field --"] + extracted_fields,
                    key=f"mapping_{template_column}",
                )
                if selected_field != "-- Select field --":
                    mapping[template_column] = selected_field

            if len(mapping) != len(st.session_state.template_columns):
                st.info("Field mapping is optional. Complete all mappings to create a template-based Excel file.")
            else:
                output_path = excel_generator.generate_from_template(
                    st.session_state.template_bytes,
                    st.session_state.extracted_records,
                    mapping,
                )
                if output_path:
                    with open(output_path, "rb") as output_file:
                        st.download_button(
                            "📥 Download Mapped Excel",
                            data=output_file.read(),
                            file_name=Path(output_path).name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                    st.success("Mapped template Excel created successfully.")
                else:
                    st.error("Could not create the mapped Excel file.")

    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
            <p>Smart Document Extractor v1.0 | Banking Document Intelligence</p>
            <p>Powered by Groq LLM | Production Ready</p>
            <p>Made By <a href="https://www.linkedin.com/in/nitinpatilsdet/" target="_blank">Nitin Patil</a></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
