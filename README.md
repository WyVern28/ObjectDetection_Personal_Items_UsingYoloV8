# 🎯 Object Detection Web Application

Full-stack web application untuk Object Detection menggunakan YOLOv8 dengan React frontend dan Flask backend.

![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Backend](https://img.shields.io/badge/Backend-Flask-blue)
![Frontend](https://img.shields.io/badge/Frontend-React-cyan)
![AI](https://img.shields.io/badge/AI-YOLOv8-orange)

Proyek deteksi objek real-time dengan web interface modern yang dapat mendeteksi barang-barang pribadi dan objek umum.

## Barang yang Dapat Dideteksi

- Tas (backpack, handbag, suitcase)
- Aksesoris (umbrella, tie, glasses, watch)
- Peralatan makan (bottle, cup, fork, knife, spoon, bowl)
- Elektronik (laptop, mouse, remote, keyboard, cell phone, headphones)
- Lainnya (book, clock, scissors, toothbrush, wallet, keys)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Webcam (optional, untuk live detection)

### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd ObjectDetection_TR_AI
```

### 2️⃣ Backend Setup (Terminal 1)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```
Backend runs at: **http://localhost:5000**

### 3️⃣ Frontend Setup (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: **http://localhost:5173**

### 4️⃣ Open Browser
Navigate to: **http://localhost:5173**

🎉 **Done!** Start detecting objects!

---

## 📖 Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - Quick setup guide (5 minutes)
- **[INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)** - API integration details
- **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** - Full project documentation
- **[backend/README.md](./backend/README.md)** - Backend API documentation

---

## ✨ Features

### 🎥 **Real-time Webcam Detection**
- Live object detection dari webcam
- Real-time bounding boxes dan labels
- Deteksi multiple objects simultaneously

### 📸 **Image Upload Detection**
- Upload gambar dari komputer
- Instant detection results
- Support: JPG, PNG, BMP, WEBP

### 🎬 **Video Upload Detection**
- Upload video files
- Frame-by-frame detection
- Support: MP4, AVI, MOV, MKV

### 🎛️ **Multiple Models**
- YOLOv8n (6MB) - Fastest
- YOLOv8m (52MB) - Balanced
- YOLO11n (6MB) - Latest

### 🎨 **Modern UI**
- Dark theme dengan glassmorphism
- Responsive design
- Loading states & animations
- Real-time status indicators

---

## 🏗️ Architecture

```
┌─────────────────┐         HTTP/REST API         ┌─────────────────┐
│  React Frontend │ ──────────────────────────────▶│  Flask Backend  │
│  (Port 5173)    │                                │  (Port 5000)    │
│                 │ ◀────────────────────────────── │                 │
│  - Upload UI    │    JSON / Image Stream         │  - YOLO Model   │
│  - Webcam UI    │                                │  - OpenCV       │
│  - Display      │                                │  - Detection    │
└─────────────────┘                                └─────────────────┘
```

---

## 📁 Project Structure

```
ObjectDetection_TR_AI/
├── backend/                 # Flask Backend API
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # YOLO detection service
│   │   └── utils/           # Helper functions
│   ├── uploads/             # Uploaded files
│   ├── outputs/             # Detection results
│   ├── *.pt                 # YOLO models
│   └── app.py               # Main entry point
│
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── App.jsx          # Main component
│   │   └── main.jsx
│   ├── public/
│   └── package.json
│
├── QUICKSTART.md            # Quick setup guide
├── INTEGRATION_GUIDE.md     # API integration guide
└── README.md                # This file
```

---

## 🎮 Usage

### Web Interface

1. **Stop Mode** (Default)
   - Idle state, no detection running

2. **Webcam Mode**
   - Click **CAM** button
   - Webcam will start with real-time detection

3. **Upload Mode**
   - Click **FILE** button
   - Select image/video from computer
   - View detection results instantly

### Command Line (Legacy)

#### Deteksi Live Camera
```bash
cd backend
python src/detect_live.py --model yolov8n.pt --conf 0.25
```

#### Deteksi Gambar
```bash
python src/detect_image.py --source path/to/image.jpg --save
```

#### Training Custom Model
```bash
python src/train.py --data config/dataset.yaml --epochs 100
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
