from fastapi import APIRouter
from app.api.v1.endpoints import csv, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(csv.router, prefix="/csv", tags=["csv"]) 