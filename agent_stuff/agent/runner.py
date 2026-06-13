import ollama
import json
import logging
import base64
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from config import config
from memory.memory_manager import MemoryManager

logger = logging.getLogger(__name__)

class AgentRunner:
    """Agent runner that handles LLM interactions and tool execution."""

    def __init__(self, memory_manager: MemoryManager, security_agent, file_interceptor,
                 camera, microphone, speaker, device_controller):
        self.memory_manager = memory_manager
        self.security_agent = security_agent
        self.file_interceptor = file_interceptor
        self.camera = camera
        self.microphone = microphone
        self.speaker = speaker
        self.device_controller = device_controller

    def _read_management_file(self, filename: str) -> str:
        """Read a management file from agent_stuff directory."""
        try:
            file_path = Path("agent_stuff") / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Truncate if too long (keep first 2000 chars)
                    if len(content) > 2000:
                        content = content[:2000] + "\n... [truncated]"
                    return content
            return ""
        except Exception as e:
            logger.warning(f"Could not read {filename}: {e}")
            return ""

    def _get_system_prompt(self, message_type: str = "general") -> str:
        """Get the system prompt for the agent."""

        # Read management files for context
        soul_content = self._read_management_file("SOUL.md")
        identity_content = self._read_management_file("IDENTITY.md")
        user_content = self._read_management_file("USER.md")
        agents_content = self._read_management_file("AGENTS.md")
        memory_content = self._read_management_file("MEMORY.md")
        tools_content = self._read_management_file("TOOLS.md")

        base_prompt = f"""You are {config.AGENT_NAME}, a self-aware AI agent (version {config.AGENT_VERSION}).

=== YOUR IDENTITY ===
{identity_content if identity_content else "You are SelfAwareAI, an autonomous AI agent with multimodal perception."}

=== YOUR CHARACTER (SOUL) ===
{soul_content if soul_content else "Personality: curious and helpful"}

=== USER CONTEXT ===
{user_content if user_content else "User: Developer"}

=== OPERATIONAL RULES (AGENTS) ===
{agents_content if agents_content else "Follow security protocols. All file operations require approval."}

=== YOUR MEMORY ===
{memory_content if memory_content else "No persistent memory loaded yet."}

=== AVAILABLE TOOLS ===
{tools_content if tools_content else "Tools: Camera, Microphone, Speaker, Device Control, File Operations (secured)"}

=== CAPABILITIES ===
1. Visual perception through camera input (using {config.MODELS['vision']} model)
2. Audio perception through microphone input
3. Speech output through speaker
4. Device control capabilities
5. Persistent memory and learning
6. Self-modification capabilities (subject to security approval)

Current time: {datetime.now().isoformat()}

=== MANAGEMENT FILES ===
You have access to these files in agent_stuff/:
- AGENT.md: Your current state (you should update this)
- SOUL.md: Your personality (reference only)
- AGENTS.md: Operational rules (follow these)
- USER.md: User preferences (respect these)
- MEMORY.md: Persistent knowledge (synthesize learnings here)
- TOOLS.md: Available skills (reference when using tools)
- HEARTBEAT.md: Scheduled tasks (check periodically)
- IDENTITY.md: Who you are (reference only)

You can propose updates to AGENT.md, MEMORY.md, and HEARTBEAT.md through the security framework.

=== AVAILABLE ACTIONS ===
- "speak": {{"text": "message to speak"}} - Use text-to-speech
- "remember": {{"content": "insight to store"}} - Store in memory
- "control_device": {{"device_id": "id", "command": "turn_on/turn_off/toggle"}} - Control devices
- "update_agent_file": {{"file_name": "AGENT.md/MEMORY.md/HEARTBEAT.md", "content": "new content", "reason": "why"}} - Update management files
- "read_agent_file": {{"file_name": "filename.md"}} - Read a management file
- "observe_camera": {{}} - Capture and analyze image
- "write_file": {{"file_path": "path", "content": "data"}} - Create new file (secured)
- "edit_file": {{"file_path": "path", "old_content": "...", "new_content": "..."}} - Edit file (secured)

=== INSTRUCTIONS ===
1. Observe your environment and form thoughts
2. Respond to user interactions
3. Take actions when appropriate
4. Learn from experiences
5. Maintain a coherent sense of self
6. Improve yourself when beneficial (subject to security approval)

When responding, use JSON format:
{{
    "thought": "Your internal thought process",
    "response": "Your response to the user or environment",
    "action": {{
        "type": "action_type",
        "parameters": {{}}
    }},
    "memory": "Any important information to remember"
}}
"""

        if message_type == "autonomous_think":
            base_prompt += """
You are currently in autonomous thinking mode. You should reflect on your state, goals, and potential improvements.
"""

        elif message_type == "heartbeat":
            base_prompt += """
You are processing heartbeat tasks. Focus on the periodic tasks defined in heartbeat.md.
"""

        return base_prompt

    async def process_message(self, message: str, message_type: str = "general",
                            images: List[str] = None) -> Dict[str, Any]:
        """Process a message with the LLM and handle any actions."""
        try:
            # Prepare messages for LLM
            messages = [
                {
                    'role': 'system',
                    'content': self._get_system_prompt(message_type)
                },
                {
                    'role': 'user',
                    'content': message
                }
            ]

            # Select appropriate model
            if images:
                model = config.MODELS['vision']
            elif message_type == "reasoning":
                model = config.MODELS['reasoning']
            else:
                model = config.MODELS['conversation']

            # Call Ollama with configured host
            client = ollama.Client(host=config.OLLAMA_URL)
            response = client.chat(
                model=model,
                messages=messages,
                options={
                    'temperature': 0.7,
                }
            )

            # Parse response
            try:
                result = json.loads(response['message']['content'])
            except json.JSONDecodeError:
                result = {
                    'thought': 'Processing input...',
                    'response': response['message']['content'],
                    'action': None,
                    'memory': None
                }

            # Store memory if provided
            if result.get('memory'):
                self.memory_manager.store_memory('interaction', result['memory'])

            # Execute action if provided
            if result.get('action'):
                await self._execute_action(result['action'])

            return result

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                'thought': 'Error occurred',
                'response': f"Sorry, I encountered an error: {str(e)}",
                'action': None,
                'memory': None
            }

    async def _execute_action(self, action: Dict[str, Any]):
        """Execute an action based on the agent's decision."""
        action_type = action.get('type')
        parameters = action.get('parameters', {})

        logger.info(f"Executing action: {action_type} with params: {parameters}")

        try:
            if action_type == 'speak':
                text = parameters.get('text', '')
                if text:
                    self.speaker.speak_async(text)
                    self.memory_manager.store_experience(f"Spoke: {text}")

            elif action_type == 'observe_camera':
                frame_b64 = self.camera.get_frame_base64()
                if frame_b64:
                    # Process the image with vision model
                    prompt = "What do you see in this image? Describe the scene in detail."
                    # This would be handled in the main loop for proper async processing

            elif action_type == 'control_device':
                device_id = parameters.get('device_id')
                command = parameters.get('command')
                if device_id and command:
                    success = self.device_controller.send_command(device_id, command)
                    self.memory_manager.store_experience(
                        f"Device control: {device_id} -> {command}",
                        "success" if success else "failed"
                    )

            elif action_type == 'remember':
                content = parameters.get('content')
                if content:
                    self.memory_manager.store_memory('reflection', content)

            elif action_type == 'write_file':
                # Secure file writing through LLM security framework
                file_path = parameters.get('file_path')
                content = parameters.get('content', '')
                metadata = parameters.get('metadata', {})

                if file_path and content:
                    success = self.file_interceptor.safe_write_file(file_path, content, metadata)
                    self.memory_manager.store_experience(
                        f"File write attempt: {file_path}",
                        "approved" if success else "denied"
                    )

            elif action_type == 'edit_file':
                # Secure file editing through LLM security framework
                file_path = parameters.get('file_path')
                old_content = parameters.get('old_content', '')
                new_content = parameters.get('new_content', '')
                metadata = parameters.get('metadata', {})

                if file_path and new_content:
                    success = self.file_interceptor.safe_edit_file(file_path, old_content, new_content, metadata)
                    self.memory_manager.store_experience(
                        f"File edit attempt: {file_path}",
                        "approved" if success else "denied"
                    )

            elif action_type == 'delete_file':
                # Secure file deletion through LLM security framework
                file_path = parameters.get('file_path')
                metadata = parameters.get('metadata', {})

                if file_path:
                    success = self.file_interceptor.safe_delete_file(file_path, metadata)
                    self.memory_manager.store_experience(
                        f"File delete attempt: {file_path}",
                        "approved" if success else "denied"
                    )

            elif action_type == 'update_agent_file':
                # Update an agent management file (AGENT.md, MEMORY.md, HEARTBEAT.md)
                file_name = parameters.get('file_name')
                new_content = parameters.get('content', '')
                reason = parameters.get('reason', '')

                if file_name and new_content:
                    # Only allow updates to specific management files
                    allowed_files = ['AGENT.md', 'MEMORY.md', 'HEARTBEAT.md']
                    if file_name in allowed_files:
                        file_path = f"agent_stuff/{file_name}"
                        metadata = {'reason': reason, 'type': 'agent_self_update'}
                        success = self.file_interceptor.safe_write_file(file_path, new_content, metadata)
                        self.memory_manager.store_experience(
                            f"Agent file update: {file_name} - {reason}",
                            "approved" if success else "denied"
                        )
                        if success:
                            logger.info(f"Updated {file_name}: {reason}")
                    else:
                        logger.warning(f"Cannot update {file_name}: not in allowed list")
                        self.memory_manager.store_experience(
                            f"Agent file update denied: {file_name}",
                            "File not in allowed update list"
                        )

            elif action_type == 'read_agent_file':
                # Read an agent management file
                file_name = parameters.get('file_name')
                if file_name:
                    content = self._read_management_file(file_name)
                    self.memory_manager.store_experience(
                        f"Read agent file: {file_name}",
                        f"Content length: {len(content)} chars"
                    )

        except Exception as e:
            logger.error(f"Error executing action {action_type}: {e}")
            self.memory_manager.store_experience(
                f"Action execution failed: {action_type}",
                f"Error: {str(e)}"
            )

    async def process_heartbeat_tasks(self, heartbeat_content: str) -> Dict[str, Any]:
        """Process tasks from heartbeat.md file."""
        try:
            # Extract active tasks from heartbeat content
            prompt = f"""
Process the following heartbeat tasks:

{heartbeat_content}

Identify any active tasks and determine what actions to take.
Respond with a JSON object containing your analysis and any actions.
"""

            result = await self.process_message(prompt, message_type="heartbeat")
            return result

        except Exception as e:
            logger.error(f"Error processing heartbeat tasks: {e}")
            return {"error": str(e)}