from utils import *

router = APIRouter()

@router.get("/stream/{path:path}")
async def api_stream(path: str, range: str = Header(None)):
    file_path = get_absolute_path('test', f'{path}')

    if is_valid_extension(file_path) == False:
        raise HTTPException(status_code=404)

    music_info = ExtractMediaTag.extract_tags(file_path)
    music_mime = music_info.get('mime')

    music_size = file_path.stat().st_size
    music_chunk = int(music_size * 0.25) # 25% of file size

    if range:
        music_range = range.replace("bytes=", "").split("-")
        music_start = int(music_range[0])
        music_end = int(music_range[1]) if music_range[1] else music_start + music_chunk
    else:
        music_start = 0
        music_end = music_start + music_chunk

    music_end = min(music_end, music_size - 1) # it does not exceed the file size
    logging.info('Load partical contents: "%s"', str(file_path.stem))

    async with aiofiles.open(file_path, mode="rb") as music_file:
        await music_file.seek(music_start)
        data = await music_file.read(music_end - music_start + 1)
        headers = {
            'Content-Range': f'bytes {music_start}-{music_end}/{music_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(music_end - music_start + 1),
            'Content-Type': music_mime
        }

        logging.debug('Headers: "%s"', str(headers))
        logging.debug('Music Tags: "%s"', music_info)

        return Response(data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)