import os
from typing import List, Dict, Any
import time

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models.yolo import model
from app.utils.config import config


app = FastAPI(
    title="YOLOv8 Object Detection API",
    description="API for detecting objects in images using YOLOv8",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to YOLOv8 Object Detection API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": os.path.basename(config.model_path),
        "device": model.device
    }


@app.post("/detect/", response_model_exclude_none=True)
async def detect_objects(
    file: UploadFile = File(...), 
    confidence: float = Form(None)
):
    """
    Detect objects in an uploaded image.
    
    - **file**: Image file to analyze
    - **confidence**: Confidence threshold (0.0 to 1.0)
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in config.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {config.allowed_extensions}"
        )
    
    # Read file
    start_time = time.time()
    contents = await file.read()
    
    # Check file size
    file_size_mb = len(contents) / (1024 * 1024)
    if file_size_mb > config.max_file_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the {config.max_file_size_mb}MB limit."
        )
    
    # Process image with YOLOv8
    try:
        detections = model.detect_from_bytes(contents, confidence)
        process_time = time.time() - start_time
        
        return {
            "filename": file.filename,
            "detections": detections,
            "processing_time": round(process_time, 3)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )


@app.get("/model/info")
async def model_info():
    """Get information about the loaded model."""
    return {
        "model": os.path.basename(config.model_path),
        "class_count": len(model.class_names),
        "classes": model.class_names,
        "device": model.device,
        "config": config.to_dict()
    }