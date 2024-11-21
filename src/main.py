from fastapi import FastAPI

from src.auth.backends import auth_backend
from src.auth.manager import fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.host_manager.router import router
from src.world_sync.router import router as world_sync
app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(
        UserRead, UserCreate
    ),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(router)
app.include_router(world_sync)

@app.get("/")
async def root():
    return {"message": "Hello World"}
