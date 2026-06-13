#!/usr/bin/env python3
"""
Modern startup script for the Self-Aware AI Agent.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main startup function."""
    print("Self-Aware AI Agent - Modern Startup")
    print("=" * 40)

    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    print("Choose startup mode:")
    print("1. Web Server Mode (default)")
    print("2. Interactive CLI Mode")
    print("3. Autonomous Mode")
    print("4. Heartbeat Mode")

    choice = input("Enter choice (1-4, default=1): ").strip() or "1"

    if choice == "1":
        # Start web server
        print("Starting web server...")
        subprocess.run([sys.executable, 'agent_server.py'])

    elif choice == "2":
        # Start interactive CLI mode
        print("Starting interactive CLI mode...")
        subprocess.run([sys.executable, '-m', 'agent.main', '--mode', 'interactive'])

    elif choice == "3":
        # Start autonomous mode
        print("Starting autonomous mode...")
        subprocess.run([sys.executable, '-m', 'agent.main', '--mode', 'autonomous'])

    elif choice == "4":
        # Start heartbeat mode
        print("Starting heartbeat mode...")
        subprocess.run([sys.executable, '-m', 'agent.main', '--mode', 'heartbeat'])

    else:
        print("Invalid choice. Starting web server...")
        subprocess.run([sys.executable, 'agent_server.py'])

if __name__ == "__main__":
    main()