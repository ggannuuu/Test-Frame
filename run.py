import os
import subprocess

def run_backend():
    print("Starting Flask backend server...")
    subprocess.run(['python', 'app.py'])

def open_browser():
    print("Opening the frontend in a local browser...")
    os.system('start chrome http://127.0.0.1:5000')  # Change 'chrome' to your preferred browser

if __name__ == "__main__":
    run_backend()
    open_browser()
