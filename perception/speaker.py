import pyttsx3
import threading
import logging
from typing import Optional

class SpeakerPerception:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.speak_lock = threading.Lock()

    def initialize(self) -> bool:
        """Initialize the text-to-speech engine."""
        try:
            self.engine = pyttsx3.init()
            return True
        except Exception as e:
            logging.error(f"Error initializing speaker: {e}")
            return False

    def speak(self, text: str, async_speak: bool = False):
        """Speak the given text."""
        if not self.engine:
            logging.error("Speaker not initialized")
            return

        with self.speak_lock:
            if async_speak:
                # Speak asynchronously
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Speak synchronously
                self.engine.say(text)
                self.engine.runAndWait()

    def speak_async(self, text: str):
        """Speak text asynchronously in a separate thread."""
        if not self.engine:
            logging.error("Speaker not initialized")
            return

        def _speak_thread():
            with self.speak_lock:
                self.engine.say(text)
                self.engine.runAndWait()

        thread = threading.Thread(target=_speak_thread)
        thread.daemon = True
        thread.start()

    def set_voice(self, voice_id: str):
        """Set the voice for the speaker."""
        if not self.engine:
            return

        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.id == voice_id:
                self.engine.setProperty('voice', voice.id)
                break

    def set_rate(self, rate: int):
        """Set the speaking rate (words per minute)."""
        if not self.engine:
            return

        self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float):
        """Set the speaking volume (0.0 to 1.0)."""
        if not self.engine:
            return

        self.engine.setProperty('volume', volume)

    def get_voices(self):
        """Get available voices."""
        if not self.engine:
            return []

        return self.engine.getProperty('voices')

    def release(self):
        """Release the speaker engine."""
        if self.engine:
            self.engine.stop()
            self.engine = None