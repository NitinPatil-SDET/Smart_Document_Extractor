@echo off
REM Smart Document Extractor - Startup Script for Windows

echo.
echo ========================================
echo Smart Document Extractor
echo Starting Application...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version

REM Check if Ollama is running
echo.
echo [2/3] Checking Ollama connection...
timeout /t 2 /nobreak > nul

REM Start Ollama if not running (optional)
tasklist /FI "IMAGENAME eq ollama.exe" 2>nul | find /I /N "ollama.exe">nul
if errorlevel 1 (
    echo WARNING: Ollama does not appear to be running
    echo Please start Ollama separately:
    echo   Command: ollama serve
    echo.
    echo Press any key to continue anyway...
    pause
) else (
    echo Ollama is running
)

REM Check if requirements are installed
echo.
echo [3/3] Installing dependencies if needed...
pip install -q -r requirements.txt

REM Start Streamlit application
echo.
echo Starting Streamlit application...
echo Application will open in your browser at http://localhost:8501
echo.

streamlit run app.py

pause
