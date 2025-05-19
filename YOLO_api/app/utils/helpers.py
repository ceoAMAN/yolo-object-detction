import os
import pathlib
from typing import List, Tuple


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate if a file has an allowed extension.
    
    Args:
        filename: Name of the file to validate
        allowed_extensions: List of allowed extensions (with dot, e.g. ['.jpg', '.png'])
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    if not filename:
        return False
        
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions


def create_directories() -> None:
    """Create necessary directories if they don't exist."""
    required_dirs = [
        "weights",
        "app/models",
        "app/api",
        "app/utils"
    ]
    
    for directory in required_dirs:
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def format_bbox(bbox: List[float], image_size: Tuple[int, int] = None) -> List[int]:
    """
    Format bounding box coordinates.
    
    Args:
        bbox: Bounding box coordinates [x1, y1, x2, y2]
        image_size: Original image size (width, height) for normalization
        
    Returns:
        List of integers representing the bounding box
    """
    # Convert to int if they are float
    x1, y1, x2, y2 = map(int, bbox)
    
    # Normalize coordinates if image_size is provided
    if image_size:
        width, height = image_size
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))
    
    return [x1, y1, x2, y2]