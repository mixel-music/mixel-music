from mutagen import File, MutagenError
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.asf import ASF
from datetime import datetime

from core.convert_tools import *
from infra.convert_image import *
from infra.path_handler import *
import asyncio

class ExtractTags:
    def __init__(self, path: str):
        self.path = path
        self.real_path = get_path(path)
        self.tags_dict = {}
        self.suffix = get_filename(path)[2]

    async def extract_tags(self, rows: list) -> dict:
        try:
            tags = File(self.real_path, easy=True)
            if not tags: return self.tags_dict
            
            for key, value in dict(tags).items():
                if isinstance(value, list):
                    str_value = ', '.join(str(item) for item in value)
                    self.tags_dict[key] = str_value

        except MutagenError as error:
            logs.error("Failed to init mutagen, %s", error)

        self.tags_dict.update({
            'album': self.tags_dict.get('album', 'Unknown Album'),
            'albumid': get_hash_str(self.tags_dict.get('album', 'Unknown Album')),
            'artist': self.tags_dict.get('artist', 'Unknown Artist'),
            'artistid': get_hash_str(self.tags_dict.get('artist', 'Unknown Artist')),
            'bitrate': getattr(tags.info, 'bitrate', 0),
            'bpm': int(self.tags_dict.get('bpm', 0)),
            'channels': getattr(tags.info, 'channels', 0),
            'create_date': datetime.now(),
            'directory': str_path(self.real_path.parent),
            'duration': getattr(tags.info, 'length', 0.0),
            'trackid': get_hash_str(self.path),
            'mime': getattr(tags, 'mime', [''])[0],
            'path': self.path,
            'samplerate': getattr(tags.info, 'sample_rate', 0),
            'size': self.real_path.stat().st_size,
            'update_date': datetime.now(),
        })

        self.tags_dict['compilation'] = False if not self.tags_dict.get('compilation') else True
        self.tags_dict['discnumber'] = sanitize_num(self.tags_dict.get('discnumber', 0))
        self.tags_dict['disctotal'] = max(sanitize_num(self.tags_dict.get('disctotal', 0)), sanitize_num(self.tags_dict.pop('totaldiscs', 0)))
        self.tags_dict['lyrics'] = self.tags_dict.pop('unsyncedlyrics', self.tags_dict.get('lyrics', ''))
        self.tags_dict['title'] = self.tags_dict.get('title', get_filename(self.path)[1] if get_filename(self.path)[1] else 'Unknown Title')
        self.tags_dict['tracknumber'] = max(sanitize_num(self.tags_dict.get('track', 0)), sanitize_num(self.tags_dict.pop('tracknumber', 0)))
        self.tags_dict['tracktotal'] = max(sanitize_num(self.tags_dict.get('tracktotal', 0)), sanitize_num(self.tags_dict.pop('totaltracks', 0)))

        date_result, date_raw = None, self.tags_dict.get('date', '0')
        year_result, year_raw = None, self.tags_dict.get('year', '0')

        if '-' or '.' or ',' in date_raw:
            date_result = date_raw
            if ',' in date_raw:
                year_result = sanitize_num(date_raw.split(',')[0])
                date_result = date_raw.split(', ')[1]
            elif '-' in date_raw:
                year_result = sanitize_num(date_raw.split('-')[0])
            elif '.' in date_raw:
                year_result = sanitize_num(date_raw.split('.')[0])
        elif date_raw:
            date_result = date_raw

        if not year_result and year_raw:
            year_result = sanitize_num(year_raw)

        self.tags_dict['date'] = date_result
        self.tags_dict['year'] = year_result

        image_data = await self._extract_image()
        if image_data:
            self.tags_dict['imageid'] = hashlib.md5(image_data).hexdigest().upper()
            asyncio.create_task(convert_image(image_data))
        else:
            self.tags_dict['imageid'] = ''

        self.tags_dict = {key: self.tags_dict.get(key, '') for key in rows}
        return dict(sorted(self.tags_dict.items()))
    
    async def _extract_image(self):
        if self.suffix == '.mp3':
            track_tags = ID3(self.real_path)
            for tag in track_tags.values():
                return tag.data if isinstance(tag, APIC) else None
            
        elif self.suffix in ['.mp4', '.m4a', '.aac']:
            track_tags = MP4(self.real_path)
            covers = track_tags.get('covr')
            
            return covers[0] if covers else None
        
        elif self.suffix == '.flac':
            track_tags = FLAC(self.real_path)
            for picture in track_tags.pictures:
                return picture.data if picture.type == 3 else None
            
        elif self.suffix == '.alac':
            track_tags = MP4(self.real_path)
            covers = track_tags.tags.get('covr')

            return covers[0].data if covers else None
        
        elif self.suffix == '.wma':
            track_tags = ASF(self.real_path)
            if 'WM/Picture' in track_tags.asf_tags:
                pictures = track_tags.asf_tags['WM/Picture']

                return pictures[0].value.data if pictures else None
            
        elif self.suffix == '.aiff':
            track_tags = AIFF(self.real_path)
            if track_tags.tags is None: pass
            id3 = ID3(self.real_path)
            for tag in id3.values():
                return tag.data if isinstance(tag, APIC) else None