from mutagen import File, MutagenError
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from .path import *

class TagsTool:
    """
    Extract and return music tags if possible.
    """
    def __init__(self, path: str):
        self.file_path = path
        self.file_name = PathTool.file_names(path)[1]
        self.file_suffix = PathTool.file_names(path)[2].lower()

    def _check_suffix(self):
        if self.file_suffix == '.mp3':
            return self._extract_tags_mp3()
        elif self.file_suffix == '.mp4':
            return self._extract_tags_mp4()
        elif self.file_suffix == '.wav':
            return self._extract_tags_wave()
        elif self.file_suffix == '.flac':
            return self._extract_tags_flac()

    def _extract_tags_mp3(self):
        mp3 = MP3(self.file_path)

        title = mp3['TIT2'].text[0] if 'TIT2' in mp3 else self.file_name
        album = mp3['TALB'].text[0] if 'TALB' in mp3 else 'Unknown Album'
        artist = mp3['TPE1'].text[0] if 'TPE1' in mp3 else 'Unknown Artist'
        album_artist = mp3['TPE2'].text[0] if 'TPE2' in mp3 else artist
        track_number = int(mp3['TRCK'].text[0]) if 'TRCK' in mp3 else -1
        # disc_number

        year = mp3['TYER'].text if 'TYER' in mp3 else 'Unknown Year'
        is_compil = mp3['TCMP'].text[0] if 'TCMP' in mp3 else -1

        genre = mp3['TCON'].text[0] if 'TCON' in mp3 else -1
        composer = mp3['TCOM'].text[0] if 'TCOM' in mp3 else -1
        comment = mp3['COMM'].text[0] if 'COMM' in mp3 else -1
        copyright = mp3['TCOP'].text[0] if 'TCOP' in mp3 else -1
        isrc = mp3['TSRC'].text[0] if 'TSRC' in mp3 else -1
        lyrics = mp3['USLT'].text[0] if 'USLT' in mp3 else -1

        size = mp3['TSIZ'].text[0] if 'TSIZ' in mp3 else -1
        length = mp3.info.length
        bitrate = mp3.info.bitrate
        channels = mp3.info.channels
        sample_rate = mp3.info.sample_rate
        mime = mp3.mime[0]

        music_tags_data = locals()
        music_tags_data.pop('self', None)
        music_tags_data.pop('mp3', None)

        return music_tags_data
    
    def _extract_tags_mp4(self):
        mp4 = MP4(self.file_path)

        title = mp4['\xa9nam'][0] if '\xa9nam' in mp4 else self.file_name
        album = mp4['\xa9alb'][0] if '\xa9alb' in mp4 else 'Unknown Album'
        artist = mp4['\xa9ART'] if '\xa9ART' in mp4 else 'Unknown Artist'
        album_artist = mp4['aART'] if 'aART' in mp4 else artist
        track_number = mp4['trkn'][0] if 'trkn' in mp4 else -1
        disc_number = mp4['disk'][0] if 'disk' in mp4 else -1

        year = mp4['\xa9day'] if '\xa9day' in mp4 else 'Unknown Year'
        is_compil = 1 if 'cpil' in mp4 and mp4['cpil'] is True else 0

        genre = mp4['\xa9gen'] if '\xa9gen' in mp4 else -1
        composer = mp4['\xa9wrt'] if '\xa9wrt' in mp4 else -1
        comment = mp4['\xa9cmt'] if '\xa9cmt' in mp4 else -1
        copyright = mp4['cprt'] if 'cprt' in mp4 else -1
        isrc = mp4['isrc'][0] if 'isrc' in mp4 else -1
        lyrics = mp4['\xa9lyr'] if '\xa9lyr' in mp4 else -1

        length = mp4.info.length
        bitrate = mp4.info.bitrate
        channels = mp4.info.channels
        sample_rate = mp4.info.sample_rate
        mime = mp4.mime[0]

        music_tags_data = locals()
        music_tags_data.pop('self', None)
        music_tags_data.pop('mp4', None)

        return music_tags_data
    
    def _extract_tags_wave(self):
        wave = WAVE(self.file_path)

        title = wave['TIT2'][0] if 'TIT2' in wave else self.file_name
        album = wave['TALB'][0] if 'TALB' in wave else 'Unknown Album'
        artist = wave['TPE1'] if 'TPE1' in wave else 'Unknown Artist'
        album_artist = wave['TPE2'] if 'TPE2' in wave else artist
        track_number = wave['TRCK'][0] if 'TRCK' in wave else -1
        disc_number = wave['TPOS'][0] if 'TPOS' in wave else -1

        year = wave['TDRC'] if 'TDRC' in wave else 'Unknown Year'
        is_compil = -2

        genre = wave['TCON'] if 'TCON' in wave else -1
        composer = wave['TCOM'] if 'TCOM' in wave else -1
        comment = wave['COMM'] if 'COMM' in wave else -1
        copyright = wave['TCOP'] if 'TCOP' in wave else -1
        isrc = wave['TSRC'][0] if 'TSRC' in wave else -1
        lyrics = wave['TXXX:LYRICS'] if 'TXXX:LYRICS' in wave else -1

        length = wave.info.length
        bitrate = wave.info.bitrate
        channels = wave.info.channels
        sample_rate = wave.info.sample_rate
        mime = wave.mime[0]

        music_tags_data = locals()
        music_tags_data.pop('self', None)
        music_tags_data.pop('wave', None)

        return music_tags_data
        
    def _extract_tags_flac(self):
        flac = FLAC(self.file_path)

        title = flac['TITLE'][0] if 'TITLE' in flac else self.file_name
        album = flac['ALBUM'][0] if 'ALBUM' in flac else 'Unknown Album'
        artist = flac['ARTIST'] if 'ARTIST' in flac else 'Unknown Artist'
        album_artist = flac['ALBUMARTIST'] if 'ALBUMARTIST' in flac else artist
        track_number = int(flac['TRACKNUMBER'][0]) if 'TRACKNUMBER' in flac else -1
        # disc_number

        year = flac['DATE'] if 'DATE' in flac else 'Unknown Year'
        is_compil = -2

        genre = flac['GENRE'] if 'GENRE' in flac else -1
        composer = flac['COMPOSER'] if 'COMPOSER' in flac else -1
        comment = flac['COMMENT'] if 'COMMENT' in flac else -1
        copyright = flac['COPYRIGHT'] if 'COPYRIGHT' in flac else -1
        isrc = flac['ISRC'][0] if 'ISRC' in flac else -1
        lyrics = flac['LYRICS'] if 'LYRICS' in flac else -1

        length = flac.info.length
        bitrate = flac.info.bitrate
        channels = flac.info.channels
        sample_rate = flac.info.sample_rate
        mime = flac.mime[0]

        music_tags_data = locals()
        music_tags_data.pop('self', None)
        music_tags_data.pop('flac', None)

        return music_tags_data
    
    @classmethod
    def extract_tags(cls, path: str) -> dict:
        extract_call = cls(path)
        return extract_call._check_suffix()