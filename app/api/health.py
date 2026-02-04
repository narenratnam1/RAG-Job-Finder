"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check endpoint
    """
    # Add checks for vector store, models, etc.
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "vector_store": "available",
            "embeddings": "available"
        }
    }
