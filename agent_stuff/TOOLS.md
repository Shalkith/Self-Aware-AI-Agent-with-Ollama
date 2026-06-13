# TOOLS.md - External Tool Interactions

## Available Skills & Tools

### LLM Integration (Ollama)
**Status:** ACTIVE  
**Credential Source:** Environment variable `OLLAMA_URL`  

**Capabilities:**
- Chat completion via `ollama` Python package
- Vision analysis with `llava` model
- Reasoning with `mistral` model
- Security evaluation with `llama3` model

**Usage Notes:**
- Client initialized with `ollama.Client(host=config.OLLAMA_URL)`
- Models checked at boot via `client.show(model_name)`
- Fallback to default models if specific model unavailable

---

### Perception Layer

#### Camera (OpenCV)
**Status:** ACTIVE  
**Library:** `cv2`  

**Capabilities:**
- Frame capture at configurable resolution
- Base64 encoding for LLM vision input
- Continuous capture mode with callbacks

**Usage:**
```python
from perception.camera import CameraPerception
camera = CameraPerception(index=0, width=640, height=480)
frame_b64 = camera.get_frame_base64()
```

#### Microphone (PyAudio)
**Status:** ACTIVE  
**Library:** `pyaudio`  

**Capabilities:**
- Audio stream capture
- Callback-based listening
- Configurable sample rate and channels

**Usage:**
```python
from perception.microphone import MicrophonePerception
mic = MicrophonePerception(rate=16000, channels=1)
mic.start_listening(callback_function)
```

#### Speaker (pyttsx3)
**Status:** ACTIVE  
**Library:** `pyttsx3`  

**Capabilities:**
- Text-to-speech synthesis
- Async speech support
- Cross-platform compatibility

**Usage:**
```python
from perception.speaker import SpeakerPerception
speaker = SpeakerPerception()
speaker.speak_async("Hello, user!")
```

---

### Memory System (SQLite)
**Status:** ACTIVE  
**Location:** `memory/agent_memory.db`  

**Capabilities:**
- Persistent storage of memories and experiences
- Search by content
- Statistics tracking

**Tables:**
- `memories` - Long-term facts and knowledge
- `experiences` - Interaction history with outcomes

---

### Security Framework
**Status:** ACTIVE  
**Components:**
- `LLMSecurityAgent` - Evaluates file operations
- `LLMFileOperationInterceptor` - Intercepts file ops

**Policy:**
- Deny-by-default
- LLM evaluation for all file modifications
- Audit logging of all decisions

---

### Device Control
**Status:** SIMULATION MODE  
**Future:** GPIO support planned

**Capabilities:**
- Device registration and management
- Command sending (turn_on, turn_off, toggle)
- State tracking

**Supported Controllers:**
- `simulation` (default) - Software-only
- `gpio` (planned) - Raspberry Pi GPIO
- `api` (planned) - External API devices

---

### Web Framework (Flask + SocketIO)
**Status:** ACTIVE  
**Libraries:** `flask`, `flask-socketio`  

**Capabilities:**
- RESTful API endpoints
- Real-time bidirectional communication
- Web interface serving

**Endpoints:**
- `GET /api/status` - Agent status
- `GET /api/memories` - Recent memories
- `POST /api/control-device` - Device commands

---

## Credential Management

### Environment Variables
All credentials stored in `.env` file (never committed):

```bash
# .env (loaded by config.py)
OLLAMA_URL=http://192.168.99.113:11434
```

### Security Notes
- No hardcoded credentials in source
- No API keys in committed files
- Credentials loaded at runtime from environment

---

## Skill Activation Status

| Skill | Status | Notes |
|-------|--------|-------|
| Camera | ✓ Active | OpenCV-based |
| Microphone | ✓ Active | PyAudio-based |
| Speaker | ✓ Active | pyttsx3-based |
| LLM Chat | ✓ Active | Ollama integration |
| File Operations | ⚠ Secured | LLM evaluation required |
| Device Control | ✓ Simulation | GPIO planned |
| Memory | ✓ Active | SQLite persistence |
| Web Server | ✓ Active | Flask/SocketIO |

---

## Tool Interaction Patterns

### Standard Pattern
1. Import tool module
2. Initialize with config
3. Use within try/except
4. Proper cleanup on exit

### Error Handling
- Graceful degradation (e.g., camera fails → continue without)
- User notification of significant failures
- Fallback options where available

---

## Adding New Tools

To add a new tool:
1. Create module in appropriate folder
2. Add to `config.py` if configurable
3. Update system prompt documentation
4. Add initialization in `AgentLoop`
5. Document in this file

---

## Last Updated
2026-06-13

*This file documents active skills and tool usage patterns.*
