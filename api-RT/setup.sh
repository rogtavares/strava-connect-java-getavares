#!/bin/bash
# Quick start script for FastAPI development

echo "🚀 Starting Strava Insights API Setup..."
echo ""

# Check Python version
echo "✅ Checking Python version..."
python --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your OpenWeather API key!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🏃 To start the API server, run:"
echo "   python run.py"
echo ""
echo "📚 API Documentation will be available at:"
echo "   http://localhost:8000/docs"
echo ""
