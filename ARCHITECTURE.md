# Architecture Document

## Smart Document Extractor - System Design

### Overview

Smart Document Extractor is a modular, production-ready system for intelligent extraction of structured data from banking PDF documents. The architecture follows SOLID principles and is designed for scalability, maintainability, and robustness.

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI Layer                       │
│  (User Interface, File Upload, Field Input, Results Display)    │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│              Application Controller Layer                       │
│         (Session Management, State, Orchestration)              │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│              Services Layer (Core Business Logic)               │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐       │
│  │ PDFReader  │  │DocumentExtr. │  │ExcelGenerator    │       │
│  │  Service   │  │   Service    │  │   Service        │       │
│  └────────────┘  └──────────────┘  └──────────────────┘       │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│              Utilities Layer (Cross-Cutting Concerns)           │
│  ┌──────────┐  ┌─────────┐  ┌────────────┐  ┌──────────┐     │
│  │ Logger   │  │ Helpers │  │  Prompts   │  │  Config  │     │
│  └──────────┘  └─────────┘  └────────────┘  └──────────┘     │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│              External Integration Layer                         │
│  ┌──────────────────────┐  ┌────────────────────────┐         │
│  │  PDF Processing      │  │  Ollama LLM API        │         │
│  │  (pdfplumber/PyMuPDF)│  │  (HTTP REST API)       │         │
│  └──────────────────────┘  └────────────────────────┘         │
└────────────────┬──────────────────────────────────────────────┘
                 │
┌────────────────▼──────────────────────────────────────────────┐
│              File System & External Services                    │
│  ┌──────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐       │
│  │ Uploads  │  │ Outputs  │  │  Logs   │  │Ollama    │       │
│  │ Directory│  │Directory │  │Directory│  │Server    │       │
│  └──────────┘  └──────────┘  └─────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Breakdown

### 1. PDFReader Service (`services/pdf_reader.py`)

**Responsibility**: Extract text from PDF documents

**Key Components**:
- `PDFReader` class - Main PDF processing engine
- `_extract_with_pdfplumber()` - Primary extraction method
- `_extract_with_pymupdf()` - Fallback extraction method

**Design Pattern**: Strategy Pattern
- Uses pdfplumber as primary strategy
- Falls back to PyMuPDF if primary fails
- Ensures robust PDF text extraction

**Data Flow**:
```
PDF File
    ↓
Validate (exists, is PDF, readable)
    ↓
Try pdfplumber extraction
    ↓
If empty, try PyMuPDF extraction
    ↓
Clean text (whitespace, special chars)
    ↓
Return cleaned text
```

**Error Handling**:
- File not found
- Invalid PDF format
- Corrupted PDF
- Extraction failure
- Empty content

### 2. DocumentExtractor Service (`services/llm_extractor.py`)

**Responsibility**: Extract structured fields using LLM

**Key Components**:
- `DocumentExtractor` class - LLM integration engine
- `extract_fields()` - Main extraction method
- `_call_ollama()` - API communication
- `validate_json()` - Output validation
- `retry_extraction()` - Failure recovery

**Design Pattern**: Retry Pattern with Exponential Backoff
- Automatic retries on failure
- Improved prompts on subsequent attempts
- JSON validation for output quality

**Data Flow**:
```
PDF Text + Field List
    ↓
Build extraction prompt
    ↓
Call Ollama API
    ↓
Parse JSON response
    ↓
Validate JSON structure
    ↓
If invalid, retry with improved prompt
    ↓
Return validated extraction
```

**LLM Communication**:
```
{
  "model": "qwen3:8b",
  "prompt": "Extract these fields: ...",
  "system": "You are an expert banking extraction engine",
  "temperature": 0.1,
  "stream": false
}
    ↓
[Ollama LLM Processing]
    ↓
{
  "response": "{\"field1\": \"value1\", ...}",
  "model": "qwen3:8b",
  ...
}
```

**Error Handling**:
- Connection failures
- Timeout handling
- Invalid JSON parsing
- Missing required fields
- LLM hallucination prevention

### 3. ExcelGenerator Service (`services/excel_generator.py`)

