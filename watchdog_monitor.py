import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        super().__init__()

    def on_any_event(self, event):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, 'run.py'])

def main():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='app/src', recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
