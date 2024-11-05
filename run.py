import os
import subprocess
import time

def run_backend():
    print("Starting Flask backend server...")
    subprocess.Popen(['python', './backend/app.py'])

def open_browser():
    print("Opening the frontend in a local browser...")
    time.sleep(5) 
    os.system('start chrome http://127.0.0.1:5000')  # Change 'chrome' to your preferred browser
    # os.system('start http://127.0.0.1:5000')

if __name__ == "__main__":
    run_backend()
    open_browser()
