from flask import Blueprint, request, jsonify, current_app
import logging

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/control-device', methods=['POST'])
def control_device():
    """API endpoint to control a device."""
    try:
        # Get the shared device controller from the app context
        device_controller = current_app.device_controller

        data = request.get_json()
        device_id = data.get('device_id')
        command = data.get('command')
        parameters = data.get('parameters', {})

        if not device_id or not command:
            return jsonify({'error': 'device_id and command are required'}), 400

        success = device_controller.send_command(device_id, command, parameters)

        if success:
            return jsonify({'status': 'success', 'message': f'Command {command} sent to {device_id}'})
        else:
            return jsonify({'status': 'error', 'message': f'Failed to send command {command} to {device_id}'}), 500

    except Exception as e:
        logging.error(f"Error in control_device: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/devices/<device_id>/state', methods=['GET'])
def get_device_state(device_id):
    """API endpoint to get device state."""
    try:
        # Get the shared device controller from the app context
        device_controller = current_app.device_controller

        state = device_controller.get_device_state(device_id)

        if state is None:
            return jsonify({'error': 'Device not found'}), 404

        return jsonify({'device_id': device_id, 'state': state})

    except Exception as e:
        logging.error(f"Error in get_device_state: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/devices/<device_id>/state', methods=['POST'])
def set_device_state(device_id):
    """API endpoint to set device state."""
    try:
        # Get the shared device controller from the app context
        device_controller = current_app.device_controller

        data = request.get_json()
        state = data.get('state')

        if not state:
            return jsonify({'error': 'state is required'}), 400

        # For simulation, we'll just update the state directly
        # In a real implementation, this would send a command to the device
        device = device_controller.devices.get(device_id)
        if not device:
            return jsonify({'error': 'Device not found'}), 404

        device['state'] = state
        return jsonify({'device_id': device_id, 'state': state})

    except Exception as e:
        logging.error(f"Error in set_device_state: {e}")
        return jsonify({'error': str(e)}), 500