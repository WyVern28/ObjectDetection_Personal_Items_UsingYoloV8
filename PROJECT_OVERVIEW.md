# Object Detection Web Application

Full-stack web application untuk Object Detection menggunakan YOLOv8 dengan React frontend dan Flask backend.

## 🏗️ Arsitektur Proyek

```
ObjectDetection_TR_AI/
├── backend/                    # Flask Backend (All-in-One)
│   ├── app/                    # Flask application
│   │   ├── routes/             # API endpoints
│   │   ├── services/           # Business logic
│   │   └── utils/              # Helper functions
│   ├── src/                    # Original scripts
│   ├── config/                 # Dataset configs
│   ├── Datasets/               # Training datasets
│   ├── runs/                   # Training results
│   ├── *.pt                    # YOLO models
│   └── app.py                  # Main entry point
│
└── frontend/                   # React Frontend (To be created)
    └── ...
```

## 🎯 Tujuan Project

Membuat web application yang dapat:
1. ✅ Upload gambar dan deteksi objek
2. ✅ Real-time webcam detection
3. ✅ Menampilkan hasil deteksi dengan bounding boxes
4. ✅ Switch between multiple YOLO models
5. ✅ Adjust confidence threshold
6. ✅ View detection statistics

## 🚀 Tech Stack

### Backend (Flask)
- **Framework**: Flask 3.0+
- **Object Detection**: YOLOv8 (Ultralytics)
- **Computer Vision**: OpenCV
- **Deep Learning**: PyTorch
- **CORS**: Flask-CORS

### Frontend (React) - To be created
- **Framework**: React 18+
- **Build Tool**: Vite atau Create React App
- **Styling**: Tailwind CSS / Material-UI
- **HTTP Client**: Axios / Fetch API
- **State Management**: React Hooks / Context API

## 📦 Backend Structure (✅ Completed)

Backend Flask sudah lengkap dengan:

### API Endpoints:
- `POST /api/detection/image` - Upload & detect image
- `POST /api/detection/image/base64` - Detect base64 image
- `POST /api/detection/stream/frame` - Detect webcam frame
- `GET /api/detection/stream/video` - Video stream
- `GET /api/model/info` - Model information
- `GET /api/model/list` - Available models
- `GET /api/model/classes` - Detectable classes
- `POST /api/model/change` - Change model
- `POST /api/model/confidence` - Set confidence threshold

### Features:
- ✅ CORS enabled untuk React
- ✅ Base64 encoding support
- ✅ Multiple model support (YOLOv8n, YOLOv8m, YOLO11n)
- ✅ Configurable confidence threshold
- ✅ Error handling & validation
- ✅ Production-ready dengan gunicorn

## 🎨 Frontend Requirements (To be created)

Frontend React akan memiliki:

### Pages/Components:
1. **Home Page**
   - Deskripsi aplikasi
   - Quick start guide

2. **Image Detection**
   - Upload image form
   - Display original & detected image
   - Show detection results (class, confidence, bbox)
   - Download annotated image

3. **Live Detection**
   - Webcam access
   - Real-time object detection
   - FPS counter
   - Toggle detection on/off

4. **Settings**
   - Select model (YOLOv8n, YOLOv8m, YOLO11n)
   - Adjust confidence threshold
   - View available classes

5. **About**
   - Model information
   - Statistics
   - Documentation

### UI/UX Features:
- Responsive design (mobile-friendly)
- Loading states & spinners
- Error handling & user feedback
- Dark/Light mode (optional)
- Smooth transitions & animations

## 🔄 Communication Flow

```
┌─────────────┐          HTTP/REST API          ┌─────────────┐
│   React     │ ────────────────────────────────▶ │   Flask     │
│  Frontend   │                                   │  Backend    │
│             │ ◀──────────────────────────────── │             │
│             │      JSON Response / Stream       │             │
└─────────────┘                                   └─────────────┘
     │                                                   │
     │ User Interface                                    │ AI Processing
     │ - Upload Image                                    │ - YOLO Model
     │ - Webcam Stream                                   │ - OpenCV
     │ - Display Results                                 │ - PyTorch
     └───────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
# Masuk ke folder backend
cd backend

# Buat virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Jalankan server
python app.py
```

Backend akan berjalan di: `http://localhost:5000`

### 2. Frontend Setup (To be created)

```bash
# Masuk ke folder frontend
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

Frontend akan berjalan di: `http://localhost:3000` atau `http://localhost:5173`

## 📋 Development Roadmap

### Phase 1: Backend ✅ (Completed)
- [x] Setup Flask application
- [x] Create API endpoints
- [x] Implement YOLO detection service
- [x] Add model management
- [x] Enable CORS
- [x] Add validation & error handling
- [x] Write documentation

### Phase 2: Frontend (Next)
- [ ] Setup React project (Vite/CRA)
- [ ] Create page layouts
- [ ] Implement image upload component
- [ ] Implement webcam component
- [ ] Create results display component
- [ ] Add model selection & settings
- [ ] Style with CSS framework
- [ ] Add responsive design
- [ ] Testing & bug fixes

### Phase 3: Integration & Testing
- [ ] Connect frontend to backend
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] User testing
- [ ] Documentation updates

### Phase 4: Deployment (Optional)
- [ ] Docker containerization
- [ ] Backend deployment (Heroku/AWS)
- [ ] Frontend deployment (Vercel/Netlify)
- [ ] CI/CD setup

## 🛠️ Development Tips

### Backend Development:
- Backend sudah siap dan dapat di-test menggunakan Postman atau cURL
- Gunakan `python app.py` untuk development
- Gunakan `gunicorn` untuk production
- Log errors untuk debugging

### Frontend Development:
- Gunakan Axios untuk API calls
- Implement loading states
- Handle errors gracefully
- Use environment variables untuk API URL
- Test on different screen sizes

### API Integration Example:

```javascript
// services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const detectImage = async (imageFile, conf = 0.25) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('conf', conf);

  const response = await axios.post(`${API_URL}/detection/image`, formData);
  return response.data;
};

export const detectFrame = async (base64Frame, conf = 0.25) => {
  const response = await axios.post(`${API_URL}/detection/stream/frame`, {
    frame: base64Frame,
    conf,
    return_image: true
  });
  return response.data;
};
```

## 📊 Models Available

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| YOLOv8n | 6 MB | Fastest | Good | Real-time, Low resource |
| YOLOv8m | 52 MB | Medium | High | Balanced performance |
| YOLO11n | 6 MB | Fastest | Good | Latest architecture |

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [YOLOv8 Docs](https://docs.ultralytics.com/)
- [Axios Documentation](https://axios-http.com/)

## 📝 Notes

- Backend sudah fully functional dan siap untuk frontend
- CORS sudah dikonfigurasi untuk localhost:3000 dan localhost:5173
- Semua file model, dataset, dan scripts sudah ada di folder backend
- Frontend tinggal dibuat dan connect ke API

## 🤝 Next Steps

1. **Buat React Frontend:**
   - Setup React project dengan Vite
   - Buat component structure
   - Implementasi API integration
   - Styling & responsive design

2. **Testing:**
   - Test semua endpoints
   - Test upload & webcam detection
   - Cross-browser testing

3. **Deployment:**
   - Docker setup
   - Deploy ke cloud platform

---

**Status**: Backend ✅ Complete | Frontend ⏳ To be created

**Last Updated**: November 25, 2024
