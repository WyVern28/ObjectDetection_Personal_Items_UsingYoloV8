# 🚀 Quick Start Guide

Panduan cepat untuk menjalankan Object Detection Web Application.

## ⚡ Quick Setup (5 Menit)

### 1️⃣ Setup Backend (Terminal 1)

```bash
# Masuk ke folder backend
cd backend

# Buat & aktivasi virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Jalankan server
python app.py
```

✅ Backend berjalan di: **http://localhost:5000**

---

### 2️⃣ Setup Frontend (Terminal 2)

```bash
# Masuk ke folder frontend
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

✅ Frontend berjalan di: **http://localhost:5173**

---

### 3️⃣ Buka Browser

Navigate to: **http://localhost:5173**

🎉 **Done!** Aplikasi siap digunakan.

---

## 🎮 Cara Menggunakan

### 1. **Stop Mode** (Default)
- Tidak ada deteksi yang berjalan
- Status: SYSTEM IDLE

### 2. **Webcam Mode**
- Klik tombol **CAM** untuk mulai deteksi real-time
- Webcam akan otomatis aktif
- Objek terdeteksi akan ditandai dengan bounding box

### 3. **Upload Mode**
- Klik tombol **FILE** untuk upload gambar
- Pilih gambar dari komputer
- Hasil deteksi akan langsung ditampilkan

---

## 🔧 Troubleshooting

### ❌ Backend Error: "Model not found"
```bash
# Model akan auto-download saat pertama run
# Atau download manual:
cd backend
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### ❌ Frontend Error: "Failed to fetch"
```bash
# Pastikan backend running di port 5000
curl http://localhost:5000/api/health

# Jika tidak ada response, restart backend:
cd backend
python app.py
```

### ❌ Camera Error: "Cannot open camera"
```bash
# Cek camera availability
python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened()); cap.release()"

# Jika False, coba camera index lain (1, 2, etc.)
```

### ❌ CORS Error
```bash
# Check frontend .env file
# File: frontend/.env
VITE_API_URL=http://localhost:5000

# Restart frontend setelah update .env
cd frontend
npm run dev
```

---

## 📦 System Requirements

### Backend:
- Python 3.8+
- CUDA (optional, untuk GPU acceleration)
- Webcam (untuk live detection)

### Frontend:
- Node.js 16+
- npm atau yarn

---

## 🎯 Features Available

✅ **Upload Image Detection**
- Drag & drop atau klik untuk upload
- Support: JPG, PNG, BMP, WEBP

✅ **Real-time Webcam Detection**
- Live object detection
- Real-time bounding boxes

✅ **3 Mode Detection:**
- STOP (idle)
- WEBCAM (live stream)
- UPLOAD (image processing)

✅ **Multiple Models:**
- YOLOv8n (fastest)
- YOLOv8m (balanced)
- YOLO11n (latest)

---

## 🔗 Useful Links

- **Backend API Docs:** http://localhost:5000/
- **Health Check:** http://localhost:5000/api/health
- **Video Stream:** http://localhost:5000/video_feed
- **Integration Guide:** [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)
- **Project Overview:** [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)

---

## 📝 Default Configuration

### Backend (Port 5000)
- Model: `yolov8n.pt` (6MB, fastest)
- Confidence: `0.25`
- CORS: Enabled for localhost:3000 & localhost:5173

### Frontend (Port 5173)
- Build Tool: Vite
- Framework: React 19
- Styling: Tailwind CSS
- API URL: http://localhost:5000

---

## 🚀 Production Deployment

### Backend
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
cd frontend
npm run build
# Serve dist/ folder dengan nginx/apache/vercel
```

---

## 🆘 Need Help?

1. Check [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) untuk detail API
2. Check [backend/README.md](./backend/README.md) untuk backend docs
3. Check logs di terminal untuk error messages
4. Issue? Open di GitHub repository

---

**Happy Detecting! 🎯**
