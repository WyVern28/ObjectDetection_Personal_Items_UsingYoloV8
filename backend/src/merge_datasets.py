"""
Merge Multiple YOLO Datasets into One
This script combines multiple datasets with different classes into a single dataset
"""

import os
import shutil
import yaml
from pathlib import Path
from collections import defaultdict


def merge_datasets(dataset_paths: list, output_path: str, dataset_name: str = "merged_dataset"):
    """
    Merge multiple YOLO format datasets into one

    Args:
        dataset_paths: List of paths to dataset folders (each should have data.yaml)
        output_path: Where to save the merged dataset
        dataset_name: Name for the merged dataset
    """

    output_dir = Path(output_path) / dataset_name

    # Create output directories
    for split in ['train', 'valid', 'test']:
        (output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
        (output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)

    # Collect all classes from all datasets
    all_classes = []
    class_mapping = {}  # {dataset_idx: {old_class_id: new_class_id}}

    print("=" * 50)
    print("Analyzing datasets...")
    print("=" * 50)

    for i, dataset_path in enumerate(dataset_paths):
        dataset_path = Path(dataset_path)
        yaml_file = dataset_path / 'data.yaml'

        if not yaml_file.exists():
            print(f"Warning: {yaml_file} not found, skipping...")
            continue

        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)

        classes = data.get('names', [])
        if isinstance(classes, dict):
            classes = [classes[k] for k in sorted(classes.keys())]

        print(f"\nDataset {i+1}: {dataset_path.name}")
        print(f"  Classes: {classes}")

        # Map old class IDs to new class IDs
        class_mapping[i] = {}
        for old_id, class_name in enumerate(classes):
            if class_name not in all_classes:
                all_classes.append(class_name)
            new_id = all_classes.index(class_name)
            class_mapping[i][old_id] = new_id

    print(f"\n{'=' * 50}")
    print(f"Merged classes ({len(all_classes)} total):")
    print("=" * 50)
    for i, cls in enumerate(all_classes):
        print(f"  {i}: {cls}")

    # Copy and remap images and labels
    print(f"\n{'=' * 50}")
    print("Merging datasets...")
    print("=" * 50)

    file_counter = defaultdict(int)

    for i, dataset_path in enumerate(dataset_paths):
        dataset_path = Path(dataset_path)

        if not (dataset_path / 'data.yaml').exists():
            continue

        print(f"\nProcessing: {dataset_path.name}")

        for split in ['train', 'valid', 'test']:
            # Try different possible paths
            img_dirs = [
                dataset_path / split / 'images',
                dataset_path / 'images' / split,
                dataset_path / split,
            ]

            label_dirs = [
                dataset_path / split / 'labels',
                dataset_path / 'labels' / split,
                dataset_path / split,
            ]

            img_dir = None
            label_dir = None

            for d in img_dirs:
                if d.exists():
                    img_dir = d
                    break

            for d in label_dirs:
                if d.exists():
                    label_dir = d
                    break

            if img_dir is None:
                continue

            # Process images
            for img_file in img_dir.glob('*'):
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                    # Generate unique filename
                    new_name = f"ds{i}_{file_counter[split]:06d}{img_file.suffix}"
                    file_counter[split] += 1

                    # Copy image
                    shutil.copy(img_file, output_dir / 'images' / split / new_name)

                    # Copy and remap label
                    label_file = label_dir / f"{img_file.stem}.txt"
                    if label_file.exists():
                        new_label_path = output_dir / 'labels' / split / f"{Path(new_name).stem}.txt"

                        with open(label_file, 'r') as f:
                            lines = f.readlines()

                        new_lines = []
                        for line in lines:
                            parts = line.strip().split()
                            if len(parts) >= 5:
                                old_class_id = int(parts[0])
                                new_class_id = class_mapping[i].get(old_class_id, old_class_id)
                                parts[0] = str(new_class_id)
                                new_lines.append(' '.join(parts) + '\n')

                        with open(new_label_path, 'w') as f:
                            f.writelines(new_lines)

        print(f"  Done!")

    # Create merged data.yaml
    merged_yaml = {
        'path': str(output_dir.absolute()),
        'train': 'images/train',
        'val': 'images/valid',
        'test': 'images/test',
        'nc': len(all_classes),
        'names': all_classes
    }

    yaml_path = output_dir / 'data.yaml'
    with open(yaml_path, 'w') as f:
        yaml.dump(merged_yaml, f, default_flow_style=False)

    print(f"\n{'=' * 50}")
    print("Merge completed!")
    print("=" * 50)
    print(f"Output directory: {output_dir}")
    print(f"Config file: {yaml_path}")
    print(f"\nDataset statistics:")
    for split in ['train', 'valid', 'test']:
        img_count = len(list((output_dir / 'images' / split).glob('*')))
        print(f"  {split}: {img_count} images")

    print(f"\nTo train, run:")
    print(f"  python src/train.py --data {yaml_path} --epochs 100 --imgsz 640")

    return str(yaml_path)


if __name__ == "__main__":
    # === CONFIGURE YOUR DATASETS HERE ===

    # List of dataset folders inside Datasets/
    datasets = [
        "Datasets/glasses-4",
        "Datasets/earbuds-4",
        "Datasets/Personal-Belongings-3",
    ]

    # Output location
    output_path = "datasets"

    # Check which datasets exist
    existing_datasets = []
    for ds in datasets:
        if Path(ds).exists():
            existing_datasets.append(ds)
        else:
            print(f"Dataset not found: {ds}")

    if existing_datasets:
        merge_datasets(existing_datasets, output_path, "personal_items_merged")
    else:
        print("\nNo datasets found!")
        print("Please check the Datasets folder.")
