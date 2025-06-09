# CSV Analysis API Documentation

## Overview

The CSV Analysis API is a FastAPI-based service that allows users to upload CSV files and perform AI-powered analysis using LangChain and OpenAI. The API provides endpoints for file management, intelligent data analysis, and structured insights generation.

**Base URL**: `http://localhost:8000`  
**API Version**: `v1`  
**API Prefix**: `/api/v1`

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Upload CSV](#upload-csv)
  - [Analyze CSV](#analyze-csv)
  - [Generate Insights](#generate-insights)
  - [List Files](#list-files)
  - [Delete File](#delete-file)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)
- [Examples](#examples)
- [Setup Instructions](#setup-instructions)

## Authentication

Currently, the API does not require authentication. However, for the analysis functionality to work, you need to set up an OpenAI API key in the environment variables.

**Environment Variable**: `OPENAI_API_KEY`

## Endpoints

### Health Check

Check the health status of the API.

**Endpoint**: `GET /api/v1/health`

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-06-09T13:15:19.979388"
}
```

**Example**:
```bash
curl http://localhost:8000/api/v1/health
```

---

### Upload CSV

Upload a CSV file for analysis.

**Endpoint**: `POST /api/v1/csv/upload`

**Content-Type**: `multipart/form-data`

**Parameters**:
- `file` (required): CSV file to upload

**File Requirements**:
- File extension: `.csv`
- Maximum size: 10MB
- Format: Standard CSV format

**Response**:
```json
{
  "filename": "sample_data.csv",
  "size": 455,
  "rows": 10,
  "columns": ["Name", "Age", "City", "Salary", "Department", "Experience"],
  "message": "File uploaded successfully"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/csv/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_data.csv"
```

**Error Responses**:
- `400 Bad Request`: Invalid file type or size
- `500 Internal Server Error`: File processing error

---

### Analyze CSV

Perform AI-powered analysis on an uploaded CSV file.

**Endpoint**: `POST /api/v1/csv/analyze`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "query": "What is the average salary by department?",
  "filename": "sample_data.csv"
}
```

**Parameters**:
- `query` (string, required): Analysis question or query
- `filename` (string, required): Name of the uploaded CSV file

**Response**:
```json
{
  "query": "What is the average salary by department?",
  "analysis": "1. The average salary by department is as follows:\n   - Engineering: $74750\n   - Marketing: $77000\n   - Design: $66666.67\n\n2. Key insights from the data:\n   - The dataset consists of 10 rows and 6 columns...",
  "filename": "sample_data.csv",
  "timestamp": "2025-06-09T13:15:55.432989"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/csv/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the average salary by department?",
    "filename": "sample_data.csv"
  }'
```

**Error Responses**:
- `404 Not Found`: File not found
- `500 Internal Server Error`: Analysis error or missing OpenAI API key

---

### Generate Insights

Generate structured insights (cards and charts) from uploaded CSV file using AI.

**Endpoint**: `POST /api/v1/insights/generate`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "filename": "sample_data.csv"
}
```

**Parameters**:
- `filename` (string, required): Name of the uploaded CSV file

**Response**:
```json
{
  "card": {
    "title": "Average Salary Across Departments",
    "columns_used": ["Salary"],
    "response_description": "This card displays the average salary of employees across all departments in the dataset.",
    "value": 72600,
    "type": "card"
  },
  "chart": {
    "title": "Employee Distribution by Department",
    "labels": ["Engineering", "Marketing", "Design"],
    "data": [4.0, 3.0, 3.0],
    "type": "chart"
  },
  "filename": "sample_data.csv",
  "timestamp": "2025-06-09T14:52:08.017820"
}
```

**Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/insights/generate" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "sample_data.csv"
  }'
```

**Error Responses**:
- `404 Not Found`: File not found
- `500 Internal Server Error`: Insights generation error or missing OpenAI API key

---

### List Files

Get a list of all uploaded CSV files.

**Endpoint**: `GET /api/v1/csv/files`

**Response**:
```json
["sample_data.csv", "another_file.csv"]
```

**Example**:
```bash
curl http://localhost:8000/api/v1/csv/files
```

---

### Delete File

Delete an uploaded CSV file.

**Endpoint**: `DELETE /api/v1/csv/files/{filename}`

**Parameters**:
- `filename` (path parameter): Name of the file to delete

**Response**:
```json
{
  "message": "File sample_data.csv deleted successfully"
}
```

**Example**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/csv/files/sample_data.csv"
```

**Error Responses**:
- `404 Not Found`: File not found

## Data Models

### CSVUploadResponse
```json
{
  "filename": "string",
  "size": "integer",
  "rows": "integer",
  "columns": ["string"],
  "message": "string"
}
```

### AnalysisRequest
```json
{
  "query": "string",
  "filename": "string"
}
```

### AnalysisResponse
```json
{
  "query": "string",
  "analysis": "string",
  "filename": "string",
  "timestamp": "string"
}
```

### InsightsRequest
```json
{
  "filename": "string"
}
```

### InsightsResponse
```json
{
  "card": {
    "title": "string",
    "columns_used": ["string"],
    "response_description": "string",
    "value": "number",
    "type": "string"
  },
  "chart": {
    "title": "string",
    "labels": ["string"],
    "data": ["number"],
    "type": "string"
  },
  "filename": "string",
  "timestamp": "string"
}
```

### Card
```json
{
  "title": "string",
  "columns_used": ["string"],
  "response_description": "string",
  "value": "number",
  "type": "string"
}
```

### Chart
```json
{
  "title": "string",
  "labels": ["string"],
  "data": ["number"],
  "type": "string"
}
```

### ErrorResponse
```json
{
  "error": "string",
  "message": "string",
  "details": "object (optional)"
}
```

### HealthResponse
```json
{
  "status": "string",
  "version": "string",
  "timestamp": "string"
}
```

## Error Handling

The API uses standard HTTP status codes and returns error responses in the following format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "details": {
    "additional_info": "value"
  }
}
```

**Common Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limits

Currently, there are no rate limits implemented. However, consider implementing rate limiting for production use.

## Examples

### Complete Workflow Example

1. **Upload a CSV file**:
```bash
curl -X POST "http://localhost:8000/api/v1/csv/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data.csv"
```

2. **List uploaded files**:
```bash
curl http://localhost:8000/api/v1/csv/files
```

3. **Generate structured insights**:
```bash
curl -X POST "http://localhost:8000/api/v1/insights/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "data.csv"
  }'
```

4. **Analyze the data with custom query**:
```bash
curl -X POST "http://localhost:8000/api/v1/csv/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key trends in this dataset?",
    "filename": "data.csv"
  }'
```

### Python Example

```python
import requests

# Base URL
base_url = "http://localhost:8000/api/v1"

# Upload file
with open("data.csv", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{base_url}/csv/upload", files=files)
    print("Upload response:", response.json())

# Generate insights
insights_data = {"filename": "data.csv"}
response = requests.post(f"{base_url}/insights/generate", json=insights_data)
insights = response.json()
print("Card:", insights["card"])
print("Chart:", insights["chart"])

# Analyze data
analysis_data = {
    "query": "What is the correlation between age and salary?",
    "filename": "data.csv"
}
response = requests.post(f"{base_url}/csv/analyze", json=analysis_data)
print("Analysis response:", response.json())
```

### JavaScript Example

```javascript
// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/csv/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log('Upload success:', data));

// Generate insights
fetch('http://localhost:8000/api/v1/insights/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    filename: 'data.csv'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Card insight:', data.card);
  console.log('Chart insight:', data.chart);
});

// Analyze data
fetch('http://localhost:8000/api/v1/csv/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'What are the main insights?',
    filename: 'data.csv'
  })
})
.then(response => response.json())
.then(data => console.log('Analysis result:', data));
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the server**:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

### API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## File Format Requirements

### CSV File Requirements
- **Format**: Standard CSV (Comma-Separated Values)
- **Encoding**: UTF-8
- **Headers**: First row should contain column names
- **Size Limit**: 10MB maximum
- **Supported Extensions**: `.csv`

### Sample CSV Format
```csv
Name,Age,City,Salary,Department
John Doe,28,New York,75000,Engineering
Jane Smith,32,San Francisco,85000,Marketing
```

## Analysis Capabilities

The AI analysis can handle various types of queries:

- **Statistical Analysis**: Averages, distributions, correlations
- **Trend Analysis**: Patterns and trends in the data
- **Comparative Analysis**: Comparing different groups or categories
- **Insight Generation**: Key findings and recommendations
- **Data Summarization**: Concise summaries of large datasets

### Structured Insights

The insights generation provides ready-to-use components for frontend applications:

#### Card Insights
- **Purpose**: Display key metrics and summary statistics
- **Examples**: Total sales, average salary, customer count, revenue metrics
- **Usage**: Dashboard cards, KPI displays, summary widgets

#### Chart Insights
- **Purpose**: Visualize trends, distributions, and comparisons
- **Examples**: Daily revenue charts, department distributions, time series data
- **Usage**: Bar charts, line charts, pie charts, trend visualizations

### Example Queries
- "What is the average salary by department?"
- "Show me the age distribution"
- "Which city has the highest average salary?"
- "What are the key trends in this dataset?"
- "Find correlations between experience and salary"

## Support

For technical support or questions:
- Check the API documentation at `/docs`
- Review error messages in the response
- Ensure all required environment variables are set
- Verify file format and size requirements

---

**Version**: 1.0.0  
**Last Updated**: June 2025 