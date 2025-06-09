import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.insights import InsightsRequest, InsightsResponse
from app.utils.csv_handler import CSVHandler
from app.utils.insights_service import InsightsService

router = APIRouter()

# Initialize services
csv_handler = CSVHandler()
insights_service = None


def get_insights_service():
    """Dependency to get insights service."""
    global insights_service
    if insights_service is None:
        try:
            insights_service = InsightsService()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return insights_service


@router.post("/generate", response_model=InsightsResponse)
async def generate_insights(
    request: InsightsRequest,
    insights_service: InsightsService = Depends(get_insights_service)
):
    """Generate structured insights (card and chart) from uploaded CSV file."""
    try:
        # Check if file exists
        file_path = os.path.join("uploads", request.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Read CSV
        df = csv_handler.read_csv(file_path)
        
        # Generate insights
        insights_result = await insights_service.generate_insights(df, request.filename)
        
        return insights_result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}") 