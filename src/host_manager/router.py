from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from src.auth.manager import current_user
from src.auth.models import User
from src.host_manager.domain import Host
from src.host_manager.manager import HostManager, get_host_manager
from src.host_manager.schemas import CreateHost

router = APIRouter()


@router.get("/current_host")
async def get_current_host(
    manager: Annotated[HostManager, Depends(get_host_manager)]
) -> Optional[Host]:
    return manager.read_host_from_file()


@router.post("/create_host")
async def create_host(
    manager: Annotated[HostManager, Depends(get_host_manager)],
    curr_user: Annotated[User, Depends(current_user)],
    create_host: CreateHost = Depends(),

) -> None:
    host = Host(
        ip=create_host.ip,
        port=create_host.port,
        user_id=curr_user.id,
    )
    manager.write_host_to_file(host)
