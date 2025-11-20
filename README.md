# Deteksi Barang-Barang Pribadi (Personal Items Detection)

Proyek deteksi objek menggunakan YOLOv8 untuk mendeteksi barang-barang pribadi secara real-time.

## Barang yang Dapat Dideteksi

- Tas (backpack, handbag, suitcase)
- Aksesoris (umbrella, tie, glasses, watch)
- Peralatan makan (bottle, cup, fork, knife, spoon, bowl)
- Elektronik (laptop, mouse, remote, keyboard, cell phone, headphones)
- Lainnya (book, clock, scissors, toothbrush, wallet, keys)

## Setup & Instalasi

### 1. Buat Virtual Environment

```bash
# Buat virtual environment
python -m venv venv

# Aktivasi (Windows)
venv\Scripts\activate

# Aktivasi (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Model YOLOv8

Model akan otomatis didownload saat pertama kali dijalankan, atau download manual:

```bash
# Download model pre-trained
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

## Penggunaan

### Deteksi Live Camera

```bash
# Gunakan model default (YOLOv8n pre-trained COCO)
python src/detect_live.py

# Dengan opsi tambahan
python src/detect_live.py --model yolov8n.pt --camera 0 --conf 0.5 --show-fps

# Gunakan model custom hasil training
python src/detect_live.py --model runs/train/personal_items/weights/best.pt
```

**Kontrol:**
- `q` - Keluar
- `s` - Screenshot
- `f` - Toggle FPS

### Deteksi pada Gambar

```bash
python src/detect_image.py --source path/to/image.jpg --save
python src/detect_image.py --source path/to/folder/ --save
```

## Dataset

### Opsi 1: Gunakan Model Pre-trained (Tercepat)

YOLOv8 pre-trained pada COCO sudah bisa mendeteksi banyak barang pribadi. Langsung jalankan:

```bash
python src/detect_live.py
```

### Opsi 2: Download Dataset dari Roboflow (Recommended)

1. Buat akun di [Roboflow](https://roboflow.com)
2. Cari dataset di [Roboflow Universe](https://universe.roboflow.com):
   - [Personal Belongings](https://universe.roboflow.com/search?q=personal+belongings)
   - [Personal Items](https://universe.roboflow.com/search?q=personal+items)
   - [Daily Objects](https://universe.roboflow.com/search?q=daily+objects)

3. Download dalam format YOLOv8:
   ```bash
   python src/download_dataset.py --source roboflow --api-key YOUR_API_KEY
   ```

### Opsi 3: COCO Dataset Subset

```bash
# Lihat instruksi download COCO
python src/download_dataset.py --source coco
```

Menggunakan fiftyone:
```python
pip install fiftyone

import fiftyone as fo
import fiftyone.zoo as foz

# Download hanya class personal items
dataset = foz.load_zoo_dataset(
    "coco-2017",
    split="validation",
    classes=["backpack", "handbag", "laptop", "cell phone", "book"]
)

# Export ke format YOLO
dataset.export(
    export_dir="datasets/coco_personal",
    dataset_type=fo.types.YOLOv5Dataset
)
```

### Opsi 4: Buat Dataset Sendiri

1. Kumpulkan gambar barang pribadi Anda
2. Annotate menggunakan:
   - [LabelImg](https://github.com/heartexlabs/labelImg)
   - [CVAT](https://cvat.org)
   - [Roboflow Annotate](https://roboflow.com)
3. Export dalam format YOLO

## Training Model Custom

```bash
# Training dengan dataset Anda
python src/train.py --data config/dataset.yaml --epochs 100 --batch 16

# Training dengan GPU
python src/train.py --device 0 --epochs 100

# Training dengan CPU (lebih lambat)
python src/train.py --device cpu --epochs 50 --batch 8
```

### Tips Training

1. **Mulai dengan model kecil**: `yolov8n.pt` untuk testing
2. **Gunakan GPU**: Training jauh lebih cepat
3. **Augmentasi data**: YOLOv8 sudah include augmentasi otomatis
4. **Monitor training**: Cek `runs/train/personal_items/` untuk metrics

## Struktur Proyek

```
ObjectDetection_TR_AI/
├── config/
│   └── dataset.yaml          # Konfigurasi dataset
├── datasets/                  # Folder dataset
│   └── personal_items/
│       ├── images/
│       │   ├── train/
│       │   ├── val/
│       │   └── test/
│       └── labels/
│           ├── train/
│           ├── val/
│           └── test/
├── src/
│   ├── detect_live.py        # Deteksi live camera
│   ├── detect_image.py       # Deteksi gambar
│   ├── download_dataset.py   # Download dataset
│   └── train.py              # Training model
├── runs/                     # Hasil training
├── requirements.txt
└── README.md
```

## Troubleshooting

### Camera tidak terbuka
```python
# Cek camera index
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} is available")
        cap.release()
```

### CUDA/GPU tidak terdeteksi
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
```

### Memory Error saat training
- Kurangi batch size: `--batch 8` atau `--batch 4`
- Gunakan model lebih kecil: `yolov8n.pt`
- Kurangi image size: `--imgsz 416`

## Quick Start

```bash
# 1. Setup environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan deteksi live (model pre-trained)
python src/detect_live.py --show-fps
```

## Referensi

- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/)
- [Roboflow Universe](https://universe.roboflow.com/)
- [COCO Dataset](https://cocodataset.org/)
