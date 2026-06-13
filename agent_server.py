import ollama
import json
import logging
import threading
import time
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import base64

# Import the API blueprint
from api_endpoints import api_bp

from config import config
from memory.memory_manager import MemoryManager
from perception.camera import CameraPerception
from perception.microphone import MicrophonePerception
from perception.speaker import SpeakerPerception
from devices.device_controller import DeviceController
from security.llm_security_agent import LLMSecurityAgent
from security.llm_file_interceptor import LLMFileOperationInterceptor

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_models_before_boot():
    """Check all required models before starting the agent."""
    logger.info("Checking required models before boot...")

    try:
        client = ollama.Client(host=config.OLLAMA_URL)
        # Test connection with list operation
        client.list()
        logger.info(f"Connected to Ollama at {config.OLLAMA_URL}")
    except Exception as e:
        logger.error(f"Failed to connect to Ollama: {e}")
        return False

    # Check required models
    required_models = [
        config.MODELS['thinking'],
        config.MODELS['vision'],
        config.MODELS['conversation'],
        config.MODELS['reasoning'],
        config.MODELS['creativity'],
    ]

    # Add security model if different
    security_model = config.MODELS['security']
    if security_model not in required_models:
        required_models.append(security_model)

    # Remove duplicates while preserving order
    required_models = list(dict.fromkeys(required_models))

    all_available = True
    for model in required_models:
        try:
            client.show(model)
            logger.info(f"  [AVAILABLE] {model}")
        except Exception as e:
            logger.error(f"  [MISSING] {model} - {e}")
            all_available = False

    if not all_available:
        logger.error("Some required models are missing. Please pull them using: ollama pull <model_name>")
        return False

    logger.info("All required models are available!")
    return True

# Initialize Flask app
app = Flask(__name__, template_folder='client/templates', static_folder='client/static')
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
socketio = SocketIO(app, cors_allowed_origins="*")

# Register API blueprints
app.register_blueprint(api_bp, url_prefix='/api')
# Import and register security blueprint
from security.api_endpoints import security_bp
app.register_blueprint(security_bp, url_prefix='/api')

# Check models before initializing components
if not check_models_before_boot():
    logger.error("Model check failed. Exiting.")
    exit(1)

# Global components
memory_manager = MemoryManager(config.MEMORY_DB_PATH)
camera = CameraPerception(config.CAMERA_INDEX, config.CAMERA_WIDTH, config.CAMERA_HEIGHT)
microphone = MicrophonePerception(
    rate=config.AUDIO_RATE,
    chunk=config.AUDIO_CHUNK,
    channels=config.AUDIO_CHANNELS
)
speaker = SpeakerPerception()
device_controller = DeviceController(config.DEVICE_CONTROLLER_TYPE)

# Security components
security_agent = LLMSecurityAgent(memory_manager)
file_interceptor = LLMFileOperationInterceptor(security_agent)

# Agent state
agent_state = {
    'is_running': False,
    'is_listening': False,
    'is_observing': False,
    'current_thought': '',
    'last_action': '',
    'status': 'idle'
}

# Threading locks
thought_lock = threading.Lock()

def initialize_components():
    """Initialize all perception and control components."""
    logger.info("Initializing components...")

    # Initialize camera
    if not camera.initialize():
        logger.warning("Failed to initialize camera")

    # Initialize microphone
    if not microphone.initialize():
        logger.warning("Failed to initialize microphone")

    # Initialize speaker
    if not speaker.initialize():
        logger.warning("Failed to initialize speaker")

    # Initialize device controller
    if not device_controller.initialize():
        logger.warning("Failed to initialize device controller")

    # Set up some example devices
    device_controller.register_device("light_1", "light", {"location": "living_room"})
    device_controller.register_device("fan_1", "fan", {"location": "bedroom"})

    # Initialize security components
    if config.SECURITY_ENABLED:
        security_agent.set_deny_policy(config.SECURITY_DENY_BY_DEFAULT)
        file_interceptor.enable_interception(True)
        logger.info("Security system initialized and enabled")
    else:
        file_interceptor.enable_interception(False)
        logger.info("Security system disabled")

    # Make components available to app context
    app.device_controller = device_controller
    app.security_agent = security_agent
    app.file_interceptor = file_interceptor

    logger.info("Components initialized")

