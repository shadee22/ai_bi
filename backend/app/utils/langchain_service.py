import os
import pandas as pd
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.core.config import settings


class LangChainService:
    """Service for LangChain-based CSV analysis."""
    
    def __init__(self):
        """Initialize LangChain service."""
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Initialize OpenAI model
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            api_key=settings.openai_api_key
        )
        
        # Create analysis chain
        self.analysis_chain = self._create_analysis_chain()
    
    def _create_analysis_chain(self):
        """Create the analysis chain for CSV data."""
        
        # Define the prompt template
        prompt = ChatPromptTemplate.from_template("""
You are a data analyst expert. Analyze the following CSV data based on the user's query.

CSV Data Summary:
{csv_summary}

User Query: {query}

Please provide a comprehensive analysis that includes:
1. Direct answer to the user's question
2. Key insights from the data
3. Relevant statistics or patterns
4. Recommendations if applicable

Analysis:
""")
        
        # Create the chain
        chain = (
            {"csv_summary": RunnablePassthrough(), "query": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    async def analyze_csv(self, df: pd.DataFrame, query: str) -> str:
        """Analyze CSV data based on user query."""
        try:
            # Get CSV summary
            csv_summary = self._get_detailed_summary(df)
            
            # Run analysis
            result = await self.analysis_chain.ainvoke({
                "csv_summary": csv_summary,
                "query": query
            })
            
            return result
            
        except Exception as e:
            raise Exception(f"Error during analysis: {str(e)}")
    
    def _get_detailed_summary(self, df: pd.DataFrame) -> str:
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
            summary += f"- {col}: {unique_count} unique values\n"
        
        return summary 