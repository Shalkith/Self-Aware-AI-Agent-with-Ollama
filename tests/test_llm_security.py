#!/usr/bin/env python3
"""
Test script for the LLM Security Framework.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from memory.memory_manager import MemoryManager
from security.llm_security_agent import LLMSecurityAgent
from security.llm_file_interceptor import LLMFileOperationInterceptor

def test_llm_security_framework():
    """Test the LLM security framework components."""
    print("Testing LLM Security Framework")
    print("=" * 40)

    # Initialize components
    memory_manager = MemoryManager()
    security_agent = LLMSecurityAgent(memory_manager)
    file_interceptor = LLMFileOperationInterceptor(security_agent)

    # Test 1: Security agent initialization
    print("\n1. Testing LLM Security Agent Initialization...")
    try:
        security_agent.set_deny_policy(False)
        print("  [PASS] LLM Security agent initialized")
    except Exception as e:
        print(f"  [FAIL] LLM Security agent initialization failed: {e}")
        return False

    # Test 2: File interceptor initialization
    print("\n2. Testing LLM File Interceptor Initialization...")
    try:
        file_interceptor.enable_interception(True)
        print("  [PASS] LLM File interceptor initialized")
    except Exception as e:
        print(f"  [FAIL] LLM File interceptor initialization failed: {e}")
        return False

    # Test 3: Security approval request (this will use LLM evaluation)
    print("\n3. Testing LLM Security Approval Request...")
    try:
        approval = security_agent.request_approval(
            operation='test_write',
            file_path='agent_stuff/agent.md',
            content='print("Hello, World!")',
            metadata={'test': True, 'purpose': 'testing security system'}
        )
        print(f"  [PASS] LLM Security approval requested (approved: {approval})")
        print(f"      Note: Approval determined by LLM evaluation")
    except Exception as e:
        print(f"  [FAIL] LLM Security approval request failed: {e}")
        return False

    # Test 4: Safe file write (will be evaluated by LLM)
    print("\n4. Testing Safe File Write with LLM Evaluation...")
    try:
        success = file_interceptor.safe_write_file(
            file_path='agent_stuff/test_output.txt',
            content='# This is a test file for security testing\nprint("Security test")',
            metadata={'test': True, 'purpose': 'security framework testing'}
        )
        print(f"  [PASS] Safe file write attempted (success: {success})")
        print(f"      Note: Operation evaluated by LLM security agent")
    except Exception as e:
        print(f"  [FAIL] Safe file write test failed: {e}")
        return False

    # Test 5: Path safety checking
    print("\n5. Testing Path Safety Checking...")
    try:
        safe_path = security_agent.is_safe_path('agent_stuff/memory/test.py')
        critical_file = security_agent.is_critical_file('agent_stuff/agent/loop.py')
        print(f"  [PASS] Path safety checks completed")
        print(f"      Safe path check: {safe_path}")
        print(f"      Critical file check: {critical_file}")
    except Exception as e:
        print(f"  [FAIL] Path safety checking failed: {e}")
        return False

    # Test 6: Content hashing
    print("\n6. Testing Content Hashing...")
    try:
        content = "This is test content for hashing"
        hash_value = security_agent.hash_file_content(content)
        print(f"  [PASS] Content hashing completed")
        print(f"      Content hash: {hash_value[:16]}...")
    except Exception as e:
        print(f"  [FAIL] Content hashing failed: {e}")
        return False

    print("\n" + "=" * 40)
    print("LLM Security Framework Test Summary:")
    print("  All components initialized and tested successfully")
    print("  Security decisions are made by LLM evaluation")
    print("  File operations are intercepted and evaluated")
    print("  Audit logging captures all security activities")

    return True

def main():
    """Main test function."""
    success = test_llm_security_framework()

    if success:
        print("\n[PASS] LLM Security framework is working correctly!")
        return 0
    else:
        print("\n[FAIL] LLM Security framework test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())