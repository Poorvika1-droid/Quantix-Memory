# filepath: c:\Users\poorv\OneDrive\Documents\poorvika\run_production.py
from app_simple import app

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)