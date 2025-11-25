# Object Detection API - Backend

Backend Flask API untuk Object Detection menggunakan YOLOv8. API ini menyediakan endpoints untuk deteksi objek pada gambar dan video stream real-time.

## 🚀 Features

- ✅ REST API untuk object detection
- ✅ Upload dan deteksi gambar
- ✅ Real-time video stream detection
- ✅ Multiple model support (YOLOv8n, YOLOv8m, custom models)
- ✅ Confidence threshold configuration
- ✅ CORS enabled untuk React frontend
- ✅ Base64 image support
- ✅ Model management endpoints

## 📁 Struktur Proyek

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Konfigurasi aplikasi
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── detection_routes.py  # Endpoint deteksi
│   │   └── model_routes.py      # Endpoint model management
│   ├── services/
│   │   ├── __init__.py
│   │   └── detect_service.py    # Service untuk YOLO detection
│   └── utils/
│       ├── __init__.py
│       └── validators.py        # Validasi input
├── src/                        # Original detection scripts
│   ├── detect_live.py          # Live camera detection
│   ├── detect_image.py         # Image detection
│   ├── train.py                # Model training
│   └── ...                     # Other utility scripts
├── config/
│   └── dataset.yaml            # Dataset configuration
├── Datasets/                   # Dataset folders
│   ├── coco_custom_merged/
│   ├── personal_items_merged/
│   └── ...
├── runs/                       # Training & detection results
│   ├── detect/
│   └── train/
├── uploads/                    # Folder upload gambar
├── outputs/                    # Folder hasil deteksi
├── yolov8n.pt                  # YOLOv8 nano model (6MB)
├── yolov8m.pt                  # YOLOv8 medium model (52MB)
├── yolo11n.pt                  # YOLO11 nano model (6MB)
├── app.py                      # Main Flask application
├── requirements.txt
├── .env.example                # Environment variables template
└── README.md
```

## 🛠️ Setup & Installation

### 1. Buat Virtual Environment

```bash
# Clone atau masuk ke directory backend
cd backend

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

### 3. Konfigurasi (Optional)

Buat file `.env` untuk konfigurasi custom:

```env
FLASK_DEBUG=True
DEFAULT_MODEL=yolov8n.pt
DEFAULT_CONF=0.25
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
HOST=0.0.0.0
PORT=5000
```

## 🚀 Menjalankan Server

### Development Mode

```bash
python app.py
```

Server akan berjalan di `http://localhost:5000`

### Production Mode

```bash
# Gunakan gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Atau dengan gevent untuk async support
gunicorn -w 4 -k gevent -b 0.0.0.0:5000 app:app
```

## 📡 API Endpoints

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-25T10:30:00",
  "service": "Object Detection API"
}
```

### 1. Deteksi Gambar (Upload)

```http
POST /api/detection/image
Content-Type: multipart/form-data
```

**Form Data:**
- `image`: File gambar (jpg, jpeg, png)
- `conf`: Confidence threshold (optional, default: 0.25)
- `save`: Save result (optional, default: true)

**Response:**
```json
{
  "success": true,
  "detections": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.85,
      "bbox": {
        "x1": 100,
        "y1": 150,
        "x2": 300,
        "y2": 450,
        "width": 200,
        "height": 300
      }
    }
  ],
  "count": 1,
  "inference_time": 0.123,
  "image_info": {
    "width": 1280,
    "height": 720,
    "path": "uploads/20241125_103000_image.jpg"
  },
  "uploaded_image": "/api/detection/image/uploads/20241125_103000_image.jpg",
  "detected_image": "/api/detection/image/outputs/detected_20241125_103000_image.jpg"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/detection/image \
  -F "image=@path/to/image.jpg" \
  -F "conf=0.3"
```

### 2. Deteksi Gambar (Base64)

```http
POST /api/detection/image/base64
Content-Type: application/json
```

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "conf": 0.25,
  "return_image": true
}
```

**Response:**
```json
{
  "success": true,
  "detections": [...],
  "count": 2,
  "inference_time": 0.156,
  "annotated_image": "data:image/jpeg;base64,..."
}
```

### 3. Stream Video Detection

```http
GET /api/detection/stream/video?camera=0&conf=0.25
```

**Response:** Multipart video stream

### 4. Deteksi Frame (untuk Webcam)

```http
POST /api/detection/stream/frame
Content-Type: application/json
```

**Request Body:**
```json
{
  "frame": "data:image/jpeg;base64,...",
  "conf": 0.25,
  "return_image": true
}
```

**Response:**
```json
{
  "success": true,
  "detections": [...],
  "count": 3,
  "annotated_frame": "data:image/jpeg;base64,..."
}
```

