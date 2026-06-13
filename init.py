#!/usr/bin/env python3
"""
Initialization script for the Self-Aware AI Agent.
This script sets up the environment and verifies all components.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """Check if Python version is sufficient."""
    import sys
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version}")
    return True

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'flask',
        'flask-socketio',
        'ollama',
        'opencv-python',
        'pyaudio',
        'pyttsx3',
        'gpiozero',
        'requests',
        'pillow',
        'numpy'
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package}")

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        return False

    return True

def install_dependencies():
    """Install missing dependencies."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def check_ollama():
    """Check if Ollama is accessible."""
    try:
        import ollama
        # Try to connect to Ollama
        client = ollama.Client()
        version = client.version()
        print(f"✓ Ollama is accessible (Version: {version})")
        return True
    except Exception as e:
        print(f"⚠ Ollama connection failed: {e}")
        print("  Make sure Ollama is running and accessible at the configured URL")
        return False

def check_camera():
    """Check if camera is accessible."""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✓ Camera is accessible")
                cap.release()
                return True
            else:
                print("⚠ Camera opened but failed to capture frame")
                cap.release()
                return False
        else:
            print("⚠ Camera is not accessible")
            return False
    except Exception as e:
        print(f"⚠ Camera check failed: {e}")
        return False

def check_microphone():
    """Check if microphone is accessible."""
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        input_devices = 0
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                input_devices += 1

        p.terminate()

        if input_devices > 0:
            print(f"✓ Microphone is accessible ({input_devices} input device(s) found)")
            return True
        else:
            print("⚠ No microphone input devices found")
            return False
    except Exception as e:
        print(f"⚠ Microphone check failed: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = [
        'memory',
        'client/static/css',
        'client/static/js',
        'client/templates',
        'perception',
        'devices'
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory created: {directory}")

def main():
    """Main initialization function."""
    parser = argparse.ArgumentParser(description="Initialize the Self-Aware AI Agent")
    parser.add_argument("--install-deps", action="store_true",
                        help="Install missing dependencies")
    parser.add_argument("--check-only", action="store_true",
                        help="Only check components, don't install anything")

    args = parser.parse_args()

    print("Self-Aware AI Agent Initialization")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        return 1

    print("\nChecking dependencies...")
    deps_ok = check_dependencies()

    if not deps_ok and args.install_deps:
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            return 1
        # Recheck after installation
        deps_ok = check_dependencies()

    if not deps_ok and not args.check_only:
        print("\nSome dependencies are missing. Run with --install-deps to install them.")
        return 1

    print("\nChecking system components...")
    check_ollama()
    check_camera()
    check_microphone()

    print("\nCreating directories...")
    create_directories()

    print("\nInitialization completed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())