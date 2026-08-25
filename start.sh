#!/bin/bash

# Smart Document Extractor - Startup Script for Linux/Mac

echo ""
echo "========================================"
echo "Smart Document Extractor"
echo "Starting Application..."
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org"
    exit 1
fi

echo "[1/3] Checking Python installation..."
python3 --version

# Check if Ollama is running
echo ""
echo "[2/3] Checking Ollama connection..."
sleep 2

if ! pgrep -x "ollama" > /dev/null; then
    echo "WARNING: Ollama does not appear to be running"
    echo "Please start Ollama separately in another terminal:"
    echo "  Command: ollama serve"
    echo ""
    read -p "Press Enter to continue anyway..."
else
    echo "Ollama is running"
fi

# Check and install requirements
echo ""
echo "[3/3] Installing dependencies if needed..."
pip3 install -q -r requirements.txt

# Start Streamlit application
echo ""
echo "Starting Streamlit application..."
echo "Application will open in your browser at http://localhost:8501"
echo ""

streamlit run app.py

read -p "Press Enter to exit..."
