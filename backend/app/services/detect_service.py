"""
Object Detection Service
Handles YOLO model loading and inference
"""

import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Tuple, Optional
import base64
from pathlib import Path
import time


class DetectionService:
    """Service for handling object detection operations"""

    def __init__(self, model_path: str = 'yolov8n.pt', conf_threshold: float = 0.25):
        """
        Initialize detection service

        Args:
            model_path: Path to YOLO model
            conf_threshold: Confidence threshold for detections
        """
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.model = None
        self.load_model()

    def load_model(self) -> bool:
        """Load YOLO model"""
        try:
            print(f"Loading model: {self.model_path}")
            self.model = YOLO(self.model_path)
            print(f"Model loaded successfully: {self.model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def get_model_info(self) -> Dict:
        """Get model information"""
        if self.model is None:
            return {'error': 'Model not loaded'}

        return {
            'model_path': self.model_path,
            'conf_threshold': self.conf_threshold,
            'classes': self.model.names,
            'num_classes': len(self.model.names)
        }

    def detect_image(
        self,
        image_path: str,
        conf: Optional[float] = None,
        save_result: bool = True,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Detect objects in an image

        Args:
            image_path: Path to input image
            conf: Confidence threshold (uses default if None)
            save_result: Whether to save annotated image
            output_path: Path to save output image

        Returns:
            Dictionary containing detection results
        """
        if self.model is None:
            return {'error': 'Model not loaded'}

        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {'error': 'Could not read image'}

            # Run detection
            conf_threshold = conf if conf is not None else self.conf_threshold
            start_time = time.time()
            results = self.model(image, conf=conf_threshold, verbose=False)
            inference_time = time.time() - start_time

            # Process results
            detections = []
            annotated_image = image.copy()

            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        cls_name = self.model.names[cls_id]
                        confidence = float(box.conf[0])
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        # Add to detections list
                        detections.append({
                            'class_id': cls_id,
                            'class_name': cls_name,
                            'confidence': round(confidence, 3),
                            'bbox': {
                                'x1': x1,
                                'y1': y1,
                                'x2': x2,
                                'y2': y2,
                                'width': x2 - x1,
                                'height': y2 - y1
                            }
                        })

                        # Draw on image
                        color = (0, 255, 0)
                        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)

                        # Draw label
                        label = f"{cls_name}: {confidence:.2f}"
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                        cv2.rectangle(
                            annotated_image,
                            (x1, y1 - label_size[1] - 10),
                            (x1 + label_size[0], y1),
                            color,
                            -1
                        )
                        cv2.putText(
                            annotated_image,
                            label,
                            (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 0),
                            2
                        )

            # Save annotated image
            output_image_path = None
            if save_result:
                if output_path is None:
                    timestamp = int(time.time())
                    output_path = f"outputs/detected_{timestamp}.jpg"

                output_image_path = output_path
                cv2.imwrite(output_path, annotated_image)

            # Get image dimensions
            height, width = image.shape[:2]

            return {
                'success': True,
                'detections': detections,
                'count': len(detections),
                'inference_time': round(inference_time, 3),
                'image_info': {
                    'width': width,
                    'height': height,
                    'path': image_path
                },
                'output_image': output_image_path,
                'conf_threshold': conf_threshold
            }

        except Exception as e:
            return {'error': str(e)}

    def detect_frame(
        self,
        frame: np.ndarray,
        conf: Optional[float] = None,
        draw_boxes: bool = True
    ) -> Tuple[np.ndarray, List[Dict]]:
        """
        Detect objects in a single frame

        Args:
            frame: Input frame (numpy array)
            conf: Confidence threshold
            draw_boxes: Whether to draw bounding boxes

        Returns:
            Tuple of (annotated_frame, detections_list)
        """
        if self.model is None:
            return frame, []

        try:
            conf_threshold = conf if conf is not None else self.conf_threshold
            results = self.model(frame, conf=conf_threshold, verbose=False)

            detections = []
            annotated_frame = frame.copy()

            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        cls_name = self.model.names[cls_id]
                        confidence = float(box.conf[0])
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        detections.append({
                            'class_id': cls_id,
                            'class_name': cls_name,
                            'confidence': round(confidence, 3),
                            'bbox': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
                        })

                        if draw_boxes:
                            color = (0, 255, 0)
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                            label = f"{cls_name}: {confidence:.2f}"
                            cv2.putText(
                                annotated_frame,
                                label,
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                color,
                                2
                            )

            return annotated_frame, detections

        except Exception as e:
            print(f"Error in detect_frame: {e}")
            return frame, []

    def frame_to_base64(self, frame: np.ndarray, quality: int = 90) -> str:
        """Convert frame to base64 string"""
        try:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, buffer = cv2.imencode('.jpg', frame, encode_param)
            base64_str = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/jpeg;base64,{base64_str}"
        except Exception as e:
            print(f"Error converting frame to base64: {e}")
            return ""

    def get_classes(self) -> List[str]:
        """Get list of detectable classes"""
        if self.model is None:
            return []
        return list(self.model.names.values())

    def change_model(self, model_path: str) -> bool:
        """Change detection model"""
        try:
            self.model_path = model_path
            return self.load_model()
        except Exception as e:
            print(f"Error changing model: {e}")
            return False


# Singleton instance
_detection_service = None


def get_detection_service(model_path: str = 'yolov8n.pt', conf: float = 0.25) -> DetectionService:
    """Get or create detection service instance"""
    global _detection_service
    if _detection_service is None:
        _detection_service = DetectionService(model_path, conf)
    return _detection_service
