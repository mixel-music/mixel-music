from pathlib import Path
from fastapi import FastAPI, Request, Response, HTTPException, Header
from fastapi.templating import Jinja2Templates

app = FastAPI()
tms = Jinja2Templates(directory="static").TemplateResponse

@app.get("/")
async def tamayaRouteMain(request: Request):
  return tms("index.html", context={"request": request})

@app.get("/api/{musicPath:path}")
async def tamayaMusicStreaming(musicPath: str, range: str = Header(None)):
  listAllowExtensions = ['.mp3', '.flac', '.wav', '.m4a', '.alac', '.opus', '.aac']
  fileExtensionHandle = ''.join(Path(musicPath).suffixes)

  # Security: Check valid extension to prevent directory traversal
  if fileExtensionHandle not in listAllowExtensions or ".." in musicPath:
     raise HTTPException(status_code=404, detail="404 Not Found")
  
  mediaPath = Path(f"media/{musicPath}")

  if not mediaPath.is_file():
     raise HTTPException(status_code=404, detail="404 Not Found")
  
  mediaSizeCheck = mediaPath.stat().st_size
  mediaChunkSize = int(mediaSizeCheck * 0.5) # Set 5% of the file size

  mediaStart, mediaEnd = range.replace("bytes=", "").split("-")
  mediaStart = int(mediaStart)
  mediaEnd = int(mediaEnd) if mediaEnd else mediaStart + mediaChunkSize
  mediaEnd = min(mediaEnd, mediaSizeCheck - 1) # Ensure 'mediaEnd' does not exceed the file size

  with open(mediaPath, "rb") as mediaFile:
    mediaFile.seek(mediaStart)
    data = mediaFile.read(mediaEnd - mediaStart + 1)

    headers = {
        'Content-Range': f'bytes {mediaStart}-{mediaEnd}/{mediaSizeCheck}',
        'Accept-Ranges': 'bytes',
    }
    return Response(data, status_code=206, headers=headers, media_type="audio/" + fileExtensionHandle)