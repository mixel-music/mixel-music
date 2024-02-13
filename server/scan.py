from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
from utils import *

import asyncio
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

        event_handler = Handler(patterns=['*.mp3', '*.mp4', '*.wav', '*.flac'])
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
            logging.debug("event detected on %s", event.src_path)
            print("Watchdog received created event - % s." % event.src_path)
            
            libPath = Path(event.src_path)
            music_rel_path = libPath.relative_to(Path(get_absolute_path()))
            print(music_rel_path)
            logging.debug("%s", music_rel_path)
            music_name = music_rel_path.stem
            music_id = hashlib.md5(music_name.encode()).hexdigest()
            print(music_id)

            music_real_path = get_absolute_path(music_rel_path)
            album_tags = ExtractMediaTag.extract_tags(music_real_path)
            asyncio.run(insert_music(
                music_id,
                str(album_tags.get('title')),
                str(album_tags.get('album')),
                str(album_tags.get('artist')),
                '', # album artist
                str(album_tags.get('track_number')),
                '', # Disc Number
                str(album_tags.get('track_number')),
                str(album_tags.get('is_compil')),
                str(album_tags.get('genre')),
                str(album_tags.get('composer')),
                str(album_tags.get('comment')),
                str(album_tags.get('copyright')),
                str(album_tags.get('isrc')),
                str(album_tags.get('lyrics')),
                str(album_tags.get('length')),
                str(album_tags.get('bitrate')),
                str(album_tags.get('channels')),
                str(album_tags.get('sample_rate')),
                str(album_tags.get('mime'))
            ))
            logging.debug('insert music data...')

        elif event.event_type == 'modified':
            logging.debug("event detected on %s", event.src_path)
            print("Watchdog received modified event - % s." % event.src_path)
        elif event.event_type == 'deleted':
            logging.debug("event detected on %s", event.src_path)
            print("Watchdog received deleted event - % s." % event.src_path)

watchdog = Watchdog()
watchdog.run()