from fastapi import FastAPI

from src.auth.backends import auth_backend
from src.auth.manager import fastapi_users
from src.auth.schemas import UserRead, UserCreate

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


@app.get("/")
async def root():
    return {"message": "Hello World"}
