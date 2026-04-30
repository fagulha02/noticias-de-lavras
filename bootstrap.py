import streamlit.web.cli as stcli
import os, sys, webbrowser, time
from threading import Thread

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, path)
    return path

def open_browser():
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    Thread(target=open_browser).start()
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("app.py"),
        "--global.developmentMode=false",
        "--server.headless=true",
        "--server.port=8501"
    ]
    sys.exit(stcli.main())
