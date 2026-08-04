import os
import subprocess
import sys

def main():
    print("Launching Streamlit Assessment Form...")
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
