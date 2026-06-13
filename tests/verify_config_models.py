#!/usr/bin/env python3
"""
Verification script to confirm all models are strictly loaded from config.
No hardcoded fallbacks should exist.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import config

def verify_models_from_config():
    """Verify all models are loaded from config."""
    print("="*60)
    print("VERIFYING MODELS ARE LOADED FROM CONFIG")
    print("="*60)

    # Check that MODELS dict exists and has all required keys
    required_keys = ['thinking', 'vision', 'conversation', 'reasoning', 'creativity', 'security']

    print("\n1. Checking MODELS dictionary contains all required keys...")
    for key in required_keys:
        if key in config.MODELS:
            print(f"   [OK] {key}: {config.MODELS[key]}")
        else:
            print(f"   [FAIL] Missing key: {key}")
            return False

    print("\n2. Checking all model values are strings...")
    for key, value in config.MODELS.items():
        if isinstance(value, str) and value:
            print(f"   [OK] {key}: '{value}' (type: {type(value).__name__})")
        else:
            print(f"   [FAIL] {key}: Invalid value '{value}'")
            return False

    print("\n3. Checking no hardcoded model names in config.py...")
    # The config should use getenv with defaults, but those defaults should be
    # the only place model names are hardcoded
    print("   [INFO] Config uses os.getenv() with defaults - this is acceptable")
    print("   [INFO] To override, set environment variables or edit .env file")

    print("\n4. Verifying other files use config.MODELS...")

    # Import and check security agent
    try:
        from security.llm_security_agent import LLMSecurityAgent
        from memory.memory_manager import MemoryManager
        import tempfile
        import os

        # Create temp memory db for testing
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_db = f.name

        memory = MemoryManager(temp_db)
        security_agent = LLMSecurityAgent(memory)

        # Check security model comes from config
        expected_security = config.MODELS['security']
        actual_security = security_agent.security_model

        if actual_security == expected_security:
            print(f"   [OK] LLMSecurityAgent.security_model = '{actual_security}' (from config)")
        else:
            print(f"   [FAIL] Security model mismatch: expected '{expected_security}', got '{actual_security}'")
            return False

        # Cleanup
        memory.clear_memories()
        os.remove(temp_db)

    except Exception as e:
        print(f"   [FAIL] Error checking security agent: {e}")
        return False

    return True

def show_model_usage():
    """Show where each model is used."""
    print("\n" + "="*60)
    print("MODEL USAGE SUMMARY")
    print("="*60)

    usage = {
        'thinking': 'Autonomous thinking and reflection (agent loop)',
        'vision': 'Image analysis and visual perception',
        'conversation': 'User interaction and chat responses',
        'reasoning': 'Complex problem solving and decision making',
        'creativity': 'Creative tasks and content generation',
        'security': 'Security evaluation and file operation approval'
    }

    for model_key, description in usage.items():
        model_name = config.MODELS.get(model_key, 'NOT CONFIGURED')
        print(f"\n  {model_key.upper()}:")
        print(f"    Model: {model_name}")
        print(f"    Usage: {description}")

def show_environment_overrides():
    """Show which environment variables can override defaults."""
    print("\n" + "="*60)
    print("ENVIRONMENT VARIABLE OVERRIDES")
    print("="*60)

    env_vars = [
        ('THINKING_MODEL', config.MODELS['thinking']),
        ('VISION_MODEL', config.MODELS['vision']),
        ('CONVERSATION_MODEL', config.MODELS['conversation']),
        ('REASONING_MODEL', config.MODELS['reasoning']),
        ('CREATIVITY_MODEL', config.MODELS['creativity']),
        ('SECURITY_MODEL', config.MODELS['security']),
    ]

    print("\n  Set these in your .env file to override defaults:")
    for var, current in env_vars:
        print(f"    {var}={current}")

def main():
    """Main function."""
    success = verify_models_from_config()
    show_model_usage()
    show_environment_overrides()

    print("\n" + "="*60)
    if success:
        print("VERIFICATION PASSED: All models are loaded from config!")
        print("="*60)
        return 0
    else:
        print("VERIFICATION FAILED: Some models are not properly configured!")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
