#!/usr/bin/env python3
"""
Model checking script for Self-Aware AI Agent.
Verifies that all required LLM models are available before booting.
"""

import ollama
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import config

def check_model_availability(model_name: str, model_tag: str = None) -> bool:
    """Check if a model is available in Ollama."""
    try:
        full_model_name = f"{model_name}:{model_tag}" if model_tag else model_name

        # Try to get model info
        client = ollama.Client(host=config.OLLAMA_URL)
        client.show(model_name)

        print(f"  [AVAILABLE] {model_name}")
        return True

    except Exception as e:
        print(f"  [MISSING] {model_name} - {e}")
        return False

def check_all_models():
    """Check all required models for the agent."""
    print("Self-Aware AI Agent - Model Check")
    print("=" * 40)
    print(f"Ollama URL: {config.OLLAMA_URL}")
    print()

    # Test Ollama connection first
    try:
        client = ollama.Client(host=config.OLLAMA_URL)
        # Try a simple list operation to test connection
        client.list()
        print("[PASS] Connected to Ollama")
        print()
    except Exception as e:
        print(f"[FAIL] Failed to connect to Ollama: {e}")
        print("Please ensure Ollama is running and accessible.")
        return False

    # Check required models
    print("Checking required models...")
    required_models = [
        config.MODELS['thinking'],
        config.MODELS['vision'],
        config.MODELS['conversation'],
        config.MODELS['reasoning'],
        config.MODELS['creativity'],
    ]

    # Add security model if different
    security_model = config.MODELS.get('security', config.MODELS['reasoning'])
    if security_model not in required_models:
        required_models.append(security_model)

    # Remove duplicates while preserving order
    required_models = list(dict.fromkeys(required_models))

    all_available = True
    for model in required_models:
        if not check_model_availability(model):
            all_available = False

    print()
    if all_available:
        print("[PASS] All required models are available!")
        return True
    else:
        print("[FAIL] Some required models are missing.")
        print("Please pull the missing models using:")
        print("  ollama pull <model_name>")
        return False

def pull_missing_models():
    """Attempt to pull missing models."""
    print("\nAttempting to pull missing models...")

    required_models = [
        config.MODELS['thinking'],
        config.MODELS['vision'],
        config.MODELS['conversation'],
        config.MODELS['reasoning'],
        config.MODELS['creativity'],
    ]

    security_model = config.MODELS.get('security', config.MODELS['reasoning'])
    if security_model not in required_models:
        required_models.append(security_model)

    required_models = list(dict.fromkeys(required_models))

    client = ollama.Client(host=config.OLLAMA_URL)

    for model in required_models:
        try:
            print(f"  Pulling {model}...")
            # This will pull the model if it doesn't exist
            client.pull(model)
            print(f"  [PASS] {model} pulled successfully")
        except Exception as e:
            print(f"  [FAIL] Failed to pull {model}: {e}")

def main():
    """Main function."""
    print("Self-Aware AI Agent Model Checker")
    print("=" * 40)

    # Check models
    success = check_all_models()

    if not success:
        choice = input("\nWould you like to attempt to pull missing models? (y/N): ").strip().lower()
        if choice == 'y':
            pull_missing_models()
            # Recheck after pulling
            success = check_all_models()

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())