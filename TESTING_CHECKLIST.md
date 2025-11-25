# 🧪 Testing Checklist

Checklist untuk memastikan frontend dan backend terintegrasi dengan baik.

---

## 📋 Pre-Testing Checklist

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Git installed (optional)
- [ ] Webcam connected (optional, for webcam testing)

### Environment Setup
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` file created di frontend folder
- [ ] YOLO model files exist (yolov8n.pt, yolov8m.pt, yolo11n.pt)

---

## 🔧 Backend Testing

### 1. Backend Starts Successfully
```bash
cd backend
python app.py
```
**Expected Output:**
```
==================================================
🚀 Object Detection API Server
==================================================
Server running on: http://localhost:5000
Health check: http://localhost:5000/api/health
API docs: http://localhost:5000/
==================================================
```
- [ ] ✅ Server starts without errors
- [ ] ✅ Port 5000 is available
- [ ] ✅ YOLO model loads successfully

### 2. Health Check
```bash
curl http://localhost:5000/api/health
```
**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-26T...",
  "service": "Object Detection API"
}
```
- [ ] ✅ Returns 200 status code
- [ ] ✅ Returns JSON with "healthy" status

### 3. Root Endpoint
```bash
curl http://localhost:5000/
```
**Expected Response:**
```json
{
  "message": "Object Detection API",
  "version": "1.0.0",
  "endpoints": {...}
}
```
- [ ] ✅ Returns API information
- [ ] ✅ Lists all available endpoints

### 4. Stop Camera Endpoint
```bash
curl -X POST http://localhost:5000/stop_camera
```
**Expected Response:**
```json
{
  "success": true,
  "message": "Camera stopped"
}
```
- [ ] ✅ Returns 200 status
- [ ] ✅ Success is true

### 5. Set Webcam Endpoint
```bash
curl -X POST http://localhost:5000/set_webcam
```
**Expected Response:**
```json
{
  "success": true,
  "message": "Webcam set"
}
```
- [ ] ✅ Returns 200 status
- [ ] ✅ Success is true

### 6. Upload Image Endpoint
```bash
# Prepare test image first
curl -X POST http://localhost:5000/upload -F "file=@path/to/test.jpg"
```
**Expected Response:**
```json
{
  "success": true,
  "type": "image",
  "filename": "...",
  "detections": [...],
  "count": ...,
  "image": "data:image/jpeg;base64,..."
}
```
- [ ] ✅ Accepts image file
- [ ] ✅ Returns detection results
- [ ] ✅ Returns base64 image

### 7. Video Feed Endpoint
Open browser: `http://localhost:5000/video_feed`
- [ ] ✅ Browser prompts for camera permission
- [ ] ✅ Video stream displays
- [ ] ✅ Objects are detected and boxed
- [ ] ✅ Stream runs smoothly

---

## 🎨 Frontend Testing

### 1. Frontend Starts Successfully
```bash
cd frontend
npm run dev
```
**Expected Output:**
```
VITE v7.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```
- [ ] ✅ Vite server starts
- [ ] ✅ Port 5173 is available
- [ ] ✅ No compilation errors

### 2. Frontend Opens in Browser
Open: `http://localhost:5173`
- [ ] ✅ Page loads without errors
- [ ] ✅ UI displays correctly
- [ ] ✅ Dark theme visible
- [ ] ✅ Three buttons visible (STOP, CAM, FILE)

