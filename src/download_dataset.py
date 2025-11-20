"""
Download Dataset for Personal Items Detection
Options:
1. Use COCO subset (personal items classes)
2. Download from Roboflow
3. Download custom dataset
"""

import os
import argparse
import requests
import zipfile
from pathlib import Path
import shutil


def download_roboflow_dataset(api_key: str = None):
    """
    Download personal items dataset from Roboflow

    Popular datasets for personal items:
    - https://universe.roboflow.com/personal-items/personal-belongings
    - https://universe.roboflow.com/detection-bswxt/personal-protective-equipment-combined-model
    """
    try:
        from roboflow import Roboflow

        if api_key:
            rf = Roboflow(api_key=api_key)

            # Example: Download personal belongings dataset
            # You can change this to any dataset you prefer
            project = rf.workspace("personal-items").project("personal-belongings")
            dataset = project.version(1).download("yolov8")

            print(f"Dataset downloaded to: {dataset.location}")
            return dataset.location
        else:
            print("Please provide Roboflow API key")
            print("Get your API key at: https://app.roboflow.com/settings/api")
            return None

    except Exception as e:
        print(f"Error downloading from Roboflow: {e}")
        return None


def download_sample_dataset():
    """
    Download a sample dataset for testing
    Using Open Images Dataset subset
    """
    dataset_dir = Path("datasets/personal_items")
    dataset_dir.mkdir(parents=True, exist_ok=True)

    print("Creating sample dataset structure...")

    # Create directory structure
    for split in ['train', 'val', 'test']:
        (dataset_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
        (dataset_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)

    print(f"Dataset structure created at: {dataset_dir}")
    print("\nTo get a real dataset, you have several options:")
    print("\n1. COCO Dataset (Recommended for beginners):")
    print("   - Contains many personal items like backpack, handbag, laptop, etc.")
    print("   - Download: https://cocodataset.org/#download")
    print("   - Use fiftyone to filter: pip install fiftyone")

    print("\n2. Roboflow Universe (Easy to use):")
    print("   - https://universe.roboflow.com/search?q=personal+items")
    print("   - https://universe.roboflow.com/search?q=personal+belongings")
    print("   - Free account gives you access to many datasets")

    print("\n3. Open Images Dataset:")
    print("   - https://storage.googleapis.com/openimages/web/index.html")
    print("   - Filter for specific personal item classes")

    print("\n4. Create your own dataset:")
    print("   - Use your phone to capture images")
    print("   - Annotate with LabelImg or Roboflow")

    return str(dataset_dir)


def download_coco_personal_items():
    """
    Instructions for downloading COCO dataset and filtering personal items
    """
    print("=" * 60)
    print("COCO Dataset - Personal Items Subset")
    print("=" * 60)

    print("""
COCO dataset contains these personal item classes:
- backpack (24)
- umbrella (25)
- handbag (26)
- tie (27)
- suitcase (28)
- bottle (39)
- wine glass (40)
- cup (41)
- fork (42)
- knife (43)
- spoon (44)
- bowl (45)
- laptop (63)
- mouse (64)
- remote (65)
- keyboard (66)
- cell phone (67)
- book (73)
- clock (74)
- scissors (76)
- toothbrush (79)

To download and filter COCO:

Option 1: Using fiftyone (Recommended)
--------------------------------------
pip install fiftyone

import fiftyone as fo
import fiftyone.zoo as foz

# Download COCO with only personal items
dataset = foz.load_zoo_dataset(
    "coco-2017",
    split="validation",
    label_types=["detections"],
    classes=["backpack", "handbag", "suitcase", "umbrella", "tie",
             "bottle", "cup", "fork", "knife", "spoon", "bowl",
             "laptop", "mouse", "remote", "keyboard", "cell phone",
             "book", "clock", "scissors", "toothbrush"]
)

# Export to YOLO format
dataset.export(
    export_dir="datasets/coco_personal_items",
    dataset_type=fo.types.YOLOv5Dataset
)

Option 2: Manual Download
-------------------------
1. Download from https://cocodataset.org/#download
2. Use pycocotools to filter specific classes
3. Convert annotations to YOLO format
""")

    return None


def main():
    parser = argparse.ArgumentParser(description='Download Dataset')
    parser.add_argument('--source', type=str, default='sample',
                        choices=['sample', 'roboflow', 'coco'],
                        help='Dataset source')
    parser.add_argument('--api-key', type=str, default=None,
                        help='Roboflow API key')
    args = parser.parse_args()

    if args.source == 'sample':
        download_sample_dataset()
    elif args.source == 'roboflow':
        download_roboflow_dataset(args.api_key)
    elif args.source == 'coco':
        download_coco_personal_items()


if __name__ == "__main__":
    main()
