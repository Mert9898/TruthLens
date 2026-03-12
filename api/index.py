import sys
import os

# Add the project root to sys.path so we can import the backend package correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.app.main import app as _app
    app = _app
except Exception as e:
    # Print error to stdout so it might show up in Vercel logs
    print(f"Error importing app: {e}")
    raise e
