import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from security.llm_security_agent import LLMSecurityAgent

logger = logging.getLogger(__name__)

class LLMFileOperationInterceptor:
    """Intercepts file operations and enforces LLM-based security policies."""

    def __init__(self, security_agent: LLMSecurityAgent):
        self.security_agent = security_agent
        self.interception_enabled = True

    def _check_security_approval(self, operation: str, file_path: str,
                               content: str = None, metadata: Dict = None) -> bool:
        """Check if operation is approved by LLM security agent."""
        if not self.interception_enabled:
            return True

        return self.security_agent.request_approval(operation, file_path, content, metadata)

    def safe_write_file(self, file_path: str, content: str,
                       metadata: Dict = None) -> bool:
        """Safely write a file with LLM security approval."""
        try:
            # Check if operation is approved
            if not self._check_security_approval('write_file', file_path, content, metadata):
                logger.warning(f"File write denied by LLM security agent: {file_path}")
                return False

            # Perform the write operation
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"File written successfully: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error writing file {file_path}: {e}")
            return False

    def safe_edit_file(self, file_path: str, old_content: str, new_content: str,
                      metadata: Dict = None) -> bool:
        """Safely edit a file with LLM security approval."""
        try:
            # Check if operation is approved
            edit_metadata = {
                'old_content_hash': self.security_agent.hash_file_content(old_content),
                'new_content_hash': self.security_agent.hash_file_content(new_content)
            }
            if metadata:
                edit_metadata.update(metadata)

            if not self._check_security_approval('edit_file', file_path, new_content, edit_metadata):
                logger.warning(f"File edit denied by LLM security agent: {file_path}")
                return False

            # Perform the edit operation
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            logger.info(f"File edited successfully: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error editing file {file_path}: {e}")
            return False

    def safe_delete_file(self, file_path: str, metadata: Dict = None) -> bool:
        """Safely delete a file with LLM security approval."""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                logger.warning(f"File not found for deletion: {file_path}")
                return False

            # Check if operation is approved
            if not self._check_security_approval('delete_file', file_path, None, metadata):
                logger.warning(f"File deletion denied by LLM security agent: {file_path}")
                return False

            # Perform the delete operation
            os.remove(file_path)
            logger.info(f"File deleted successfully: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False

    def safe_create_directory(self, dir_path: str, metadata: Dict = None) -> bool:
        """Safely create a directory with LLM security approval."""
        try:
            # Check if operation is approved
            if not self._check_security_approval('create_directory', dir_path, None, metadata):
                logger.warning(f"Directory creation denied by LLM security agent: {dir_path}")
                return False

            # Perform the create operation
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created successfully: {dir_path}")
            return True

        except Exception as e:
            logger.error(f"Error creating directory {dir_path}: {e}")
            return False

    def enable_interception(self, enabled: bool = True):
        """Enable or disable file operation interception."""
        self.interception_enabled = enabled
        logger.info(f"File operation interception {'enabled' if enabled else 'disabled'}")