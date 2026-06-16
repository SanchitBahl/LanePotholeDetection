"""
Core Computer Vision module for real-time lane and pothole detection.
Handles YOLOv8n inference and lightweight lane detection pipeline.
"""

import cv2
import numpy as np
from ultralytics import YOLO
import av


class DetectionEngine:
    """Manages pothole detection and lane tracking in real-time."""

    def __init__(self, model_size: int = 320, conf_threshold: float = 0.5):
        """
        Initialize detection engine.
        
        Args:
            model_size: Inference resolution (320 or 640 for speed/accuracy tradeoff)
            conf_threshold: YOLOv8n confidence threshold
        """
        self.model_size = model_size
        self.conf_threshold = conf_threshold
        # Download and load YOLOv8n pretrained model
        self.model = YOLO('yolov8n.pt')
        self.class_names = self.model.names
        
        # Detection stats for UI
        self.last_detection_count = 0
        self.last_lanes_count = 0

    def detect_potholes(self, frame: np.ndarray) -> tuple:
        """
        Detect potholes using YOLOv8n.
        
        Args:
            frame: Input BGR image frame
            
        Returns:
            (annotated_frame, detection_list)
            detection_list: List of dicts with 'box', 'conf', 'class_id'
        """
        results = self.model.predict(
            source=frame,
            imgsz=self.model_size,
            conf=self.conf_threshold,
            verbose=False
        )
        
        detections = []
        annotated_frame = frame.copy()
        
        if results and len(results) > 0:
            result = results[0]
            
            # Extract bounding boxes and confidence scores
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                class_id = int(box.cls[0])
                
                detections.append({
                    'box': (x1, y1, x2, y2),
                    'conf': conf,
                    'class_id': class_id,
                    'class_name': self.class_names.get(class_id, 'Unknown')
                })
                
                # Draw bounding box
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # Draw label
                label = f"{self.class_names.get(class_id, 'Unknown')}: {conf:.2f}"
                cv2.putText(
                    annotated_frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )
        
        self.last_detection_count = len(detections)
        return annotated_frame, detections

    def detect_lanes(self, frame: np.ndarray) -> tuple:
        """
        Lightweight lane detection using Canny edges and Hough lines.
        
        Args:
            frame: Input BGR image frame
            
        Returns:
            (annotated_frame, lanes_list)
            lanes_list: List of lane line coordinates
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Define region of interest (lower half of frame focused on road)
        roi_mask = np.zeros_like(edges)
        points = np.array([
            [0, height // 2],
            [0, height],
            [width, height],
            [width, height // 2]
        ], dtype=np.int32)
        cv2.fillPoly(roi_mask, [points], 255)
        roi_edges = cv2.bitwise_and(edges, roi_mask)
        
        # Hough line detection
        lines = cv2.HoughLinesP(
            roi_edges,
            rho=1,
            theta=np.pi / 180,
            threshold=50,
            minLineLength=30,
            maxLineGap=10
        )
        
        annotated_frame = frame.copy()
        lanes_list = []
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                lanes_list.append(((x1, y1), (x2, y2)))
                # Draw lane line in green
                cv2.line(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        self.last_lanes_count = len(lanes_list)
        return annotated_frame, lanes_list

    def process_frame(
        self,
        frame: np.ndarray,
        detect_potholes: bool = True,
        detect_lanes: bool = True
    ) -> tuple:
        """
        Process a single frame for both lane and pothole detection.
        
        Args:
            frame: Input BGR image frame
            detect_potholes: Enable pothole detection
            detect_lanes: Enable lane detection
            
        Returns:
            (output_frame, potholes, lanes, stats_dict)
        """
        output = frame.copy()
        potholes = []
        lanes = []
        stats = {}
        
        if detect_potholes:
            output, potholes = self.detect_potholes(output)
            stats['potholes'] = len(potholes)
        
        if detect_lanes:
            output, lanes = self.detect_lanes(output)
            stats['lanes'] = len(lanes)
        
        return output, potholes, lanes, stats

    def create_video_frame_callback(self, detect_potholes: bool, detect_lanes: bool):
        """
        Create a video frame processing callback for streamlit-webrtc.
        
        Args:
            detect_potholes: Enable pothole detection
            detect_lanes: Enable lane detection
            
        Returns:
            Callback function for WebRTC stream
        """
        def callback(frame: av.VideoFrame) -> av.VideoFrame:
            # Convert av.VideoFrame to numpy array (BGR)
            image = frame.to_ndarray(format="bgr24")
            
            # Process frame
            processed_image, _, _, _ = self.process_frame(
                image,
                detect_potholes=detect_potholes,
                detect_lanes=detect_lanes
            )
            
            # Convert back to av.VideoFrame
            return av.VideoFrame.from_ndarray(processed_image, format="bgr24")
        
        return callback

    def get_stats(self) -> dict:
        """Return latest detection statistics."""
        return {
            'last_potholes': self.last_detection_count,
            'last_lanes': self.last_lanes_count
        }
