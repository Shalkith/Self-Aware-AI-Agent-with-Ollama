# Self-Aware AI Agent - Test Suite

This folder contains all test scripts for the Self-Aware AI Agent.

## Running Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Individual Tests

```bash
# Setup verification
python tests/test_setup.py

# Senses test (camera, microphone, speaker)
python tests/test_senses.py

# Security agent test
python tests/test_security_agent.py

# File interceptor test
python tests/test_file_interceptor.py

# Security framework offline test
python tests/test_security_offline.py

# Model availability check
python tests/check_models.py

# Configuration verification
python tests/verify_config_models.py

# LLM Security framework test
python tests/test_llm_security.py
```

## Test Descriptions

| Test File | Purpose |
|-----------|---------|
| `test_setup.py` | Verify all imports and basic component initialization |
| `test_senses.py` | Test camera, microphone, speaker, memory, and device controller |
| `test_security_agent.py` | Test LLM security agent with safe/unsafe operations |
| `test_file_interceptor.py` | Test file operation interception |
| `test_security_offline.py` | Test security framework without Ollama |
| `test_llm_security.py` | Test LLM security framework components |
| `check_models.py` | Verify Ollama models are available |
| `verify_config_models.py` | Verify all models loaded from config |
| `run_tests.py` | Test runner that executes all tests |

## Test Requirements

- All tests can be run from the project root directory
- Tests automatically add the project root to Python path
- Some tests require Ollama to be running (marked in output)
- Hardware tests (camera, microphone, speaker) require actual hardware
