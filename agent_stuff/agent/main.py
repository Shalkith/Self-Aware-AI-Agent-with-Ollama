#!/usr/bin/env python3
"""
Main entry point for the Self-Aware AI Agent.
"""

import asyncio
import logging
import argparse
from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agent_stuff.agent.loop import AgentLoop
from config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE) if config.LOG_FILE else logging.StreamHandler(),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main async function to run the agent."""
    parser = argparse.ArgumentParser(description="Self-Aware AI Agent")
    parser.add_argument("--mode", choices=["interactive", "autonomous", "heartbeat"],
                       default="autonomous", help="Agent mode")
    parser.add_argument("--heartbeat-interval", type=int, default=1800,
                       help="Heartbeat check interval in seconds (default: 1800)")

    args = parser.parse_args()

    logger.info(f"Starting Self-Aware AI Agent (Mode: {args.mode})")
    logger.info(f"Ollama URL: {config.OLLAMA_URL}")
    logger.info(f"Agent Name: {config.AGENT_NAME}")

    # Create and start agent loop
    agent_loop = AgentLoop()

    try:
        if args.mode == "interactive":
            # Interactive mode - process user input
            await run_interactive_mode(agent_loop)
        elif args.mode == "heartbeat":
            # Heartbeat mode - focus on periodic tasks
            await run_heartbeat_mode(agent_loop, args.heartbeat_interval)
        else:
            # Autonomous mode - full agent operation
            await agent_loop.start()

    except KeyboardInterrupt:
        logger.info("Agent stopped by user")
    except Exception as e:
        logger.error(f"Agent error: {e}")
    finally:
        agent_loop.stop()

async def run_interactive_mode(agent_loop):
    """Run agent in interactive mode."""
    logger.info("Running in interactive mode. Type 'quit' to exit.")

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            if user_input.strip():
                result = await agent_loop.process_user_message(user_input)
                print(f"\nAgent: {result.get('response', 'No response')}")

        except KeyboardInterrupt:
            break
        except EOFError:
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")

async def run_heartbeat_mode(agent_loop, interval):
    """Run agent in heartbeat mode."""
    logger.info(f"Running in heartbeat mode (interval: {interval}s)")

    while True:
        try:
            await agent_loop._check_heartbeat_tasks()
            await asyncio.sleep(interval)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Error in heartbeat mode: {e}")
            await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())