### 3. Console Check
Open browser DevTools (F12) → Console tab
- [ ] ✅ No JavaScript errors
- [ ] ✅ No network errors
- [ ] ✅ No CORS errors
- [ ] ✅ API_BASE is correct (http://localhost:5000)

### 4. Initial State
- [ ] ✅ Status shows "SYSTEM IDLE"
- [ ] ✅ Red indicator dot visible
- [ ] ✅ STOP button is highlighted/active
- [ ] ✅ Abstract background visible

---

## 🔗 Integration Testing

### Test 1: Stop Button
**Steps:**
1. Click **STOP** button
2. Observe status indicator

**Expected Result:**
- [ ] ✅ Status shows "SYSTEM IDLE"
- [ ] ✅ Red indicator dot
- [ ] ✅ Abstract background visible
- [ ] ✅ No errors in console

### Test 2: Webcam Detection
**Steps:**
1. Click **CAM** button
2. Allow camera permission if prompted
3. Wait for stream to load

**Expected Result:**
- [ ] ✅ Status changes to "SOURCE: webcam"
- [ ] ✅ Green indicator dot (pulsing)
- [ ] ✅ Webcam stream appears
- [ ] ✅ Objects are detected with bounding boxes
- [ ] ✅ Labels show class name and confidence
- [ ] ✅ Stream is smooth (no lag)

**Console Check:**
- [ ] ✅ No "Failed to fetch" errors
- [ ] ✅ No CORS errors
- [ ] ✅ Image loads from `/video_feed`

### Test 3: Image Upload
**Steps:**
1. Click **FILE** button
2. Select an image file (JPG/PNG)
3. Wait for processing

**Expected Result:**
- [ ] ✅ Status changes to "PROCESSING..."
- [ ] ✅ Loading animation appears
- [ ] ✅ After processing, status shows "SOURCE: upload"
- [ ] ✅ Green indicator dot
- [ ] ✅ Detected image displays
- [ ] ✅ Bounding boxes visible
- [ ] ✅ Labels show class name and confidence

**Console Check:**
- [ ] ✅ Upload POST succeeds (200 status)
- [ ] ✅ Response contains base64 image
- [ ] ✅ No errors

### Test 4: Image Upload (No Objects)
**Steps:**
1. Upload image with no detectable objects
2. Wait for processing

**Expected Result:**
- [ ] ✅ Processing completes
- [ ] ✅ Image displays
- [ ] ✅ No bounding boxes (correct behavior)
- [ ] ✅ No errors

### Test 5: Switch Between Modes
**Steps:**
1. Click **CAM** button (webcam mode)
2. Wait for stream
3. Click **FILE** button (upload mode)
4. Select image
5. Click **STOP** button

**Expected Result:**
- [ ] ✅ Each mode switches correctly
- [ ] ✅ Previous content clears
- [ ] ✅ Status updates correctly
- [ ] ✅ No memory leaks
- [ ] ✅ No lingering streams

### Test 6: Error Handling
**Steps:**
1. Stop backend server
2. Try to click **CAM** or upload file

**Expected Result:**
- [ ] ✅ Alert shows error message
- [ ] ✅ App returns to STOP mode
- [ ] ✅ No app crash
- [ ] ✅ Console shows error details

### Test 7: Large Image Upload
**Steps:**
1. Upload a large image (> 5MB)
2. Wait for processing

**Expected Result:**
- [ ] ✅ Loading state shows
- [ ] ✅ Processing completes (may take longer)
- [ ] ✅ Result displays correctly
- [ ] ✅ No timeout errors

---

## 🌐 Browser Compatibility Testing

### Chrome/Edge
- [ ] ✅ UI renders correctly
- [ ] ✅ Webcam works
- [ ] ✅ Upload works
- [ ] ✅ No console errors

### Firefox
- [ ] ✅ UI renders correctly
- [ ] ✅ Webcam works
- [ ] ✅ Upload works
- [ ] ✅ No console errors

### Safari (Mac)
- [ ] ✅ UI renders correctly
- [ ] ✅ Webcam works
- [ ] ✅ Upload works
- [ ] ✅ No console errors

---

## 📱 Responsive Design Testing

### Desktop (1920x1080)
- [ ] ✅ UI scales properly
- [ ] ✅ Buttons visible and clickable
- [ ] ✅ Video/image fills screen appropriately

### Tablet (768x1024)
- [ ] ✅ UI adapts to tablet size
- [ ] ✅ Controls accessible
- [ ] ✅ Content readable

### Mobile (375x667)
- [ ] ✅ UI usable on mobile
- [ ] ✅ Buttons not too small
- [ ] ✅ Text readable

---

## 🔍 Performance Testing

### Backend Performance
- [ ] ✅ Image detection < 1 second
- [ ] ✅ Video stream FPS > 15
- [ ] ✅ Memory usage stable
- [ ] ✅ CPU usage acceptable

### Frontend Performance
- [ ] ✅ Page load < 2 seconds
- [ ] ✅ Smooth animations
- [ ] ✅ No UI lag
- [ ] ✅ Memory usage stable

---

## 🐛 Known Issues Check

### Issue: Port Already in Use
**Test:** Try starting backend when port 5000 is busy
- [ ] ✅ Shows clear error message
- [ ] ✅ Suggests using different port

### Issue: Camera Not Found
**Test:** Run webcam mode without camera
- [ ] ✅ Backend returns error
- [ ] ✅ Frontend shows alert
- [ ] ✅ App doesn't crash

### Issue: Invalid File Type
**Test:** Upload .txt or .pdf file
- [ ] ✅ Backend rejects file
- [ ] ✅ Frontend shows error
- [ ] ✅ App remains functional

---

## ✅ Final Checklist

### Documentation
- [ ] ✅ README.md is up to date
- [ ] ✅ QUICKSTART.md exists
- [ ] ✅ INTEGRATION_GUIDE.md exists
- [ ] ✅ All API endpoints documented

### Code Quality
- [ ] ✅ No syntax errors
- [ ] ✅ No console warnings
- [ ] ✅ Error handling implemented
- [ ] ✅ Code is commented

### Security
- [ ] ✅ CORS properly configured
- [ ] ✅ File upload validation exists
- [ ] ✅ No sensitive data exposed

### Deployment Readiness
- [ ] ✅ .env.example files exist
- [ ] ✅ .gitignore configured
- [ ] ✅ Dependencies listed
- [ ] ✅ Setup instructions clear

---

## 📊 Test Results Summary

**Total Tests:** _____ / _____
**Passed:** _____ ✅
**Failed:** _____ ❌
**Skipped:** _____ ⏭️

**Overall Status:** [ PASS / FAIL ]

---

## 🎯 Sign Off

**Tester Name:** _________________
**Date:** _________________
**Environment:**
- OS: _________________
- Python Version: _________________
- Node Version: _________________
- Browser: _________________

**Notes:**
_______________________________________________
_______________________________________________
_______________________________________________

---

**Testing Complete!** 🎉

If all tests pass, the application is ready for development/production use.
