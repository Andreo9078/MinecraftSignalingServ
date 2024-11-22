import json
import os
import shutil
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from starlette.responses import FileResponse

from src.auth.manager import current_user
from src.auth.models import User
from src.config import WORLD_STORAGE_PATH
from src.host_manager.manager import HostManager, get_host_manager
from src.utils import generate_world_manifest


async def current_user_is_host(
    curr_user: Annotated[User, Depends(current_user)],
    manager: Annotated[HostManager, Depends(get_host_manager)]
) -> None:
    host = manager.read_host_from_file()
    if host is None:
        raise HTTPException(400, detail="You are not a host")

    if curr_user.id != host.user_id:
        raise HTTPException(400, detail="You are not a host")


router = APIRouter(
    dependencies=[Depends(current_user_is_host)],
)


@router.post("/world/files/{file_path:path}")
async def upload_world_file(
    file_path: str, file: UploadFile = File(...)
):
    """Сохраняет файл на сервере."""
    file_full_path = WORLD_STORAGE_PATH / file_path
    os.makedirs(file_full_path.parent, exist_ok=True)
    with open(file_full_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "Файл загружен."}


@router.get("/world/files/{file_path:path}")
async def get_world_file(file_path: str):
    """Возвращает отдельный файл мира."""
    file_full_path = WORLD_STORAGE_PATH / file_path
    if not file_full_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден.")
    return FileResponse(file_full_path)


@router.delete("/world/files/{file_path:path}")
async def delete_world_file(file_path: str):
    """Удаляет файл с сервера."""
    file_full_path = WORLD_STORAGE_PATH / file_path
    if file_full_path.exists():
        file_full_path.unlink()
        return {"message": "Файл удалён."}
    raise HTTPException(status_code=404, detail="Файл не найден.")


@router.get("/world/manifest")
async def get_world_manifest():
    """Возвращает манифест мира (хэши файлов)."""
    manifest_file = Path("world_manifest.json")
    if not manifest_file.exists():
        raise HTTPException(status_code=404, detail="Манифест мира не найден.")
    return FileResponse(manifest_file, media_type="application/json")


@router.post("/world/manifest/update")
async def update_manifest():
    """Обновляет серверный манифест."""
    manifest = generate_world_manifest(WORLD_STORAGE_PATH)
    manifest_path = Path("world_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f)
    return {"message": "Манифест обновлён."}
