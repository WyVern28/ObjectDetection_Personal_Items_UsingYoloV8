"""
Flask Backend for Object Detection API
Main application entry point
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Import routes
from app.routes.detection_routes import detection_bp
from app.routes.model_routes import model_bp
from app.config import Config

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for React frontend
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Ensure upload and output directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    # Register blueprints
    app.register_blueprint(detection_bp, url_prefix='/api/detection')
    app.register_blueprint(model_bp, url_prefix='/api/model')

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'Object Detection API'
        }), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'Object Detection API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'detect_image': '/api/detection/image',
                'detect_stream': '/api/detection/stream',
                'get_models': '/api/model/list',
                'get_classes': '/api/model/classes',
                'upload': '/api/detection/upload',
                'video_feed': '/api/detection/video_feed',
                'stop_camera': '/stop_camera',
                'set_webcam': '/set_webcam'
            }
        }), 200

    # Frontend-compatible endpoints (root level)
    @app.route('/stop_camera', methods=['POST'])
    def stop_camera():
        """Stop camera - frontend compatible endpoint"""
        return jsonify({'success': True, 'message': 'Camera stopped'}), 200

    @app.route('/set_webcam', methods=['POST'])
    def set_webcam():
        """Set webcam - frontend compatible endpoint"""
        return jsonify({'success': True, 'message': 'Webcam set'}), 200

    @app.route('/upload', methods=['POST'])
    def upload_root():
        """Upload endpoint at root level - redirects to API"""
        from flask import redirect
        return redirect('/api/detection/upload', code=307)

    @app.route('/video_feed', methods=['GET'])
    def video_feed_root():
        """Video feed at root level - redirects to API"""
        from flask import redirect
        return redirect(f'/api/detection/video_feed?{request.query_string.decode()}', code=307)

    @app.route('/processed_image', methods=['GET'])
    def processed_image_root():
        """Processed image at root level - redirects to API"""
        from flask import redirect
        return redirect('/api/detection/processed_image', code=307)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 50)
    print("🚀 Object Detection API Server")
    print("=" * 50)
    print(f"Server running on: http://localhost:5000")
    print(f"Health check: http://localhost:5000/api/health")
    print(f"API docs: http://localhost:5000/")
    print("=" * 50)
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
