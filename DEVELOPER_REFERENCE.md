# Developer Quick Reference

Quick reference guide for developers working with Smart Document Extractor.

## 🚀 Quick Start for Developers

### Clone/Setup
```bash
cd DataExctractionCode
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run Application
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Streamlit
streamlit run app.py
```

Application opens at: `http://localhost:8501`

---

## 📁 Project Structure

```
app.py                    # Main entry point
│
├── services/             # Core business logic
│   ├── pdf_reader.py      # PDF text extraction
│   ├── llm_extractor.py   # LLM-based extraction
│   └── excel_generator.py # Excel output
│
├── utils/                # Utilities & helpers
│   ├── logger.py          # Logging setup
│   ├── prompts.py         # LLM prompts
│   └── helpers.py         # Helper functions
│
└── [configs, docs, etc]
```

---

## 🔧 Key Classes & Methods

### PDFReader

```python
from services.pdf_reader import PDFReader

reader = PDFReader()

# Extract text from PDF
text = reader.extract_text_from_pdf("path/to/file.pdf")

# Get PDF info
info = reader.get_pdf_info("path/to/file.pdf")
```

### DocumentExtractor

```python
from services.llm_extractor import DocumentExtractor

extractor = DocumentExtractor(
    ollama_url="http://localhost:11434",
    model="qwen3:8b"
)

# Check connection
is_connected = extractor.check_ollama_connection()

# Extract fields
fields = ["Customer Name", "Loan Number", "Amount"]
result = extractor.extract_fields(pdf_text, fields)

# Result: {"Customer Name": "John", "Loan Number": "123", ...}
```

### ExcelGenerator

```python
from services.excel_generator import ExcelGenerator

generator = ExcelGenerator(output_dir="outputs")

# Generate single document
path = generator.generate_excel(data)

# Generate batch
paths = generator.generate_excel_batch(data_list)

# Read Excel
data = generator.read_excel_data(path)
```

### Utilities

```python
from utils import (
    logger,
    setup_logger,
    clean_text,
    save_uploaded_file,
    safe_json_loads,
    build_extraction_prompt,
    build_retry_prompt
)

# Logging
logger.info("Message")
logger.error("Error occurred")

# Text cleaning
clean = clean_text(raw_text)

# Safe JSON parsing
data = safe_json_loads(json_string)

# Prompt building
prompt = build_extraction_prompt(pdf_text, fields)
```

---

## 📝 Common Development Tasks

### Add a New Service

```python
# services/new_service.py
from utils.logger import logger

class NewService:
    def __init__(self):
        self.logger = logger
    
    def process(self, data):
        self.logger.info("Processing")
        # Implementation
        return result
```

### Add a New Utility Function

```python
# utils/helpers.py
def new_function(param):
    """
    Description of function.
    
    Args:
        param: Parameter description
        
    Returns:
        Return description
    """
    logger.debug(f"Processing {param}")
    # Implementation
    return result
```

### Customize LLM Prompt

```python
# utils/prompts.py
SYSTEM_PROMPT = """Your custom system prompt"""

def build_custom_prompt(pdf_text, fields):
    return f"""Custom prompt logic"""
```

### Add Custom Excel Formatting

```python
# services/excel_generator.py
def _format_worksheet(self, worksheet):
    # Custom formatting logic
    pass
```

---

## 🧪 Testing

### Test a Service

```python
# test_services.py
from services.pdf_reader import PDFReader

def test_pdf_extraction():
    reader = PDFReader()
    text = reader.extract_text_from_pdf("test.pdf")
    assert text is not None
    assert len(text) > 0

# Run with: python test_services.py
```

### Test Ollama Connection

```python
from services.llm_extractor import DocumentExtractor

extractor = DocumentExtractor()
if extractor.check_ollama_connection():
    print("✓ Ollama running")
else:
    print("✗ Ollama not running")
```

### Test JSON Parsing

```python
from utils.helpers import safe_json_loads

json_str = '{"key": "value"}'
result = safe_json_loads(json_str)
assert result == {"key": "value"}
```

---

## 🐛 Debugging

### View Logs

```bash
# Latest log file
tail -f logs/app_YYYYMMDD.log

# Search for errors
grep "ERROR" logs/app_*.log

# Specific module
grep "pdf_reader" logs/app_*.log
```

### Enable Debug Logging

In app.py:
```python
from utils.logger import setup_logger
logger = setup_logger(log_dir="logs")
logger.setLevel(logging.DEBUG)
```

### Debug Streamlit App

```python
# Add to app.py
import streamlit as st

# Display debug info
with st.expander("Debug Info"):
    st.write(st.session_state)
    st.write(f"PDF path: {st.session_state.uploaded_file_path}")
```

---

## 🔌 API Integration

### Ollama API Calls

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen3:8b",
        "prompt": "Your prompt",
        "stream": False
    }
)

result = response.json()
print(result["response"])
```

### Error Handling

```python
try:
    # API call
    result = extractor.extract_fields(text, fields)
