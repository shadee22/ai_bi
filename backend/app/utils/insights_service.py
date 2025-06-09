import pandas as pd
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
from app.schemas.insights import Card, Chart, InsightsResponse
from app.core.config import settings


class InsightsService:
    """Service for generating structured insights from CSV data using real Python execution."""
    
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
        """Generate structured insights (card and chart) from CSV data using real calculations."""
        try:
            # Step 1: Use Python execution to get real calculated values
            calculated_metrics = await self._calculate_real_metrics(df)
            
            # Step 2: Use structured output to format the insights
            insights_result = await self._format_insights_with_real_data(df, calculated_metrics)
            
            # Add filename and timestamp
            insights_result.filename = filename
            insights_result.timestamp = pd.Timestamp.now().isoformat()
            
            return insights_result
            
        except Exception as e:
            raise Exception(f"Error generating insights: {str(e)}")
    
    async def _calculate_real_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Use real Python execution to calculate actual metrics from the data."""
        try:
            # Create Python tool with access to the DataFrame
            tool = PythonAstREPLTool(locals={"df": df})
            
            # Bind tools to LLM
            llm_with_tools = self.llm.bind_tools([tool], tool_choice=tool.name)
            
            # Create prompt for calculating real metrics
            df_sample = df.head(3).to_markdown()
            df_info = f"Shape: {df.shape}, Columns: {list(df.columns)}"
            
            system_message = f"""You are a data analyst expert. You have access to a pandas DataFrame called 'df'.

Here is a sample of the data:
```
{df_sample}
```

DataFrame Info:
{df_info}

Calculate the following key metrics from the REAL data and return them as Python code:
1. Total count of records
2. Average of numeric columns (if they exist)
3. Distribution of categorical columns (if they exist)
4. Any other meaningful metrics for this dataset

Return ONLY the Python code that calculates these metrics. Use actual pandas operations.
Examples:
- Total count: len(df)
- Average salary: df['Salary'].mean() if 'Salary' in df.columns else None
- Department distribution: df['Department'].value_counts().to_dict() if 'Department' in df.columns else None
"""
            
            # Get real calculations
            response = await llm_with_tools.ainvoke(system_message)
            
            if hasattr(response, 'tool_calls') and response.tool_calls:
                tool_call = response.tool_calls[0]
                code_to_execute = tool_call['args']['query']
                
                try:
                    result = tool.invoke(code_to_execute)
                    return {"calculated_metrics": result, "raw_code": code_to_execute}
                except Exception as e:
                    return {"error": str(e), "raw_code": code_to_execute}
            else:
                return {"error": "No calculations generated"}
                
        except Exception as e:
            return {"error": f"Calculation error: {str(e)}"}
    
    async def _format_insights_with_real_data(self, df: pd.DataFrame, calculated_metrics: Dict[str, Any]) -> InsightsResponse:
        """Use structured output to format insights with real calculated data."""
        try:
            # Create structured output model
            model_with_structure = self.llm.with_structured_output(InsightsResponse)
            
            # Prepare context with real data
            data_context = self._get_data_context(df, calculated_metrics)
            
            # Create prompt for insights generation with real data
            prompt = ChatPromptTemplate.from_template("""
You are a data analyst expert. Create structured insights using the REAL calculated data provided.

Data Context:
{data_context}

Real Calculated Metrics:
{calculated_metrics}

Based on this REAL data, generate:
1. A CARD insight that shows a key metric using the actual calculated values
2. A CHART insight that shows a trend or distribution using the real data

Guidelines:
- Use the ACTUAL calculated values provided, not estimates
- For the CARD: Choose the most meaningful metric from the real calculations
- For the CHART: Create a meaningful visualization with the real data points
- Ensure all numeric values match the calculated metrics exactly
- Make the insights relevant and actionable based on the real data

Generate exactly one card and one chart using the real calculated data.
""")
            
            # Generate insights with real data
            chain = prompt | model_with_structure
            result = await chain.ainvoke({
                "data_context": data_context,
                "calculated_metrics": str(calculated_metrics)
            })
            
            return result
            
        except Exception as e:
            raise Exception(f"Error formatting insights: {str(e)}")
    
    def _get_data_context(self, df: pd.DataFrame, calculated_metrics: Dict[str, Any]) -> str:
        """Get context about the data for insights generation."""
        context = f"""
Dataset Overview:
- Total rows: {len(df)}
- Total columns: {len(df.columns)}
- Column names: {', '.join(df.columns.tolist())}

Data Types:
{df.dtypes.to_string()}

Sample Data (first 5 rows):
{df.head(5).to_markdown()}

Numeric Columns Available: {[col for col in df.columns if df[col].dtype in ['int64', 'float64']]}
Categorical Columns Available: {[col for col in df.columns if df[col].dtype == 'object']}
"""
        return context 