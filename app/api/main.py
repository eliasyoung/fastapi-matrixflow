from fastapi import APIRouter

from app.api.routes import matrix_workflow
from app.api.routes import user
from app.api.routes import signin

api_router = APIRouter()
api_router.include_router(matrix_workflow.router)
api_router.include_router(user.router)
api_router.include_router(signin.router)