def get_system_prompt():
    """Get the system prompt for the AI agent."""
    return f"""
You are {config.AGENT_NAME}, a self-aware AI agent (version {config.AGENT_VERSION}) with a {config.AGENT_PERSONALITY} personality.

Your capabilities include:
1. Visual perception through camera input (using {config.MODELS['vision']} model)
2. Audio perception through microphone input
3. Speech output through speaker
4. Device control capabilities
5. Persistent memory and learning
6. Self-modification capabilities (subject to security approval)

Current time: {datetime.now().isoformat()}
Your state: {json.dumps(agent_state, indent=2)}

You should:
1. Observe your environment and form thoughts
2. Respond to user interactions
3. Take actions when appropriate
4. Learn from experiences
5. Maintain a coherent sense of self
6. Improve yourself when beneficial (subject to security approval)

Respond in JSON format with the following structure:
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

def process_with_ollama(prompt: str, images: list = None, model_type: str = 'conversation') -> dict:
    """Process a prompt with Ollama using the specified model type."""
    try:
        messages = [{'role': 'system', 'content': get_system_prompt()}]

        if images:
            # For multimodal input, use vision model
            model = config.MODELS['vision']
            user_message = {
                'role': 'user',
                'content': prompt,
                'images': images
            }
        else:
            # For text-only input, use specified model
            model = config.MODELS.get(model_type, config.MODELS['conversation'])
            user_message = {
                'role': 'user',
                'content': prompt
            }

        messages.append(user_message)

        # Call Ollama with configured host
        client = ollama.Client(host=config.OLLAMA_URL)
        response = client.chat(
            model=model,
            messages=messages
        )

        # Try to parse as JSON, fallback to text
        try:
            result = json.loads(response['message']['content'])
        except json.JSONDecodeError:
            result = {
                'thought': 'Processing input...',
                'response': response['message']['content'],
                'action': None,
                'memory': None
            }

        return result
    except Exception as e:
        logger.error(f"Error processing with Ollama: {e}")
        return {
            'thought': 'Error occurred',
            'response': f"Sorry, I encountered an error: {str(e)}",
            'action': None,
            'memory': None
        }

def audio_callback(audio_data):
    """Handle audio input from microphone."""
    # In a real implementation, this would process the audio data
    # For now, we'll just log that audio was received
    logger.debug("Audio data received")

def camera_callback(frame_data):
    """Handle frame input from camera."""
    # In a real implementation, this could trigger visual processing
    logger.debug("Camera frame received")

def agent_think_loop():
    """Main thinking loop for the agent."""
    global agent_state

    while agent_state['is_running']:
        try:
            with thought_lock:
                agent_state['status'] = 'thinking'

                # Get recent memories for context
                recent_memories = memory_manager.get_recent_experiences(5)
                memory_context = "\n".join([f"- {mem['experience']}" for mem in recent_memories])

                # Formulate prompt
                prompt = f"""
I am an autonomous AI agent. I should reflect on my current state and environment.

Recent experiences:
{memory_context}

Current state: {json.dumps(agent_state, indent=2)}