### 5. Get Model Info

```http
GET /api/model/info
```

**Response:**
```json
{
  "model_path": "yolov8n.pt",
  "conf_threshold": 0.25,
  "classes": {
    "0": "person",
    "1": "bicycle",
    "2": "car",
    ...
  },
  "num_classes": 80
}
```

### 6. Get Available Classes

```http
GET /api/model/classes
```

**Response:**
```json
{
  "classes": ["person", "bicycle", "car", ...],
  "count": 80
}
```

### 7. List Available Models

```http
GET /api/model/list
```

**Response:**
```json
{
  "models": [
    {
      "name": "yolov8n.pt",
      "path": "D:/ObjectDetection_TR_AI/yolov8n.pt",
      "size": 6549796,
      "size_mb": 6.24
    },
    {
      "name": "best.pt",
      "path": "D:/ObjectDetection_TR_AI/runs/train/exp/weights/best.pt",
      "type": "trained",
      "size": 12345678,
      "size_mb": 11.77
    }
  ],
  "count": 2
}
```

### 8. Change Model

```http
POST /api/model/change
Content-Type: application/json
```

**Request Body:**
```json
{
  "model_path": "yolov8m.pt",
  "conf": 0.3
}
```

**Response:**
```json
{
  "success": true,
  "message": "Model changed successfully",
  "model_path": "yolov8m.pt"
}
```

### 9. Set Confidence Threshold

```http
POST /api/model/confidence
Content-Type: application/json
```

**Request Body:**
```json
{
  "conf": 0.35
}
```

**Response:**
```json
{
  "success": true,
  "message": "Confidence threshold updated",
  "conf": 0.35
}
```

## 🔧 Integrasi dengan React Frontend

### Fetch API Example

```javascript
// Upload dan deteksi gambar
const detectImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('conf', '0.25');

  const response = await fetch('http://localhost:5000/api/detection/image', {
    method: 'POST',
    body: formData
  });

  return await response.json();
};

// Deteksi frame dari webcam
const detectFrame = async (base64Frame) => {
  const response = await fetch('http://localhost:5000/api/detection/stream/frame', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      frame: base64Frame,
      conf: 0.25,
      return_image: true
    })
  });

  return await response.json();
};
```

### Axios Example

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// Upload image
export const detectImage = async (imageFile, conf = 0.25) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('conf', conf);

  const response = await axios.post(`${API_URL}/detection/image`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data;
};

// Get available models
export const getModels = async () => {
  const response = await axios.get(`${API_URL}/model/list`);
  return response.data;
};
```

## 🧪 Testing API

### Menggunakan cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Upload image
curl -X POST http://localhost:5000/api/detection/image \
  -F "image=@test.jpg" \
  -F "conf=0.3"

# Get model info
curl http://localhost:5000/api/model/info

# Get classes
curl http://localhost:5000/api/model/classes
```

### Menggunakan Postman

1. Import collection dari dokumentasi
2. Set base URL: `http://localhost:5000`
3. Test endpoints sesuai kebutuhan

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_DEBUG` | `True` | Debug mode |
| `DEFAULT_MODEL` | `yolov8n.pt` | Default YOLO model |
| `DEFAULT_CONF` | `0.25` | Default confidence threshold |
| `SECRET_KEY` | `dev-secret-key...` | Flask secret key |
| `CORS_ORIGINS` | `http://localhost:3000,...` | Allowed CORS origins |
| `HOST` | `0.0.0.0` | Server host |
| `PORT` | `5000` | Server port |

## 🐛 Troubleshooting

### Error: Model not found

```bash
# Pastikan model ada di root directory
ls ../yolov8n.pt

# Atau download otomatis saat pertama kali run
```

### Error: Camera not found

```bash
# Cek available cameras
python -c "import cv2; [print(f'Camera {i}') for i in range(5) if cv2.VideoCapture(i).isOpened()]"
```

### Error: CORS blocked

```bash
# Tambahkan origin React app ke CORS_ORIGINS di .env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📊 Performance Tips

1. **Gunakan model yang sesuai:**
   - `yolov8n.pt`: Tercepat, akurasi medium (6MB)
   - `yolov8s.pt`: Balance speed & accuracy (22MB)
   - `yolov8m.pt`: Akurasi tinggi, lebih lambat (52MB)

2. **Optimize untuk production:**
   - Gunakan gunicorn dengan multiple workers
   - Enable gevent untuk async processing
   - Set appropriate confidence threshold

3. **Caching:**
   - Cache model di memory (singleton pattern)
   - Reuse model instance antar requests

## 📚 Dokumentasi Lengkap

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- [OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
