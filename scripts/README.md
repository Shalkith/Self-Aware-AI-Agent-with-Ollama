# Self-Aware AI Agent Scripts

This folder contains utility scripts for the Self-Aware AI Agent.

## Available Scripts

### Startup Scripts

| Script | Description |
|--------|-------------|
| `start_agent.py` | Simple startup script that checks Ollama and starts the agent server |
| `start_agent_modern.py` | Interactive startup with multiple mode options (Web, CLI, Autonomous, Heartbeat) |
| `start_agent.bat` | Windows batch file for starting the agent |
| `start_agent_modern.bat` | Windows batch file with mode selection |

**Usage:**
```bash
# From project root
python scripts/start_agent.py
python scripts/start_agent_modern.py

# Or on Windows, run the batch files from scripts/ folder
scripts/start_agent.bat
```

### Utility Scripts

| Script | Description |
|--------|-------------|
| `init.py` | Initialization script - checks Python version, dependencies, and Ollama |
| `reset.py` | Reset script - clears agent memories and database |
| `reset_agent.bat` | Windows batch file for resetting the agent |
| `demonstrate_agent_usage.py` | Demonstration of agent self-improvement capabilities |

**Usage:**
```bash
# Initialize the environment
python scripts/init.py

# Reset agent memories
python scripts/reset.py

# Run demonstration
python scripts/demonstrate_agent_usage.py
```

## Quick Start

The easiest way to start the agent is directly:
```bash
python agent_server.py
```

Or use one of the startup scripts for additional features like dependency checking.
