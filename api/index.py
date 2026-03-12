from backend.app.main import app as _app

# Vercel needs a handler that is an instance of FastAPI
app = _app
