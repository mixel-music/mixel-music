from mutagen.id3 import ID3
from mutagen.id3._frames import APIC
from mutagen.flac import FLAC, Picture
from pathlib import Path

class extract_metadata:
    """
    Identify the type of media file and extract its metadata.
    """
    def __init__(self, path):
        self.path = path
        self.type = Path(path).suffix

    def m_title(self):
        if self.type == '.mp3':
            dir = ID3(self.path)
            res = dir.get('TIT2', ['Unknown Title'])[0]
            return res
        elif self.type == '.flac':
            dir = FLAC(self.path)
            res = dir.get('title', ['Unknown Title'])[0]
            return res
        else:
            return False

    def m_album(self):
        if self.type == '.mp3':
            dir = ID3(self.path)
            res = dir.get('TALB', ['Unknown Album'])[0]
            return res
        elif self.type == '.flac':
            dir = FLAC(self.path)
            res = dir.get('album', ['Unknown Album'])[0]
            return res
        else:
            return False

    def m_artists(self):
        if self.type == '.mp3':
            dir = ID3(self.path)
            res = dir.get('TPE1', ['Unknown Artist'])[0]
            return res
        elif self.type == '.flac':
            dir = FLAC(self.path)
            res = dir.get('artist', ['Unknown Artist'])[0]
            return res
        else:
            return False

    def m_release(self):
        if self.type == '.mp3':
            dir = ID3(self.path)
            res = dir.get('TDRC', ['Unknown Year'])[0]
            return res
        elif self.type == '.flac':
            dir = FLAC(self.path)
            res = dir.get('date', ['Unknown Year'])[0]
            return res
        else:
            return False

    def m_image(self):
        if self.type == '.mp3':
            dir = ID3(self.path)
            for tag in dir.values():
                if isinstance(tag, APIC):
                    res = []
                    res = tag.data # Set first image to front cover
                    return res
        elif self.type == '.flac':
            dir = FLAC(self.path)
            if dir.pictures:
                res = dir.pictures[0].data # Set first image to front cover
                return res
        else:
            return False