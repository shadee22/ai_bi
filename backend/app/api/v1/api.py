from fastapi import APIRouter
from app.api.v1.endpoints import csv, health, insights

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(csv.router, prefix="/csv", tags=["csv"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"]) 