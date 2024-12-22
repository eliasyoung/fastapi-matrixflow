import sys
import logging

from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.main import api_router

from app.settings import settings
from app.database import sessionManager

from pydantic import BaseModel

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

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
