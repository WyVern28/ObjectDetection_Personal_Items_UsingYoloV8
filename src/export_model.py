"""
Export trained YOLO model to various formats
"""

import argparse
from ultralytics import YOLO
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Export YOLO Model')
    parser.add_argument('--model', type=str,
                        default='runs/train/personal_items4/weights/best.pt',
                        help='Path to trained model')
    parser.add_argument('--format', type=str, default='onnx',
                        choices=['onnx', 'torchscript', 'tflite', 'coreml',
                                'openvino', 'engine', 'saved_model'],
                        help='Export format')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Image size for export')
    parser.add_argument('--half', action='store_true',
                        help='FP16 quantization')
    parser.add_argument('--int8', action='store_true',
                        help='INT8 quantization')
    parser.add_argument('--dynamic', action='store_true',
                        help='Dynamic axes for ONNX')
    args = parser.parse_args()

    # Load model
    print(f"Loading model: {args.model}")
    model = YOLO(args.model)

    # Export
    print(f"\nExporting to {args.format.upper()} format...")
    export_path = model.export(
        format=args.format,
        imgsz=args.imgsz,
        half=args.half,
        int8=args.int8,
        dynamic=args.dynamic
    )

    print(f"\nExport completed!")
    print(f"Exported model saved at: {export_path}")

    # Show usage examples
    print("\n" + "=" * 50)
    print("Usage Examples:")
    print("=" * 50)

    if args.format == 'onnx':
        print(f"""
# Python with ONNX Runtime
import onnxruntime as ort
session = ort.InferenceSession('{export_path}')

# Or use with Ultralytics
from ultralytics import YOLO
model = YOLO('{export_path}')
results = model.predict('image.jpg')
""")
    elif args.format == 'torchscript':
        print(f"""
# Load with PyTorch
import torch
model = torch.jit.load('{export_path}')
""")
    elif args.format == 'tflite':
        print(f"""
# Use on mobile devices or edge devices
# Or with Python TFLite interpreter
import tensorflow as tf
interpreter = tf.lite.Interpreter(model_path='{export_path}')
""")

    return export_path


if __name__ == "__main__":
    main()
