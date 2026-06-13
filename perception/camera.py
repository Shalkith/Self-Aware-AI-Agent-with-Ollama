import cv2
import base64
import threading
import time
from typing import Optional, Callable
import logging

class CameraPerception:
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        self.is_capturing = False
        self.frame_callback = None
        self.capture_thread = None
        self.last_frame = None

    def initialize(self) -> bool:
        """Initialize the camera."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                logging.error("Failed to open camera")
                return False

            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            return True
        except Exception as e:
            logging.error(f"Error initializing camera: {e}")
            return False

    def capture_frame(self) -> Optional[bytes]:
        """Capture a single frame and return as JPEG bytes."""
        if not self.cap or not self.cap.isOpened():
            return None

        try:
            ret, frame = self.cap.read()
            if not ret:
                return None

            # Store last frame
            self.last_frame = frame.copy()

            # Encode as JPEG
            success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not success:
                return None

            return buffer.tobytes()
        except Exception as e:
            logging.error(f"Error capturing frame: {e}")
            return None

    def get_frame_base64(self) -> Optional[str]:
        """Capture a frame and return as base64 encoded string."""
        frame_bytes = self.capture_frame()
        if frame_bytes is None:
            return None

        return base64.b64encode(frame_bytes).decode('utf-8')

    def start_continuous_capture(self, callback: Callable[[bytes], None], interval: float = 0.1):
        """Start continuous frame capture with callback."""
        if self.is_capturing:
            return

        self.frame_callback = callback
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_loop, args=(interval,))
        self.capture_thread.daemon = True
        self.capture_thread.start()

    def _capture_loop(self, interval: float):
        """Internal capture loop."""
        while self.is_capturing:
            frame_bytes = self.capture_frame()
            if frame_bytes and self.frame_callback:
                try:
                    self.frame_callback(frame_bytes)
                except Exception as e:
                    logging.error(f"Error in frame callback: {e}")

            time.sleep(interval)

    def stop_continuous_capture(self):
        """Stop continuous frame capture."""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join()

    def get_last_frame(self):
        """Get the last captured frame."""
        return self.last_frame

    def release(self):
        """Release the camera."""
        self.stop_continuous_capture()
        if self.cap:
            self.cap.release()
            self.cap = None