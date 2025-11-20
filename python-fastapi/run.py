#!/usr/bin/env python3
"""
Development server starter for Strava Insights API
Automatically loads .env file and starts FastAPI with hot reload
"""

import os
import subprocess
import sys
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
        print(f"✅ Loaded environment from {env_file}")
    else:
        print(f"⚠️  .env file not found. Copy .env.example to .env")

def main():
    load_env()
    
    # Get configuration from env or use defaults
    host = os.getenv("FASTAPI_HOST", "127.0.0.1")
    port = os.getenv("FASTAPI_PORT", "8000")
    
    print(f"\n🚀 Starting Strava Insights API")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Backend URL: {os.getenv('BACKEND_URL', 'http://localhost:8080')}")
    print(f"   OpenWeather Key: {'✅ Configured' if os.getenv('OPENWEATHER_API_KEY') else '❌ Not configured'}")
    print()
    
    # Start uvicorn
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app:app",
        "--host", host,
        "--port", port,
        "--reload",
        "--log-level", "info"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
