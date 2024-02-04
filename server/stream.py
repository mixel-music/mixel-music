from fastapi import APIRouter, Response, HTTPException, Header
from server.utils.modules import *
from mutagen import MutagenError, mp3, m4a, mp4, flac, wave, oggopus, aac
import mutagen

router = APIRouter()

@router.get("/stream/{path:path}")
async def api_stream(path: str, range: str = Header(None)):
  ext_enable = [".mp3", ".m4a", ".flac", ".alac", ".wav", ".opus", ".aac"]
  ext_import = os.path.splitext(path)
  ext_import = ext_import[1]
  file_path = os.path.join(get_root_path(), "test", f"{path}")

  print(file_path)

  """
  Check valid ext to prevent directory traversal
  """
  if ext_import not in ext_enable or ".." in path: raise HTTPException(status_code=404)
  if not os.path.isfile(file_path): raise HTTPException(status_code=404)
  
  music_file = mutagen.File(file_path)
  music_mime = music_file.mime[0]
  music_tags_dict = music_file.tags
  #print(music_tags_dict['TIT2'])

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