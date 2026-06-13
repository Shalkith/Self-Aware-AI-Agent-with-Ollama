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

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

```
ollama_self_aware_robot/
├── agent_stuff/             # Agent components
│   ├── agent/               # Main agent loop and runner
│   │   ├── __init__.py
│   │   ├── loop.py
│   │   ├── runner.py
│   │   └── main.py
│   ├── agent.md             # Agent configuration
│   └── heartbeat.md         # Periodic tasks
├── security/                # Security framework
│   ├── llm_security_agent.py
│   ├── llm_file_interceptor.py
│   └── api_endpoints.py
├── perception/              # Sensor modules
│   ├── camera.py
│   ├── microphone.py
│   └── speaker.py
├── memory/                  # Memory system
│   └── memory_manager.py
├── devices/                 # Device control
│   └── device_controller.py
├── client/                  # Web interface
│   ├── static/
│   └── templates/
├── tests/                   # Test suite
│   └── ...
├── docs/                    # Documentation
│   └── ...
├── scripts/                 # Utility scripts
│   ├── start_agent.py
│   └── ...
├── agent_server.py          # Web server entry point
├── config.py                # Configuration
├── requirements.txt         # Dependencies
└── README.md                # Project overview
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
python scripts/reset.py
```

Or on Windows:
```bash
scripts\reset_agent.bat
```

Options:
- `--full`: Completely reset the database
- `--memory-only`: Reset only memories and experiences
- `--config`: Reset configuration to defaults

## Startup Scripts

Alternative startup scripts are available in the `scripts/` folder:

```bash
# Interactive startup with mode selection
python scripts/start_agent_modern.py

# Initialize environment and check dependencies
python scripts/init.py
```

## API Endpoints

The agent server provides several API endpoints:

- `GET /api/status`: Get current agent status
- `GET /api/memories`: Get recent memories
- `GET /api/experiences`: Get recent experiences
- `GET /api/devices`: Get registered devices
- `POST /api/control-device`: Send command to a device
- `POST /api/think`: Trigger a thinking cycle

## Documentation

- [docs/USAGE.md](docs/USAGE.md): Detailed usage guide
- [docs/SECURITY.md](docs/SECURITY.md): Security framework documentation
- [docs/SELF_IMPROVEMENT.md](docs/SELF_IMPROVEMENT.md): Guide to safe self-improvement
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): Architecture documentation
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md): Configuration options

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