import re
import hashlib
import mimetypes


tag_patterns = {
    'details': re.compile(r'\s*feat\.?\s.*'),
    'bracket': re.compile(r'\s*\([^)]*[:;,][^)]*\)'),
    'year_month_day': re.compile(r'^(\d{4})[-., ]?(\d{1,2})[-., ]?(\d{1,2})$'),
    'year_month': re.compile(r'^(\d{4})[-., ]?(\d{1,2})$'),
    'year': re.compile(r'^(\d{4})$'),
}


def get_mime(path: str) -> str:
    try:
        type = mimetypes.guess_type(path, strict=True)
        if type:
            return type[0]
        else:
            return 'application/octet-stream'
    except:
        return 'application/octet-stream'


def hash_str(*args) -> str:
    try:
        return hashlib.md5(''.join(str(arg) for arg in args).encode()).hexdigest()
    except ValueError:
        return ''


def safe_list(extra, key, default='') -> str:
    extra = dict(extra)
    
    try:
        value = extra.get(key, [default])
        return value[0] if value else default
    except:
        return ''


def convert_date(date: int | str) -> tuple[str, int]:
    try:
        if isinstance(date, int):
            date = str(date)
    
        match = tag_patterns['year_month_day'].match(date)
        if match:
            year, month, day = match.groups()
            month = month.zfill(2)
            day = day.zfill(2)

            return f"{year}-{month}-{day}", year

        match = tag_patterns['year_month'].match(date)
        if match:
            year, month = match.groups()
            month = month.zfill(2)

            return f"{year}-{month}", year

        match = tag_patterns['year'].match(date)
        if match:
            year = match.group(1)
            return year, year
        
    except:
        return '', 0


def convert_artist(name: str) -> str:
    try:
        artist_value = tag_patterns['bracket'].sub('', name)
        artist_value = tag_patterns['details'].sub('', name)

        return artist_value
    
    except:
        return ''
