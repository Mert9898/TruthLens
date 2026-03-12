import sys
import os

# Ensure the current directory is in sys.path (standard for Vercel)
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.main import app
except Exception as e:
    print(f"CRITICAL: Failed to import FastAPI app from local 'app' package: {e}")
    raise e
