# Backend Structure Documentation

Dokumentasi lengkap struktur backend Flask untuk Object Detection API.

## 📂 Directory Structure

```
backend/
├── app/                                # Flask application package
│   ├── __init__.py                     # Package initializer
│   ├── config.py                       # Configuration settings
│   │
│   ├── routes/                         # API route handlers
│   │   ├── __init__.py
│   │   ├── detection_routes.py         # Detection endpoints
│   │   └── model_routes.py             # Model management endpoints
│   │
│   ├── services/                       # Business logic layer
│   │   ├── __init__.py
│   │   └── detect_service.py           # YOLO detection service
│   │
│   └── utils/                          # Helper utilities
│       ├── __init__.py
│       └── validators.py               # Input validation functions
│
├── src/                                # Original detection scripts
│   ├── detect_live.py                  # Standalone live detection
│   ├── detect_image.py                 # Standalone image detection
│   ├── train.py                        # Model training script
│   ├── merge_datasets.py               # Dataset merging utility
│   ├── merge_coco_custom.py            # COCO dataset merger
│   ├── download_dataset.py             # Dataset downloader
│   ├── download_roboflow.py            # Roboflow integration
│   └── export_model.py                 # Model export utility
│
├── config/                             # Configuration files
│   └── dataset.yaml                    # Dataset configuration (25 classes)
│
├── Datasets/                           # Training datasets
│   ├── coco_custom_merged/             # Merged COCO dataset
│   ├── earbuds-4/                      # Earbuds dataset
│   ├── glasses-4/                      # Glasses dataset
│   ├── personal_items_merged/          # Merged personal items
│   └── Personal-Belongings-3/          # Personal belongings dataset
│
├── runs/                               # Training & detection outputs
│   ├── detect/                         # Detection results
│   └── train/                          # Training results & weights
│
├── uploads/                            # User uploaded images
│   └── .gitkeep
│
├── outputs/                            # Detection output images
│   └── .gitkeep
│
├── yolov8n.pt                          # YOLOv8 Nano (6.3MB) - Fastest
├── yolov8m.pt                          # YOLOv8 Medium (50MB) - Accurate
├── yolo11n.pt                          # YOLO11 Nano (5.4MB) - Latest
│
├── app.py                              # Main Flask application entry
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── README.md                           # Full documentation
├── QUICKSTART.md                       # Quick start guide
└── STRUCTURE.md                        # This file
```

## 🏗️ Architecture Layers

### 1. **Application Layer** (`app.py`)
- Main Flask application factory
- Blueprint registration
- CORS configuration
- Error handlers
- Health check endpoint

### 2. **Routes Layer** (`app/routes/`)
- HTTP request handling
- Input validation
- Response formatting
- Endpoint definitions

#### Detection Routes (`detection_routes.py`)
```python
POST /api/detection/image          # Upload & detect
POST /api/detection/image/base64   # Base64 detection
POST /api/detection/stream/frame   # Single frame detection
GET  /api/detection/stream/video   # Video stream
GET  /api/detection/image/uploads/<filename>
GET  /api/detection/image/outputs/<filename>
```

#### Model Routes (`model_routes.py`)
```python
GET  /api/model/info          # Model information
GET  /api/model/classes       # Available classes
GET  /api/model/list          # List models
POST /api/model/change        # Switch model
POST /api/model/confidence    # Set threshold
```

### 3. **Service Layer** (`app/services/`)
- Core business logic
- YOLO model management
- Detection processing
- Frame encoding/decoding

#### DetectionService (`detect_service.py`)
```python
class DetectionService:
    - load_model()              # Load YOLO model
    - detect_image()            # Detect objects in image
    - detect_frame()            # Detect in video frame
    - frame_to_base64()         # Convert frame to base64
    - get_classes()             # Get detectable classes
    - change_model()            # Switch detection model
```

### 4. **Utils Layer** (`app/utils/`)
- Helper functions
- Input validators
- Common utilities

#### Validators (`validators.py`)
```python
- allowed_file()           # Check file extension
- validate_image()         # Validate image file
- validate_confidence()    # Validate conf threshold
- validate_camera_index()  # Validate camera index
```

### 5. **Configuration Layer** (`app/config.py`)
```python
class Config:
    BASE_DIR              # Backend root directory
    UPLOAD_FOLDER         # Upload directory
    OUTPUT_FOLDER         # Output directory
    DATASETS_FOLDER       # Datasets location
    RUNS_FOLDER           # Training results
    DEFAULT_MODEL         # Default YOLO model
    DEFAULT_CONF          # Default confidence
    CORS_ORIGINS          # Allowed origins
```

