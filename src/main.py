from fastapi import FastAPI
from .routers.auth_router import router
from contextlib import asynccontextmanager
from .database import init_db
from .core.third_party.oauth_client import *
from .core.config import settings
from starlette.middleware.sessions import SessionMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    init_google()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.CSRF_KEY)

app.include_router(router)

