import pandas as pd
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.insights import Card, Chart, InsightsResponse
from app.core.config import settings


class InsightsService:
    """Service for generating structured insights from CSV data."""
    
    def __init__(self):
        """Initialize insights service."""
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Initialize OpenAI model
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            api_key=settings.openai_api_key
        )
    
    async def generate_insights(self, df: pd.DataFrame, filename: str) -> InsightsResponse:
        """Generate structured insights (card and chart) from CSV data."""
        try:
            # Get data summary for context
            data_summary = self._get_data_summary(df)
            
            # Create structured output model
            model_with_structure = self.llm.with_structured_output(InsightsResponse)
            
            # Create prompt for insights generation
            prompt = ChatPromptTemplate.from_template("""
You are a data analyst expert. Analyze the following CSV data and generate structured insights.

CSV Data Summary:
{data_summary}

Based on this data, generate:
1. A CARD insight that shows a key metric (like total sales, average salary, total count, etc.)
2. A CHART insight that shows a trend or distribution (like daily revenue, department distribution, etc.)

Guidelines:
- For the CARD: Choose the most meaningful metric from the data, calculate it, and provide a clear title
- For the CHART: Create a meaningful visualization with appropriate labels and data points
- Use actual data from the CSV to calculate real values
- Make the insights relevant and actionable
- Ensure all numeric values are calculated from the actual data

Generate exactly one card and one chart that would be most valuable for understanding this dataset.
""")
            
            # Generate insights
            chain = prompt | model_with_structure
            result = await chain.ainvoke({"data_summary": data_summary})
            
            # Add filename and timestamp
            result.filename = filename
            result.timestamp = pd.Timestamp.now().isoformat()
            
            return result
            
        except Exception as e:
            raise Exception(f"Error generating insights: {str(e)}")
    
    def _get_data_summary(self, df: pd.DataFrame) -> str:
        """Get a detailed summary of the CSV data for analysis."""
        summary = f"""
Dataset Overview:
- Total rows: {len(df)}
- Total columns: {len(df.columns)}
- Column names: {', '.join(df.columns.tolist())}

Data Types:
{df.dtypes.to_string()}

Sample Data (first 10 rows):
{df.head(10).to_string()}

Statistical Summary:
{df.describe().to_string()}

Missing Values:
{df.isnull().sum().to_string()}

Unique Values per Column:
"""
        
        for col in df.columns:
            unique_count = df[col].nunique()
            if unique_count <= 20:  # Only show unique values if not too many
                unique_values = df[col].unique()[:10]  # Limit to first 10
                summary += f"- {col}: {unique_count} unique values - {unique_values}\n"
            else:
                summary += f"- {col}: {unique_count} unique values\n"
        
        return summary 