"""
Model API Routes
Endpoints for model management operations
"""

from flask import Blueprint, request, jsonify
import os
from pathlib import Path

from app.services.detect_service import get_detection_service
from app.config import Config

model_bp = Blueprint('model', __name__)


@model_bp.route('/info', methods=['GET'])
def get_model_info():
    """
    Get current model information

    Returns:
        JSON with model details
    """
    try:
        service = get_detection_service()
        info = service.get_model_info()
        return jsonify(info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@model_bp.route('/classes', methods=['GET'])
def get_classes():
    """
    Get list of detectable classes

    Returns:
        JSON with list of class names
    """
    try:
        service = get_detection_service()
        classes = service.get_classes()
        return jsonify({
            'classes': classes,
            'count': len(classes)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@model_bp.route('/list', methods=['GET'])
def list_available_models():
    """
    List available YOLO models in the project

    Returns:
        JSON with list of available models
    """
    try:
        # Look for .pt files in backend directory
        base_dir = Path(Config.BASE_DIR)
        models = []

        # Search for .pt files in backend root
        for pt_file in base_dir.glob('*.pt'):
            models.append({
                'name': pt_file.name,
                'path': str(pt_file),
                'size': pt_file.stat().st_size,
                'size_mb': round(pt_file.stat().st_size / (1024 * 1024), 2)
            })

        # Also check runs/train for custom models
        runs_dir = base_dir / 'runs' / 'train'
        if runs_dir.exists():
            for weights_dir in runs_dir.glob('*/weights'):
                for pt_file in weights_dir.glob('*.pt'):
                    models.append({
                        'name': pt_file.name,
                        'path': str(pt_file),
                        'type': 'trained',
                        'size': pt_file.stat().st_size,
                        'size_mb': round(pt_file.stat().st_size / (1024 * 1024), 2)
                    })

        return jsonify({
            'models': models,
            'count': len(models)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@model_bp.route('/change', methods=['POST'])
def change_model():
    """
    Change the detection model

    Expected JSON:
        {
            "model_path": "path/to/model.pt",
            "conf": 0.25 (optional)
        }

    Returns:
        JSON with success status
    """
    try:
        data = request.get_json()

        if not data or 'model_path' not in data:
            return jsonify({'error': 'model_path is required'}), 400

        model_path = data['model_path']

        # Check if model file exists
        if not os.path.exists(model_path):
            return jsonify({'error': f'Model file not found: {model_path}'}), 404

        # Try to change model
        service = get_detection_service()
        success = service.change_model(model_path)

        if success:
            return jsonify({
                'success': True,
                'message': 'Model changed successfully',
                'model_path': model_path
            }), 200
        else:
            return jsonify({'error': 'Failed to load model'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@model_bp.route('/confidence', methods=['POST'])
def set_confidence():
    """
    Set confidence threshold

    Expected JSON:
        {
            "conf": 0.25
        }

    Returns:
        JSON with success status
    """
    try:
        data = request.get_json()

        if not data or 'conf' not in data:
            return jsonify({'error': 'conf is required'}), 400

        conf = data['conf']

        if not (0 < conf <= 1):
            return jsonify({'error': 'conf must be between 0 and 1'}), 400

        service = get_detection_service()
        service.conf_threshold = conf

        return jsonify({
            'success': True,
            'message': 'Confidence threshold updated',
            'conf': conf
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
