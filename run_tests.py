#!/usr/bin/env python3
"""
Test runner for the Self-Aware AI Agent.
This script runs all tests for the agent components.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_test_script(script_name):
    """Run a test script and return the result."""
    try:
        print(f"Running {script_name}...")
        result = subprocess.run([sys.executable, script_name],
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✓ {script_name} passed")
            return True
        else:
            print(f"  ✗ {script_name} failed")
            print(f"    Stdout: {result.stdout}")
            print(f"    Stderr: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ {script_name} timed out")
        return False
    except Exception as e:
        print(f"  ✗ {script_name} error: {e}")
        return False

def main():
    """Main test runner function."""
    print("Self-Aware AI Agent Test Runner")
    print("=" * 40)

    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # Test scripts to run
    test_scripts = [
        'test_setup.py',
        # Add more test scripts here as needed
    ]

    # Run tests
    results = []
    for script in test_scripts:
        if Path(script).exists():
            result = run_test_script(script)
            results.append((script, result))
        else:
            print(f"Skipping {script} (not found)")

    # Summary
    print("\nTest Summary:")
    all_passed = True
    for script, result in results:
        status = "✓" if result else "✗"
        print(f"  {status} {script}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())