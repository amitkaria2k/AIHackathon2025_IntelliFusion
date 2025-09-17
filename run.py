#!/usr/bin/env python3
"""
IntelliFusion AI Document Assistant
Bosch AI Hackathon 2025

Main entry point for the application.
This script launches the Streamlit application.

Usage:
    python run.py
    
or 
    
    streamlit run app/main.py
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Launch the IntelliFusion application"""
    
    # Get the directory where this script is located
    root_dir = Path(__file__).parent.absolute()
    app_file = root_dir / "app" / "main.py"
    
    if not app_file.exists():
        print("❌ Error: Application file not found at app/main.py")
        print("Please ensure the project structure is correct.")
        sys.exit(1)
    
    # Check if streamlit is available
    try:
        import importlib.util
        if importlib.util.find_spec("streamlit") is None:
            raise ImportError("streamlit not found")
        print("✅ Streamlit found")
    except ImportError:
        print("❌ Error: Streamlit not found. Please install requirements:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Check for .env file
    env_file = root_dir / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found. Please copy .env.example to .env and configure your settings.")
        print("cp .env.example .env  # Linux/macOS")
        print("copy .env.example .env  # Windows")
    
    print("🚀 Launching IntelliFusion AI Document Assistant...")
    print(f"📁 Root directory: {root_dir}")
    print(f"📄 App file: {app_file}")
    print("🌐 Application will be available at: http://localhost:8501")
    print("=" * 60)
    
    # Launch streamlit
    try:
        # Change to root directory for proper imports
        os.chdir(root_dir)
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_file),
            "--server.port", "8501",
            "--server.address", "127.0.0.1"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
