"""Routes package"""
from .detection_routes import detection_bp
from .model_routes import model_bp

__all__ = ['detection_bp', 'model_bp']
