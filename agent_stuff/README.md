# Agent Stuff - Self-Aware AI Agent Management Files

This folder contains the core agent management files that define the agent's identity, behavior, and operational guidelines.

## Management File System

| File | Purpose | Updated By |
|------|---------|------------|
| [AGENT.md](AGENT.md) | Current state and runtime configuration | Agent |
| [SOUL.md](SOUL.md) | Personality, values, and behavioral boundaries | Agent/User |
| [AGENTS.md](AGENTS.md) | Operational standards and security rules | Agent/User |
| [USER.md](USER.md) | Human user context and preferences | User |
| [MEMORY.md](MEMORY.md) | Long-term persistent knowledge | Agent |
| [TOOLS.md](TOOLS.md) | External tools and skills documentation | Agent/User |
| [HEARTBEAT.md](HEARTBEAT.md) | Proactive background tasks and schedules | Agent/User |
| [IDENTITY.md](IDENTITY.md) | Agent identity and role definition | Agent |

## Directory Structure

```
agent_stuff/
├── AGENT.md          # State and configuration
├── SOUL.md           # Character and personality
├── AGENTS.md         # Operational rules
├── USER.md           # User context
├── MEMORY.md         # Long-term memory
├── TOOLS.md          # Tools and skills
├── HEARTBEAT.md      # Background tasks
├── IDENTITY.md       # Identity definition
├── agent/            # Agent code modules
│   ├── __init__.py
│   ├── loop.py
│   ├── runner.py
│   └── main.py
└── memory/           # Daily journal logs
    └── YYYY-MM-DD.md
```

## File Purposes

### AGENT.md
Runtime state tracking. Updated by the agent to reflect:
- Current status (idle, active, error)
- Last actions taken
- Current thoughts
- Active capabilities
- System health

### SOUL.md
The agent's "character sheet". Defines:
- Core personality traits
- Communication style and voice
- Behavioral boundaries
- Self-improvement ethics
- Emotional simulation guidelines

### AGENTS.md
Rules of engagement. Specifies:
- Operational standards
- Data handling policies
- Multi-agent coordination
- Security constraints
- Error handling protocols

### USER.md
Human user context. Contains:
- User profile and goals
- Work style preferences
- Coding preferences
- Constraints and boundaries
- Learning preferences

### MEMORY.md
Long-term knowledge synthesis. Stores:
- Durable facts
- Permanent preferences
- Synthesized truths
- Experience patterns
- Cross-session knowledge

### TOOLS.md
External capabilities. Documents:
- Available skills
- Tool usage patterns
- Credential management
- API integrations
- Skill activation status

### HEARTBEAT.md
Proactive task management. Defines:
- Scheduled routines
- Background tasks
- Priority levels
- Cron-style schedules
- Autonomous behaviors

### IDENTITY.md
Who the agent is. Defines:
- Name and version
- Title and role
- Operational scope
- Core values
- Lifecycle stages

## Daily Journals

The `memory/` subdirectory contains daily journal files:
- Format: `YYYY-MM-DD.md`
- Captures raw interaction history
- Referenced for MEMORY.md synthesis
- Automatically managed

## Usage

These files are read by the agent to:
1. Understand its identity and role
2. Adapt to user preferences
3. Follow operational guidelines
4. Maintain persistent knowledge
5. Execute scheduled tasks

The agent may update these files (subject to security approval) to:
- Reflect current state (AGENT.md)
- Synthesize learnings (MEMORY.md)
- Update task status (HEARTBEAT.md)
- Refine self-understanding (SOUL.md, IDENTITY.md)

## Security Note

All modifications to these files go through the LLM-based security framework:
- Changes evaluated for safety
- Audit trail maintained
- Deny-by-default policy applies
- Critical files have additional protection
