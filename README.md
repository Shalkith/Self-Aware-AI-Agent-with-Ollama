# Self-Aware AI Agent with Ollama

This project implements a self-aware AI agent that can perceive its environment through camera and microphone, communicate through speakers, control devices, and maintain persistent memory. The agent uses Ollama for LLM processing and provides a web-based interface for interaction and monitoring.

![AI Agent Architecture](https://placehold.co/800x400?text=Self-Aware+AI+Agent+Architecture)

## Features

- **Full Autonomous Behavior**: Continuous environmental monitoring and self-directed action
- **Multimodal Perception**: Camera, microphone, and speaker integration
- **Device Control**: Control external devices (lights, fans, etc.)
- **Task Execution**: Perform various tasks based on user input or autonomous decisions
- **Web-Based Client Interface**: Real-time interaction and monitoring
- **Persistent Memory System**: SQLite-based storage for experiences and knowledge
- **Reset Functionality**: Clear memory and reset state with simple script
- **Security Framework**: Code modification protection with approval system

## Architecture

See [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) for detailed architecture documentation.

```
ollama_self_aware_robot/
├── nanobot_style/           # Nanobot-style agent components
│   ├── agent/               # Main agent loop and runner
│   │   ├── __init__.py
│   │   ├── loop.py
│   │   ├── runner.py
│   │   └── main.py
│   ├── agent.md             # Agent configuration
│   └── heartbeat.md         # Periodic tasks
├── agent_server.py          # Web server
├── config.py                # Configuration
├── reset.py                 # Reset script
├── init.py                  # Initialization script
├── start_agent.py           # Startup script
├── test_setup.py            # Setup test script
├── run_tests.py             # Test runner
├── requirements.txt         # Dependencies
├── README.md                # Project overview
├── USAGE.md                 # Usage guide
├── SECURITY.md              # Security framework documentation
├── SELF_IMPROVEMENT.md      # Self-improvement guide
├── AGENT_ARCHITECTURE.md    # Architecture documentation
├── PROJECT_SUMMARY.md       # Detailed project summary
├── start_agent.bat          # Windows startup script
├── reset_agent.bat          # Windows reset script
├── client/                  # Web client interface
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
├── perception/              # Camera, mic, speaker modules
│   ├── camera.py
│   ├── microphone.py
│   └── speaker.py
├── memory/                  # Memory system
│   └── memory_manager.py
├── devices/                 # Device control
│   └── device_controller.py
├── security/                # Security framework
│   ├── llm_security_agent.py
│   ├── llm_file_interceptor.py
│   └── api_endpoints.py
└── api_endpoints.py         # Additional API endpoints
```

## Requirements

- Python 3.8+
- Ollama server (local or remote)
- Camera and microphone access
- Speaker output capability

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Ollama**:
   - Make sure Ollama is running
   - Update `OLLAMA_URL` in `config.py` if using a remote server

3. **Run the agent server**:
   ```bash
   python agent_server.py
   ```
   Or on Windows, double-click `start_agent.bat`

4. **Access the web interface** at `http://localhost:5000`

## Web Interface

The web interface provides:

1. **Agent Control Panel**:
   - Start/Stop the autonomous agent
   - View current status and thoughts
   - See last actions taken

2. **Agent Interaction**:
   - Send messages to the agent
   - View agent responses and thoughts
   - Camera feed display

3. **Device Control**:
   - Control registered devices (lights, fans, etc.)
   - View device states

4. **Memory & Experiences**:
   - View agent's memories
   - See recent experiences

## Usage

### Manual Interaction

1. Type messages in the input field and press Send or Enter
2. The agent will respond with both its thoughts and response
3. The agent may take actions based on its response

### Autonomous Mode

1. Click "Start Agent" to enable autonomous behavior
2. The agent will:
   - Continuously observe its environment
   - Form thoughts and make decisions
   - Take actions when appropriate
   - Learn from experiences

### Device Control

1. Registered devices appear in the Device Control panel
2. Click "On" or "Off" buttons to control devices
3. Device states are displayed below each device

## Reset Script

To reset the agent and clear all memories:

```bash
python reset.py
```

Or on Windows, double-click `reset_agent.bat`

Options:
- `--full`: Completely reset the database
- `--memory-only`: Reset only memories and experiences
- `--config`: Reset configuration to defaults

## API Endpoints

The agent server provides several API endpoints:

- `GET /api/status`: Get current agent status
- `GET /api/memories`: Get recent memories
- `GET /api/experiences`: Get recent experiences
- `GET /api/devices`: Get registered devices
- `POST /api/control-device`: Send command to a device
- `POST /api/think`: Trigger a thinking cycle

## Documentation

- [USAGE.md](USAGE.md): Detailed usage guide
- [SECURITY.md](SECURITY.md): Security framework documentation
- [SELF_IMPROVEMENT.md](SELF_IMPROVEMENT.md): Guide to safe self-improvement
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md): Comprehensive project overview
- [config.py](config.py): Configuration options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Ollama](https://ollama.ai) for local LLM inference
- [Flask](https://palletsprojects.com/p/flask/) for the web framework
- [OpenCV](https://opencv.org/) for computer vision capabilities
- All the open-source libraries that made this project possible