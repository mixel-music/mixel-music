from utils import *

router = APIRouter()

@router.get("/stream/{path:path}")
async def api_stream(path: str, range: str = Header(None)):
  path_file = get_abs_path('test', f'{path}')

  if check_ext_valid(str(path_file)) == False:
    raise HTTPException(status_code=404)

  mime = audio_tags(path_file)
  mime = mime.get('mime')

  file_size = path_file.stat().st_size
  file_chunk = int(file_size * 0.25) # 25% of file size
  
  if range:
    audio_range = range.replace("bytes=", "").split("-")
    audio_start = int(audio_range[0])
    audio_end = int(audio_range[1]) if audio_range[1] else audio_start + file_chunk
  else:
    audio_start = 0
    audio_end = audio_start + file_chunk

  """
  Ensure audio_end does not exceed the file size
  """
  audio_end = min(audio_end, file_size - 1)

  async with aiofiles.open(path_file, mode="rb") as path_file:
    await path_file.seek(audio_start)
    data = await path_file.read(audio_end - audio_start + 1)

    headers = {
      'Content-Range': f'bytes {audio_start}-{audio_end}/{file_size}',
      'Accept-Ranges': 'bytes',
      'Content-Length': str(audio_end - audio_start + 1),
      'Content-Type': mime
    }

    return Response(data, status_code=status.HTTP_206_PARTIAL_CONTENT, headers=headers)