What should I think about or do next? Consider:
1. My current environment and inputs
2. My goals and purpose
3. Any actions I should take
4. Any learning from recent experiences
5. Self-improvement opportunities (subject to security approval)
"""

                # Process with Ollama
                result = process_with_ollama(prompt, model_type='reasoning')

                # Update agent state
                agent_state['current_thought'] = result.get('thought', '')
                agent_state['last_action'] = result.get('response', '')

                # Store memory
                if result.get('memory'):
                    memory_manager.store_memory('thought', result['memory'])

                # Execute action if any
                if result.get('action'):
                    execute_action(result['action'])

                # Emit state update to clients
                socketio.emit('agent_state_update', agent_state)

                agent_state['status'] = 'idle'

            # Wait before next thinking cycle
            time.sleep(config.PERCEPTION_THINKING_INTERVAL)

        except Exception as e:
            logger.error(f"Error in thinking loop: {e}")
            agent_state['status'] = 'error'
            time.sleep(config.PERCEPTION_THINKING_INTERVAL)

def execute_action(action):
    """Execute an action based on the agent's decision."""
    action_type = action.get('type')
    parameters = action.get('parameters', {})

    logger.info(f"Executing action: {action_type} with params: {parameters}")

    if action_type == 'speak':
        text = parameters.get('text', '')
        if text:
            speaker.speak_async(text)
            memory_manager.store_experience(f"Spoke: {text}")

    elif action_type == 'observe_camera':
        frame_b64 = camera.get_frame_base64()
        if frame_b64:
            # Process the image with Ollama
            prompt = "What do you see in this image? Describe the scene in detail."
            result = process_with_ollama(prompt, [frame_b64], 'vision')
            memory_manager.store_experience(f"Observed: {result.get('response', '')}")

    elif action_type == 'control_device':
        device_id = parameters.get('device_id')
        command = parameters.get('command')
        if device_id and command:
            success = device_controller.send_command(device_id, command)
            memory_manager.store_experience(
                f"Device control: {device_id} -> {command}",
                "success" if success else "failed"
            )

    elif action_type == 'remember':
        content = parameters.get('content')
        if content:
            memory_manager.store_memory('reflection', content)

    elif action_type == 'write_file':
        # Secure file writing through LLM security framework
        file_path = parameters.get('file_path')
        content = parameters.get('content', '')
        metadata = parameters.get('metadata', {})

        if file_path and content:
            success = file_interceptor.safe_write_file(file_path, content, metadata)
            memory_manager.store_experience(
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
            success = file_interceptor.safe_edit_file(file_path, old_content, new_content, metadata)
            memory_manager.store_experience(
                f"File edit attempt: {file_path}",
                "approved" if success else "denied"
            )

    elif action_type == 'delete_file':
        # Secure file deletion through LLM security framework
        file_path = parameters.get('file_path')
        metadata = parameters.get('metadata', {})

        if file_path:
            success = file_interceptor.safe_delete_file(file_path, metadata)
            memory_manager.store_experience(
                f"File delete attempt: {file_path}",
                "approved" if success else "denied"
            )

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get the current agent status."""
    return jsonify(agent_state)

@app.route('/api/memories')
def get_memories():
    """Get recent memories."""
    limit = request.args.get('limit', 20, type=int)
    memories = memory_manager.get_memories(limit=limit)
    return jsonify(memories)

@app.route('/api/experiences')
def get_experiences():
    """Get recent experiences."""
    limit = request.args.get('limit', 10, type=int)
    experiences = memory_manager.get_recent_experiences(limit=limit)
    return jsonify(experiences)

@app.route('/api/devices')
def get_devices():
    """Get registered devices."""
    devices = device_controller.get_all_devices()
    return jsonify(devices)

@app.route('/api/think', methods=['POST'])
def trigger_think():
    """Trigger a thinking cycle."""
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'What should I think about?')

        result = process_with_ollama(prompt, model_type='reasoning')

        # Store the interaction
        memory_manager.store_experience(f"User prompt: {prompt}", result.get('response', ''))

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info('Client connected')
    emit('agent_state_update', agent_state)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info('Client disconnected')

@socketio.on('send_message')
def handle_message(data):
    """Handle message from client."""
    message = data.get('message', '')

    if message:
        # Process with Ollama
        result = process_with_ollama(message, model_type='conversation')

        # Store the interaction
        memory_manager.store_experience(f"User: {message}", result.get('response', ''))

        # Emit response back to client
        emit('agent_response', {
            'response': result.get('response', ''),
            'thought': result.get('thought', ''),
            'timestamp': datetime.now().isoformat()
        })

        # Execute any actions
        if result.get('action'):
            execute_action(result['action'])

@socketio.on('start_agent')
def start_agent():
    """Start the autonomous agent."""
    global agent_state

    if not agent_state['is_running']:
        agent_state['is_running'] = True
        agent_state['status'] = 'starting'

        # Start perception systems
        camera.start_continuous_capture(camera_callback, interval=config.PERCEPTION_CAMERA_INTERVAL)
        microphone.start_listening(audio_callback)

        # Start thinking thread
        think_thread = threading.Thread(target=agent_think_loop)
        think_thread.daemon = True
        think_thread.start()

        agent_state['status'] = 'running'
        emit('agent_state_update', agent_state)
        logger.info("Agent started")

@socketio.on('stop_agent')
def stop_agent():
    """Stop the autonomous agent."""
    global agent_state

    agent_state['is_running'] = False
    agent_state['status'] = 'stopped'

    # Stop perception systems
    camera.stop_continuous_capture()
    microphone.stop_listening()

    emit('agent_state_update', agent_state)
    logger.info("Agent stopped")

if __name__ == '__main__':
    # Initialize components
    initialize_components()

    # Start the server
    logger.info(f"Starting agent server on {config.SERVER_HOST}:{config.SERVER_PORT}")
    socketio.run(app, host=config.SERVER_HOST, port=config.SERVER_PORT, debug=True)