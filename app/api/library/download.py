from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from core.depends import get_library_repo
from tools.path_handler import get_filename, get_path

router = APIRouter()

@router.get("/download/{track_id}")
async def api_get_download(
    track_id: str,
    service: get_library_repo = Depends(),
) -> FileResponse:
    
    file_info = await service.get_track(track_id)
    return FileResponse(
        get_path(file_info.get('filepath')), filename=get_filename(file_info.get('filepath'))[0]
    )
