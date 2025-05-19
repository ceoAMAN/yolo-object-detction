import os
from typing import Dict, Any

# Base configuration
BASE_CONFIG = {
    "model_name": "yolov8n.pt",
    "confidence_threshold": 0.5,
    "max_image_size": 1280,
    "allowed_extensions": [".jpg", ".jpeg", ".png", ".bmp"],
    "max_file_size_mb": 10,
}

class Config:
    """Configuration for the YOLO API."""
    
    def __init__(self):
        self.model_path = os.path.join("weights", BASE_CONFIG["model_name"])
        self.confidence_threshold = float(
            os.getenv("CONFIDENCE_THRESHOLD", BASE_CONFIG["confidence_threshold"])
        )
        self.max_image_size = int(
            os.getenv("MAX_IMAGE_SIZE", BASE_CONFIG["max_image_size"])
        )
        self.allowed_extensions = BASE_CONFIG["allowed_extensions"]
        self.max_file_size_mb = float(
            os.getenv("MAX_FILE_SIZE_MB", BASE_CONFIG["max_file_size_mb"])
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "model_path": self.model_path,
            "confidence_threshold": self.confidence_threshold,
            "max_image_size": self.max_image_size,
            "allowed_extensions": self.allowed_extensions,
            "max_file_size_mb": self.max_file_size_mb,
        }


# Create a global config instance
config = Config()