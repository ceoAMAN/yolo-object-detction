from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Any

from app.utils.config import config

router = APIRouter(prefix="/config", tags=["configuration"])


@router.get("/")
async def get_config():
    """Get the current configuration."""
    return config.to_dict()


@router.put("/update")
async def update_config(
    confidence_threshold: float = Query(None, ge=0.0, le=1.0),
    max_image_size: int = Query(None, ge=100, le=4096),
    max_file_size_mb: float = Query(None, ge=1.0, le=50.0)
):
    """
    Update configuration parameters.
    
    - **confidence_threshold**: Minimum confidence threshold for detections (0.0 to 1.0)
    - **max_image_size**: Maximum image dimension in pixels
    - **max_file_size_mb**: Maximum file size in MB
    """
    updates = {}
    
    if confidence_threshold is not None:
        config.confidence_threshold = confidence_threshold
        updates["confidence_threshold"] = confidence_threshold
        
    if max_image_size is not None:
        config.max_image_size = max_image_size
        updates["max_image_size"] = max_image_size
        
    if max_file_size_mb is not None:
        config.max_file_size_mb = max_file_size_mb
        updates["max_file_size_mb"] = max_file_size_mb
        
    if not updates:
        return {"message": "No updates provided"}
        
    return {
        "message": "Configuration updated successfully",
        "updates": updates,
        "config": config.to_dict()
    }