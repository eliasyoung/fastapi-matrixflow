from fastapi import APIRouter

from app.api.routes import matrix_workflow

api_router = APIRouter()
api_router.include_router(matrix_workflow.router)
