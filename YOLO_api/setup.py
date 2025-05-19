"""
Script to download YOLOv8 weights and set up the project.
"""

import os
import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Setup YOLOv8 Object Detection API")
    parser.add_argument(
        "--model", 
        type=str, 
        default="yolov8n.pt", 
        choices=[
            "yolov8n.pt", 
            "yolov8s.pt", 
            "yolov8m.pt", 
            "yolov8l.pt", 
            "yolov8x.pt"
        ],
        help="YOLOv8 model to use"
    )
    args = parser.parse_args()
    
    # Create directory structure
    print("Creating directory structure...")
    os.makedirs("weights", exist_ok=True)
    
    # Initialize package structure
    print("Initializing package structure...")
    if os.path.exists("setup_package.py"):
        os.system(f"{sys.executable} setup_package.py")
    
    # Download YOLOv8 weights
    print(f"Downloading YOLOv8 weights ({args.model})...")
    try:
        from ultralytics import YOLO
        model = YOLO(args.model)
        model_path = os.path.join("weights", args.model)
        model.save(model_path)
        print(f"Model saved to {model_path}")
    except ImportError:
        print("Error: Ultralytics package not found. Install with 'pip install ultralytics'")
        sys.exit(1)
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        sys.exit(1)
    
    # Update config file with model name
    config_file = "app/utils/config.py"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            content = f.read()
        
        content = content.replace(
            '"model_name": "yolov8n.pt"', 
            f'"model_name": "{args.model}"'
        )
        
        with open(config_file, "w") as f:
            f.write(content)
    
    print("\nSetup completed successfully!")
    print("\nTo start the API server, run:")
    print("  uvicorn app.api.main:app --reload")
    print("\nAccess the API documentation at http://localhost:8000/docs")


if __name__ == "__main__":
    main()