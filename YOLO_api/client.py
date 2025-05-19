"""
Example client script to test the YOLO API.
"""

import argparse
import requests
import json
import os
from PIL import Image, ImageDraw, ImageFont
import io
import matplotlib.pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(description="Test YOLO API with an image")
    parser.add_argument("--url", type=str, default="http://localhost:8000", help="API URL")
    parser.add_argument("--image", type=str, required=True, help="Path to image file")
    parser.add_argument("--confidence", type=float, default=0.5, help="Confidence threshold")
    parser.add_argument("--save", type=str, default=None, help="Save annotated image")
    parser.add_argument("--show", action="store_true", help="Show annotated image")
    return parser.parse_args()


def detect_objects(url, image_path, confidence):
    """Send image to API for object detection."""
    endpoint = f"{url}/detect/"
    
    # Prepare the file and params
    files = {"file": open(image_path, "rb")}
    data = {"confidence": confidence}
    
    # Send POST request
    try:
        response = requests.post(endpoint, files=files, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def draw_detections(image_path, detections, output_path=None, show=False):
    """Draw bounding boxes on the image with class names and confidence."""
    # Load image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Try to get a font (use default if not available)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()
    
    # Define colors (one for each class, cycling through)
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0)
    ]
    
    # Draw each detection
    for det in detections:
        # Get values
        class_name = det["class_name"]
        confidence = det["confidence"]
        x1, y1, x2, y2 = det["bbox"]
        
        # Calculate color index
        color_idx = det["class_id"] % len(colors)
        color = colors[color_idx]
        
        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
        
        # Draw label
        label = f"{class_name}: {confidence:.2f}"
        text_w, text_h = draw.textsize(label, font=font) if hasattr(draw, "textsize") else (
            font.getsize(label) if hasattr(font, "getsize") else (len(label) * 7, 15)
        )
        draw.rectangle([x1, y1, x1 + text_w, y1 + text_h], fill=color)
        draw.text((x1, y1), label, fill=(255, 255, 255), font=font)
    
    # Save if output path provided
    if output_path:
        image.save(output_path)
        print(f"Annotated image saved to {output_path}")
    
    # Show if requested
    if show:
        plt.figure(figsize=(10, 8))
        plt.imshow(image)
        plt.axis('off')
        plt.show()
    
    return image


def main():
    args = parse_args()
    
    # Check if image exists
    if not os.path.isfile(args.image):
        print(f"Error: Image file '{args.image}' not found")
        return
    
    # Call API
    print(f"Sending image to {args.url}/detect/...")
    result = detect_objects(args.url, args.image, args.confidence)
    
    if result:
        # Print detections
        print(f"\nDetected {len(result['detections'])} objects:")
        for i, det in enumerate(result['detections'], 1):
            print(f"{i}. {det['class_name']} (Conf: {det['confidence']:.2f}, "
                  f"Box: {det['bbox']})")
        
        # Processing time
        print(f"\nProcessing time: {result.get('processing_time', 'N/A')} seconds")
        
        # Visualize results
        if args.show or args.save:
            draw_detections(args.image, result['detections'], args.save, args.show)
    else:
        print("No detection results received")


if __name__ == "__main__":
    main()