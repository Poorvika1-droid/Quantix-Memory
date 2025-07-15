#!/bin/bash

echo ""
echo "========================================"
echo "   Quantix Memory AI - Startup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python found. Checking version..."
python3 --version

echo ""
echo "Installing/updating dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Starting Quantix Memory AI..."
echo ""
echo "Open your browser and go to: http://localhost:5000"
echo "Press Ctrl+C to stop the application"
echo ""

python3 app.py 