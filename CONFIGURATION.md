# Self-Aware AI Agent Configuration

This document explains the configuration system for the Self-Aware AI Agent.

## Configuration Overview

All configuration is centralized in the `config.py` file. The system uses a `Config` class with class-level attributes that can be overridden by environment variables.

## Configuration Structure

### Agent Identity

```python
AGENT_NAME = os.getenv('AGENT_NAME', 'SelfAwareAI')
AGENT_VERSION = os.getenv('AGENT_VERSION', '1.0.0')
AGENT_PERSONALITY = os.getenv('AGENT_PERSONALITY', 'curious and helpful')
```

### Ollama Configuration

```python
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
```

### Model Configuration

The agent uses different models for different tasks:

```python
MODELS = {
    'thinking': os.getenv('THINKING_MODEL', 'llama3'),
    'vision': os.getenv('VISION_MODEL', 'llava'),
    'conversation': os.getenv('CONVERSATION_MODEL', 'llama3'),
    'reasoning': os.getenv('REASONING_MODEL', 'mistral'),
    'creativity': os.getenv('CREATIVITY_MODEL', 'llama3')
}
```

### Server Configuration

```python
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
```

### Camera Configuration

```python
CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))
CAMERA_WIDTH = int(os.getenv('CAMERA_WIDTH', 640))
CAMERA_HEIGHT = int(os.getenv('CAMERA_HEIGHT', 480))
CAMERA_FPS = int(os.getenv('CAMERA_FPS', 30))
```

### Audio Configuration

```python
AUDIO_RATE = int(os.getenv('AUDIO_RATE', 16000))
AUDIO_CHUNK = int(os.getenv('AUDIO_CHUNK', 1024))
AUDIO_CHANNELS = int(os.getenv('AUDIO_CHANNELS', 1))
AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'int16')
```

### Memory Configuration

```python
MEMORY_DB_PATH = os.getenv('MEMORY_DB_PATH', 'memory/agent_memory.db')
MEMORY_MAX_RECENT_EXPERIENCES = int(os.getenv('MEMORY_MAX_RECENT_EXPERIENCES', 50))
MEMORY_MAX_LONG_TERM_MEMORIES = int(os.getenv('MEMORY_MAX_LONG_TERM_MEMORIES', 1000))
```

### Device Configuration

```python
DEVICE_CONTROLLER_TYPE = os.getenv('DEVICE_CONTROLLER_TYPE', 'simulation')
DEVICE_POLLING_INTERVAL = float(os.getenv('DEVICE_POLLING_INTERVAL', 1.0))
```

### Perception Configuration

```python
PERCEPTION_CAMERA_INTERVAL = float(os.getenv('PERCEPTION_CAMERA_INTERVAL', 5.0))
PERCEPTION_THINKING_INTERVAL = float(os.getenv('PERCEPTION_THINKING_INTERVAL', 10.0))
PERCEPTION_AUDIO_THRESHOLD = int(os.getenv('PERCEPTION_AUDIO_THRESHOLD', 500))
```

### API Configuration

```python
API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
API_MAX_RETRIES = int(os.getenv('API_MAX_RETRIES', 3))
```

### Logging Configuration

```python
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/agent.log')
```

### Web Interface Configuration

```python
WEB_REFRESH_INTERVAL = int(os.getenv('WEB_REFRESH_INTERVAL', 1000))  # milliseconds
```

## Environment Variables

All configuration values can be overridden using environment variables. For example:

```bash
export AGENT_NAME="MyCustomAI"
export OLLAMA_URL="http://remote-server:11434"
export VISION_MODEL="llava-phi3"
export CAMERA_INDEX=1
```

## Model Selection Guide

### Thinking Model
- **Purpose**: Autonomous reflection and self-analysis
- **Default**: `llama3`
- **Environment Variable**: `THINKING_MODEL`

### Vision Model
- **Purpose**: Image analysis and visual perception
- **Default**: `llava`
- **Environment Variable**: `VISION_MODEL`

### Conversation Model
- **Purpose**: User interaction and dialogue
- **Default**: `llama3`
- **Environment Variable**: `CONVERSATION_MODEL`

### Reasoning Model
- **Purpose**: Complex problem solving and logical reasoning
- **Default**: `mistral`
- **Environment Variable**: `REASONING_MODEL`

### Creativity Model
- **Purpose**: Creative tasks and idea generation
- **Default**: `llama3`
- **Environment Variable**: `CREATIVITY_MODEL`

## Usage in Code

To access configuration values in your code:

```python
from config import config

# Access configuration values
agent_name = config.AGENT_NAME
ollama_url = config.OLLAMA_URL
vision_model = config.MODELS['vision']
```

## Best Practices

1. **Use Environment Variables**: For deployment flexibility, set configuration via environment variables
2. **Model Specialization**: Choose models appropriate for each task type
3. **Resource Management**: Adjust intervals and limits based on system resources
4. **Security**: Never commit sensitive configuration to version control

## Example Configuration

Here's an example of a custom configuration for a specialized agent:

```bash
# Agent Identity
export AGENT_NAME="HomeAssistant"
export AGENT_VERSION="2.1.0"
export AGENT_PERSONALITY="helpful and efficient"

# Models
export THINKING_MODEL="mistral"
export VISION_MODEL="llava-phi3"
export CONVERSATION_MODEL="llama3"
export REASONING_MODEL="mixtral"
export CREATIVITY_MODEL="llama3"

# Server
export SERVER_HOST="0.0.0.0"
export SERVER_PORT=5000

# Camera
export CAMERA_INDEX=0
export CAMERA_WIDTH=1280
export CAMERA_HEIGHT=720

# Memory
export MEMORY_DB_PATH="/var/lib/ai-agent/memory.db"
export MEMORY_MAX_RECENT_EXPERIENCES=100
```

This configuration system provides flexibility to customize the agent's behavior, models, and resource usage for different deployment scenarios.