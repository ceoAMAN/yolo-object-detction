# YOLOv8 Object Detection API

A FastAPI-based API for object detection using YOLOv8 and PyTorch.

## Features

- Image upload endpoint for object detection
- YOLOv8 pre-trained model integration
- JSON response with bounding boxes, class labels, and confidence scores
- Configurable confidence threshold

## Requirements

- Python 3.8+
- PyTorch
- FastAPI
- Ultralytics YOLOv8

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download YOLOv8 weights:
   ```
   mkdir -p weights
   python -c "from ultralytics import YOLO; YOLO('yolov8n.pt').save('weights/yolov8n.pt')"
   ```

## Usage

1. Start the API server:
   ```
   uvicorn app.api.main:app --reload
   ```

2. The API will be available at http://localhost:8000

3. Access the API documentation at http://localhost:8000/docs

## API Endpoints

### POST /detect/

Upload an image to get object detection results.

**Parameters:**
- `file`: Image file (form-data)
- `confidence`: Minimum confidence threshold (optional, default: 0.5)

**Response:**
```json
{
  "detections": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.97,
      "bbox": [100, 200, 300, 400]
    },
    ...
  ]
}
```

## Model Information

The API uses YOLOv8n by default, but can be configured to use other YOLOv8 variants.

## License

MIT
