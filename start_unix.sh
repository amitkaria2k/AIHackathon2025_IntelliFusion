#!/bin/bash
# IntelliFusion AI Document Assistant - Linux/macOS Startup Script
# Bosch AI Hackathon 2025

echo "========================================"
echo " IntelliFusion AI Document Assistant"
echo " Bosch AI Hackathon 2025"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "Copying .env.example to .env..."
    cp ".env.example" ".env"
    echo "✅ Created .env file"
    echo "Please edit .env with your Bosch credentials before running the app"
    read -p "Press any key to continue..."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Launch the application
echo "🚀 Starting IntelliFusion..."
echo
echo "The application will open in your browser at:"
echo "http://localhost:8501"
echo
echo "Press Ctrl+C to stop the application"
echo

python run.py
