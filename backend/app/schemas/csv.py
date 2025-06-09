from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CSVUploadResponse(BaseModel):
    """Response model for CSV upload."""
    filename: str
    size: int
    rows: int
    columns: List[str]
    message: str = "File uploaded successfully"


class AnalysisRequest(BaseModel):
    """Request model for CSV analysis."""
    query: str = Field(..., description="The analysis query for the CSV data")
    filename: str = Field(..., description="The filename to analyze")


class AnalysisResponse(BaseModel):
    """Response model for CSV analysis."""
    query: str
    analysis: str
    filename: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = "healthy"
    version: str
    timestamp: str 