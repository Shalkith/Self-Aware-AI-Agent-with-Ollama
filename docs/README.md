# Self-Aware AI Agent Documentation

This folder contains comprehensive documentation for the Self-Aware AI Agent project.

## Documentation Files

| File | Description |
|------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Detailed architecture and design patterns |
| [CONFIGURATION.md](CONFIGURATION.md) | Configuration options and environment variables |
| [SECURITY.md](SECURITY.md) | Security framework and LLM-based protection |
| [SELF_IMPROVEMENT.md](SELF_IMPROVEMENT.md) | Guidelines for safe self-improvement |
| [USAGE.md](USAGE.md) | Usage instructions and operation modes |

## Quick Start

See the main [README.md](../README.md) in the project root for quick start instructions.

## Key Concepts

### LLM-Based Security Framework
The agent uses a separate LLM to evaluate all code modification requests. See [SECURITY.md](SECURITY.md) for details.

### Nanobot-Style Architecture
The agent follows a modular architecture with an agent loop pattern. See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

### Multi-Model Support
The agent uses multiple specialized models for different tasks:
- **Thinking**: llama3 (autonomous reflection)
- **Vision**: llava (image analysis)
- **Conversation**: llama3 (user interaction)
- **Reasoning**: mistral (problem solving)
- **Security**: llama3 (security evaluation)

See [CONFIGURATION.md](CONFIGURATION.md) to customize model selection.
