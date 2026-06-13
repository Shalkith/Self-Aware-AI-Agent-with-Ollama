import pyaudio
import threading
import time
import logging
from typing import Callable, Optional

class MicrophonePerception:
    def __init__(self, rate: int = 16000, chunk: int = 1024, channels: int = 1, format_type: int = pyaudio.paInt16):
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.format_type = format_type
        self.audio = None
        self.stream = None
        self.is_listening = False
        self.audio_callback = None
        self.listen_thread = None

    def initialize(self) -> bool:
        """Initialize the microphone."""
        try:
            self.audio = pyaudio.PyAudio()
            return True
        except Exception as e:
            logging.error(f"Error initializing microphone: {e}")
            return False

    def start_listening(self, callback: Callable[[bytes], None]):
        """Start listening to microphone input."""
        if self.is_listening:
            return

        try:
            self.stream = self.audio.open(
                format=self.format_type,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )

            self.audio_callback = callback
            self.is_listening = True
            self.listen_thread = threading.Thread(target=self._listen_loop)
            self.listen_thread.daemon = True
            self.listen_thread.start()

            return True
        except Exception as e:
            logging.error(f"Error starting microphone: {e}")
            return False

    def _listen_loop(self):
        """Internal listening loop."""
        while self.is_listening:
            try:
                data = self.stream.read(self.chunk)
                if self.audio_callback:
                    self.audio_callback(data)
            except Exception as e:
                logging.error(f"Error in audio callback: {e}")

    def stop_listening(self):
        """Stop listening to microphone input."""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join()

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def release(self):
        """Release the microphone."""
        self.stop_listening()
        if self.audio:
            self.audio.terminate()
            self.audio = None