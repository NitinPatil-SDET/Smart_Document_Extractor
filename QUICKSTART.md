# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Python Dependencies (1 min)

```bash
pip install -r requirements.txt
```

### Step 2: Configure Groq (2 min)

Copy `.env.example` to `.env` and set `GROQ_API_KEY` to your Groq API key.

### Step 3: Run the Application (30 sec)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Manual:**
```bash
streamlit run app.py
```

### Step 4: Upload and Extract (2 min)

1. Open http://localhost:8501 in your browser
2. Upload a PDF file
3. Enter field names to extract
4. Click "Extract Fields"
5. Download Excel file

---

## 📋 Verification Checklist

- [ ] Python 3.11+ installed
- [ ] Dependencies installed via pip
- [ ] Groq API key configured in `.env`
- [ ] Streamlit application started
- [ ] Browser showing http://localhost:8501
- [ ] PDF uploaded successfully
- [ ] Fields extracted
- [ ] Excel downloaded

## ⚠️ Common Issues

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "Groq API key is missing"
Set `GROQ_API_KEY` in the project `.env` file and restart Streamlit.

## 🎯 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check the project structure in the repository
3. Explore the Streamlit configuration options
4. Customize field extraction prompts in `utils/prompts.py`

## 💡 Tips

- Keep your Groq API key in `.env`; do not commit it
- Larger PDFs take longer to process
- Try with a test PDF first to verify setup
- Check `logs/` directory for detailed error messages
- Use Ctrl+C to stop the Streamlit application

---

**Ready to extract? 🚀 Start the application and upload your first PDF!**
