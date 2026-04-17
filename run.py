import subprocess
import time
import sys
import os

def run_backend():
    print("Starting Backend (FastAPI)...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])

def run_frontend():
    print("Starting Frontend (Streamlit)...")
    return subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--browser.gatherUsageStats", "false"])

if __name__ == "__main__":
    backend_proc = run_backend()
    time.sleep(2)  # Wait for backend to start
    frontend_proc = run_frontend()
    
    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping PredictaCore...")
        backend_proc.terminate()
        frontend_proc.terminate()
