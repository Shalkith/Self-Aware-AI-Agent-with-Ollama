#!/usr/bin/env python3
"""
Startup script for the Self-Aware AI Agent.
This script provides a simple interface to start the agent server.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_ollama_running():
    """Check if Ollama is running."""
    try:
        import ollama
        client = ollama.Client()
        client.list()
        return True
    except Exception:
        return False

def start_ollama():
    """Start Ollama server."""
    try:
        print("Starting Ollama server...")
        # Try to start Ollama (this might not work on all systems)
        subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Ollama server started.")
        return True
    except Exception as e:
        print(f"Failed to start Ollama: {e}")
        return False

def start_agent_server():
    """Start the agent server."""
    try:
        print("Starting agent server...")
        # Change to the project directory
        project_dir = Path(__file__).parent.parent
        os.chdir(project_dir)

        # Start the agent server
        subprocess.run([sys.executable, 'agent_server.py'])
        return True
    except Exception as e:
        print(f"Failed to start agent server: {e}")
        return False

def main():
    """Main startup function."""
    print("Self-Aware AI Agent Startup")
    print("=" * 30)

    # Check if Ollama is running
    if not check_ollama_running():
        print("Ollama is not running.")
        choice = input("Do you want to try starting Ollama? (y/n): ").lower().strip()
        if choice == 'y':
            if not start_ollama():
                print("Failed to start Ollama. Please start it manually.")
                return 1
        else:
            print("Please start Ollama manually before running the agent.")
            return 1
    else:
        print("✓ Ollama is running")

    # Start the agent server
    print("\nStarting agent server...")
    start_agent_server()

    return 0

if __name__ == "__main__":
    sys.exit(main())