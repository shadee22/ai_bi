import os
import pandas as pd
from typing import List, Tuple, Optional
from fastapi import UploadFile, HTTPException
from app.core.config import settings


class CSVHandler:
    """Utility class for handling CSV files."""
    
    @staticmethod
    def validate_file(file: UploadFile) -> None:
        """Validate uploaded file."""
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"File type not allowed. Allowed types: {settings.allowed_extensions}"
            )
        
        # Check file size
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_file_size} bytes"
            )
    
    @staticmethod
    async def save_file(file: UploadFile) -> str:
        """Save uploaded file and return file path."""
        # Create upload directory if it doesn't exist
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_path = os.path.join(settings.upload_dir, file.filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path
    
    @staticmethod
    def read_csv(file_path: str) -> pd.DataFrame:
        """Read CSV file and return DataFrame."""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading CSV file: {str(e)}"
            )
    
    @staticmethod
    def get_csv_info(df: pd.DataFrame) -> Tuple[int, List[str]]:
        """Get basic information about CSV data."""
        rows = len(df)
        columns = df.columns.tolist()
        return rows, columns
    
    @staticmethod
    def get_csv_summary(df: pd.DataFrame) -> str:
        """Get a summary of the CSV data."""
        summary = f"""
CSV Data Summary:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Column names: {', '.join(df.columns.tolist())}

Data Types:
{df.dtypes.to_string()}

First 5 rows:
{df.head().to_string()}

Basic Statistics:
{df.describe().to_string()}
"""
        return summary 