"""
Live Camera Object Detection for Personal Items
Uses YOLOv8 for real-time detection
"""

import cv2
import argparse
from ultralytics import YOLO
import time


def main():
    parser = argparse.ArgumentParser(description='Live Camera Object Detection')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='Path to YOLO model (default: yolov8n.pt)')
    parser.add_argument('--camera', type=int, default=0,
                        help='Camera index (default: 0)')
    parser.add_argument('--conf', type=float, default=0.25,
                        help='Confidence threshold (default: 0.25)')
    parser.add_argument('--show-fps', action='store_true',
                        help='Show FPS on screen')
    parser.add_argument('--all-objects', action='store_true',
                        help='Detect all objects (not just personal items)')
    args = parser.parse_args()

    # Load model
    print(f"Loading model: {args.model}")
    model = YOLO(args.model)

    # Personal items classes from COCO dataset
    personal_items = [
        # Bags & Accessories
        'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',

        # Electronics
        'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',

        # Personal & Home items
        'book', 'clock', 'scissors',

        # Furniture (optional - can be useful)
        'chair', 'couch', 'bed', 'dining table',

        # Vehicles (optional)
        'bicycle', 'motorcycle', 'car'
    ]

    print(f"Opening camera {args.camera}...")
    cap = cv2.VideoCapture(args.camera)

    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("Press 'q' to quit")
    print("Press 's' to save screenshot")
    print("Press 'f' to toggle FPS display")
    print("Press 'a' to toggle all objects mode")

    all_objects_mode = args.all_objects
    if all_objects_mode:
        print("Mode: Detecting ALL objects")
    else:
        print("Mode: Detecting personal items only")

    show_fps = args.show_fps
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame")
            break

        # Run detection
        results = model(frame, conf=args.conf, verbose=False)

        # Filter results for personal items only
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    cls_id = int(box.cls[0])
                    cls_name = model.names[cls_id]

                    # Check if we should display this object
                    should_display = all_objects_mode or (cls_name in personal_items)

                    if should_display:
                        # Get box coordinates
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])

                        # Color: green for personal items, blue for others
                        color = (0, 255, 0) if cls_name in personal_items else (255, 165, 0)

                        # Draw box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                        # Draw label
                        label = f"{cls_name}: {conf:.2f}"
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                        cv2.rectangle(frame, (x1, y1 - label_size[1] - 10),
                                     (x1 + label_size[0], y1), color, -1)
                        cv2.putText(frame, label, (x1, y1 - 5),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # Calculate and display FPS
        if show_fps:
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display frame
        cv2.imshow('Personal Items Detection', frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            filename = f"screenshot_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Screenshot saved: {filename}")
        elif key == ord('f'):
            show_fps = not show_fps
        elif key == ord('a'):
            all_objects_mode = not all_objects_mode
            mode_text = "ALL objects" if all_objects_mode else "personal items only"
            print(f"Switched to: {mode_text}")

    cap.release()
    cv2.destroyAllWindows()
    print("Detection stopped")


if __name__ == "__main__":
    main()
