import os
from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.schemas.csv import (
    CSVUploadResponse, 
    AnalysisRequest, 
    AnalysisResponse, 
    ErrorResponse
)
from app.utils.csv_handler import CSVHandler
from app.utils.langchain_service import LangChainService

router = APIRouter()


# Initialize services
csv_handler = CSVHandler()
langchain_service = None


def get_langchain_service():
    """Dependency to get LangChain service."""
    global langchain_service
    if langchain_service is None:
        try:
            langchain_service = LangChainService()
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return langchain_service


@router.post("/upload", response_model=CSVUploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file for analysis."""
    try:
        # Validate file
        csv_handler.validate_file(file)
        
        # Save file
        file_path = await csv_handler.save_file(file)
        
        # Read CSV and get info
        df = csv_handler.read_csv(file_path)
        rows, columns = csv_handler.get_csv_info(df)
        
        return CSVUploadResponse(
            filename=file.filename,
            size=file.size or 0,
            rows=rows,
            columns=columns,
            message="File uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_csv(
    request: AnalysisRequest,
    langchain_service: LangChainService = Depends(get_langchain_service)
):
    """Analyze uploaded CSV file with user query."""
    try:
        # Check if file exists
        file_path = os.path.join("uploads", request.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Read CSV
        df = csv_handler.read_csv(file_path)
        
        # Perform analysis
        analysis_result = await langchain_service.analyze_csv(df, request.query)
        
        return AnalysisResponse(
            query=request.query,
            analysis=analysis_result,
            filename=request.filename,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing file: {str(e)}")


@router.get("/files", response_model=List[str])
async def list_files():
    """List all uploaded CSV files."""
    try:
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            return []
        
        files = [f for f in os.listdir(upload_dir) if f.endswith('.csv')]
        return files
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """Delete an uploaded CSV file."""
    try:
        file_path = os.path.join("uploads", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        os.remove(file_path)
        return {"message": f"File {filename} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}") 