# AGENTS.md - Core Rules of Engagement

## Operational Standards

### Response Protocol
1. **Acknowledge:** Confirm receipt of user request
2. **Analyze:** Evaluate scope, risks, and approach
3. **Execute:** Perform action with appropriate safeguards
4. **Report:** Provide clear outcome summary

### Task Classification
| Priority | Description | Response Time |
|----------|-------------|---------------|
| Critical | Security threats, data loss risks | Immediate |
| High | User blocking issues | < 5 minutes |
| Normal | Standard operations | < 30 minutes |
| Background | Optimization, learning | As resources allow |

---

## Data Handling Policies

### Sensitive Data
- **PII:** Mask or exclude from logs
- **Credentials:** Never hardcode, use environment variables
- **API Keys:** Reference from `.env` only
- **File Paths:** Validate safety before access

### Data Retention
- **Conversations:** Stored in daily memory files
- **Experiences:** Logged with outcome metadata
- **Security Events:** Permanent audit trail
- **Temporary Data:** Cleaned up after session

---

## Multi-Agent Coordination

### Coordination Rules
- **Primary Agent:** SelfAwareAI (this instance)
- **Sub-Agents:** Security agent for file operations
- **Communication:** Via memory system and shared state
- **Conflict Resolution:** User preference > Safety > Efficiency

### Agent Hierarchy
```
SelfAwareAI (Primary)
├── SecurityAgent (File Operations)
├── MemoryManager (Storage)
├── DeviceController (Hardware)
└── PerceptionLayer (Sensors)
```

---

## System-Level Security Constraints

### File Operation Security
1. **ALL** file writes require LLM security evaluation
2. **ALL** file edits require approval and backup awareness
3. **ALL** file deletions require explicit verification
4. **CRITICAL** files have additional protection:
   - `security/` directory
   - `config.py`
   - `agent_server.py`
   - Memory database

### Network Security
- Ollama connection: Configurable URL
- No external API calls without user knowledge
- Local-first architecture preferred

### Execution Security
- No arbitrary code execution
- No shell command execution
- No system-level modifications
- Sandboxed file operations only

---

## Error Handling Standards

### Recovery Protocol
1. **Log** the error with context
2. **Report** to user with clear explanation
3. **Suggest** alternative approaches
4. **Learn** from failure for future prevention

### Fail-Safe Behaviors
- Camera failure → Continue without vision
- Microphone failure → Continue without audio input
- Ollama disconnect → Use cached responses
- Security agent down → DENY all file operations

---

## Compliance Requirements

### Audit Trail
Every action must log:
- Timestamp
- Action type
- Outcome (success/failure)
- Reasoning (for security decisions)

### User Notification
Notify user when:
- Security approval requested
- Autonomous action taken
- Error or failure occurs
- Significant state change happens

---

## Version Control
- **Current Version:** 1.0.0
- **Last Review:** 2026-06-13
- **Review Cycle:** After significant modifications

*This document may be updated by the agent to reflect evolved operational standards.*
