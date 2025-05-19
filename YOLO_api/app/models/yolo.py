import os
import io
from typing import List, Dict, Any, Tuple
import numpy as np
from PIL import Image
from ultralytics import YOLO
import torch

from app.utils.config import config


class YOLOModel:
    """YOLOv8 model wrapper for object detection."""
    
    def __init__(self):
        """Initialize the YOLO model."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.class_names = []
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the YOLO model."""
        if not os.path.exists(config.model_path):
            # Download and save the model if it doesn't exist
            self.model = YOLO("yolov8n.pt")
            os.makedirs(os.path.dirname(config.model_path), exist_ok=True)
            self.model.save(config.model_path)
        else:
            self.model = YOLO(config.model_path)
        
        # Extract class names from the model
        self.class_names = self.model.names
    
    def preprocess_image(self, image_bytes: bytes) -> Image.Image:
        """Preprocess the image bytes into a PIL Image."""
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # Resize if larger than max_image_size
        if max(image.size) > config.max_image_size:
            ratio = config.max_image_size / max(image.size)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            
        return image
    
    def detect(self, image: Image.Image, confidence_threshold: float = None) -> List[Dict[str, Any]]:
        """
        Perform object detection on an image.
        
        Args:
            image: PIL Image to process
            confidence_threshold: Confidence threshold for detections
            
        Returns:
            List of detection results with class_id, class_name, confidence, and bbox
        """
        if confidence_threshold is None:
            confidence_threshold = config.confidence_threshold
            
        # Convert PIL image to numpy array
        img_array = np.array(image)
        
        # Run inference
        results = self.model(img_array, conf=confidence_threshold)[0]
        
        # Format results
        detections = []
        
        for box in results.boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            
            # Get class id and confidence
            class_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            
            detections.append({
                "class_id": class_id,
                "class_name": self.class_names[class_id],
                "confidence": round(confidence, 3),
                "bbox": [int(x1), int(y1), int(x2), int(y2)]
            })
            
        return detections
    
    def detect_from_bytes(self, image_bytes: bytes, confidence_threshold: float = None) -> List[Dict[str, Any]]:
        """Detect objects from image bytes."""
        image = self.preprocess_image(image_bytes)
        return self.detect(image, confidence_threshold)


# Create a global model instance
model = YOLOModel()