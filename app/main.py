import sys
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.main import api_router

from app.settings import settings
from app.database import sessionManager

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.log_level == "DEBUG" else logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionManager._engine is not None:
        await sessionManager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
