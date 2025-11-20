"""
Train YOLOv8 model for Personal Items Detection
"""

import argparse
from ultralytics import YOLO
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Train YOLOv8 Model')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='Base model (yolov8n/s/m/l/x.pt)')
    parser.add_argument('--data', type=str, default='config/dataset.yaml',
                        help='Path to dataset.yaml')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of epochs')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size')
    parser.add_argument('--batch', type=int, default=16,
                        help='Batch size')
    parser.add_argument('--device', type=str, default='0',
                        help='Device (0 for GPU, cpu for CPU)')
    parser.add_argument('--project', type=str, default='runs/train',
                        help='Project directory')
    parser.add_argument('--name', type=str, default='personal_items',
                        help='Experiment name')
    args = parser.parse_args()

    # Load model
    print(f"Loading base model: {args.model}")
    model = YOLO(args.model)

    # Train
    print("Starting training...")
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        patience=50,
        save=True,
        plots=True,
        verbose=True
    )

    print(f"\nTraining completed!")
    print(f"Best model saved at: {results.save_dir}/weights/best.pt")
    print(f"Last model saved at: {results.save_dir}/weights/last.pt")

    # Validate
    print("\nRunning validation...")
    metrics = model.val()

    print(f"\nValidation Results:")
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")

    return results


if __name__ == "__main__":
    main()
