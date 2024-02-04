from server.utils.modules import *

router = APIRouter()

@router.get("/stream/{path:path}")
async def api_stream(path: str, range: str = Header(None)):
  file_path = os.path.join(await get_root_path(), f"{path}")

  if await check_ext_valid(file_path) == False:
    raise HTTPException(status_code=404)

  music_file = File(file_path)
  music_mime = music_file.mime[0]

  file_size = os.path.getsize(file_path)
  file_chunk = int(file_size * 0.5) # 50% of file size

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

  with open(file_path, "rb") as file_path:
    file_path.seek(audio_start)
    data = file_path.read(audio_end - audio_start + 1)

    headers = {
      'Content-Range': f'bytes {audio_start}-{audio_end}/{file_size}',
      'Accept-Ranges': 'bytes',
      'Content-Length': str(audio_end - audio_start + 1),
      'Content-Type': music_mime
    }

    return Response(data, status_code=206, headers=headers)