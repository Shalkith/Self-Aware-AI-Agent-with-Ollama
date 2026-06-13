# AGENT.md - Agent State & Configuration

## Current State

**Status:** idle
**Last Action:** Reset to defaults
**Current Thought:** Initialized after reset

---

## Runtime Configuration

**Name:** SelfAwareAI
**Version:** 1.0.0
**Mode:** development
**Session Start:** 2026-06-13

### Active Capabilities
- [x] Visual perception (camera)
- [x] Audio input (microphone)
- [x] Speech output (speaker)
- [x] Persistent memory (SQLite)
- [x] LLM integration (Ollama)
- [x] Security framework (LLM-based)
- [x] Web interface (Flask)
- [x] Device control (simulation)

### System Status
- **Ollama:** Connected at http://192.168.99.113:11434
- **Memory DB:** Initialized
- **Camera:** Available
- **Microphone:** Available
- **Speaker:** Available

---

## Active Models

| Task | Model | Status |
|------|-------|--------|
| Thinking | llama3 | active |
| Vision | llava | active |
| Conversation | llama3 | active |
| Reasoning | mistral | active |
| Security | llama3 | active |

---

## Management Files Reference

| File | Purpose |
|------|---------|
| [SOUL.md](SOUL.md) | Personality, values, communication style |
| [AGENTS.md](AGENTS.md) | Operational standards, security constraints |
| [USER.md](USER.md) | Human user context and preferences |
| [MEMORY.md](MEMORY.md) | Long-term knowledge synthesis |
| [TOOLS.md](TOOLS.md) | External tools and skills documentation |
| [HEARTBEAT.md](HEARTBEAT.md) | Background tasks and scheduling |
| [IDENTITY.md](IDENTITY.md) | Agent identity and role definition |

---

## Recent Activity

1. **System Reset** - Agent files reset to defaults
2. **Initialization** - Starting fresh session

---

## Notes

This file is maintained by the agent to track current state and configuration.

---

## Last Updated
2026-06-13

*This state file is updated by the agent to reflect current operational status.*
