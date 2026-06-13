#!/usr/bin/env python3
"""
Reset script for the Self-Aware AI Agent.
This script clears all memories and resets the agent to its initial state.
"""

import os
import sys
import sqlite3
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import config
from memory.memory_manager import MemoryManager


def reset_agent_memory():
    """Reset all agent memories and experiences."""
    try:
        # Initialize memory manager
        memory_manager = MemoryManager(config.MEMORY_DB_PATH)

        # Clear all memories and experiences
        memory_manager.clear_memories()

        print("[PASS] Agent memory cleared successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Error clearing agent memory: {e}")
        return False


def reset_database():
    """Completely reset the database file."""
    try:
        if os.path.exists(config.MEMORY_DB_PATH):
            os.remove(config.MEMORY_DB_PATH)
            print("[PASS] Database file deleted")
        else:
            print("[INFO] No existing database file found")

        # Reinitialize the database
        memory_manager = MemoryManager(config.MEMORY_DB_PATH)
        print("[PASS] Database reinitialized")
        return True
    except Exception as e:
        print(f"[FAIL] Error resetting database: {e}")
        return False


def reset_daily_journals():
    """Reset daily journal files in agent_stuff/memory/."""
    try:
        agent_dir = Path("agent_stuff")
        memory_dir = agent_dir / "memory"

        if memory_dir.exists():
            # Count journal files
            journal_files = list(memory_dir.glob("*.md"))
            if journal_files:
                for journal_file in journal_files:
                    journal_file.unlink()
                print(f"[PASS] Cleared {len(journal_files)} daily journal(s)")
            else:
                print("[INFO] No daily journals to clear")

            # Create today's journal
            today = datetime.now().strftime("%Y-%m-%d")
            today_journal = memory_dir / f"{today}.md"
            default_journal = f"""# Daily Journal - {today}

## Session Start
- **Time:** {datetime.now().strftime("%H:%M")} UTC
- **Status:** Session initialized after reset

## Activities
<!-- Agent will log activities here -->

## Notes
<!-- Session notes and observations -->

---

*Daily journal created after reset.*
"""
            today_journal.write_text(default_journal)
            print(f"[PASS] Created new journal for {today}")

        return True
    except Exception as e:
        print(f"[FAIL] Error resetting daily journals: {e}")
        return False


