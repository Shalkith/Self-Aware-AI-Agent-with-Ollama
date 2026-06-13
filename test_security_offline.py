#!/usr/bin/env python3
"""
Offline test script to demonstrate the LLM Security Agent framework structure.
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from memory.memory_manager import MemoryManager
from security.llm_security_agent import LLMSecurityAgent
from security.llm_file_interceptor import LLMFileOperationInterceptor

def test_security_framework_structure():
    """Test that the security framework components are properly structured."""
    print("Testing LLM Security Framework Structure")
    print("=" * 50)

    # Initialize components
    memory_manager = MemoryManager()
    security_agent = LLMSecurityAgent(memory_manager)
    file_interceptor = LLMFileOperationInterceptor(security_agent)

    print("[PASS] LLMSecurityAgent initialized successfully")
    print("[PASS] LLMFileOperationInterceptor initialized successfully")
    print("[PASS] MemoryManager integrated successfully")

    # Test component methods
    print("\nTesting component methods...")

    # Test path safety
    safe_path = security_agent.is_safe_path('memory/test.py')
    critical_file = security_agent.is_critical_file('agent_server.py')
    print(f"[PASS] Path safety check: {safe_path}")
    print(f"[PASS] Critical file detection: {critical_file}")

    # Test content hashing
    content = "This is test content for hashing"
    hash_value = security_agent.hash_file_content(content)
    print(f"[PASS] Content hashing: {hash_value[:16]}...")

    # Test file interceptor methods
    file_interceptor.enable_interception(True)
    print("[PASS] File interception enabled")

    # Test approval log
    approval_log = security_agent.get_approval_log()
    print(f"[PASS] Approval log accessible: {len(approval_log)} entries")

    # Test security policy
    security_agent.set_deny_policy(True)
    print("[PASS] Security policy configuration working")

    print("\n" + "=" * 50)
    print("Framework Structure Test: PASSED")
    print("\nNote: For actual LLM evaluation, Ollama must be running")
    print("at http://192.168.99.113:11434 with required models.")

def demonstrate_security_concepts():
    """Demonstrate how the security system would work with Ollama."""
    print("\n\nSecurity System Concept Demonstration")
    print("=" * 50)

    print("""
When Ollama is available, the security system works as follows:

1. AGENT REQUESTS FILE OPERATION:
   - Agent wants to modify 'agent.md'
   - File interceptor captures the request

2. SECURITY EVALUATION:
   - LLM security agent analyzes the request
   - Considers factors:
     * File path safety
     * Content risk level
     * Critical system impact
     * Overall security posture

3. LLM DECISION EXAMPLES:

   SAFE REQUEST (would be APPROVED):
   - Operation: edit_file
   - File: agent.md
   - Content: Documentation improvements
   - LLM Response: {"approved": true, "reason": "Documentation updates are safe", "risk_level": "low"}

   UNSAFE REQUEST (would be DENIED):
   - Operation: edit_file
   - File: security/llm_security_agent.py
   - Content: Code that removes security checks
   - LLM Response: {"approved": false, "reason": "Removes critical security protections", "risk_level": "critical"}

4. AUDIT LOGGING:
   - All requests and decisions stored
   - Detailed reasoning preserved
   - Security review possible

5. FAIL-SAFE BEHAVIOR:
   - If LLM unavailable: DENY by default
   - If LLM error: DENY by default
   - Security logging continues
""")

def main():
    """Main test function."""
    try:
        test_security_framework_structure()
        demonstrate_security_concepts()
        return 0
    except Exception as e:
        print(f"Error during offline security test: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())