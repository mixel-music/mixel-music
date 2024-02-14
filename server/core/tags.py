from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wavpack import WavPack
import mutagen
import logging

def TagsTool(music_path):
    music_tags = mutagen.File(music_path, easy=True)

    if music_tags is not None:
        for title, value in music_tags.items():
            print(f"{f'{title}': {value}}")
    else:
        logging.debug("Unknown music format")