def reset_agent_files():
    """Reset agent management files to defaults."""
    try:
        agent_dir = Path("agent_stuff")

        if not agent_dir.exists():
            print("[FAIL] agent_stuff directory not found")
            return False

        # Reset AGENT.md (runtime state)
        agent_md_path = agent_dir / "AGENT.md"
        default_agent_md = """# AGENT.md - Agent State & Configuration

## Current State

**Status:** idle
**Last Action:** Reset to defaults
**Current Thought:** Initialized after reset

---

## Runtime Configuration

**Name:** SelfAwareAI
**Version:** 1.0.0
**Mode:** development
**Session Start:** {date}

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
- **Ollama:** Connected at {ollama_url}
- **Memory DB:** Initialized
- **Camera:** Available
- **Microphone:** Available
- **Speaker:** Available

---

## Active Models

| Task | Model | Status |
|------|-------|--------|
| Thinking | {thinking_model} | active |
| Vision | {vision_model} | active |
| Conversation | {conversation_model} | active |
| Reasoning | {reasoning_model} | active |
| Security | {security_model} | active |

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
{date}

*This state file is updated by the agent to reflect current operational status.*
""".format(
            date=datetime.now().strftime("%Y-%m-%d"),
            ollama_url=config.OLLAMA_URL,
            thinking_model=config.MODELS['thinking'],
            vision_model=config.MODELS['vision'],
            conversation_model=config.MODELS['conversation'],
            reasoning_model=config.MODELS['reasoning'],
            security_model=config.MODELS['security']
        )
        agent_md_path.write_text(default_agent_md)
        print("[PASS] AGENT.md reset to default")

        # Reset SOUL.md (keep as-is, contains personality definition)
        soul_md_path = agent_dir / "SOUL.md"
        if soul_md_path.exists():
            print("[INFO] SOUL.md preserved (character definition)")
        else:
            print("[INFO] SOUL.md not found (will be created by agent if needed)")

        # Reset MEMORY.md (clear learned knowledge)
        memory_md_path = agent_dir / "MEMORY.md"
        default_memory_md = """# MEMORY.md - Long-Term Persistent Memory

## Durable Facts

### Project Facts
- **Project Name:** Self-Aware AI Agent with Ollama
- **Created:** {date}
- **Primary Language:** Python 3.11+
- **Architecture:** Modular agent-based system

### Technical Facts
- Ollama server configured in config.py
- Security framework uses LLM evaluation
- Memory stored in SQLite database

---

## Permanent Preferences

### System Preferences
- Deny-by-default security policy
- Log all file operations
- Maintain audit trails

---

## Synthesized Truths

*Knowledge will be synthesized here as the agent learns.*

---

## Experience Patterns

*Patterns will be identified and recorded here.*

---

## Persistent State

### Agent State
- Status: idle
- Session: {date}

---

## Cross-Session Knowledge

*Long-term knowledge accumulated across sessions.*

---

## Memory Maintenance

### Auto-Update Triggers
- User corrections
- Pattern emergence
- Structure changes
- Significant decisions

---

## Last Updated
{date}

*This memory file persists across sessions and informs agent behavior.*
""".format(date=datetime.now().strftime("%Y-%m-%d"))
        memory_md_path.write_text(default_memory_md)
        print("[PASS] MEMORY.md reset to default (learned knowledge cleared)")

        # Reset HEARTBEAT.md (clear completed tasks, keep structure)
        heartbeat_md_path = agent_dir / "HEARTBEAT.md"
        default_heartbeat_md = """# HEARTBEAT.md - Proactive Background Tasks

## Active Tasks

### Periodic Health Checks
- **Frequency:** Every 5 minutes
- **Action:** Check Ollama connection status
- **On Failure:** Log error, notify user

### Memory Maintenance
- **Frequency:** Every 30 minutes
- **Action:**
  - Summarize old experiences
  - Archive outdated temporary memories
  - Update MEMORY.md with synthesized learnings
- **On Completion:** Log statistics

### Log Rotation
- **Frequency:** Daily at midnight
- **Action:**
  - Rotate agent.log if > 10MB
  - Archive old logs to logs/archive/
  - Create new log file

### Device Status Polling
- **Frequency:** Every 60 seconds
- **Action:**
  - Check registered device states
  - Update device state cache
  - Detect offline devices

---

## Scheduled Routines

### Hourly Tasks
| Time | Task | Description |
|------|------|-------------|
| :00 | Experience Summary | Compile last hour's experiences |
| :00 | Security Log Review | Check for denied operations |

### Daily Tasks
| Time | Task | Description |
|------|------|-------------|
| 00:00 | Log Rotation | Rotate and archive logs |
| 00:00 | Memory Optimization | Vacuum SQLite database |
| 08:00 | Morning Report | Summarize overnight activity |
| 20:00 | Evening Summary | Daily experience synthesis |

### Weekly Tasks
| Day | Time | Task |
|-----|------|------|
| Sunday | 00:00 | Full memory backup |
| Sunday | 00:00 | Review and update MEMORY.md |

---

## Autonomous Behaviors

### When Idle
- Review recent memories for patterns
- Consider self-improvement opportunities
- Check heartbeat tasks for updates
- Update AGENT.md with current state

### On Event Triggers
- **Security Alert:** Immediate security log review
- **Device Offline:** Attempt reconnection
- **Memory Threshold:** Trigger memory optimization
- **Error Spike:** Analyze error patterns

---

## Task Priority Levels

1. **Critical** (Execute immediately)
   - Security violations
   - System errors
   - User emergency requests

2. **High** (Execute within 5 minutes)
   - Connection failures
   - Device malfunctions
   - Memory capacity warnings

3. **Normal** (Execute on schedule)
   - Regular health checks
   - Log maintenance
   - Experience summaries

4. **Low** (Execute when idle)
   - Pattern analysis
   - Self-improvement research
   - Archive cleanup

---

## Task Modification

To add new tasks:
1. Add to "Active Tasks" or "Scheduled Routines"
2. Specify frequency and action
3. Set priority level
4. Agent will pick up on next heartbeat cycle

To mark task complete:
- Move task from "Active Tasks" to "Completed Tasks" section
- Include completion date and outcome

---

## Completed Tasks

<!-- Move completed tasks here:

Example:
- [2026-06-13] Initial heartbeat system setup - COMPLETED
-->

---

## Last Updated
{date}

*This file is checked periodically by the agent. Tasks are executed based on schedule and priority.*
""".format(date=datetime.now().strftime("%Y-%m-%d"))
        heartbeat_md_path.write_text(default_heartbeat_md)
        print("[PASS] HEARTBEAT.md reset (completed tasks cleared)")

        # Preserve other management files (they contain definitions, not state)
        preserve_files = ["SOUL.md", "AGENTS.md", "USER.md", "TOOLS.md", "IDENTITY.md", "README.md"]
        for filename in preserve_files:
            file_path = agent_dir / filename
            if file_path.exists():
                print(f"[INFO] {filename} preserved (contains definitions)")
            else:
                print(f"[WARN] {filename} not found")

        # Reset daily journals
        reset_daily_journals()

        return True
    except Exception as e:
        print(f"[FAIL] Error resetting agent files: {e}")
        import traceback
        traceback.print_exc()
        return False


