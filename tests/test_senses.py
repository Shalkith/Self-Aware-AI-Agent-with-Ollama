#!/usr/bin/env python3
"""
Test script for the Self-Aware AI Agent's senses and components.
Tests camera, microphone, speaker, memory, and device controller.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
import time
import base64

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_camera():
    """Test camera perception."""
    print("\n" + "="*60)
    print("TESTING CAMERA PERCEPTION")
    print("="*60)

    try:
        from perception.camera import CameraPerception
        from config import config

        camera = CameraPerception(
            camera_index=config.CAMERA_INDEX,
            width=config.CAMERA_WIDTH,
            height=config.CAMERA_HEIGHT
        )

        print(f"  Camera index: {config.CAMERA_INDEX}")
        print(f"  Resolution: {config.CAMERA_WIDTH}x{config.CAMERA_HEIGHT}")

        # Initialize camera
        print("\n  Initializing camera...")
        if camera.initialize():
            print("  [PASS] Camera initialized successfully")
        else:
            print("  [FAIL] Failed to initialize camera")
            return False

        # Capture a frame
        print("\n  Capturing frame...")
        frame = camera.capture_frame()
        if frame:
            print(f"  [PASS] Frame captured successfully ({len(frame)} bytes)")

            # Test base64 encoding
            frame_b64 = camera.get_frame_base64()
            if frame_b64:
                print(f"  [PASS] Frame encoded to base64 ({len(frame_b64)} chars)")
            else:
                print("  [FAIL] Failed to encode frame to base64")
        else:
            print("  [FAIL] Failed to capture frame")
            return False

        # Release camera
        camera.release()
        print("  [PASS] Camera released")
        return True

    except Exception as e:
        print(f"  [FAIL] Camera test error: {e}")
        return False

def test_microphone():
    """Test microphone perception."""
    print("\n" + "="*60)
    print("TESTING MICROPHONE PERCEPTION")
    print("="*60)

    try:
        from perception.microphone import MicrophonePerception
        from config import config

        microphone = MicrophonePerception(
            rate=config.AUDIO_RATE,
            chunk=config.AUDIO_CHUNK,
            channels=config.AUDIO_CHANNELS
        )

        print(f"  Sample rate: {config.AUDIO_RATE} Hz")
        print(f"  Channels: {config.AUDIO_CHANNELS}")
        print(f"  Chunk size: {config.AUDIO_CHUNK}")

        # Initialize microphone
        print("\n  Initializing microphone...")
        if microphone.initialize():
            print("  [PASS] Microphone initialized successfully")
        else:
            print("  [FAIL] Failed to initialize microphone")
            return False

        # Test listening with a callback
        audio_data_received = []

        def audio_callback(data):
            audio_data_received.append(data)
            if len(audio_data_received) == 1:
                print(f"  [PASS] Audio data received ({len(data)} bytes)")

        print("\n  Starting microphone (listening for 2 seconds)...")
        microphone.start_listening(audio_callback)

        # Listen for 2 seconds
        time.sleep(2)

        # Stop listening
        microphone.stop_listening()
        print(f"  [PASS] Microphone stopped. Received {len(audio_data_received)} audio chunks")

        # Release microphone
        microphone.release()
        print("  [PASS] Microphone released")

        return len(audio_data_received) > 0

    except Exception as e:
        print(f"  [FAIL] Microphone test error: {e}")
        return False

def test_speaker():
    """Test speaker perception."""
    print("\n" + "="*60)
    print("TESTING SPEAKER PERCEPTION")
    print("="*60)

    try:
        from perception.speaker import SpeakerPerception

        speaker = SpeakerPerception()

        # Initialize speaker
        print("\n  Initializing speaker...")
        if speaker.initialize():
            print("  [PASS] Speaker initialized successfully")
        else:
            print("  [FAIL] Failed to initialize speaker")
            return False

        # Test speaking
        test_message = "Hello, I am the self-aware AI agent. My speaker is working."
        print(f"\n  Testing speech output...")
        print(f"  Message: '{test_message}'")

        speaker.speak(test_message)
        print("  [PASS] Speech synthesis completed")

        # Test async speaking
        print("\n  Testing async speech...")
        speaker.speak_async("This is an async speech test.")
        time.sleep(3)  # Wait for speech to complete
        print("  [PASS] Async speech completed")

        # Release speaker
        speaker.release()
        print("  [PASS] Speaker released")
        return True

    except Exception as e:
        print(f"  [FAIL] Speaker test error: {e}")
        return False

def test_memory_manager():
    """Test memory manager."""
    print("\n" + "="*60)
    print("TESTING MEMORY MANAGER")
    print("="*60)

    try:
        from memory.memory_manager import MemoryManager
        from config import config

        # Use a test database (relative to project root)
        project_root = Path(__file__).parent.parent
        test_db_path = project_root / "memory" / "test_senses.db"
        memory_manager = MemoryManager(str(test_db_path))
        print(f"  Database path: {test_db_path}")
        print("  [PASS] Memory manager initialized")

        # Test storing memory
        print("\n  Testing memory storage...")
        memory_manager.store_memory('test', 'This is a test memory', {'test': True})
        print("  [PASS] Memory stored")

        # Test retrieving memories
        memories = memory_manager.get_memories(limit=5)
        print(f"  [PASS] Retrieved {len(memories)} memories")

        # Test storing experience
        print("\n  Testing experience storage...")
        memory_manager.store_experience('Test experience', 'success', {'test': True})
        print("  [PASS] Experience stored")

        # Test retrieving experiences
        experiences = memory_manager.get_recent_experiences(limit=5)
        print(f"  [PASS] Retrieved {len(experiences)} experiences")

        # Test search
        print("\n  Testing memory search...")
        results = memory_manager.search_memories('test')
        print(f"  [PASS] Search returned {len(results)} results")

        # Test statistics
        print("\n  Testing memory statistics...")
        stats = memory_manager.get_memory_stats()
        print(f"  Memory count: {stats['memory_count']}")
        print(f"  Experience count: {stats['experience_count']}")
        print("  [PASS] Statistics retrieved")

        # Clean up test database
        print("\n  Cleaning up test database...")
        memory_manager.clear_memories()
        os.remove(str(test_db_path))
        print("  [PASS] Test database cleaned up")

        return True

    except Exception as e:
        print(f"  [FAIL] Memory manager test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_device_controller():
    """Test device controller."""
    print("\n" + "="*60)
    print("TESTING DEVICE CONTROLLER")
    print("="*60)

    try:
        from devices.device_controller import DeviceController

        # Test simulation mode
        print("\n  Testing simulation mode...")
        controller = DeviceController(controller_type='simulation')

        if controller.initialize():
            print("  [PASS] Device controller initialized (simulation mode)")
        else:
            print("  [FAIL] Failed to initialize device controller")
            return False

        # Register devices
        print("\n  Registering test devices...")
        controller.register_device('living_room_light', 'light', {'location': 'living_room'})
        controller.register_device('bedroom_fan', 'fan', {'location': 'bedroom'})
        print("  [PASS] Devices registered")

        # Get all devices
        devices = controller.get_all_devices()
        print(f"\n  Registered devices: {list(devices.keys())}")

        # Test commands
        print("\n  Testing device commands...")

        # Turn on light
        result = controller.send_command('living_room_light', 'turn_on')
        state = controller.get_device_state('living_room_light')
        print(f"  Living room light ON: {result}, State: {state}")

        # Turn off light
        result = controller.send_command('living_room_light', 'turn_off')
        state = controller.get_device_state('living_room_light')
        print(f"  Living room light OFF: {result}, State: {state}")

        # Toggle fan
        result = controller.send_command('bedroom_fan', 'toggle')
        state = controller.get_device_state('bedroom_fan')
        print(f"  Bedroom fan TOGGLE: {result}, State: {state}")

        print("  [PASS] Device commands executed")

        # Release controller
        controller.release()
        print("  [PASS] Device controller released")

        return True

    except Exception as e:
        print(f"  [FAIL] Device controller test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Test configuration."""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION")
    print("="*60)

    try:
        from config import config

        print(f"  Agent name: {config.AGENT_NAME}")
        print(f"  Agent version: {config.AGENT_VERSION}")
        print(f"  Agent personality: {config.AGENT_PERSONALITY}")
        print(f"  Ollama URL: {config.OLLAMA_URL}")
        print(f"\n  Models configured:")
        for model_type, model_name in config.MODELS.items():
            print(f"    - {model_type}: {model_name}")

        print(f"\n  Security enabled: {config.SECURITY_ENABLED}")
        print(f"  Deny by default: {config.SECURITY_DENY_BY_DEFAULT}")

        print("\n  [PASS] Configuration loaded successfully")
        return True

    except Exception as e:
        print(f"  [FAIL] Configuration test error: {e}")
        return False

def main():
    """Main test function."""
    print("\n" + "="*60)
    print("SELF-AWARE AI AGENT - SENSES TEST")
    print("="*60)
    print("\nThis will test all agent components:")
    print("  1. Configuration")
    print("  2. Camera (visual perception)")
    print("  3. Microphone (audio input)")
    print("  4. Speaker (audio output)")
    print("  5. Memory Manager")
    print("  6. Device Controller")
    print("\nMake sure your camera and microphone are connected.")
    print("You should hear a voice message during the speaker test.")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)

    results = {}

    # Run all tests
    results['config'] = test_config()
    results['memory'] = test_memory_manager()
    results['devices'] = test_device_controller()
    results['camera'] = test_camera()
    results['microphone'] = test_microphone()
    results['speaker'] = test_speaker()

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for component, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status} {component.capitalize()}")

    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    print(f"\n  Total: {total} | Passed: {passed} | Failed: {failed}")

    if all(results.values()):
        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("SOME TESTS FAILED")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
