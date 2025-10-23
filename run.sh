#!/bin/bash

# CreatorPulse Quick Start Script

echo "=€ Starting CreatorPulse..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "   Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "=Ý Please edit .env file and add your API keys before continuing."
    echo "Press Enter when ready..."
    read
fi

# Run the app
echo ""
echo "( Launching CreatorPulse on http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
