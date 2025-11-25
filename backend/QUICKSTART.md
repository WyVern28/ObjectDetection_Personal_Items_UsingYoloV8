# Quick Start Guide - Backend Flask API

Panduan cepat untuk menjalankan Flask backend API.

## 🚀 Langkah Cepat (5 Menit)

### 1. Setup Environment

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Instalasi pertama kali akan memakan waktu beberapa menit karena harus download PyTorch dan dependencies lainnya.

### 3. Jalankan Server

```bash
python app.py
```

Output yang akan muncul:
```
==================================================
🚀 Object Detection API Server
==================================================
Server running on: http://localhost:5000
Health check: http://localhost:5000/api/health
API docs: http://localhost:5000/
==================================================
```

### 4. Test API

Buka browser dan akses: `http://localhost:5000/api/health`

Atau gunakan cURL:
```bash
curl http://localhost:5000/api/health
```

Response yang diharapkan:
```json
{
  "status": "healthy",
  "timestamp": "2024-11-25T...",
  "service": "Object Detection API"
}
```

## ✅ API Ready!

Backend sudah berjalan dan siap menerima request dari React frontend!

## 📡 Test Detection

### Test dengan cURL (Upload Image)

```bash
curl -X POST http://localhost:5000/api/detection/image \
  -F "image=@path/to/your/image.jpg" \
  -F "conf=0.25"
```

### Test dengan Python

```python
import requests

# Upload image
url = "http://localhost:5000/api/detection/image"
files = {"image": open("test.jpg", "rb")}
data = {"conf": 0.25}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### Test dengan Postman

1. Method: `POST`
2. URL: `http://localhost:5000/api/detection/image`
3. Body: `form-data`
   - Key: `image`, Type: `File`, Value: Select your image
   - Key: `conf`, Type: `Text`, Value: `0.25`
4. Send!

## 🔧 Konfigurasi (Optional)

Buat file `.env` untuk custom config:

```env
FLASK_DEBUG=True
DEFAULT_MODEL=yolov8n.pt
DEFAULT_CONF=0.25
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
HOST=0.0.0.0
PORT=5000
```

## 📊 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/` | GET | API documentation |
| `/api/detection/image` | POST | Detect objects in image |
| `/api/detection/image/base64` | POST | Detect from base64 |
| `/api/detection/stream/frame` | POST | Detect single frame |
| `/api/model/info` | GET | Get model info |
| `/api/model/list` | GET | List available models |
| `/api/model/classes` | GET | Get detectable classes |

Lihat [README.md](README.md) untuk dokumentasi lengkap.

## 🐛 Troubleshooting

### Error: Port already in use
```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Error: Module not found
```bash
# Pastikan virtual environment aktif
# Install ulang dependencies
pip install -r requirements.txt
```

### Error: Model not found
Model sudah ada di folder backend (`yolov8n.pt`, `yolov8m.pt`, `yolo11n.pt`). Pastikan Anda berada di folder `backend` saat menjalankan server.

## 🎯 Next Steps

1. ✅ Backend sudah running
2. 🔜 Buat React frontend
3. 🔗 Connect frontend ke backend API
4. 🎨 Implement UI/UX

## 📚 Resources

- [Full API Documentation](README.md)
- [Project Overview](../PROJECT_OVERVIEW.md)
- [YOLOv8 Docs](https://docs.ultralytics.com/)

---

**Happy Coding! 🚀**
