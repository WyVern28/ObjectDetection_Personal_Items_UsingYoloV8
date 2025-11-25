"""
Detection API Routes
Endpoints for object detection operations
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from datetime import datetime
import base64

from app.services.detect_service import get_detection_service
from app.utils.validators import allowed_file, validate_image
from app.config import Config

detection_bp = Blueprint('detection', __name__)


@detection_bp.route('/image', methods=['POST'])
def detect_image():
    """
    Detect objects in an uploaded image

    Expected form data:
        - image: Image file (jpg, jpeg, png)
        - conf: Confidence threshold (optional, default: 0.25)
        - save: Whether to save result (optional, default: true)

    Returns:
        JSON with detection results and image URL
    """
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']

        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400

        # Get parameters
        conf = request.form.get('conf', type=float, default=0.25)
        save = request.form.get('save', type=str, default='true').lower() == 'true'

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Validate image
        if not validate_image(filepath):
            os.remove(filepath)
            return jsonify({'error': 'Invalid or corrupted image file'}), 400

        # Run detection
        service = get_detection_service()
        output_path = os.path.join(Config.OUTPUT_FOLDER, f"detected_{filename}") if save else None
        result = service.detect_image(filepath, conf=conf, save_result=save, output_path=output_path)

        if 'error' in result:
            return jsonify({'error': result['error']}), 500

        # Add URLs to response
        result['uploaded_image'] = f"/api/detection/image/uploads/{filename}"
        if save and result.get('output_image'):
            output_filename = os.path.basename(result['output_image'])
            result['detected_image'] = f"/api/detection/image/outputs/{output_filename}"

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@detection_bp.route('/image/base64', methods=['POST'])
def detect_image_base64():
    """
    Detect objects in a base64 encoded image

    Expected JSON:
        {
            "image": "base64_string",
            "conf": 0.25 (optional),
            "return_image": true (optional)
        }

    Returns:
        JSON with detection results
    """
    try:
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode base64 image
        try:
            image_data = data['image']
            if ',' in image_data:
                image_data = image_data.split(',')[1]

            img_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(img_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                return jsonify({'error': 'Could not decode image'}), 400

        except Exception as e:
            return jsonify({'error': f'Invalid base64 image: {str(e)}'}), 400

        # Get parameters
        conf = data.get('conf', 0.25)
        return_image = data.get('return_image', False)

        # Save temporary file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_path = os.path.join(Config.UPLOAD_FOLDER, f"temp_{timestamp}.jpg")
        cv2.imwrite(temp_path, image)

        # Run detection
        service = get_detection_service()
        result = service.detect_image(temp_path, conf=conf, save_result=False)

        # Clean up temp file
        os.remove(temp_path)

        if 'error' in result:
            return jsonify({'error': result['error']}), 500

        # Optionally return annotated image as base64
        if return_image and result.get('output_image'):
            annotated_image = cv2.imread(result['output_image'])
            result['annotated_image'] = service.frame_to_base64(annotated_image)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@detection_bp.route('/stream/start', methods=['POST'])
def start_stream():
    """
    Start webcam stream detection

    Expected JSON:
        {
            "camera": 0 (optional, default: 0),
            "conf": 0.25 (optional)
        }

    Returns:
        JSON with stream session info
    """
    try:
        data = request.get_json() or {}
        camera_index = data.get('camera', 0)
        conf = data.get('conf', 0.25)

        # Try to open camera
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return jsonify({'error': f'Cannot open camera {camera_index}'}), 500

        # Store camera info (in production, use Redis or session management)
        # For now, just return success
        cap.release()

        return jsonify({
            'success': True,
            'message': 'Stream initialized',
            'camera': camera_index,
            'conf': conf,
            'stream_url': f'/api/detection/stream/video?camera={camera_index}&conf={conf}'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@detection_bp.route('/stream/video', methods=['GET'])
def video_stream():
    """
    Stream video with object detection

    Query parameters:
        - camera: Camera index (default: 0)
        - conf: Confidence threshold (default: 0.25)

    Returns:
        Video stream with multipart/x-mixed-replace
    """
    from flask import Response

    camera_index = request.args.get('camera', default=0, type=int)
    conf = request.args.get('conf', default=0.25, type=float)

    def generate_frames():
        """Generate frames with detection"""
        cap = cv2.VideoCapture(camera_index)
        service = get_detection_service()

        try:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                # Run detection
                annotated_frame, detections = service.detect_frame(frame, conf=conf, draw_boxes=True)

                # Encode frame
                ret, buffer = cv2.imencode('.jpg', annotated_frame)
                frame_bytes = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        finally:
            cap.release()

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@detection_bp.route('/stream/frame', methods=['POST'])
def detect_stream_frame():
    """
    Detect objects in a single frame from stream

    Expected JSON:
        {
            "frame": "base64_string",
            "conf": 0.25 (optional),
            "return_image": true (optional)
        }

    Returns:
        JSON with detection results for the frame
    """
    try:
        data = request.get_json()

        if not data or 'frame' not in data:
            return jsonify({'error': 'No frame data provided'}), 400

        # Decode base64 frame
        frame_data = data['frame']
        if ',' in frame_data:
            frame_data = frame_data.split(',')[1]

        img_bytes = base64.b64decode(frame_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Could not decode frame'}), 400

        # Get parameters
        conf = data.get('conf', 0.25)
        return_image = data.get('return_image', True)

        # Run detection
        service = get_detection_service()
        annotated_frame, detections = service.detect_frame(frame, conf=conf, draw_boxes=True)

        result = {
            'success': True,
            'detections': detections,
            'count': len(detections)
        }

        # Return annotated frame as base64
        if return_image:
            result['annotated_frame'] = service.frame_to_base64(annotated_frame)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@detection_bp.route('/image/uploads/<filename>', methods=['GET'])
def get_uploaded_image(filename):
    """Serve uploaded image"""
    try:
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@detection_bp.route('/image/outputs/<filename>', methods=['GET'])
def get_output_image(filename):
    """Serve output/detected image"""
    try:
        filepath = os.path.join(Config.OUTPUT_FOLDER, filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
