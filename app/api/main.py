from fastapi import APIRouter

from app.api.routes import matrix_flow

api_router = APIRouter()
api_router.include_router(matrix_flow.router)
