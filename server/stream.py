from utils import *

import io #test
from PIL import Image # test

router = APIRouter()

@router.get("/stream/{path:path}")
async def api_stream(path: str, range: str = Header(None), img: int = None):
  path_file = get_abs_path('test', f'{path}')

  if check_ext_valid(str(path_file)) == False:
    raise HTTPException(status_code=404)

  music_file = File(path_file)
  music_mime = music_file.mime[0] # 해당 부분 extract_metadata와 통합 필요

  file_size = path_file.stat().st_size
  file_chunk = int(file_size * 0.5) # 50% of file size

  ## 이미지 처리 부분 image.py로 이동하기, 테스트 용도로 이곳에 작성.
  if img == 1:
    img_size = (500, 500)

    test = extract_metadata(path_file)
    test_img = Image.open(io.BytesIO(test.m_image()))
    test_img.thumbnail(img_size)
    test_img.save('test.jpeg') # 정상작동, DB에 파일 등록 이후 data/cache에 일괄 저장하는 방향으로

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

  # 아래 부분 다시 작성할 필요 있음

  with open(path_file, "rb") as path_file:
    path_file.seek(audio_start)
    data = path_file.read(audio_end - audio_start + 1)

    headers = {
      'Content-Range': f'bytes {audio_start}-{audio_end}/{file_size}',
      'Accept-Ranges': 'bytes',
      'Content-Length': str(audio_end - audio_start + 1),
      'Content-Type': music_mime
    }

    return Response(data, status_code=206, headers=headers)