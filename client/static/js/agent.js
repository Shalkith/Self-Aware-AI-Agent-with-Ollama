// Agent client-side functionality

class AgentClient {
    constructor() {
        this.socket = io();
        this.initializeEventHandlers();
        this.initializeUI();
    }

    initializeEventHandlers() {
        // SocketIO event handlers
        this.socket.on('connect', () => {
            console.log('Connected to agent server');
            this.updateConnectionStatus(true);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from agent server');
            this.updateConnectionStatus(false);
        });

        this.socket.on('agent_state_update', (data) => {
            this.updateAgentStatus(data);
        });

        this.socket.on('agent_response', (data) => {
            this.displayAgentResponse(data);
        });
    }

    initializeUI() {
        // Button event handlers
        document.getElementById('send-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        document.getElementById('start-btn').addEventListener('click', () => {
            this.socket.emit('start_agent');
        });

        document.getElementById('stop-btn').addEventListener('click', () => {
            this.socket.emit('stop_agent');
        });

        document.getElementById('capture-btn').addEventListener('click', () => {
            this.captureAndAnalyze();
        });

        // Tab event handlers
        document.getElementById('memories-tab').addEventListener('click', () => {
            this.refreshMemories();
        });

        document.getElementById('experiences-tab').addEventListener('click', () => {
            this.refreshExperiences();
        });

        // Initial data load
        this.refreshDevices();
        this.refreshMemories();
        this.refreshExperiences();
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            statusElement.textContent = connected ? 'Connected' : 'Disconnected';
            statusElement.className = connected ? 'text-success' : 'text-danger';
        }
    }

    updateAgentStatus(status) {
        // Update status text and indicator
        const statusText = document.getElementById('status-text');
        const statusIndicator = document.getElementById('status-indicator');

        if (statusText) statusText.textContent = status.status;
        if (statusIndicator) {
            statusIndicator.className = 'status-indicator status-' + status.status;
        }

        // Update current thought
        const currentThought = document.getElementById('current-thought');
        if (currentThought) {
            currentThought.textContent = status.current_thought || 'No thoughts yet...';
        }

        // Update last action
        const lastAction = document.getElementById('last-action');
        if (lastAction) {
            lastAction.textContent = status.last_action || 'No actions yet...';
        }
    }

    sendMessage() {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();

        if (message) {
            this.socket.emit('send_message', {message: message});
            messageInput.value = '';
        }
    }

    displayAgentResponse(data) {
        const responsesContainer = document.getElementById('responses-container');
        if (!responsesContainer) return;

        const responseElement = document.createElement('div');
        responseElement.className = 'mb-3';
        responseElement.innerHTML = `
            <div class="thought-bubble">
                <strong>Thought:</strong> ${data.thought || 'No thought recorded'}
            </div>
            <div class="agent-response">
                <strong>Response:</strong> ${data.response}
            </div>
            <small class="text-muted">${new Date(data.timestamp).toLocaleString()}</small>
        `;

        responsesContainer.innerHTML = '';
        responsesContainer.appendChild(responseElement);
        responsesContainer.scrollTop = responsesContainer.scrollHeight;
    }

    captureAndAnalyze() {
        // In a real implementation, this would capture from the camera
        // For now, we'll simulate this with a message
        const responsesContainer = document.getElementById('responses-container');
        if (!responsesContainer) return;

        const responseElement = document.createElement('div');
        responseElement.className = 'mb-3';
        responseElement.innerHTML = `
            <div class="thought-bubble">
                <strong>Thought:</strong> Analyzing visual input...
            </div>
            <div class="agent-response">
                <strong>Response:</strong> Camera capture and analysis would be implemented here.
            </div>
            <small class="text-muted">${new Date().toLocaleString()}</small>
        `;

        responsesContainer.innerHTML = '';
        responsesContainer.appendChild(responseElement);
        responsesContainer.scrollTop = responsesContainer.scrollHeight;
    }

    refreshDevices() {
        fetch('/api/devices')
            .then(response => response.json())
            .then(devices => {
                this.updateDevicesList(devices);
            })
            .catch(error => {
                console.error('Error fetching devices:', error);
            });
    }

    updateDevicesList(devices) {
        const devicesList = document.getElementById('devices-list');
        if (!devicesList) return;

        if (Object.keys(devices).length === 0) {
            devicesList.innerHTML = '<div class="text-muted">No devices registered</div>';
            return;
        }

        let html = '';
        for (const [id, device] of Object.entries(devices)) {
            html += `
                <div class="mb-2">
                    <div class="d-flex justify-content-between align-items-center">
                        <span>${device.type} (${id})</span>
                        <div>
                            <button class="btn btn-sm btn-success" onclick="agentClient.sendDeviceCommand('${id}', 'turn_on')">On</button>
                            <button class="btn btn-sm btn-secondary" onclick="agentClient.sendDeviceCommand('${id}', 'turn_off')">Off</button>
                        </div>
                    </div>
                    <small class="text-muted">State: ${device.state || 'unknown'}</small>
                </div>
            `;
        }
        devicesList.innerHTML = html;
    }

    refreshMemories() {
        fetch('/api/memories')
            .then(response => response.json())
            .then(memories => {
                this.updateMemoriesList(memories);
            })
            .catch(error => {
                console.error('Error fetching memories:', error);
            });
    }

    updateMemoriesList(memories) {
        const memoriesList = document.getElementById('memories-list');
        if (!memoriesList) return;

        if (memories.length === 0) {
            memoriesList.innerHTML = '<div class="text-muted">No memories yet...</div>';
            return;
        }

        let html = '';
        memories.forEach(memory => {
            html += `
                <div class="memory-item">
                    <div><strong>${memory.memory_type}</strong></div>
                    <div>${memory.content}</div>
                    <small class="text-muted">${new Date(memory.timestamp).toLocaleString()}</small>
                </div>
            `;
        });
        memoriesList.innerHTML = html;
    }

    refreshExperiences() {
        fetch('/api/experiences')
            .then(response => response.json())
            .then(experiences => {
                this.updateExperiencesList(experiences);
            })
            .catch(error => {
                console.error('Error fetching experiences:', error);
            });
    }

    updateExperiencesList(experiences) {
        const experiencesList = document.getElementById('experiences-list');
        if (!experiencesList) return;

        if (experiences.length === 0) {
            experiencesList.innerHTML = '<div class="text-muted">No experiences yet...</div>';
            return;
        }

        let html = '';
        experiences.forEach(exp => {
            html += `
                <div class="memory-item">
                    <div>${exp.experience}</div>
                    ${exp.outcome ? `<div><strong>Outcome:</strong> ${exp.outcome}</div>` : ''}
                    <small class="text-muted">${new Date(exp.timestamp).toLocaleString()}</small>
                </div>
            `;
        });
        experiencesList.innerHTML = html;
    }

    sendDeviceCommand(deviceId, command) {
        fetch('/api/control-device', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                device_id: deviceId,
                command: command
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Device command response:', data);
            // Refresh device list
            this.refreshDevices();
        })
        .catch(error => {
            console.error('Error sending device command:', error);
        });
    }
}

// Initialize the agent client when the page loads
document.addEventListener('DOMContentLoaded', function() {
    window.agentClient = new AgentClient();
});