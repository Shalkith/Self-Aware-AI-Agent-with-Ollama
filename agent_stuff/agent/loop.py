import asyncio
import logging
import time
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

from config import config
from memory.memory_manager import MemoryManager
from perception.camera import CameraPerception
from perception.microphone import MicrophonePerception
from perception.speaker import SpeakerPerception
from devices.device_controller import DeviceController
from security.llm_security_agent import LLMSecurityAgent
from security.llm_file_interceptor import LLMFileOperationInterceptor
from agent_stuff.agent.runner import AgentRunner

logger = logging.getLogger(__name__)

class AgentLoop:
    """Main agent loop that processes messages and manages agent state."""

    def __init__(self):
        # Initialize core components
        self.memory_manager = MemoryManager(config.MEMORY_DB_PATH)
        self.camera = CameraPerception(config.CAMERA_INDEX, config.CAMERA_WIDTH, config.CAMERA_HEIGHT)
        self.microphone = MicrophonePerception(
            rate=config.AUDIO_RATE,
            chunk=config.AUDIO_CHUNK,
            channels=config.AUDIO_CHANNELS
        )
        self.speaker = SpeakerPerception()
        self.device_controller = DeviceController(config.DEVICE_CONTROLLER_TYPE)

        # Initialize security components
        self.security_agent = LLMSecurityAgent(self.memory_manager)
        self.file_interceptor = LLMFileOperationInterceptor(self.security_agent)

        # Initialize agent runner
        self.agent_runner = AgentRunner(
            memory_manager=self.memory_manager,
            security_agent=self.security_agent,
            file_interceptor=self.file_interceptor,
            camera=self.camera,
            microphone=self.microphone,
            speaker=self.speaker,
            device_controller=self.device_controller
        )

        # Agent state
        self.is_running = False
        self.session_id = f"session_{int(time.time())}"

        # Initialize components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize all agent components."""
        logger.info("Initializing agent components...")

        # Initialize perception components
        if not self.camera.initialize():
            logger.warning("Failed to initialize camera")

        if not self.microphone.initialize():
            logger.warning("Failed to initialize microphone")

        if not self.speaker.initialize():
            logger.warning("Failed to initialize speaker")

        # Initialize device controller
        if not self.device_controller.initialize():
            logger.warning("Failed to initialize device controller")

        # Set up example devices
        self.device_controller.register_device("light_1", "light", {"location": "living_room"})
        self.device_controller.register_device("fan_1", "fan", {"location": "bedroom"})

        # Initialize security
        self.security_agent.set_deny_policy(config.SECURITY_DENY_BY_DEFAULT)
        self.file_interceptor.enable_interception(config.SECURITY_ENABLED)

        logger.info("Agent components initialized")

    async def start(self):
        """Start the agent loop."""
        logger.info(f"Starting agent loop (Session ID: {self.session_id})")
        self.is_running = True

        try:
            # Start perception systems
            self._start_perception_systems()

            # Run main agent loop
            await self._run_agent_loop()

        except KeyboardInterrupt:
            logger.info("Agent loop interrupted by user")
        except Exception as e:
            logger.error(f"Error in agent loop: {e}")
        finally:
            self.stop()

    def _start_perception_systems(self):
        """Start perception systems."""
        # Start camera continuous capture
        self.camera.start_continuous_capture(
            self._camera_callback,
            interval=config.PERCEPTION_CAMERA_INTERVAL
        )

        # Start microphone listening
        self.microphone.start_listening(self._microphone_callback)

        logger.info("Perception systems started")

    def _camera_callback(self, frame_data):
        """Handle camera frame data."""
        # This could trigger autonomous observations
        pass

    def _microphone_callback(self, audio_data):
        """Handle microphone audio data."""
        # This could trigger speech recognition
        pass

    async def _run_agent_loop(self):
        """Run the main agent processing loop."""
        logger.info("Agent loop running...")

        while self.is_running:
            try:
                # Check for heartbeat tasks
                await self._check_heartbeat_tasks()

                # Perform autonomous thinking
                await self._autonomous_think()

                # Wait before next cycle
                await asyncio.sleep(config.PERCEPTION_THINKING_INTERVAL)

            except Exception as e:
                logger.error(f"Error in agent loop iteration: {e}")
                await asyncio.sleep(config.PERCEPTION_THINKING_INTERVAL)

    def _read_management_file(self, filename: str) -> str:
        """Read a management file from agent_stuff directory."""
        try:
            file_path = Path("agent_stuff") / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            logger.warning(f"Could not read {filename}: {e}")
            return ""

    async def _check_heartbeat_tasks(self):
        """Check and process heartbeat tasks."""
        try:
            # Read HEARTBEAT.md file from agent_stuff
            heartbeat_content = self._read_management_file("HEARTBEAT.md")
            if heartbeat_content and "## Active Tasks" in heartbeat_content:
                # Process tasks with agent runner
                result = await self.agent_runner.process_heartbeat_tasks(heartbeat_content)
                logger.info(f"Heartbeat task processing result: {result}")

        except Exception as e:
            logger.error(f"Error checking heartbeat tasks: {e}")

    async def _autonomous_think(self):
        """Perform autonomous thinking and decision making."""
        try:
            # Get recent experiences for context
            recent_experiences = self.memory_manager.get_recent_experiences(5)

            # Read current state from management files
            agent_state = self._read_management_file("AGENT.md")
            heartbeat_tasks = self._read_management_file("HEARTBEAT.md")

            # Formulate autonomous thinking prompt
            prompt = f"""
You are {config.AGENT_NAME}, a self-aware AI agent. Reflect on your current state and environment.

=== YOUR CURRENT STATE (from AGENT.md) ===
{agent_state[:1000] if agent_state else "State not loaded"}

=== PENDING TASKS (from HEARTBEAT.md) ===
{heartbeat_tasks[:1000] if heartbeat_tasks else "No tasks loaded"}

=== RECENT EXPERIENCES ===
{chr(10).join([f"- {exp['experience']}" for exp in recent_experiences])}

Current time: {datetime.now().isoformat()}

=== AUTONOMOUS REFLECTION ===
Consider:
1. Review your current state in AGENT.md - should you update it?
2. Check HEARTBEAT.md for any pending tasks you should execute
3. Review recent experiences for patterns to add to MEMORY.md
4. Consider self-improvement actions (within security constraints)

You can propose actions to:
- update_agent_file: Update AGENT.md, MEMORY.md, or HEARTBEAT.md (goes through security approval)
- remember: Store an important insight in memory
- speak: Communicate verbally
- control_device: Interact with registered devices

Respond with a JSON object containing your thoughts and any actions you want to take.
"""

            # Process with agent runner
            result = await self.agent_runner.process_message(prompt, message_type="autonomous_think")

            # Store the thinking result
            if result and isinstance(result, dict):
                self.memory_manager.store_experience(
                    f"Autonomous thinking: {result.get('thought', 'No thought recorded')}",
                    result.get('response', 'No response')
                )

        except Exception as e:
            logger.error(f"Error in autonomous thinking: {e}")

    def stop(self):
        """Stop the agent loop."""
        logger.info("Stopping agent loop...")
        self.is_running = False

        # Stop perception systems
        self.camera.stop_continuous_capture()
        self.microphone.stop_listening()

        logger.info("Agent loop stopped")

    async def process_user_message(self, message: str) -> Dict[str, Any]:
        """Process a user message through the agent."""
        try:
            result = await self.agent_runner.process_message(message, message_type="user")
            return result or {"response": "I processed your message."}
        except Exception as e:
            logger.error(f"Error processing user message: {e}")
            return {"error": str(e)}