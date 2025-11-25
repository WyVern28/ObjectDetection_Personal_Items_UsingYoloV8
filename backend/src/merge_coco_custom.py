"""
Merge COCO dataset with custom dataset
Creates a combined dataset with 80 COCO classes + custom classes
"""

import argparse
import shutil
import yaml
import random
from pathlib import Path
from ultralytics import YOLO
from tqdm import tqdm


# COCO 80 classes
COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


def download_coco_subset(output_dir: Path, num_images: int = 5000):
    """Download COCO dataset subset using ultralytics"""
    print(f"\nDownloading COCO128 dataset (subset for merging)...")

    # Use YOLO to download coco128 (small subset)
    # For larger subset, we'll use coco.yaml
    from ultralytics.data.utils import check_det_dataset

    # Download coco128 first as base
    coco_yaml = 'coco128.yaml'
    dataset_info = check_det_dataset(coco_yaml)

    return dataset_info


def merge_datasets(coco_dir: Path, custom_dir: Path, output_dir: Path,
                   custom_classes: list, max_coco_images: int = 5000):
    """
    Merge COCO and custom datasets

    Args:
        coco_dir: Path to COCO dataset
        custom_dir: Path to custom dataset
        output_dir: Path for merged dataset
        custom_classes: List of custom class names
        max_coco_images: Maximum COCO images to include
    """

    # Combined classes: COCO (0-79) + Custom (80+)
    combined_classes = COCO_CLASSES + custom_classes
    num_coco_classes = len(COCO_CLASSES)

    print(f"\nTotal classes: {len(combined_classes)}")
    print(f"  - COCO classes (0-79): {num_coco_classes}")
    print(f"  - Custom classes (80-{79 + len(custom_classes)}): {len(custom_classes)}")

    # Create output directories
    for split in ['train', 'val', 'test']:
        (output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
        (output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)

    # Copy COCO data
    print("\nCopying COCO data...")
    coco_images_dir = coco_dir / 'images'
    coco_labels_dir = coco_dir / 'labels'

    for split in ['train', 'val']:
        split_name = 'train2017' if split == 'train' else 'val2017'

        # Check different possible directory structures
        possible_img_dirs = [
            coco_images_dir / split_name,
            coco_images_dir / split,
            coco_dir / split / 'images',
        ]

        possible_lbl_dirs = [
            coco_labels_dir / split_name,
            coco_labels_dir / split,
            coco_dir / split / 'labels',
        ]

        img_dir = None
        lbl_dir = None

        for d in possible_img_dirs:
            if d.exists():
                img_dir = d
                break

        for d in possible_lbl_dirs:
            if d.exists():
                lbl_dir = d
                break

        if img_dir is None or lbl_dir is None:
            print(f"  Skipping {split} - directories not found")
            continue

        images = list(img_dir.glob('*.jpg')) + list(img_dir.glob('*.png'))

        # Limit COCO images
        if len(images) > max_coco_images:
            images = random.sample(images, max_coco_images)

        print(f"  Copying {len(images)} COCO {split} images...")

        for img_path in tqdm(images, desc=f"COCO {split}"):
            # Copy image
            dst_img = output_dir / 'images' / split / f"coco_{img_path.name}"
            shutil.copy2(img_path, dst_img)

            # Copy label (COCO labels stay same class IDs 0-79)
            lbl_path = lbl_dir / f"{img_path.stem}.txt"
            if lbl_path.exists():
                dst_lbl = output_dir / 'labels' / split / f"coco_{img_path.stem}.txt"
                shutil.copy2(lbl_path, dst_lbl)

    # Copy custom data with remapped class IDs
    print("\nCopying custom data...")

    custom_splits = {
        'train': custom_dir / 'images' / 'train',
        'val': custom_dir / 'images' / 'valid',
        'test': custom_dir / 'images' / 'test'
    }

    custom_label_splits = {
        'train': custom_dir / 'labels' / 'train',
        'val': custom_dir / 'labels' / 'valid',
        'test': custom_dir / 'labels' / 'test'
    }

    for split, img_dir in custom_splits.items():
        if not img_dir.exists():
            print(f"  Skipping custom {split} - directory not found")
            continue

        lbl_dir = custom_label_splits[split]
        images = list(img_dir.glob('*.jpg')) + list(img_dir.glob('*.png'))

        print(f"  Copying {len(images)} custom {split} images...")

        for img_path in tqdm(images, desc=f"Custom {split}"):
            # Copy image
            dst_img = output_dir / 'images' / split / f"custom_{img_path.name}"
            shutil.copy2(img_path, dst_img)

            # Remap labels (add offset for custom classes)
            lbl_path = lbl_dir / f"{img_path.stem}.txt"
            if lbl_path.exists():
                dst_lbl = output_dir / 'labels' / split / f"custom_{img_path.stem}.txt"

                with open(lbl_path, 'r') as f:
                    lines = f.readlines()

                remapped_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        old_class_id = int(parts[0])
                        new_class_id = old_class_id + num_coco_classes  # Offset by 80
                        parts[0] = str(new_class_id)
                        remapped_lines.append(' '.join(parts) + '\n')

                with open(dst_lbl, 'w') as f:
                    f.writelines(remapped_lines)

    # Create data.yaml
    data_yaml = {
        'path': str(output_dir.absolute()),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': len(combined_classes),
        'names': combined_classes
    }

    yaml_path = output_dir / 'data.yaml'
    with open(yaml_path, 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False, allow_unicode=True)

    print(f"\nDataset merged successfully!")
    print(f"Output directory: {output_dir}")
    print(f"Config file: {yaml_path}")

    # Count files
    for split in ['train', 'val', 'test']:
        img_count = len(list((output_dir / 'images' / split).glob('*')))
        print(f"  {split}: {img_count} images")

    return yaml_path


def main():
    parser = argparse.ArgumentParser(description='Merge COCO and Custom Dataset')
    parser.add_argument('--coco-dir', type=str, default='datasets/coco128',
                        help='Path to COCO dataset')
    parser.add_argument('--custom-dir', type=str,
                        default='Datasets/personal_items_merged',
                        help='Path to custom dataset')
    parser.add_argument('--output-dir', type=str,
                        default='Datasets/coco_custom_merged',
                        help='Output directory for merged dataset')
    parser.add_argument('--max-coco', type=int, default=5000,
                        help='Maximum COCO images to include')
    parser.add_argument('--download-coco', action='store_true',
                        help='Download COCO dataset first')
    args = parser.parse_args()

    coco_dir = Path(args.coco_dir)
    custom_dir = Path(args.custom_dir)
    output_dir = Path(args.output_dir)

    # Read custom classes from data.yaml
    custom_yaml = custom_dir / 'data.yaml'
    with open(custom_yaml, 'r') as f:
        custom_config = yaml.safe_load(f)
    custom_classes = custom_config['names']

    print("=" * 50)
    print("COCO + Custom Dataset Merger")
    print("=" * 50)
    print(f"\nCustom classes: {custom_classes}")

    # Download COCO if requested
    if args.download_coco or not coco_dir.exists():
        print("\nDownloading COCO128 dataset...")
        # YOLO will download to datasets/coco128
        model = YOLO('yolov8n.pt')
        model.val(data='coco128.yaml', verbose=False)
        coco_dir = Path('datasets/coco128')

    # Merge datasets
    yaml_path = merge_datasets(
        coco_dir=coco_dir,
        custom_dir=custom_dir,
        output_dir=output_dir,
        custom_classes=custom_classes,
        max_coco_images=args.max_coco
    )

    print("\n" + "=" * 50)
    print("Next Steps:")
    print("=" * 50)
    print(f"""
# Train with merged dataset:
python src/train.py --data {yaml_path} --epochs 100 --name coco_custom

# Or directly:
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.train(data='{yaml_path}', epochs=100)
""")


if __name__ == "__main__":
    main()
