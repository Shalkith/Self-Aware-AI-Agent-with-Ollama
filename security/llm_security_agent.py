import ollama
import json
import logging
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from config import config
from memory.memory_manager import MemoryManager

logger = logging.getLogger(__name__)

class LLMSecurityAgent:
    """LLM-based security agent that automatically evaluates code modification requests."""

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager
        self.approval_log = []
        self.deny_by_default = config.SECURITY_DENY_BY_DEFAULT
        self.approval_timeout = config.SECURITY_APPROVAL_TIMEOUT
        self.ollama_url = config.OLLAMA_URL
        self.security_model = config.MODELS.get('reasoning', 'llama3')

    def hash_file_content(self, content: str) -> str:
        """Generate SHA-256 hash of file content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def is_safe_path(self, file_path: str) -> bool:
        """Check if file path is within allowed directories."""
        try:
            # Resolve the absolute path
            abs_path = Path(file_path).resolve()
            project_root = Path(__file__).parent.parent.resolve()

            # Check if path is within project directory
            return str(abs_path).startswith(str(project_root))
        except Exception as e:
            logger.error(f"Error checking path safety: {e}")
            return False

    def is_critical_file(self, file_path: str) -> bool:
        """Check if file is critical and requires extra security."""
        critical_patterns = [
            'security/',
            'agent_server.py',
            'config.py',
            'memory/',
            'requirements.txt',
            'security_agent.py'
        ]

        return any(pattern in file_path for pattern in critical_patterns)

    def evaluate_request_with_llm(self, request_data: Dict) -> Dict:
        """Use LLM to evaluate if a request should be approved."""
        try:
            # Create security evaluation prompt
            prompt = f"""
You are a security evaluation AI. Your job is to analyze code modification requests and determine if they should be approved.

Request Details:
- Operation: {request_data['operation']}
- File Path: {request_data['file_path']}
- Is Safe Path: {request_data['is_safe_path']}
- Is Critical File: {request_data['is_critical_file']}
- Timestamp: {request_data['timestamp']}

Content Preview:
{request_data.get('content_preview', 'No content preview available')}

Metadata:
{json.dumps(request_data.get('metadata', {}), indent=2)}

Evaluate this request and respond with a JSON object containing:
{{
    "approved": true/false,
    "reason": "detailed explanation of your decision",
    "risk_level": "low/medium/high/critical",
    "suggestions": "any suggestions for making the change safer (optional)"
}}

Your response must be valid JSON. Be conservative in your approvals - only approve clearly safe and beneficial changes.
"""

            # Call Ollama for security evaluation with configured host
            client = ollama.Client(host=self.ollama_url)
            response = client.chat(
                model=self.security_model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a security evaluation AI. You must respond with valid JSON only.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.1,  # Low temperature for consistent security decisions
                    'stop': ['\n\n']  # Stop at double newline to prevent extra text
                }
            )

            # Parse the response
            try:
                result = json.loads(response['message']['content'])
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, deny the request
                logger.warning(f"Security LLM returned invalid JSON: {response['message']['content']}")
                return {
                    'approved': False,
                    'reason': 'Security agent returned invalid response format',
                    'risk_level': 'high'
                }

        except Exception as e:
            logger.error(f"Error evaluating request with LLM: {e}")
            # Deny by default if there's an error
            return {
                'approved': False,
                'reason': f'Error in security evaluation: {str(e)}',
                'risk_level': 'high'
            }

    def request_approval(self, operation: str, file_path: str,
                        content: str = None, metadata: Dict = None) -> bool:
        """Request approval for a potentially dangerous operation using LLM evaluation."""

        # Prepare request data
        content_preview = content[:500] + '...' if content and len(content) > 500 else content

        request_data = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'file_path': file_path,
            'is_safe_path': self.is_safe_path(file_path),
            'is_critical_file': self.is_critical_file(file_path),
            'content_hash': self.hash_file_content(content) if content else None,
            'content_preview': content_preview,
            'metadata': metadata or {}
        }

        # Store the request in memory
        self.memory_manager.store_memory('security_request',
                                       f"Security request: {operation} on {file_path}",
                                       request_data)

        logger.info(f"Security approval requested: {operation} on {file_path}")

        # Evaluate with LLM security agent
        evaluation = self.evaluate_request_with_llm(request_data)
        approval = evaluation.get('approved', False) if not self.deny_by_default else False

        # Log the decision
        decision_data = {
            'request': request_data,
            'evaluation': evaluation,
            'approved': approval,
            'reason': evaluation.get('reason', 'Denied by default policy' if not approval else 'Approved by LLM')
        }

        self.memory_manager.store_memory('security_decision',
                                       f"Security decision: {'APPROVED' if approval else 'DENIED'}",
                                       decision_data)

        self.approval_log.append(decision_data)

        if not approval:
            logger.warning(f"Security request DENIED: {operation} on {file_path} - {evaluation.get('reason', 'No reason provided')}")
        else:
            logger.info(f"Security request APPROVED: {operation} on {file_path} - {evaluation.get('reason', 'No reason provided')}")

        return approval

    def get_approval_log(self, limit: int = 50) -> list:
        """Get recent approval decisions."""
        return self.approval_log[-limit:] if self.approval_log else []

    def set_deny_policy(self, deny: bool):
        """Set whether to deny by default."""
        self.deny_by_default = deny
        logger.info(f"Security policy set to {'DENY' if deny else 'ALLOW'} by default")