## 🔄 Request Flow

### Image Detection Flow:
```
1. Client sends POST /api/detection/image with image file
2. detection_routes.py receives request
3. Validates file type and size
4. Saves to uploads/ folder
5. Calls detect_service.detect_image()
6. YOLO model processes image
7. Service draws bounding boxes
8. Saves result to outputs/
9. Returns JSON with detections + image URLs
10. Client receives response
```

### Webcam Detection Flow:
```
1. Client captures frame from webcam
2. Converts frame to base64
3. Sends POST /api/detection/stream/frame
4. detection_routes.py receives base64 data
5. Decodes to numpy array
6. Calls detect_service.detect_frame()
7. YOLO processes frame
8. Returns detections + annotated frame (base64)
9. Client displays result
10. Repeat for next frame
```

## 📊 Data Models

### Detection Result Format:
```json
{
  "success": true,
  "detections": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.856,
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
    "path": "uploads/image.jpg"
  },
  "uploaded_image": "/api/detection/image/uploads/image.jpg",
  "detected_image": "/api/detection/image/outputs/detected_image.jpg"
}
```

### Error Response Format:
```json
{
  "error": "Error message description"
}
```

## 🎯 Key Features

### 1. Singleton Pattern
- `DetectionService` uses singleton pattern
- Model loaded once and reused
- Improves performance
- Reduces memory usage

### 2. CORS Support
- Configured for React frontend
- Allowed origins: localhost:3000, localhost:5173
- All HTTP methods enabled
- Credentials support

### 3. File Handling
- Automatic directory creation
- Secure filename handling
- Size limits (16MB)
- Automatic cleanup possible

### 4. Error Handling
- Try-catch blocks in all routes
- Validation before processing
- Meaningful error messages
- HTTP status codes

### 5. Configuration Management
- Environment variable support
- Default values provided
- Multiple environment configs
- Easy to customize

## 🔐 Security Considerations

1. **File Upload**
   - Extension whitelist (png, jpg, jpeg, gif, bmp)
   - Size limit (16MB)
   - Secure filename sanitization

2. **CORS**
   - Specific origins only
   - Not allowing all origins (*)

3. **Input Validation**
   - Confidence threshold: 0 < conf <= 1
   - Camera index: 0 <= index < 10
   - Image validation with OpenCV

4. **Error Messages**
   - Generic error messages for production
   - Detailed logs for debugging

## 🚀 Performance Optimization

1. **Model Caching**
   - Singleton service instance
   - Model loaded once
   - Reused across requests

2. **Async Support**
   - Gunicorn with gevent workers
   - Non-blocking I/O
   - Better concurrency

3. **Image Processing**
   - Efficient OpenCV operations
   - JPEG compression for base64
   - Adjustable quality

4. **Response Size**
   - Optional image return
   - Compressed JSON
   - Streaming for video

## 📦 Dependencies

### Core:
- Flask 3.0+ (Web framework)
- ultralytics 8.0+ (YOLOv8)
- opencv-python 4.8+ (Computer vision)
- torch 2.0+ (Deep learning)

### Supporting:
- flask-cors (CORS handling)
- Pillow (Image processing)
- numpy (Array operations)
- PyYAML (Config parsing)

### Optional:
- gunicorn (Production server)
- gevent (Async workers)
- matplotlib (Visualization)
- tqdm (Progress bars)

## 🔄 Scalability

### Horizontal Scaling:
- Stateless API design
- Multiple workers with gunicorn
- Load balancer ready

### Vertical Scaling:
- GPU support for faster inference
- Batch processing capability
- Model optimization (TensorRT, ONNX)

### Future Enhancements:
- Redis for session management
- Database for detection history
- Queue system (Celery) for long tasks
- WebSocket for real-time updates

## 📚 API Standards

- RESTful design
- JSON responses
- Consistent error format
- HTTP status codes
- Versioned endpoints (/api/v1)

## 🧪 Testing

### Manual Testing:
```bash
# Health check
curl http://localhost:5000/api/health

# Upload test
curl -X POST http://localhost:5000/api/detection/image \
  -F "image=@test.jpg"

# Get models
curl http://localhost:5000/api/model/list
```

### Automated Testing (Future):
- Unit tests for services
- Integration tests for routes
- Load testing
- CI/CD pipeline

---

**Last Updated**: November 25, 2024
**Backend Status**: ✅ Production Ready
**Next**: Create React Frontend
