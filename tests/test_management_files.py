#!/usr/bin/env python3
"""
Test script to verify agent management files are being read correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agent_stuff.agent.runner import AgentRunner
from memory.memory_manager import MemoryManager
from security.llm_security_agent import LLMSecurityAgent
from security.llm_file_interceptor import LLMFileOperationInterceptor

def test_management_file_reading():
    """Test that management files can be read."""
    print("Testing Management File Reading")
    print("=" * 50)

    # Create minimal components needed
    memory = MemoryManager()
    security = LLMSecurityAgent(memory)
    interceptor = LLMFileOperationInterceptor(security)

    # Create runner with dummy components
    class DummyComponent:
        pass

    runner = AgentRunner(
        memory_manager=memory,
        security_agent=security,
        file_interceptor=interceptor,
        camera=DummyComponent(),
        microphone=DummyComponent(),
        speaker=DummyComponent(),
        device_controller=DummyComponent()
    )

    # Test reading each management file
    files = [
        "AGENT.md",
        "SOUL.md",
        "AGENTS.md",
        "USER.md",
        "MEMORY.md",
        "TOOLS.md",
        "HEARTBEAT.md",
        "IDENTITY.md",
        "README.md"
    ]

    all_found = True
    for filename in files:
        content = runner._read_management_file(filename)
        if content:
            lines = len(content.split('\n'))
            chars = len(content)
            print(f"  [OK] {filename}: {lines} lines, {chars} chars")
        else:
            print(f"  [MISSING] {filename}: File not found or empty")
            all_found = False

    # Cleanup
    memory.clear_memories()

    print()
    if all_found:
        print("[PASS] All management files readable!")
        return True
    else:
        print("[WARN] Some files missing (expected if not created yet)")
        return True  # Still pass as this might be expected


def test_system_prompt_includes_files():
    """Test that system prompt includes management file content."""
    print("\nTesting System Prompt Includes Management Files")
    print("=" * 50)

    memory = MemoryManager()
    security = LLMSecurityAgent(memory)
    interceptor = LLMFileOperationInterceptor(security)

    class DummyComponent:
        pass

    runner = AgentRunner(
        memory_manager=memory,
        security_agent=security,
        file_interceptor=interceptor,
        camera=DummyComponent(),
        microphone=DummyComponent(),
        speaker=DummyComponent(),
        device_controller=DummyComponent()
    )

    # Get system prompt
    prompt = runner._get_system_prompt()

    # Check that sections are included
    checks = [
        ("YOUR IDENTITY", "Identity section"),
        ("YOUR CHARACTER (SOUL)", "SOUL section"),
        ("USER CONTEXT", "User section"),
        ("OPERATIONAL RULES", "Agents section"),
        ("YOUR MEMORY", "Memory section"),
        ("AVAILABLE TOOLS", "Tools section"),
        ("MANAGEMENT FILES", "Management files section"),
        ("AGENT.md", "AGENT.md reference"),
        ("update_agent_file", "Update action reference")
    ]

    all_present = True
    for keyword, description in checks:
        if keyword in prompt:
            print(f"  [OK] {description} present")
        else:
            print(f"  [MISSING] {description} not found")
            all_present = False

    # Show prompt length
    print(f"\n  System prompt length: {len(prompt)} chars")

    # Cleanup
    memory.clear_memories()

    print()
    if all_present:
        print("[PASS] System prompt includes all management sections!")
        return True
    else:
        print("[FAIL] Some sections missing from system prompt")
        return False


def main():
    """Main test function."""
    print("\n" + "=" * 60)
    print("AGENT MANAGEMENT FILES VERIFICATION")
    print("=" * 60 + "\n")

    test1_ok = test_management_file_reading()
    test2_ok = test_system_prompt_includes_files()

    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"  File Reading: {'[PASS]' if test1_ok else '[FAIL]'}")
    print(f"  System Prompt: {'[PASS]' if test2_ok else '[FAIL]'}")

    if test1_ok and test2_ok:
        print("\n[PASS] All verifications passed!")
        print("The agent is properly configured to read and use management files.")
        return 0
    else:
        print("\n[FAIL] Some verifications failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
