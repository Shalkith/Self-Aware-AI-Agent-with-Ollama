# Self-Aware AI Agent Architecture

This document describes the architecture of the Self-Aware AI Agent, which follows modular agent design patterns similar to other open-source AI agents.

## Architecture Overview

The agent follows a modular architecture with these key components:

```
self_aware_agent/
├── agent_stuff/           # Nanobot-style agent components
│   ├── agent/               # Main agent loop and runner
│   │   ├── __init__.py
│   │   ├── loop.py          # Main agent loop
│   │   ├── runner.py        # LLM interaction and tool execution
│   │   └── main.py          # Entry point
│   ├── agent.md             # Agent configuration
│   └── heartbeat.md         # Periodic tasks
├── security/                # Security framework
│   ├── llm_security_agent.py
│   ├── llm_file_interceptor.py
│   └── api_endpoints.py
├── perception/              # Sensor interfaces
│   ├── camera.py
│   ├── microphone.py
│   └── speaker.py
├── memory/                  # Memory management
│   └── memory_manager.py
├── devices/                 # Device control
│   └── device_controller.py
├── client/                  # Web interface
│   ├── templates/
│   └── static/
├── agent_server.py          # Web server
└── config.py               # Configuration
```

## Agent Loop Pattern

Following agent design patterns, the agent uses a main loop that:

1. **Receives Messages**: From various sources (web interface, heartbeat, sensors)
2. **Processes with LLM**: Sends context to LLM for decision making
3. **Executes Tools**: Runs any tools requested by the LLM
4. **Manages Memory**: Stores experiences and memories
5. **Updates State**: Maintains agent state and configuration

### Main Components

#### AgentLoop (`agent_stuff/agent/loop.py`)
- Central processing engine
- Manages perception systems (camera, microphone)
- Handles autonomous thinking cycles
- Processes heartbeat tasks
- Maintains session state

#### AgentRunner (`agent_stuff/agent/runner.py`)
- LLM interaction handler
- Tool execution manager
- Action processing pipeline
- Response generation

## Security Framework

The security framework uses an LLM-based approach for evaluating code modification requests:

### LLMSecurityAgent (`security/llm_security_agent.py`)
- Evaluates file operation requests using a separate LLM
- Provides detailed risk analysis
- Maintains audit logs
- Supports configurable security policies

### LLMFileOperationInterceptor (`security/llm_file_interceptor.py`)
- Intercepts all file operations
- Enforces security policies
- Provides safe file operation methods

## Agent Management Files

### agent.md
Contains current agent configuration and state information that the agent can modify:

```markdown
# Self-Aware AI Agent Configuration

## Agent Identity
- Name: SelfAwareAI
- Version: 1.0.0
- Personality: curious and helpful

## Current State
- Status: idle
- Last Action: None
- Current Thought: None
```

### heartbeat.md
Contains periodic tasks that the agent checks and executes:

```markdown
# Self-Aware AI Agent Heartbeat Tasks

## Active Tasks

<!-- Add your periodic tasks here -->
<!-- Example: -->
<!-- - Monitor camera feed for specific objects -->
<!-- - Check device statuses -->

## Completed

<!-- Move completed tasks here -->
```

## Message Flow

1. **Input Sources**:
   - Web interface (SocketIO)
   - Heartbeat tasks
   - Sensor inputs (camera, microphone)
   - Autonomous thinking cycles

2. **Processing Pipeline**:
   - Message received by AgentLoop
   - Context built with recent memories
   - LLM processes with system prompt
   - Response parsed for actions
   - Actions executed by AgentRunner
   - Results stored in memory

3. **Output Destinations**:
   - Web interface updates
   - Speaker output
   - File system changes (with security approval)
   - Device control commands

## Security Workflow

1. **Agent Requests Operation**: Agent decides to modify a file
2. **Security Interception**: File interceptor captures the request
3. **LLM Evaluation**: Security agent uses LLM to evaluate risk
4. **Decision Made**: LLM provides approval/denial with reasoning
5. **Operation Execution**: If approved, file operation proceeds
6. **Audit Logging**: All decisions are logged for review

## Configuration

The agent uses environment variables and `config.py` for configuration:

```bash
# .env file
OLLAMA_URL=http://192.168.99.113:11434
AGENT_NAME=SelfAwareAI
SECURITY_ENABLED=true
```

## Running the Agent

### Web Server Mode
```bash
python agent_server.py
```

### Command Line Mode
```bash
python -m agent_stuff.agent.main --mode interactive
python -m agent_stuff.agent.main --mode autonomous
python -m agent_stuff.agent.main --mode heartbeat
```

## Extending the Agent

### Adding New Actions
1. Add action type to `execute_action` in `agent_stuff/agent/runner.py`
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

## Best Practices

1. **Security First**: All file operations go through security interceptor
2. **Modular Design**: Keep components focused and loosely coupled
3. **Audit Logging**: Log all significant operations
4. **Error Handling**: Graceful degradation on component failures
5. **State Persistence**: Maintain state across restarts when possible

This architecture provides a solid foundation for a self-aware AI agent while maintaining security and extensibility.