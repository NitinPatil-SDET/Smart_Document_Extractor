# Installation & Setup Guide

Complete step-by-step guide to set up Smart Document Extractor on your system.

## 📋 Prerequisites

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.11 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 5GB+ (for Ollama and models)
- **Internet**: Required for initial setup and model downloads

## 🔍 System Requirements Check

### Windows

```powershell
# Check Python version
python --version

# Check available disk space
(Get-Volume C).SizeRemaining / 1GB
```

### macOS/Linux

```bash
# Check Python version
python3 --version

# Check available disk space
df -h /
```

---

## 📦 Installation Steps

### Step 1: Install Python (if not already installed)

#### Windows
1. Download from: https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```powershell
   python --version
   ```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

---

### Step 2: Set Up Project Directory

#### Windows
```powershell
# Navigate to project folder
cd c:\ABFL\PDFDataExctraction\DataExctractionCode

# Verify structure
ls
```

#### macOS/Linux
```bash
# Navigate to project folder
cd ~/path/to/DataExctractionCode

# Verify structure
ls -la
```

---

### Step 3: Create Virtual Environment (Recommended)

#### Windows
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try again:
.\venv\Scripts\Activate.ps1

# You should see (venv) in your prompt
```

#### macOS/Linux
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

---

### Step 4: Install Python Dependencies

```bash
# Ensure pip is up to date
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Expected installation time**: 2-5 minutes depending on internet speed

**Verification**:
```bash
pip list
```

Should show:
- streamlit (1.28.1)
- pdfplumber (0.10.3)
- PyMuPDF (1.23.8)
- pandas (2.1.1)
- openpyxl (3.10.10)
- requests (2.31.0)
- python-dotenv (1.0.0)

---

### Step 5: Install Ollama

#### Windows
1. Download from: https://ollama.ai/download
2. Run the installer: `OllamaSetup.exe`
3. Follow the installation wizard
4. Restart your computer
5. Verify installation:
   ```powershell
   ollama --version
   ```

#### macOS
```bash
# Download and install
brew install ollama

# Or download from https://ollama.ai/download
```

#### Linux (Ubuntu)
```bash
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
```

---

### Step 6: Pull Required LLM Model

This step downloads the AI model (approximately 5-8 GB).

```bash
ollama pull qwen3:8b
```

**Time required**: 5-15 minutes depending on internet speed

**Alternative models** (if preferred):
```bash
ollama pull mistral:latest      # Smaller, faster
ollama pull neural-chat:latest  # Optimized for chat
ollama pull openchat:latest     # General purpose
```

**Verify model is installed**:
```bash
ollama list
```

You should see `qwen3:8b` in the list.

---

### Step 7: Configure Environment (Optional)

Copy the example environment file:

#### Windows
```powershell
Copy-Item .env.example .env
```

#### macOS/Linux
```bash
cp .env.example .env
```

Edit `.env` if you want to customize settings:
```
OLLAMA_URL=http://localhost:11434
LLM_MODEL=qwen3:8b
LOG_LEVEL=INFO
```

---

## 🚀 Running the Application

### Option 1: Automated Startup (Recommended)

#### Windows
Double-click `start.bat` or run in PowerShell:
```powershell
.\start.bat
```

#### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Startup

**Terminal 1 - Start Ollama**:
```bash
ollama serve
```

You should see:
```
Listening on localhost:11434
```

**Terminal 2 - Start Application** (with venv activated):
```bash
streamlit run app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The application will automatically open in your browser.

---

## ✅ Verification Checklist

After installation, verify everything works:

### ✓ Python Installation
```bash
python --version  # Should be 3.11+
```

### ✓ Virtual Environment (if used)
```bash
which python  # Should show venv path
```

### ✓ Dependencies
```bash
pip list | grep streamlit
pip list | grep pandas
```

### ✓ Ollama Installation
```bash
ollama --version
```

### ✓ Model Availability
```bash
ollama list
# Should show qwen3:8b or similar
```

### ✓ Ollama Server
```bash
# In a terminal
ollama serve

