# Self-Aware AI Agent - Claude Code Project

This project implements a self-aware AI agent with multimodal perception capabilities, LLM-based security framework, and nanobot-style architecture.

## Project Overview

The Self-Aware AI Agent is designed to:
- Perceive its environment through camera and microphone
- Communicate through speakers
- Control external devices
- Maintain persistent memory and learning
- Safely improve itself through LLM-based security evaluation
- Operate in multiple modes (web, CLI, autonomous, heartbeat)

## Key Features

### Multimodal Perception
- **Camera Integration**: OpenCV-based visual perception
- **Microphone Integration**: PyAudio-based audio input
- **Speaker Integration**: Text-to-speech output

### LLM-Based Security Framework
- **Automatic Evaluation**: Security decisions made by LLM rather than manual approval
- **File Operation Interception**: All file operations are intercepted and evaluated
- **Audit Logging**: Comprehensive security activity logging
- **Configurable Policies**: Flexible security settings

### Nanobot-Style Architecture
- **Agent Loop Pattern**: Main processing loop similar to nanobot
- **Agent Management Files**: `agent.md` and `heartbeat.md` for configuration and tasks
- **Modular Structure**: Clean separation of concerns
- **Multiple Operation Modes**: Web, CLI, autonomous, heartbeat

### Multi-Model Support
- **Thinking Model**: For autonomous reflection (`llama3`)
- **Vision Model**: For image analysis (`llava`)
- **Conversation Model**: For user interaction (`llama3`)
- **Reasoning Model**: For complex problem solving (`mistral`)
- **Security Model**: For security evaluations (`llama3`)

## Architecture

```
ollama_self_aware_robot/
├── nanobot_style/           # Nanobot-style agent components
│   ├── agent/               # Main agent components
│   │   ├── __init__.py
│   │   ├── loop.py         # Main agent loop
│   │   ├── runner.py       # LLM interaction and tool execution
│   │   └── main.py         # CLI entry point
│   ├── agent.md            # Agent configuration
│   └── heartbeat.md        # Periodic tasks
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
├── tests/                   # Test suite
│   ├── test_setup.py
│   ├── test_senses.py
│   ├── test_security_agent.py
│   └── ...
├── client/                  # Web interface
│   ├── templates/
│   └── static/
├── agent_server.py          # Web server
└── config.py               # Configuration
```

## Getting Started

### Prerequisites
- Python 3.8+
- Ollama server running at `http://192.168.99.113:11434`
- Camera and microphone access
- Speaker output capability

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure as needed
4. Run the agent: `python agent_server.py` or `python -m agent.main`

### Configuration
The agent uses environment variables for configuration. See `.env.example` for all available options.

### Operation Modes
- **Web Server**: `python agent_server.py`
- **Interactive CLI**: `python -m agent.main --mode interactive`
- **Autonomous**: `python -m agent.main --mode autonomous`
- **Heartbeat**: `python -m agent.main --mode heartbeat`

## Security Framework

The security framework uses an LLM to evaluate all code modification requests:
1. Agent proposes file operation
2. File interceptor captures request
3. Security agent queries LLM for risk assessment
4. LLM provides approval/denial with reasoning
5. If approved, operation proceeds
6. All decisions logged for audit

## Development Guidelines

### Adding New Actions
1. Add action type to `execute_action` in `agent/runner.py`
2. Implement security checks if needed
3. Add to system prompt documentation

### Adding New Sensors
1. Create new module in `perception/`
2. Add to `AgentLoop` initialization
3. Add callback handlers
4. Update system prompt

### Adding New Tools
1. Add to `AgentRunner` tool execution
2. Implement security interception if needed
3. Add to system prompt for LLM awareness

## Testing

Run the test suite:
```bash
# Run all tests
python tests/run_tests.py

# Run individual tests
python tests/test_setup.py        # Setup verification
python tests/test_senses.py        # Hardware senses test
python tests/check_models.py       # Model availability check
python tests/verify_config_models.py  # Config verification
```

See `tests/README.md` for complete test documentation.

## Documentation

- `AGENT_ARCHITECTURE.md`: Detailed architecture documentation
- `SECURITY.md`: Security framework documentation
- `SELF_IMPROVEMENT.md`: Self-improvement guidelines
- `USAGE.md`: Usage instructions
- `CONFIGURATION.md`: Configuration options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.