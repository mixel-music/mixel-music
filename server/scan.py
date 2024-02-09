from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils import *

import time

logging.basicConfig(
    filename=get_absolute_path('.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Watchdog:
    target_path = get_absolute_path('test')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        logging.info("Watchdog: Starting")
        logging.debug('Watchdog: Target Path "%s"', str(self.target_path))

        event_handler = Handler()
        self.observer.schedule(event_handler, self.target_path, recursive = True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logging.info("Watchdog: Stopped")

        self.observer.join()
 
class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            logging.debug("FileSystemEvent Detected(modified)")
        elif event.event_type == 'deleted':
            logging.debug("FileSystemEvent Detected(deleted)")

watchdog = Watchdog()
watchdog.run()