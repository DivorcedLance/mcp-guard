# Router principal para la API v1
from fastapi import APIRouter
from .endpoints import chat, documents

router = APIRouter()
router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(documents.router, prefix="/documents", tags=["Documents"])
