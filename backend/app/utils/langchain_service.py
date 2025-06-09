import os
import pandas as pd
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonAstREPLTool
from app.core.config import settings


class LangChainService:
    """Service for LangChain-based CSV analysis with actual data operations."""
    
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
    
    async def analyze_csv(self, df: pd.DataFrame, query: str) -> str:
        """Analyze CSV data with actual data operations using LangChain pandas approach."""
        try:
            # Create Python tool with access to the DataFrame
            tool = PythonAstREPLTool(locals={"df": df})
            
            # Bind tools to LLM
            llm_with_tools = self.llm.bind_tools([tool], tool_choice=tool.name)
            
            # Create a simple prompt with DataFrame context
            df_sample = df.head(3).to_markdown()
            df_info = f"Shape: {df.shape}, Columns: {list(df.columns)}"
            
            system_message = f"""You are a data analyst expert. You have access to a pandas DataFrame called 'df'.

            Here is a sample of the data:
            ```
            {df_sample}
            ```

            DataFrame Info:
            {df_info}

            Given a user question about this data, write Python code to answer it.
            - Use only pandas and built-in Python libraries
            - Return ONLY the valid Python code that will give the answer
            - Make sure your code actually queries/analyzes the real data
            - Return ONLY the specific calculation result, not the full DataFrame
            - For correlations, use: df[['column1', 'column2']].corr().iloc[0,1]
            - For averages by group, use: df.groupby('column')['value'].mean()
            - For counts, use: df['column'].value_counts()
            - For searching specific values, first check if they exist: df[df['column'].str.contains('value', case=False, na=False)]
            - When searching for names or specific values, use .str.contains() instead of exact matching to be more flexible
            - If searching for a specific person, use: df[df['Name'].str.contains('person_name', case=False, na=False)]['Age'].iloc[0] if len(df[df['Name'].str.contains('person_name', case=False, na=False)]) > 0 else "Person not found"

            Examples:
            - "What is the average salary by department?" → df.groupby('Department')['Salary'].mean()
            - "How many people are in each age group?" → df['Age'].value_counts().sort_index()
            - "What's the correlation between age and salary?" → df[['Age', 'Salary']].corr().iloc[0,1]
            - "What is the age of John Doe?" → df[df['Name'].str.contains('John Doe', case=False, na=False)]['Age'].iloc[0] if len(df[df['Name'].str.contains('John Doe', case=False, na=False)]) > 0 else "Person not found"
            """
            
            # Use the simple tool calling approach
            response = await llm_with_tools.ainvoke(
                f"{system_message}\n\nUser question: {query}"
            )

            print(response)
            
            # Extract and execute the tool call
            if hasattr(response, 'tool_calls') and response.tool_calls:
                tool_call = response.tool_calls[0]
                # Access the correct field - it's 'query' not 'code'
                code_to_execute = tool_call['args']['query']
                
                try:
                    result = tool.invoke(code_to_execute)
                    
                    # Format the result for better readability
                    if isinstance(result, (int, float)):
                        return f"The result is: {result}"
                    elif isinstance(result, pd.Series):
                        return f"Results:\n{result.to_string()}"
                    elif isinstance(result, pd.DataFrame):
                        return f"Results:\n{result.to_string()}"
                    else:
                        return str(result)
                        
                except IndexError as e:
                    return f"Error: No matching data found. The search returned no results. Please check if the name or criteria you're looking for exists in the dataset."
                except KeyError as e:
                    return f"Error: Column '{str(e)}' not found in the dataset. Available columns: {list(df.columns)}"
                except Exception as e:
                    return f"Error executing the analysis: {str(e)}. Please try rephrasing your question."
            else:
                return "No tool call generated. Please try rephrasing your question."
            
        except Exception as e:
            raise Exception(f"Error during analysis: {str(e)}")
    