**Responsibility**: Generate formatted Excel output

**Key Components**:
- `ExcelGenerator` class - Excel file creation
- `generate_excel()` - Single document processing
- `generate_excel_batch()` - Batch processing
- `_format_worksheet()` - Professional styling
- `read_excel_data()` - Data import

**Design Pattern**: Builder Pattern
- Constructs Excel files step-by-step
- Applies formatting after data insertion
- Supports single and batch operations

**Data Flow**:
```
Extracted Data Dict
    ↓
Convert to DataFrame
    ↓
Create Excel Writer
    ↓
Write data to worksheet
    ↓
Apply header formatting (color, font, size)
    ↓
Auto-adjust column widths
    ↓
Freeze header row
    ↓
Apply cell alignment
    ↓
Save file
```

**Formatting Features**:
- Header styling (blue background, white font, bold)
- Auto-adjusted column widths (max 50 chars)
- Frozen header row (freeze_panes)
- Cell alignment (left, top, wrap text)
- Type-safe data conversion

### 4. Utilities Layer

#### Logger (`utils/logger.py`)
- Centralized logging configuration
- File and console handlers
- Timestamp and level logging
- Daily log rotation

#### Helpers (`utils/helpers.py`)
- `clean_text()` - Text preprocessing
- `save_uploaded_file()` - File persistence
- `safe_json_loads()` - Robust JSON parsing
- `validate_extraction_result()` - Data validation
- `ensure_directory()` - Path management

#### Prompts (`utils/prompts.py`)
- `SYSTEM_PROMPT` - LLM behavioral guidance
- `build_extraction_prompt()` - Dynamic prompt generation
- `build_retry_prompt()` - Retry-specific prompts
- Semantic field mapping examples

---

## Data Models

### Extraction Input

```python
{
    "pdf_text": str,           # Raw extracted PDF text
    "fields": List[str],       # Field names to extract
    "model": str,              # LLM model name
    "temperature": float       # LLM temperature (0-1)
}
```

### Extraction Output

```python
{
    "field1": str | None,      # Extracted value or null
    "field2": str | None,
    "field3": str | None,
    ...
}
```

### PDF Info

```python
{
    "filename": str,           # Original filename
    "file_size_kb": float,    # File size in KB
    "pages": int              # Number of pages
}
```

---

## State Management

### Streamlit Session State

```python
st.session_state = {
    'uploaded_file_path': Path | None,    # Path to uploaded PDF
    'pdf_text': str | None,               # Extracted PDF text
    'extraction_result': Dict | None,     # Extracted fields
    'excel_output_path': Path | None      # Generated Excel path
}
```

**State Lifecycle**:
1. User uploads PDF → `uploaded_file_path` set
2. PDF processed → `pdf_text` set
3. Fields extracted → `extraction_result` set
4. Excel generated → `excel_output_path` set

---

## Error Handling Strategy

### Error Hierarchy

```
ApplicationError (base)
    ├── PDFProcessingError
    │   ├── FileNotFoundError
    │   ├── InvalidPDFError
    │   └── ExtractionFailureError
    ├── LLMError
    │   ├── ConnectionError
    │   ├── TimeoutError
    │   └── InvalidResponseError
    └── ExcelGenerationError
        ├── WritePermissionError
        └── FormattingError
```

### Error Handling Flow

```
Try Operation
    ↓
Catch Specific Exception
    ↓
Log Error (DEBUG level)
    ↓
Display User Message (friendly)
    ↓
Suggest Remediation
    ↓
Continue or Stop
```

---

## Configuration Management

### Configuration Sources (Priority Order)

1. **Environment Variables** (.env file)
2. **Configuration File** (config.ini)
3. **Streamlit Sidebar** (UI settings)
4. **Hard-coded Defaults** (app constants)

### Key Configuration

```
OLLAMA_URL              # Server location
LLM_MODEL              # Model selection
TEMPERATURE            # LLM behavior
MAX_RETRIES            # Retry attempts
LOG_LEVEL              # Logging verbosity
```

---

## Security Considerations

### Data Isolation

