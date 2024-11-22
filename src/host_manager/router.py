from time import sleep
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Body

from src.auth.manager import current_user
from src.auth.models import User
from src.host_manager.domain import Host
from src.host_manager.manager import HostManager, get_host_manager
from src.host_manager.schemas import CreateHost

router = APIRouter()


def clear_host(
    manager: HostManager, delay: int = 600
) -> None:
    sleep(delay)
    manager.clear_host_from_file()


@router.get("/current_host")
async def get_current_host(
    manager: Annotated[HostManager, Depends(get_host_manager)]
) -> Optional[Host]:
    return manager.read_host_from_file()


@router.post("/create_host")
async def create_host(
    manager: Annotated[HostManager, Depends(get_host_manager)],
    curr_user: Annotated[User, Depends(current_user)],
    background_tasks: BackgroundTasks,
    create_host: CreateHost = Body(),
):
    host = Host(
        ip=create_host.ip,
        port=create_host.port,
        user_id=curr_user.id,
    )
    try:
        manager.write_host_to_file(host)
    except FileExistsError as e:
        host = manager.read_host_from_file()
        raise HTTPException(
            400, f"Host already exists: {host.model_dump()}"
        )
    background_tasks.add_task(clear_host, manager, 600)

    return {"message": "You are a host on next 10 min"}


@router.get("/clear_host")
async def clear_host(
    manager: Annotated[HostManager, Depends(get_host_manager)],
    curr_user: Annotated[User, Depends(current_user)],
):
    if curr_user.id != manager.read_host_from_file().user_id:
        raise HTTPException(403, "Permission denied")

    manager.clear_host_from_file()
