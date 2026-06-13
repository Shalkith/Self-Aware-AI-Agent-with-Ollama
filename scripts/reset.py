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

def reset_agent_files():
    """Reset agent management files to defaults."""
    try:
        agent_dir = Path("agent_stuff")

        # Reset agent.md
        agent_md_path = agent_dir / "agent.md"
        if agent_md_path.exists():
            agent_md_path.unlink()

        # Create default agent.md
        default_agent_md = """# Self-Aware AI Agent Configuration

This file contains the current configuration and state of the self-aware AI agent.

## Agent Identity
- Name: SelfAwareAI
- Version: 1.0.0
- Personality: curious and helpful

## Capabilities
- Visual perception through camera
- Audio perception through microphone
- Speech output through speaker
- Device control capabilities
- Persistent memory and learning

## Current State
- Status: idle
- Last Action: None
- Current Thought: None

## Configuration
- Ollama URL: http://192.168.99.113:11434
- Models:
  - Thinking: llama3
  - Vision: llava
  - Conversation: llama3
  - Reasoning: mistral
  - Creativity: llama3

## Security Settings
- Security Enabled: true
- Deny by Default: true

## Notes
This file can be modified by the agent itself for self-configuration.
The agent should update this file when its state or configuration changes.
"""
        agent_md_path.write_text(default_agent_md)
        print("[PASS] agent.md reset to default")

        # Reset heartbeat.md
        heartbeat_md_path = agent_dir / "heartbeat.md"
        if heartbeat_md_path.exists():
            heartbeat_md_path.unlink()

        # Create default heartbeat.md
        default_heartbeat_md = """# Self-Aware AI Agent Heartbeat Tasks

This file is checked periodically by the self-aware AI agent. Add tasks below that you want the agent to work on periodically.

## Active Tasks

<!-- Add your periodic tasks here -->
<!-- Example: -->
<!-- - Monitor camera feed for specific objects -->
<!-- - Check device statuses -->
<!-- - Review recent memories for patterns -->

## Completed

<!-- Move completed tasks here -->
<!-- Example: -->
<!-- - Analyzed user interaction patterns -->
<!-- - Optimized memory storage -->

---

*This file is automatically managed by the agent. The agent will check this file periodically and execute any active tasks listed above.*
"""
        heartbeat_md_path.write_text(default_heartbeat_md)
        print("[PASS] heartbeat.md reset to default")

        return True
    except Exception as e:
        print(f"[FAIL] Error resetting agent files: {e}")
        return False

def reset_config():
    """Reset configuration to defaults."""
    try:
        # This would reset any config files if they exist
        # For now, we just inform the user
        print("[INFO] Configuration reset not implemented (using defaults)")
        return True
    except Exception as e:
        print(f"[FAIL] Error resetting configuration: {e}")
        return False

def main():
    """Main reset function."""
    parser = argparse.ArgumentParser(description="Reset the Self-Aware AI Agent")
    parser.add_argument("--full", action="store_true",
                        help="Perform full reset (clear database file and agent files)")
    parser.add_argument("--memory-only", action="store_true",
                        help="Reset only memories and experiences")
    parser.add_argument("--agent-files-reset", action="store_true",
                        help="Reset agent management files only")
    parser.add_argument("--config", action="store_true",
                        help="Reset configuration to defaults")

    args = parser.parse_args()

    print("Self-Aware AI Agent Reset Script")
    print("=" * 40)

    if args.agent_files_reset:
        print("\nResetting agent management files...")
        success = reset_agent_files()
        if success:
            print("[PASS] Agent files reset completed successfully")
        else:
            print("[FAIL] Agent files reset failed")
            return 1

    elif args.full or not any([args.memory_only, args.config]):
        print("\nPerforming full reset...")
        success = reset_database()
        if success:
            print("[PASS] Database reset completed")
        else:
            print("[FAIL] Database reset failed")
            return 1

        # Reset agent files as part of full reset
        success = reset_agent_files()
        if success:
            print("[PASS] Agent files reset completed")
        else:
            print("[FAIL] Agent files reset failed")
            return 1

    if args.memory_only:
        print("\nResetting agent memory...")
        success = reset_agent_memory()
        if success:
            print("[PASS] Memory reset completed successfully")
        else:
            print("[FAIL] Memory reset failed")
            return 1

    if args.config:
        print("\nResetting configuration...")
        success = reset_config()
        if success:
            print("[PASS] Configuration reset completed")
        else:
            print("[FAIL] Configuration reset failed")
            return 1

    if not any([args.full, args.memory_only, args.config, args.agent_files_reset]):
        # Default behavior: clear memories only
        print("\nResetting agent memory (default)...")
        success = reset_agent_memory()
        if success:
            print("[PASS] Agent reset completed successfully")
        else:
            print("[FAIL] Agent reset failed")
            return 1

    print("\nReset operation completed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())