```
User Upload
    ↓
Saved in uploads/ (local only)
    ↓
Processed in memory
    ↓
Saved in outputs/ (local only)
    ↓
No external transmission (except local Ollama)
```

### Security Practices

- No credentials in code
- Local file isolation
- Input validation
- Error message sanitization
- Audit logging

---

## Performance Optimization

### Processing Pipeline Optimization

```
PDF Upload (synchronous, <1 sec)
    ↓
Text Extraction (pdfplumber, ~2-5 sec/page)
    ↓
LLM Processing (parallel-ready, ~5-30 sec)
    ↓
Excel Generation (fast, <1 sec)
    ↓
Total: ~10-40 seconds for typical document
```

### Caching Strategy

- Streamlit session state caches extracted PDF text
- Avoids re-extraction on retry
- Reduces API calls to Ollama

### Scalability Considerations

- Stateless service design
- No database dependencies
- Horizontal scaling ready
- API gateway compatible

---

## Extension Points

### Adding Custom Services

```python
# services/custom_service.py
class CustomExtractor:
    def extract(self, data):
        # Custom extraction logic
        pass
```

### Adding Custom Prompts

```python
# utils/prompts.py
CUSTOM_SYSTEM_PROMPT = """..."""

def build_custom_prompt(data):
    return f"..."
```

### Adding Custom Formatting

```python
# services/excel_generator.py
def _format_worksheet(self, worksheet):
    # Custom formatting
    pass
```

---

## Testing Strategy

### Unit Testing

```python
# Test individual services
def test_pdf_reader_extraction():
    reader = PDFReader()
    text = reader.extract_text_from_pdf("sample.pdf")
    assert text is not None

def test_json_parsing():
    result = safe_json_loads('{"key": "value"}')
    assert result == {"key": "value"}
```

### Integration Testing

```python
# Test end-to-end flow
def test_full_extraction_pipeline():
    # Upload PDF
    # Extract fields
    # Generate Excel
    # Verify output
```

### Manual Testing

- Verify with real banking PDFs
- Test error scenarios
- Check formatting output
- Validate Excel readability

---

## Deployment Considerations

### Pre-deployment Checklist

- [ ] All dependencies installed
- [ ] Ollama server running
- [ ] Required model pulled
- [ ] Logs directory writable
- [ ] Uploads/outputs directories writable
- [ ] Environment variables configured
- [ ] Error handling tested
- [ ] Excel output verified

### Production Deployment

```bash
# Docker (optional future enhancement)
docker build -t smart-doc-extractor .
docker run -p 8501:8501 smart-doc-extractor

# Or: Direct installation
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

---

## Future Architecture Enhancements

### Phase 2
- [ ] FastAPI backend for API endpoints
- [ ] User authentication
- [ ] Processing queue/job management
- [ ] Database for processing history

### Phase 3
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Distributed processing
- [ ] Real-time WebSocket updates

### Phase 4
- [ ] Machine learning model fine-tuning
- [ ] Advanced OCR for scanned documents
- [ ] Multiple LLM provider support
- [ ] Advanced analytics dashboard

---

## Monitoring & Observability

### Logging Levels

- **DEBUG**: Detailed execution flow
- **INFO**: Important events (extraction success)
- **WARNING**: Potential issues (fallback extraction)
- **ERROR**: Failures requiring action
- **CRITICAL**: System-level failures

### Key Metrics

- PDF extraction time
- LLM processing time
- Success/failure rates
- Average document size
- Excel generation time

### Log Analysis

```bash
# View recent errors
grep "ERROR" logs/app_*.log

# Count extractions
grep "successfully extracted" logs/app_*.log | wc -l

# Performance analysis
grep "extraction attempt" logs/app_*.log
```

---

## Conclusion

Smart Document Extractor is designed with:
- ✅ **Modularity**: Independent, replaceable components
- ✅ **Scalability**: Ready for growth and distribution
- ✅ **Maintainability**: Clear structure and documentation
- ✅ **Robustness**: Comprehensive error handling
- ✅ **Production-Ready**: Security, logging, and validation

The architecture supports both current requirements and future enhancements.
