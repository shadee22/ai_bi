from typing import List, Union
from pydantic import BaseModel, Field


class Card(BaseModel):
    """Card configuration with title, columns used, description, value, and type."""
    
    title: str = Field(description="The title of the card")
    columns_used: List[str] = Field(description="List of column names used for this card")
    response_description: str = Field(description="Description explaining what this card represents")
    value: Union[int, float] = Field(description="The main numeric value to display on the card")
    type: str = Field(default="card", description="The type of component, should be 'card'")


class Chart(BaseModel):
    """Chart configuration with title, labels, and data."""
    
    title: str = Field(description="The title of the chart")
    labels: List[str] = Field(description="List of labels for the X-axis")
    data: List[float] = Field(description="List of numeric values for the Y-axis corresponding to each label")
    type: str = Field(default="chart", description="The type of component, should be 'chart'")


class InsightsResponse(BaseModel):
    """Response model for insights generation."""
    
    card: Card = Field(description="A card insight from the data")
    chart: Chart = Field(description="A chart insight from the data")
    filename: str = Field(description="The filename that was analyzed")
    timestamp: str = Field(description="Timestamp of the analysis")


class InsightsRequest(BaseModel):
    """Request model for insights generation."""
    
    filename: str = Field(description="The filename to analyze for insights") 