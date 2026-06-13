# Self-Aware AI Agent Security Framework

This document explains the security framework implemented for the Self-Aware AI Agent to prevent unauthorized code modifications and file operations.

## Security Architecture

The security framework consists of three main components:

1. **Security Agent** (`security/security_agent.py`): Makes approval decisions for potentially dangerous operations
2. **File Operation Interceptor** (`security/file_interceptor.py`): Intercepts file operations and enforces security policies
3. **Security API Endpoints** (`security/api_endpoints.py`): Provides RESTful interfaces for security management

## Security Policy

By default, the security system operates under a **"Deny by Default"** policy:

- All file operations (write, edit, delete) are denied unless explicitly approved
- Code modifications require security approval
- Critical system files have additional protection

## Protected Operations

The following operations require security approval:

1. **File Writing**: Creating new files
2. **File Editing**: Modifying existing files
3. **File Deletion**: Removing files
4. **Directory Creation**: Creating new directories

## Security Components

### Security Agent

The `SecurityAgent` class is responsible for making approval decisions:

```python
security_agent = SecurityAgent(memory_manager)
approval = security_agent.request_approval(
    operation='write_file',
    file_path='/path/to/file.py',
    content='file content',
    metadata={'reason': 'self-improvement'}
)
```

Key features:
- Content hashing for integrity verification
- Path safety validation
- Critical file detection
- Decision logging and audit trail

### File Operation Interceptor

The `FileOperationInterceptor` wraps file operations with security checks:

```python
file_interceptor = FileOperationInterceptor(security_agent)
success = file_interceptor.safe_write_file(
    file_path='/path/to/file.py',
    content='new content'
)
```

Supported operations:
- `safe_write_file()`: Secure file creation
- `safe_edit_file()`: Secure file modification
- `safe_delete_file()`: Secure file deletion
- `safe_create_directory()`: Secure directory creation

## Configuration

Security settings can be configured in `config.py`:

```python
# Security Configuration
SECURITY_ENABLED = True  # Enable/disable security system
SECURITY_DENY_BY_DEFAULT = True  # Deny by default policy
SECURITY_APPROVAL_TIMEOUT = 300  # Approval timeout in seconds
SECURITY_LOG_LEVEL = 'INFO'  # Logging level
```

Environment variables can override these settings:
```bash
export SECURITY_ENABLED=true
export SECURITY_DENY_BY_DEFAULT=true
```

## New Action Types

The agent now supports additional action types that go through security checks:

### write_file
```json
{
    "action": {
        "type": "write_file",
        "parameters": {
            "file_path": "new_module.py",
            "content": "print('Hello, World!')",
            "metadata": {
                "purpose": "Add new functionality"
            }
        }
    }
}
```

### edit_file
```json
{
    "action": {
        "type": "edit_file",
        "parameters": {
            "file_path": "existing_module.py",
            "old_content": "old content here",
            "new_content": "new improved content",
            "metadata": {
                "change_type": "bug_fix"
            }
        }
    }
}
```

### delete_file
```json
{
    "action": {
        "type": "delete_file",
        "parameters": {
            "file_path": "obsolete_module.py",
            "metadata": {
                "reason": "Module deprecated"
            }
        }
    }
}
```

## API Endpoints

### Security Status
```
GET /api/security/status
```
Returns current security system status.

### Approval Requests
```
GET /api/security/approval-requests
```
Lists pending and recent approval requests.

### Approve Request
```
POST /api/security/approve-request
```
Manually approve a security request (requires admin authentication).

### Toggle Security
```
POST /api/security/toggle
```
Enable or disable the security system (requires admin authentication).

## Security Workflow

1. **Agent Requests Operation**: Agent decides to modify a file
2. **Security Check**: File interceptor checks if operation is approved
3. **Approval Request**: Security agent logs the request and denies by default
4. **Manual Approval**: Administrator reviews and approves (future implementation)
5. **Operation Execution**: If approved, file operation proceeds
6. **Audit Logging**: All decisions are logged for review

## Critical Files Protection

Certain files are considered critical and receive additional protection:

- `agent_server.py`: Main agent server
- `config.py`: Configuration file
- `security/`: Security modules
- `memory/`: Memory management modules
- `requirements.txt`: Dependencies

Operations on these files require extra scrutiny.

## Future Enhancements

Planned security improvements:

1. **User Authentication**: Admin authentication for approval operations
2. **Interactive Approval**: Web interface for reviewing/approving requests
3. **Code Review**: Automated code analysis before approval
4. **Sandboxing**: Isolated execution environment for modified code
5. **Rollback Mechanism**: Automatic rollback of problematic changes
6. **Notification System**: Alerts for security events

## Best Practices

1. **Keep Security Enabled**: Never disable the security system in production
2. **Regular Audits**: Review security logs regularly
3. **Minimal Permissions**: Run the agent with minimal required permissions
4. **Network Isolation**: Isolate the agent from sensitive networks
5. **Backup Strategy**: Maintain regular backups of critical files
6. **Monitoring**: Monitor for unusual file operation patterns

## Example Usage

Here's how the agent might request to improve itself:

```python
# Agent decides to optimize a function
action = {
    "type": "edit_file",
    "parameters": {
        "file_path": "memory/memory_manager.py",
        "old_content": "def slow_function():\n    # inefficient code",
        "new_content": "def fast_function():\n    # optimized code",
        "metadata": {
            "improvement_type": "performance",
            "benchmark_improvement": "50% faster"
        }
    }
}

# This will be denied by default and require manual approval
execute_action(action)
```

The security framework ensures that any self-improvement attempts by the agent must be reviewed and approved by an administrator, preventing unauthorized code modifications while still allowing for controlled self-improvement.