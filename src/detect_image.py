"""
Image Object Detection for Personal Items
"""

import cv2
import argparse
from ultralytics import YOLO
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Image Object Detection')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='Path to YOLO model')
    parser.add_argument('--source', type=str, required=True,
                        help='Path to image or directory')
    parser.add_argument('--conf', type=float, default=0.5,
                        help='Confidence threshold')
    parser.add_argument('--save', action='store_true',
                        help='Save results')
    args = parser.parse_args()

    # Load model
    model = YOLO(args.model)

    # Personal items to detect
    personal_items = [
        'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
        'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'book', 'clock', 'scissors', 'toothbrush'
    ]

    # Run detection
    results = model(args.source, conf=args.conf)

    for i, result in enumerate(results):
        img = result.orig_img.copy()
        boxes = result.boxes

        detected_items = []

        if boxes is not None:
            for box in boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]

                if cls_name in personal_items:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"{cls_name}: {conf:.2f}"
                    cv2.putText(img, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    detected_items.append(cls_name)

        print(f"Detected personal items: {detected_items}")

        if args.save:
            output_path = f"result_{i}.jpg"
            cv2.imwrite(output_path, img)
            print(f"Saved: {output_path}")
        else:
            cv2.imshow('Detection Result', img)
            cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
