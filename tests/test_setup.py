#!/usr/bin/env python3
"""
Test script to verify the Self-Aware AI Agent setup.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test if all required modules can be imported."""
    modules = [
        'ollama',
        'flask',
        'flask_socketio',
        'cv2',
        'pyaudio',
        'pyttsx3',
        'gpiozero',
        'requests',
        'PIL',
        'numpy'
    ]

    print("Testing module imports...")
    all_passed = True

    for module in modules:
        try:
            __import__(module)
            print(f"  [PASS] {module}")
        except ImportError as e:
            print(f"  [FAIL] {module} - {e}")
            all_passed = False

    return all_passed

def test_local_modules():
    """Test if local modules can be imported."""
    local_modules = [
        'config',
        'memory.memory_manager',
        'perception.camera',
        'perception.microphone',
        'perception.speaker',
        'devices.device_controller',
        'security.llm_security_agent',
        'security.llm_file_interceptor',
        'agent_stuff.agent.loop',
        'agent_stuff.agent.runner'
    ]

    print("\nTesting local module imports...")
    all_passed = True

    for module in local_modules:
        try:
            __import__(module)
            print(f"  [PASS] {module}")
        except ImportError as e:
            print(f"  [FAIL] {module} - {e}")
            all_passed = False

    return all_passed

def test_memory_manager():
    """Test the memory manager."""
    try:
        from memory.memory_manager import MemoryManager
        memory_manager = MemoryManager()

        # Test storing a memory
        memory_manager.store_memory('test', 'This is a test memory')

        # Test retrieving memories
        memories = memory_manager.get_memories(limit=1)
        if len(memories) > 0:
            print("  [PASS] Memory storage and retrieval")
        else:
            print("  [FAIL] Memory storage failed")
            return False

        # Test clearing memories
        memory_manager.clear_memories()
        memories = memory_manager.get_memories()
        if len(memories) == 0:
            print("  [PASS] Memory clearing")
        else:
            print("  [FAIL] Memory clearing failed")
            return False

        return True
    except Exception as e:
        print(f"  [FAIL] Memory manager test failed: {e}")
        return False

def test_device_controller():
    """Test the device controller."""
    try:
        from devices.device_controller import DeviceController
        device_controller = DeviceController()

        # Test initialization
        if device_controller.initialize():
            print("  [PASS] Device controller initialization")
        else:
            print("  [FAIL] Device controller initialization failed")
            return False

        # Test device registration
        device_controller.register_device("test_device", "light")
        devices = device_controller.get_all_devices()
        if "test_device" in devices:
            print("  [PASS] Device registration")
        else:
            print("  [FAIL] Device registration failed")
            return False

        # Test command sending
        success = device_controller.send_command("test_device", "turn_on")
        if success:
            print("  [PASS] Device command sending")
        else:
            print("  [FAIL] Device command sending failed")
            return False

        return True
    except Exception as e:
        print(f"  [FAIL] Device controller test failed: {e}")
        return False

def test_security_components():
    """Test the security components."""
    try:
        from security.llm_security_agent import LLMSecurityAgent
        from security.llm_file_interceptor import LLMFileOperationInterceptor
        from memory.memory_manager import MemoryManager

        memory_manager = MemoryManager()
        security_agent = LLMSecurityAgent(memory_manager)
        file_interceptor = LLMFileOperationInterceptor(security_agent)

        # Test initialization
        security_agent.set_deny_policy(True)
        file_interceptor.enable_interception(True)

        print("  [PASS] Security components initialization")
        return True
    except Exception as e:
        print(f"  [FAIL] Security components test failed: {e}")
        return False

def test_agent_files():
    """Test agent management files."""
    try:
        project_root = Path(__file__).parent.parent
        agent_dir = project_root / "agent_stuff"
        agent_md = agent_dir / "agent.md"
        heartbeat_md = agent_dir / "heartbeat.md"

        if agent_md.exists() and heartbeat_md.exists():
            print("  [PASS] Agent management files exist")
            return True
        else:
            print("  [FAIL] Agent management files missing")
            return False
    except Exception as e:
        print(f"  [FAIL] Agent files test failed: {e}")
        return False

def main():
    """Main test function."""
    print("Self-Aware AI Agent Setup Test")
    print("=" * 40)

    # Test imports
    imports_ok = test_imports()
    local_imports_ok = test_local_modules()

    # Test components
    memory_ok = test_memory_manager()
    device_ok = test_device_controller()
    security_ok = test_security_components()
    agent_files_ok = test_agent_files()

    print("\nTest Summary:")
    print(f"  Module imports: {'[PASS]' if imports_ok else '[FAIL]'}")
    print(f"  Local imports: {'[PASS]' if local_imports_ok else '[FAIL]'}")
    print(f"  Memory manager: {'[PASS]' if memory_ok else '[FAIL]'}")
    print(f"  Device controller: {'[PASS]' if device_ok else '[FAIL]'}")
    print(f"  Security components: {'[PASS]' if security_ok else '[FAIL]'}")
    print(f"  Agent files: {'[PASS]' if agent_files_ok else '[FAIL]'}")

    if all([imports_ok, local_imports_ok, memory_ok, device_ok, security_ok, agent_files_ok]):
        print("\n[PASS] All tests passed! The setup is working correctly.")
        return 0
    else:
        print("\n[FAIL] Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())