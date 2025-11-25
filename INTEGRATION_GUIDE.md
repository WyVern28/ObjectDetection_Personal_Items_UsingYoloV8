# Integration Guide - Frontend & Backend

Panduan lengkap integrasi antara React Frontend dan Flask Backend untuk Object Detection App.

## 🔗 API Endpoints Mapping

### Frontend → Backend Mapping

| Frontend Call | Backend Endpoint | Method | Description |
|--------------|------------------|--------|-------------|
| `POST /stop_camera` | `POST /stop_camera` | POST | Stop detection |
| `POST /set_webcam` | `POST /set_webcam` | POST | Initialize webcam |
| `POST /upload` | `POST /api/detection/upload` | POST | Upload image/video |
| `GET /video_feed` | `GET /api/detection/video_feed` | GET | Stream video dengan detection |
| `GET /processed_image` | `GET /api/detection/processed_image` | GET | Get last processed image |

## 📡 Backend Endpoints Detail

### 1. Stop Camera
```http
POST /stop_camera
```
**Response:**
```json
{
  "success": true,
  "message": "Camera stopped"
}
```

### 2. Set Webcam
```http
POST /set_webcam
```
**Response:**
```json
{
  "success": true,
  "message": "Webcam set"
}
```

### 3. Upload File
```http
POST /upload
Content-Type: multipart/form-data
```
**Form Data:**
- `file`: Image or video file

**Response (Image):**
```json
{
  "success": true,
  "type": "image",
  "filename": "20241126_123456_image.jpg",
  "detections": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.85,
      "bbox": {"x1": 100, "y1": 150, "x2": 300, "y2": 450}
    }
  ],
  "count": 1,
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response (Video):**
```json
{
  "success": true,
  "type": "video",
  "filename": "20241126_123456_video.mp4",
  "message": "Video uploaded, use video_feed endpoint for streaming"
}
```

### 4. Video Feed
```http
GET /video_feed?camera=0&conf=0.25
```
**Response:** Multipart video stream (MJPEG)

### 5. Processed Image
```http
GET /processed_image
```
**Response:**
```json
{
  "success": true,
  "filename": "detected_20241126_123456_image.jpg",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

## 🎨 Frontend Implementation

### App.jsx State Management
```javascript
const [inputType, setInputType] = useState('none'); // 'none', 'webcam', 'upload'
const [imageResult, setImageResult] = useState(null); // base64 image
const [streamTrigger, setStreamTrigger] = useState(0); // trigger re-render
const [isLoading, setIsLoading] = useState(false); // loading state
```

### Frontend Flow

#### 1. Stop Detection
```javascript
const handleStop = async () => {
  setInputType('none');
  setImageResult(null);
  await fetch(`${API_BASE}/stop_camera`, { method: 'POST' });
};
```

#### 2. Start Webcam
```javascript
const handleWebcam = async () => {
  setInputType('webcam');
  setImageResult(null);
  await fetch(`${API_BASE}/set_webcam`, { method: 'POST' });
  setStreamTrigger(prev => prev + 1); // Re-render stream
};
```

#### 3. Upload File
```javascript
const handleFileUpload = async (e) => {
  const file = e.target.files[0];
  const formData = new FormData();
  formData.append('file', file);

  setIsLoading(true);
  setInputType('upload');

  const res = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData
  });

  const data = await res.json();

  if (data.type === 'image') {
    setImageResult(data.image); // Display base64 image
  } else {
    setStreamTrigger(prev => prev + 1); // Trigger video stream
  }

  setIsLoading(false);
};
```

## 🔧 Configuration

### Backend Configuration
File: `backend/.env`
```env
FLASK_DEBUG=True
DEFAULT_MODEL=yolov8n.pt
DEFAULT_CONF=0.25
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
HOST=0.0.0.0
PORT=5000
```

### Frontend Configuration
File: `frontend/.env`
```env
VITE_API_URL=http://localhost:5000
```

## 🚀 Running the Application

### 1. Start Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```
Backend runs at: `http://localhost:5000`

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

### 3. Open Browser
Navigate to: `http://localhost:5173`

## 🧪 Testing the Integration

### Test 1: Health Check
```bash
curl http://localhost:5000/api/health
```
Expected: `{"status": "healthy", ...}`

### Test 2: Upload Image
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@test.jpg"
```

### Test 3: Video Stream
Open browser: `http://localhost:5000/video_feed?camera=0&conf=0.25`

## 🐛 Troubleshooting

### Issue: CORS Error
**Solution:** Check backend CORS configuration
```python
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        ...
    }
})
```

### Issue: Camera Not Found
**Solution:**
```python
# Test camera availability
import cv2
cap = cv2.VideoCapture(0)
print(cap.isOpened())  # Should be True
cap.release()
```

### Issue: Upload Failed
**Solution:**
- Check file size limits
- Check file format (jpg, png, mp4, etc.)
- Check uploads folder exists and writable

### Issue: Backend Not Responding
**Solution:**
1. Check backend is running: `http://localhost:5000/api/health`
2. Check VITE_API_URL in frontend `.env`
3. Check CORS origins include frontend URL

## 📊 Supported File Types

### Images
- `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`

### Videos
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`

## 🔒 CORS Configuration

Backend allows requests from:
- `http://localhost:3000` (CRA default)
- `http://localhost:5173` (Vite default)

To add more origins, update `backend/app.py`:
```python
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173", "http://your-domain.com"],
        ...
    }
})
```

## 📝 Notes

1. **Stateless API**: Backend tidak menyimpan session/state camera. Setiap request independen.
2. **Base64 Images**: Upload image langsung return base64 untuk display di frontend.
3. **Video Streaming**: Menggunakan MJPEG stream dengan boundary frames.
4. **File Storage**: Uploaded files disimpan di `backend/uploads/`, results di `backend/outputs/`.

## 🔗 Additional Endpoints

Backend juga menyediakan RESTful API lengkap:

- `POST /api/detection/image` - Upload & detect image (advanced)
- `POST /api/detection/stream/frame` - Detect single frame
- `GET /api/model/list` - List available models
- `POST /api/model/change` - Change detection model
- `POST /api/model/confidence` - Set confidence threshold

Lihat `backend/README.md` untuk dokumentasi lengkap.

---

**Last Updated:** 2024-11-26