except Exception as e:
    logger.error(f"Extraction failed: {e}")
    # Handle error
```

---

## 📊 Configuration

### Environment Variables (.env)

```env
OLLAMA_URL=http://localhost:11434
LLM_MODEL=qwen3:8b
LOG_LEVEL=DEBUG
```

### Config File (config.ini)

```ini
[OLLAMA]
url = http://localhost:11434
model = qwen3:8b

[EXTRACTION]
max_retries = 3
```

### Runtime Configuration

```python
# In app.py
ollama_url = st.sidebar.text_input("Ollama URL", "http://localhost:11434")
model_name = st.sidebar.text_input("Model", "qwen3:8b")
```

---

## 🚀 Performance Tips

### Optimize PDF Extraction

```python
# Single extraction is faster than double
# For large PDFs, consider:
text = reader.extract_text_from_pdf(path)  # Uses both engines
# Result is same, but double-checked for quality
```

### Optimize LLM Performance

```python
# Lower temperature for consistency
extractor = DocumentExtractor(model="qwen3:8b")
# Temperature defaults to 0.1 (deterministic)

# Use smaller model for speed
# "neural-chat" or "openchat" are faster
```

### Optimize Excel Generation

```python
# Batch generation is efficient
paths = generator.generate_excel_batch(data_list)
# vs loop:
for data in data_list:
    generator.generate_excel(data)  # Slower
```

---

## 📚 Code Examples

### Complete Extraction Pipeline

```python
from services.pdf_reader import PDFReader
from services.llm_extractor import DocumentExtractor
from services.excel_generator import ExcelGenerator

# Initialize
reader = PDFReader()
extractor = DocumentExtractor()
generator = ExcelGenerator()

# Extract from PDF
pdf_text = reader.extract_text_from_pdf("document.pdf")

# Extract fields
fields = ["Name", "Amount", "Date"]
result = extractor.extract_fields(pdf_text, fields)

# Generate Excel
excel_path = generator.generate_excel(result)

print(f"Excel saved to: {excel_path}")
```

### Batch Processing

```python
from pathlib import Path

pdf_dir = Path("uploads")
results = []

for pdf_file in pdf_dir.glob("*.pdf"):
    text = reader.extract_text_from_pdf(str(pdf_file))
    result = extractor.extract_fields(text, fields)
    results.append(result)

# Generate batch Excel
excel_path = generator.generate_excel_batch(results)
```

### Custom Logging

```python
from utils.logger import setup_logger

logger = setup_logger("MyModule")
logger.info("Starting process")

try:
    result = do_something()
    logger.info("Success")
except Exception as e:
    logger.error(f"Failed: {e}")
    raise
```

---

## 🛠️ Useful Commands

### Python Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

### Pip Commands

```bash
# Install requirements
pip install -r requirements.txt

# Add new package
pip install package_name
pip freeze > requirements.txt

# Show installed packages
pip list

# Check for outdated packages
pip list --outdated
```

### Git Commands

```bash
# Initialize repo
git init

# Add files
git add .

# Commit
git commit -m "Initial commit"

# Push
git push origin main
```

### Streamlit Commands

```bash
# Run app
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8502

# Run on all interfaces
streamlit run app.py --server.address 0.0.0.0
```

---

## 📖 Documentation References

| Document | Purpose |
|----------|---------|
| README.md | Complete documentation |
| ARCHITECTURE.md | System design details |
| INSTALLATION.md | Setup instructions |
| QUICKSTART.md | Quick reference |

---

## 🆘 Troubleshooting

### ModuleNotFoundError

```bash
# Ensure virtual environment is active
pip install -r requirements.txt
```

### Ollama Connection Error

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### PDF Extraction Returns Empty

```python
# Check if PDF is valid
import pdfplumber
with pdfplumber.open("test.pdf") as pdf:
    print(f"Pages: {len(pdf.pages)}")
    if pdf.pages:
        print(pdf.pages[0].extract_text())
```

### LLM Returns Invalid JSON

```python
# Check Ollama logs
# Retry extraction (automatic)
# Or use retry_extraction() manually
result = extractor.retry_extraction(text, fields, prev_response)
```

---

## 💡 Best Practices

### Code Style

- Use type hints
- Write docstrings
- Follow PEP8
- Use meaningful names
- Keep functions small

### Error Handling

- Always catch exceptions
- Log errors with context
- Show user-friendly messages
- Handle edge cases

### Testing

- Test each service independently
- Test integration flows
- Test error scenarios
- Use logging for debugging

### Documentation

- Update docstrings
- Add code comments where needed
- Keep README current
- Document configuration changes

---

## 🔗 Useful Links

- **Python Docs**: https://docs.python.org/3.11
- **Streamlit Docs**: https://docs.streamlit.io
- **Ollama GitHub**: https://github.com/jmorganca/ollama
- **Pandas Docs**: https://pandas.pydata.org/docs
- **Openpyxl Docs**: https://openpyxl.readthedocs.io

---

**Happy Coding! 🚀**
