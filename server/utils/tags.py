from mutagen import File, MutagenError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.wave import WAVE

from pathlib import Path

def audio_tags(path):
    name = Path(path).stem
    ext = Path(path).suffix.lower()

    if ext == '.mp3':
        mp3 = MP3(path)

        mp3_title = mp3['TIT2'].text[0] if 'TIT2' in mp3 else name
        mp3_album = mp3['TALB'].text[0] if 'TALB' in mp3 else 'Unknown Album'
        mp3_artist = mp3['TPE1'].text[0] if 'TPE1' in mp3 else 'Unknown Artist'
        mp3_album_artist = mp3['TPE2'].text[0] if 'TPE2' in mp3 else mp3_artist
        mp3_track_number = int(mp3['TRCK'].text[0]) if 'TRCK' in mp3 else -1
        # mp3_disc_number

        mp3_year = mp3['TYE'].text if 'TYE' in mp3 else 'Unknown Year'
        #mp3_date = mp3['TDA'].text if 'TDA' in mp3 else -1
        mp3_is_compil = mp3['TCP'].text[0] if 'TCP' in mp3 else -1

        mp3_genre = mp3['TCO'].text[0] if 'TCO' in mp3 else -1
        mp3_composer = mp3['TCM'].text[0] if 'TCM' in mp3 else -1
        mp3_comment = mp3['COM'].text[0] if 'COM' in mp3 else -1
        mp3_copyright = mp3['TCR'].text[0] if 'TCR' in mp3 else -1
        mp3_isrc = mp3['TRC'].text[0] if 'TRC' in mp3 else -1
        mp3_lyrics = mp3['ULT'].text[0] if 'ULT' in mp3 else -1

        mp3_length = mp3.info.length
        mp3_bitrate = mp3.info.bitrate
        mp3_channels = mp3.info.channels
        mp3_sample_rate = mp3.info.sample_rate
        mp3_mime = mp3.mime[0]

        return { 'title': mp3_title, 'album': mp3_album, 'artist': mp3_artist, 'album_artist': mp3_album_artist, 'track_number': mp3_track_number, 'year': mp3_year, 'is_compil': mp3_is_compil, 'genre': mp3_genre, 'composer': mp3_composer, 'comment': mp3_comment, 'copyright': mp3_copyright, 'isrc': mp3_isrc, 'lyrics': mp3_lyrics, 'length': mp3_length, 'bitrate': mp3_bitrate, 'channels': mp3_channels, 'sample_rate': mp3_sample_rate, 'mime': mp3_mime }
    
    if ext == '.flac':
        flac = FLAC(path)

        flac_title = flac['TITLE'][0] if 'TITLE' in flac else name
        flac_album = flac['ALBUM'][0] if 'ALBUM' in flac else 'Unknown Album'
        flac_artist = flac['ARTIST'] if 'ARTIST' in flac else 'Unknown Artist'
        flac_album_artist = flac['ALBUMARTIST'] if 'ALBUMARTIST' in flac else flac_artist
        flac_track_number = int(flac['TRACKNUMBER'][0]) if 'TRACKNUMBER' in flac else -1
        # flac_disc_number

        flac_year = flac['DATE'] if 'DATE' in flac else 'Unknown Year'
        flac_is_compil = -2

        flac_genre = flac['GENRE'] if 'GENRE' in flac else -1
        flac_composer = flac['COMPOSER'] if 'COMPOSER' in flac else -1
        flac_comment = flac['COMMENT'] if 'COMMENT' in flac else -1
        flac_copyright = flac['COPYRIGHT'] if 'COPYRIGHT' in flac else -1
        flac_isrc = flac['ISRC'][0] if 'ISRC' in flac else -1
        flac_lyrics = flac['LYRICS'] if 'LYRICS' in flac else -1

        flac_length = flac.info.length
        flac_bitrate = flac.info.bitrate
        flac_channels = flac.info.channels
        flac_sample_rate = flac.info.sample_rate
        flac_mime = flac.mime[0]

        return {'title': flac_title, 'album': flac_album, 'artist': flac_artist, 'album_artist': flac_album_artist, 'track_number': flac_track_number, 'year': flac_year, 'is_compil': flac_is_compil, 'genre': flac_genre, 'composer': flac_composer, 'comment': flac_comment, 'copyright': flac_copyright, 'isrc': flac_isrc, 'lyrics': flac_lyrics, 'length': flac_length, 'bitrate': flac_bitrate, 'channels': flac_channels, 'sample_rate': flac_sample_rate, 'mime': flac_mime }

    if ext == '.m4a' or ext == 'mp4':
        mp4 = MP4(path)

        mp4_title = mp4['\xa9nam'][0] if '\xa9nam' in mp4 else name
        mp4_album = mp4['\xa9alb'][0] if '\xa9alb' in mp4 else 'Unknown Album'
        mp4_artist = mp4['\xa9ART'] if '\xa9ART' in mp4 else 'Unknown Artist'
        mp4_album_artist = mp4['aART'] if 'aART' in mp4 else mp4_artist
        mp4_track_number = mp4['trkn'][0] if 'trkn' in mp4 else -1
        mp4_disc_number = mp4['disk'][0] if 'disk' in mp4 else -1

        mp4_year = mp4['\xa9day'] if '\xa9day' in mp4 else 'Unknown Year'
        mp4_is_compil = 1 if 'cpil' in mp4 and mp4['cpil'] is True else 0

        mp4_genre = mp4['\xa9gen'] if '\xa9gen' in mp4 else -1
        mp4_composer = mp4['\xa9wrt'] if '\xa9wrt' in mp4 else -1
        mp4_comment = mp4['\xa9cmt'] if '\xa9cmt' in mp4 else -1
        mp4_copyright = mp4['cprt'] if 'cprt' in mp4 else -1
        mp4_isrc = mp4['isrc'][0] if 'isrc' in mp4 else -1
        mp4_lyrics = mp4['\xa9lyr'] if '\xa9lyr' in mp4 else -1

        mp4_length = mp4.info.length
        mp4_bitrate = mp4.info.bitrate
        mp4_channels = mp4.info.channels
        mp4_sample_rate = mp4.info.sample_rate
        mp4_mime = mp4.mime[0]

        return {'title': mp4_title, 'album': mp4_album, 'artist': mp4_artist, 'album_artist': mp4_album_artist, 'track_number': mp4_track_number, 'year': mp4_year, 'is_compil': mp4_is_compil, 'genre': mp4_genre, 'composer': mp4_composer, 'comment': mp4_comment, 'copyright': mp4_copyright, 'isrc': mp4_isrc, 'lyrics': mp4_lyrics, 'length': mp4_length, 'bitrate': mp4_bitrate, 'channels': mp4_channels, 'sample_rate': mp4_sample_rate, 'mime': mp4_mime }

    if ext == '.wav':
        wave = WAVE(path)

        wave_title = wave['TIT2'][0] if 'TIT2' in wave else name
        wave_album = wave['TALB'][0] if 'TALB' in wave else 'Unknown Album'
        wave_artist = wave['TPE1'] if 'TPE1' in wave else 'Unknown Artist'
        wave_album_artist = wave['TPE2'] if 'TPE2' in wave else wave_artist
        wave_track_number = wave['TRCK'][0] if 'TRCK' in wave else -1
        wave_disc_number = wave['TPOS'][0] if 'TPOS' in wave else -1

        wave_year = wave['TDRC'] if 'TDRC' in wave else 'Unknown Year'
        wave_is_compil = -2

        wave_genre = wave['TCON'] if 'TCON' in wave else -1
        wave_composer = wave['TCOM'] if 'TCOM' in wave else -1
        wave_comment = wave['COMM'] if 'COMM' in wave else -1
        wave_copyright = wave['TCOP'] if 'TCOP' in wave else -1
        wave_isrc = wave['TSRC'][0] if 'TSRC' in wave else -1
        wave_lyrics = wave['TXXX:LYRICS'] if 'TXXX:LYRICS' in wave else -1

        wave_length = wave.info.length
        wave_bitrate = wave.info.bitrate
        wave_channels = wave.info.channels
        wave_sample_rate = wave.info.sample_rate
        wave_mime = wave.mime[0]

        return {'title': wave_title, 'album': wave_album, 'artist': wave_artist, 'album_artist': wave_album_artist, 'track_number': wave_track_number, 'year': wave_year, 'is_compil': wave_is_compil, 'genre': wave_genre, 'composer': wave_composer, 'comment': wave_comment, 'copyright': wave_copyright, 'isrc': wave_isrc, 'lyrics': wave_lyrics, 'length': wave_length, 'bitrate': wave_bitrate, 'channels': wave_channels, 'sample_rate': wave_sample_rate, 'mime': wave_mime }