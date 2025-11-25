"""
Configuration settings for Flask application
"""

import os
from pathlib import Path


class Config:
    """Base configuration"""

    # Base directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    ROOT_DIR = BASE_DIR  # Backend is now the root

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    # File upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

    # Dataset and model paths
    DATASETS_FOLDER = os.path.join(BASE_DIR, 'Datasets')
    RUNS_FOLDER = os.path.join(BASE_DIR, 'runs')
    CONFIG_FOLDER = os.path.join(BASE_DIR, 'config')

    # YOLO Model settings
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL') or os.path.join(BASE_DIR, 'yolov8n.pt')
    DEFAULT_CONF = float(os.environ.get('DEFAULT_CONF', '0.25'))

    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')

    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