# In another terminal
curl http://localhost:11434/api/tags
# Should return JSON with models
```

### ✓ Application Start
```bash
streamlit run app.py
# Should open browser to http://localhost:8501
```

### ✓ PDF Upload
1. Upload a test PDF
2. Should see extraction success message
3. No errors in terminal

---

## 📁 Directory Structure After Setup

```
DataExctractionCode/
├── venv/                    # Virtual environment (if created)
│
├── app.py                   # Main application
├── requirements.txt         # Dependencies
├── config.ini              # Configuration
├── .env                    # Environment variables
│
├── services/
│   ├── pdf_reader.py
│   ├── llm_extractor.py
│   └── excel_generator.py
│
├── utils/
│   ├── logger.py
│   ├── prompts.py
│   └── helpers.py
│
├── uploads/                # Auto-created on first run
├── outputs/                # Auto-created on first run
├── logs/                   # Auto-created on first run
│
├── README.md
├── QUICKSTART.md
├── ARCHITECTURE.md
└── [other files]
```

---

## 🔧 Common Installation Issues & Solutions

### Issue: "Python not found"

**Solution**:
```powershell
# Windows: Reinstall Python with "Add to PATH" checked
# macOS/Linux: Install via package manager
```

### Issue: "pip: command not found"

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Or use python3
python3 -m pip install -r requirements.txt
```

### Issue: "Permission denied" on start.sh (macOS/Linux)

**Solution**:
```bash
chmod +x start.sh
./start.sh
```

### Issue: "Ollama not found"

**Solution**:
- Verify installation: `ollama --version`
- Reinstall from https://ollama.ai
- Add Ollama to PATH if necessary

### Issue: "Model 'qwen3:8b' not found"

**Solution**:
```bash
ollama pull qwen3:8b
```

### Issue: "Port 8501 already in use"

**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: "Port 11434 already in use"

**Solution**:
Ollama is likely already running. Check:
```bash
# Windows
netstat -ano | findstr :11434

# macOS/Linux
lsof -i :11434
```

### Issue: Module import errors

**Solution**:
```bash
# Verify virtual environment is activated
# Then reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: PDF extraction returns empty

**Solution**:
- Ensure PDF is text-based, not image-based
- Try with a different PDF
- Check logs for detailed error

---

## 🌐 Network Configuration

### Local Network Access

To access the application from another computer on your network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from: `http://YOUR_IP:8501`

### Ollama on Different Machine

If Ollama runs on a different machine:

```python
# In Streamlit sidebar or .env:
OLLAMA_URL=http://other-machine:11434
```

---

## 📚 Post-Installation

### First Run Checklist

1. ✅ Application starts without errors
2. ✅ Ollama connection shows success message
3. ✅ Model availability confirmed
4. ✅ Can upload a PDF
5. ✅ Can extract fields
6. ✅ Can download Excel file
7. ✅ Logs are generated in `logs/` folder
8. ✅ Excel files are in `outputs/` folder

### Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Review [QUICKSTART.md](QUICKSTART.md) for quick reference
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) for system design
4. Explore the code in `services/` and `utils/`
5. Customize prompts in `utils/prompts.py` if needed

---

## 💡 Tips for Smooth Operation

1. **Keep Ollama running**: Always have `ollama serve` running in background
2. **Use dedicated terminal**: Run Ollama in separate terminal window
3. **Monitor logs**: Check `logs/app_*.log` for troubleshooting
4. **Test PDFs**: Start with simple PDFs before complex documents
5. **Backup outputs**: Keep important Excel files in backup location

---

## 🆘 Getting Help

### Check Logs
```bash
# View latest log
cat logs/app_YYYYMMDD.log

# Or on Windows:
type logs\app_YYYYMMDD.log
```

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "ConnectionError" | Ollama not running | Start Ollama server |
| "JSONDecodeError" | Invalid model response | Check Ollama logs |
| "FileNotFoundError" | PDF file issue | Verify PDF path |
| "ModuleNotFoundError" | Missing dependency | Run `pip install -r requirements.txt` |

### Verify Installation

Run this Python script to verify everything:

```python
# test_setup.py
import sys
print(f"Python: {sys.version}")

try:
    import streamlit
    print("✓ Streamlit installed")
except: print("✗ Streamlit missing")

try:
    import pdfplumber
    print("✓ pdfplumber installed")
except: print("✗ pdfplumber missing")

try:
    import pandas
    print("✓ pandas installed")
except: print("✗ pandas missing")

try:
    import requests
    import requests
    r = requests.get("http://localhost:11434/api/tags", timeout=5)
    print("✓ Ollama server running")
except: print("✗ Ollama server not accessible")
```

Run with:
```bash
python test_setup.py
```

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Ollama GitHub**: https://github.com/jmorganca/ollama
- **Python Docs**: https://docs.python.org/3.11
- **Project README**: [README.md](README.md)

---

## 🎉 Installation Complete!

You're now ready to use Smart Document Extractor. Start with the [QUICKSTART.md](QUICKSTART.md) guide.

**Happy extracting! 🚀**
