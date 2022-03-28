from app.api.api_v1.command import router as command_router
from app.api.api_v1.history import router as history_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(command_router, prefix="/command", tags=["Command"])
api_router.include_router(history_router, prefix="/history", tags=["History"])
