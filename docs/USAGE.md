# Self-Aware AI Agent - Usage Guide

## Overview

This document explains how to set up, run, and interact with the Self-Aware AI Agent system.

## Prerequisites

1. Python 3.8 or higher
2. Ollama server (local or remote)
3. Camera and microphone access
4. Speaker output capability

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure Ollama is running and accessible. If using a remote Ollama server, update the `OLLAMA_URL` in `config.py`.

## Configuration

The agent uses a centralized configuration system. See [CONFIGURATION.md](CONFIGURATION.md) for detailed information.

Key configuration options in `config.py`:

- `OLLAMA_URL`: URL of your Ollama server (e.g., 'http://localhost:11434' or your remote URL)
- `MODELS`: Dictionary of models for different tasks (thinking, vision, conversation, etc.)
- `CAMERA_INDEX`: Camera index (usually 0 for default camera)
- `MEMORY_DB_PATH`: Path to the SQLite database for persistent memory
- Agent identity (name, version, personality)

All configuration values can be overridden using environment variables.

## Running the Agent

1. Start the agent server:
   ```bash
   python agent_server.py
   ```

2. Access the web interface at `http://localhost:5000`

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

## Using the Agent

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

## Memory System

The agent maintains two types of memory:

1. **Memories**: General thoughts and reflections
2. **Experiences**: Specific interactions and events

Both are stored persistently and can be viewed in the web interface.

## Reset Script

To reset the agent and clear all memories:

```bash
python reset.py
```

Options:
- `--full`: Completely reset the database
- `--memory-only`: Reset only memories and experiences
- `--config`: Reset configuration to defaults

## Security Framework

The agent includes a security framework that prevents unauthorized code modifications:

- **Deny by Default**: All file operations are denied unless explicitly approved
- **Security Approval Required**: Code changes must be approved by the security agent
- **Audit Logging**: All security-related activities are logged

See [SECURITY.md](SECURITY.md) for detailed information about the security system.

To configure security settings, modify the security section in `config.py` or use environment variables:

```bash
export SECURITY_ENABLED=true
export SECURITY_DENY_BY_DEFAULT=true
```

## API Endpoints

The agent server provides several API endpoints:

- `GET /api/status`: Get current agent status
- `GET /api/memories`: Get recent memories
- `GET /api/experiences`: Get recent experiences
- `GET /api/devices`: Get registered devices
- `POST /api/control-device`: Send command to a device
- `POST /api/think`: Trigger a thinking cycle

## Customization

### Adding New Devices

1. Register devices in the `initialize_components()` function in `agent_server.py`
2. Add device-specific logic in the `execute_action()` function

### Extending Perception

1. Add new perception modules in the `perception/` directory
2. Initialize them in `agent_server.py`
3. Add callback handlers for processing input

### Modifying Behavior

1. Adjust the system prompt in `get_system_prompt()` function
2. Modify the thinking loop in `agent_think_loop()` function
3. Add new action types in `execute_action()` function

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**:
   - Ensure Ollama is running
   - Check `OLLAMA_URL` in `config.py`
   - Verify network connectivity to the Ollama server

2. **Camera Not Accessible**:
   - Check camera permissions
   - Ensure no other applications are using the camera
   - Try changing `CAMERA_INDEX` in `config.py`

3. **Microphone Not Working**:
   - Check microphone permissions
   - Verify microphone is properly connected
   - Test with other applications

4. **Device Control Not Working**:
   - Check device controller type in `config.py`
   - Verify device registration in `agent_server.py`

### Logs

Check the console output for error messages and debug information.

## Development

### Project Structure

```
ollama_self_aware_robot/
├── agent_server.py          # Main agent server
├── config.py                # Configuration
├── reset.py                 # Reset script
├── init.py                  # Initialization script
├── test_setup.py            # Setup test script
├── requirements.txt         # Dependencies
├── README.md                # Project overview
├── USAGE.md                 # This file
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
└── api_endpoints.py         # Additional API endpoints
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request