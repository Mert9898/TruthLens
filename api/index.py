import sys
import os

# Add the project root (where 'backend' folder is) to sys.path
# Vercel's root is usually the directory containing vercel.json
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from backend.app.main import app
except Exception as e:
    print(f"CRITICAL: Failed to import FastAPI app: {e}")
    raise e