def reset_config():
    """Reset configuration to defaults."""
    try:
        # Configuration is handled via environment variables and config.py
        # We don't reset config.py itself as it contains code
        print("[INFO] Configuration reset:")
        print("  - Environment variables in .env preserved")
        print("  - config.py preserved (contains defaults)")
        print("  - To reset config, edit .env or config.py manually")
        return True
    except Exception as e:
        print(f"[FAIL] Error resetting configuration: {e}")
        return False


def list_reset_options():
    """Display available reset options."""
    print("\nAvailable Reset Options:")
    print("=" * 50)
    print("\n1. Default (no args): Clear agent memory only")
    print("   python scripts/reset.py")
    print("\n2. --full: Complete reset")
    print("   - Clears database")
    print("   - Resets AGENT.md (runtime state)")
    print("   - Resets MEMORY.md (learned knowledge)")
    print("   - Resets HEARTBEAT.md (completed tasks)")
    print("   - Clears daily journals")
    print("   - Preserves: SOUL.md, AGENTS.md, USER.md, TOOLS.md, IDENTITY.md")
    print("   python scripts/reset.py --full")
    print("\n3. --memory-only: Clear memories only")
    print("   python scripts/reset.py --memory-only")
    print("\n4. --agent-files-reset: Reset management files only")
    print("   python scripts/reset.py --agent-files-reset")
    print("\n5. --database: Reset database only")
    print("   python scripts/reset.py --database")
    print("\n6. --config: Show configuration reset info")
    print("   python scripts/reset.py --config")
    print("\n7. --list: Show this help message")
    print("   python scripts/reset.py --list")


def main():
    """Main reset function."""
    parser = argparse.ArgumentParser(
        description="Reset the Self-Aware AI Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/reset.py                    # Clear memories (default)
  python scripts/reset.py --full           # Complete reset
  python scripts/reset.py --memory-only    # Clear memories only
  python scripts/reset.py --list           # Show all options
        """
    )
    parser.add_argument("--full", action="store_true",
                        help="Perform full reset (database + agent files)")
    parser.add_argument("--memory-only", action="store_true",
                        help="Reset only memories and experiences")
    parser.add_argument("--agent-files-reset", action="store_true",
                        help="Reset agent management files only")
    parser.add_argument("--database", action="store_true",
                        help="Reset database only")
    parser.add_argument("--config", action="store_true",
                        help="Show configuration reset information")
    parser.add_argument("--list", action="store_true",
                        help="List all reset options")

    args = parser.parse_args()

    # Show list option
    if args.list:
        list_reset_options()
        return 0

    print("Self-Aware AI Agent Reset Script")
    print("=" * 50)

    # Show config info
    if args.config:
        return 0 if reset_config() else 1

    # Database-only reset
    if args.database:
        print("\nResetting database...")
        success = reset_database()
        if success:
            print("\n[PASS] Database reset completed successfully")
        else:
            print("\n[FAIL] Database reset failed")
        return 0 if success else 1

    # Agent files only reset
    if args.agent_files_reset:
        print("\nResetting agent management files...")
        success = reset_agent_files()
        if success:
            print("\n[PASS] Agent files reset completed successfully")
        else:
            print("\n[FAIL] Agent files reset failed")
        return 0 if success else 1

    # Memory only reset
    if args.memory_only:
        print("\nResetting agent memory...")
        success = reset_agent_memory()
        if success:
            print("\n[PASS] Memory reset completed successfully")
        else:
            print("\n[FAIL] Memory reset failed")
        return 0 if success else 1

    # Full reset
    if args.full:
        print("\nPerforming FULL reset...")
        print("This will:")
        print("  - Clear the database")
        print("  - Reset runtime state files")
        print("  - Clear daily journals")
        print("  - Preserve personality and tool definitions\n")

        success = reset_database()
        if not success:
            print("\n[FAIL] Database reset failed")
            return 1
        print()

        success = reset_agent_files()
        if not success:
            print("\n[FAIL] Agent files reset failed")
            return 1

        print("\n[PASS] Full reset completed successfully")
        print("\nNote: The following files were preserved:")
        print("  - SOUL.md (personality)")
        print("  - AGENTS.md (operational rules)")
        print("  - USER.md (user preferences)")
        print("  - TOOLS.md (skills documentation)")
        print("  - IDENTITY.md (agent identity)")
        return 0

    # Default: memory only
    if not any([args.full, args.memory_only, args.agent_files_reset, args.database, args.config]):
        print("\nResetting agent memory (default)...")
        print("Use --list to see all options\n")
        success = reset_agent_memory()
        if success:
            print("\n[PASS] Agent memory cleared successfully")
            print("\nNote: Management files not affected.")
            print("Use --full to reset everything or --agent-files-reset for files only.")
        else:
            print("\n[FAIL] Memory reset failed")
        return 0 if success else 1

    print("\nReset operation completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
