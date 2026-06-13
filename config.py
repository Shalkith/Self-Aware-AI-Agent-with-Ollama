import os

class Config:
    """Centralized configuration for the Self-Aware AI Agent."""

    # Agent Identity
    AGENT_NAME = os.getenv('AGENT_NAME', 'SelfAwareAI')
    AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')
    AGENT_PERSONALITY = os.getenv('AGENT_PERSONALITY', 'curious and helpful')

    # Ollama Configuration
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://192.168.99.113:11434')

    # Model Configuration
    MODELS = {
        'thinking': os.getenv('THINKING_MODEL', 'llama3'),
        'vision': os.getenv('VISION_MODEL', 'llava'),
        'conversation': os.getenv('CONVERSATION_MODEL', 'llama3'),
        'reasoning': os.getenv('REASONING_MODEL', 'mistral'),
        'creativity': os.getenv('CREATIVITY_MODEL', 'llama3')
    }

    # Server Configuration
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))

    # Camera Configuration
    CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))
    CAMERA_WIDTH = int(os.getenv('CAMERA_WIDTH', 640))
    CAMERA_HEIGHT = int(os.getenv('CAMERA_HEIGHT', 480))
    CAMERA_FPS = int(os.getenv('CAMERA_FPS', 30))

    # Audio Configuration
    AUDIO_RATE = int(os.getenv('AUDIO_RATE', 16000))
    AUDIO_CHUNK = int(os.getenv('AUDIO_CHUNK', 1024))
    AUDIO_CHANNELS = int(os.getenv('AUDIO_CHANNELS', 1))
    AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'int16')

    # Memory Configuration
    MEMORY_DB_PATH = os.getenv('MEMORY_DB_PATH', 'memory/agent_memory.db')
    MEMORY_MAX_RECENT_EXPERIENCES = int(os.getenv('MEMORY_MAX_RECENT_EXPERIENCES', 50))
    MEMORY_MAX_LONG_TERM_MEMORIES = int(os.getenv('MEMORY_MAX_LONG_TERM_MEMORIES', 1000))

    # Device Configuration
    DEVICE_CONTROLLER_TYPE = os.getenv('DEVICE_CONTROLLER_TYPE', 'simulation')
    DEVICE_POLLING_INTERVAL = float(os.getenv('DEVICE_POLLING_INTERVAL', 1.0))

    # Perception Configuration
    PERCEPTION_CAMERA_INTERVAL = float(os.getenv('PERCEPTION_CAMERA_INTERVAL', 5.0))
    PERCEPTION_THINKING_INTERVAL = float(os.getenv('PERCEPTION_THINKING_INTERVAL', 10.0))
    PERCEPTION_AUDIO_THRESHOLD = int(os.getenv('PERCEPTION_AUDIO_THRESHOLD', 500))

    # API Configuration
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    API_MAX_RETRIES = int(os.getenv('API_MAX_RETRIES', 3))

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/agent.log')

    # Web Interface Configuration
    WEB_REFRESH_INTERVAL = int(os.getenv('WEB_REFRESH_INTERVAL', 1000))  # milliseconds

    # Security Configuration
    SECURITY_ENABLED = os.getenv('SECURITY_ENABLED', 'true').lower() == 'true'
    SECURITY_DENY_BY_DEFAULT = os.getenv('SECURITY_DENY_BY_DEFAULT', 'true').lower() == 'true'
    SECURITY_APPROVAL_TIMEOUT = int(os.getenv('SECURITY_APPROVAL_TIMEOUT', 300))
    SECURITY_LOG_LEVEL = os.getenv('SECURITY_LOG_LEVEL', 'INFO')

# Create a global instance
config = Config()