from datetime import datetime
from fastapi import APIRouter
from app.schemas.csv import HealthResponse
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.version,
        timestamp=datetime.now().isoformat()
    ) 