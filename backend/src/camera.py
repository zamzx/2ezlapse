import cv2
import time
from datetime import datetime
from pathlib import Path
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CameraManager:
    def __init__(self, captures_dir: Path):
        self.captures_dir = captures_dir
        self.camera = None
        self.is_capturing = False
        self.capture_thread = None
        self.interval = 1  # Default interval in seconds
        
    def initialize(self):
        """Initialize the camera"""
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise RuntimeError("Could not initialize camera")
            logger.info("Camera initialized successfully")
    
    def release(self):
        """Release the camera"""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            logger.info("Camera released")
    
    def capture_photo(self) -> str:
        """Capture a single photo and return the filename"""
        if self.camera is None:
            self.initialize()
        
        ret, frame = self.camera.read()
        if not ret:
            raise RuntimeError("Failed to capture photo")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        filepath = self.captures_dir / filename
        
        cv2.imwrite(str(filepath), frame)
        logger.info(f"Captured photo: {filename}")
        return filename
    
    def start_timelapse(self, interval: int):
        """Start timelapse capture with given interval"""
        if self.is_capturing:
            return
        
        self.interval = interval
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.start()
        logger.info(f"Started timelapse capture with {interval}s interval")
    
    def stop_timelapse(self):
        """Stop timelapse capture"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join()
        self.capture_thread = None
        logger.info("Stopped timelapse capture")
    
    def _capture_loop(self):
        """Internal loop for timelapse capture"""
        while self.is_capturing:
            try:
                self.capture_photo()
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in capture loop: {e}")
                self.is_capturing = False
                break 