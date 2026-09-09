import os
import sys
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Ensure sample datasets and database
    from ml_engine.datasets import ensure_sample_datasets
    from ml_engine.project_storage import init_db
    
    ensure_sample_datasets()
    init_db()
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    from app import app
    print("==================================================================")
    print(">> STUDIO ML PYTHON & AI COPILOT BERHASIL DIMUAT!")
    print(">> Membuka antarmuka di peramban: http://127.0.0.1:5000")
    print("==================================================================")
    app.run(host="127.0.0.1", port=5000, debug=False)
