from flask import Blueprint, request, jsonify, current_app
import logging

# Create blueprint
security_bp = Blueprint('security', __name__)

@security_bp.route('/security/approval-requests', methods=['GET'])
def get_approval_requests():
    """Get pending security approval requests."""
    try:
        # Get the security agent from app context
        security_agent = current_app.security_agent

        # Return recent decisions as examples
        approval_log = security_agent.get_approval_log(limit=20)

        return jsonify({
            'status': 'success',
            'requests': approval_log
        })

    except Exception as e:
        logging.error(f"Error getting approval requests: {e}")
        return jsonify({'error': str(e)}), 500

@security_bp.route('/security/status', methods=['GET'])
def get_security_status():
    """Get security system status."""
    try:
        # Get components from app context
        security_agent = current_app.security_agent
        file_interceptor = current_app.file_interceptor

        return jsonify({
            'status': 'active',
            'deny_by_default': security_agent.deny_by_default,
            'interception_enabled': file_interceptor.interception_enabled,
            'recent_decisions': len(security_agent.approval_log)
        })

    except Exception as e:
        logging.error(f"Error getting security status: {e}")
        return jsonify({'error': str(e)}), 500

@security_bp.route('/security/toggle', methods=['POST'])
def toggle_security():
    """Toggle security system on/off."""
    try:
        data = request.get_json()
        enabled = data.get('enabled', True)

        # Get components from app context
        file_interceptor = current_app.file_interceptor

        file_interceptor.enable_interception(enabled)

        status = "enabled" if enabled else "disabled"
        return jsonify({
            'status': 'success',
            'message': f'Security system {status}'
        })

    except Exception as e:
        logging.error(f"Error toggling security: {e}")
        return jsonify({'error': str(e)}), 500

@security_bp.route('/security/test-approval', methods=['POST'])
def test_approval():
    """Test security approval with a sample request."""
    try:
        data = request.get_json()
        operation = data.get('operation', 'test')
        file_path = data.get('file_path', 'test.py')
        content = data.get('content', '# Test content')
        metadata = data.get('metadata', {'test': True})

        # Get the security agent from app context
        security_agent = current_app.security_agent

        # Request approval
        approved = security_agent.request_approval(operation, file_path, content, metadata)

        return jsonify({
            'status': 'success',
            'approved': approved,
            'message': f'Operation {"approved" if approved else "denied"} by LLM security agent'
        })

    except Exception as e:
        logging.error(f"Error testing approval: {e}")
        return jsonify({'error': str(e)}), 500