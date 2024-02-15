from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
from tools import *
from .music import *

import asyncio
import time

logging.basicConfig(
    filename=PathTools.abs_path('conf', '.log'),
    encoding='utf-8',
    level=logging.DEBUG,
    format='[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Watchdog:
    target_path = PathTools.abs_path('library')

    def __init__(self):
        self.observer = Observer()

    def run(self):
        logging.info("Watchdog: Starting")
        logging.debug('Watchdog: Target Path "%s"', str(self.target_path))

        event_handler = Handler(patterns=['*.mp3', '*.mp4', '*.wav', '*.flac']) # for test
        self.observer.schedule(event_handler, self.target_path, recursive = True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logging.info("Watchdog: Stopped")

        self.observer.join()
 
class Handler(PatternMatchingEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            file = Tracks(PathTools.get_path(event.src_path))
            asyncio.run(file.lookup_track())
            logging.debug("event(created) detected on %s", event.src_path)
        elif event.event_type == 'modified':
            logging.debug("event(modified) detected on %s", event.src_path)
        elif event.event_type == 'deleted':
            logging.debug("event(deleted) detected on %s", event.src_path)

watchdog = Watchdog()
watchdog.run()