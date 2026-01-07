from fastapi import FastAPI
from .routers.auth_router import router
from contextlib import asynccontextmanager
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
