from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.CSRF_KEY)

app.include_router(router)

