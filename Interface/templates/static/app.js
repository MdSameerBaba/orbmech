// NEXUS Modern Web Interface - Interactive JavaScript

class NEXUSWebApp {
    constructor() {
        this.socket = io();
        this.isListening = false;
        this.currentPage = 'dashboard';
        this.jarvisActive = false;
        
        this.init();
    }
    
    init() {
        console.log('🚀 NEXUS Web Interface Initializing...');
        
        // Initialize components
        this.setupEventListeners();
        this.setupWebSocket();
        this.startRealTimeUpdates();
        this.setupVoiceControl();
        
        console.log('✅ NEXUS Web Interface Ready');
    }
    
    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateTo(item.dataset.page, item.href);
            });
        });
        
        // Voice control button
        const voiceBtn = document.getElementById('voiceBtn');
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => this.toggleVoiceControl());
        }
        
        // Interrupt button
        const interruptBtn = document.getElementById('interruptBtn');
        if (interruptBtn) {
            interruptBtn.addEventListener('click', () => this.sendInterrupt());
        }
        
        // Quick action buttons
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.executeQuickAction(action);
            });
        });
        
        // Mobile menu toggle (if needed)
        this.setupMobileMenu();
    }
    
    setupWebSocket() {
        this.socket.on('connect', () => {
            console.log('🌐 Connected to NEXUS server');
            this.showNotification('Connected to NEXUS', 'success');
        });
        
        this.socket.on('disconnect', () => {
            console.log('🌐 Disconnected from NEXUS server');
            this.showNotification('Disconnected from server', 'error');
        });
        
        this.socket.on('status', (data) => {
            console.log('📡 Status update:', data);
        });
        
        this.socket.on('new_message', (data) => {
            this.handleNewMessage(data);
        });
        
        this.socket.on('voice_status', (data) => {
            this.updateVoiceStatus(data.status);
        });
        
        this.socket.on('system_status', (data) => {
            this.updateSystemStatus(data);
        });
    }
    
    startRealTimeUpdates() {
        // Update time and date
        this.updateDateTime();
        setInterval(() => this.updateDateTime(), 1000);
        
        // Update system stats periodically
        setInterval(() => this.updateStats(), 30000);
        
        // Animate floating orbs
        this.animateOrbs();
    }
    
    updateDateTime() {
        const now = new Date();
        const timeElement = document.getElementById('currentTime');
        const dateElement = document.getElementById('currentDate');
        
        if (timeElement) {
            timeElement.textContent = now.toLocaleTimeString();
        }
        
        if (dateElement) {
            dateElement.textContent = now.toLocaleDateString();
        }
    }
    
    updateStats() {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                // Update dashboard stats if we're on dashboard page
                if (this.currentPage === 'dashboard') {
                    this.refreshDashboardStats(data);
                }
            })
            .catch(error => console.error('Error updating stats:', error));
    }
    
    setupVoiceControl() {
        // Check if Web Speech API is available
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.recognition.continuous = true;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                console.log('🎤 Voice recognition started');
                this.updateVoiceStatus('listening');
            };
            
            this.recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                
                if (event.results[event.resultIndex].isFinal) {
                    console.log('🗣️ Voice input:', transcript);
                    this.processVoiceCommand(transcript);
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('🎤 Voice recognition error:', event.error);
                this.updateVoiceStatus('error');
            };
            
            this.recognition.onend = () => {
                console.log('🎤 Voice recognition ended');
                this.updateVoiceStatus('ready');
                this.isListening = false;
            };
        } else {
            console.warn('🎤 Web Speech API not supported');
        }
    }
    
    toggleVoiceControl() {
        const voiceBtn = document.getElementById('voiceBtn');
        
        if (!this.recognition) {
            this.showNotification('Voice recognition not supported', 'error');
            return;
        }
        
        if (this.isListening) {
            this.recognition.stop();
            voiceBtn.classList.remove('active');
            this.isListening = false;
        } else {
            this.recognition.start();
            voiceBtn.classList.add('active');
            this.isListening = true;
            this.showJarvisAnimation();
        }
        
        // Emit to server
        this.socket.emit('voice_activate');
    }
    
    processVoiceCommand(command) {
        console.log('🎯 Processing voice command:', command);
        
        // Send to server for processing
        this.socket.emit('send_message', { message: command });
        
        // Hide Jarvis animation
        this.hideJarvisAnimation();
    }
    
    updateVoiceStatus(status) {
        const voiceStatus = document.querySelector('.voice-status');
        const voiceBtn = document.getElementById('voiceBtn');
        
        if (voiceStatus) {
            switch (status) {
                case 'listening':
                    voiceStatus.textContent = 'Listening...';
                    if (voiceBtn) voiceBtn.classList.add('active');
                    break;
                case 'processing':
                    voiceStatus.textContent = 'Processing...';
                    break;
                case 'error':
                    voiceStatus.textContent = 'Error occurred';
                    if (voiceBtn) voiceBtn.classList.remove('active');
                    break;
                default:
                    voiceStatus.textContent = 'Ready to listen';
                    if (voiceBtn) voiceBtn.classList.remove('active');
            }
        }
    }
    
    sendInterrupt() {
        console.log('🛑 Sending interrupt signal');
        this.socket.emit('interrupt_signal');
        this.showNotification('Interrupt signal sent', 'warning');
        
        // Stop voice recognition if active
        if (this.isListening && this.recognition) {
            this.recognition.stop();
        }
        
        // Hide Jarvis animation
        this.hideJarvisAnimation();
    }
    
    executeQuickAction(action) {
        console.log('⚡ Executing quick action:', action);
        
        const actionMessages = {
            'schedule-meeting': 'Schedule a new meeting for me',
            'send-email': 'Help me send an email',
            'add-expense': 'Add a new expense to my budget',
            'check-weather': 'What\'s the weather like today?'
        };
        
        const message = actionMessages[action] || `Execute ${action}`;
        
        // Send to server
        this.socket.emit('send_message', { message });
        
        // Show loading state
        this.showNotification(`Executing: ${action.replace('-', ' ')}`, 'info');
        
        // Show Jarvis animation briefly
        this.showJarvisAnimation();
        setTimeout(() => this.hideJarvisAnimation(), 2000);
    }
    
    navigateTo(page, url) {
        console.log('🧭 Navigating to:', page);
        
        // Update active nav item
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.page === page) {
                item.classList.add('active');
            }
        });
        
        this.currentPage = page;
        
        // Navigate to URL if provided
        if (url && url !== '#') {
            window.location.href = url;
        }
    }
    
    showJarvisAnimation() {
        const overlay = document.getElementById('jarvisOverlay');
        if (overlay) {
            overlay.classList.add('active');
            this.jarvisActive = true;
            
            // Play activation sound if available
            this.playActivationSound();
        }
    }
    
    hideJarvisAnimation() {
        const overlay = document.getElementById('jarvisOverlay');
        if (overlay) {
            overlay.classList.remove('active');
            this.jarvisActive = false;
        }
    }
    
    playActivationSound() {
        // Try to play activation sound
        try {
            const audio = new Audio('/static/activate.wav');
            audio.volume = 0.3;
            audio.play().catch(e => console.log('Could not play activation sound:', e));
        } catch (e) {
            console.log('Activation sound not available');
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 16px 20px;
            color: white;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            max-width: 350px;
        `;
        
        // Add notification-specific colors
        const colors = {
            success: '#00ff88',
            error: '#ff4757',
            warning: '#ffaa00',
            info: '#00d4ff'
        };
        
        if (colors[type]) {
            notification.style.borderLeftColor = colors[type];
            notification.style.borderLeftWidth = '4px';
        }
        
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    animateOrbs() {
        const orbs = document.querySelectorAll('.orb');
        orbs.forEach((orb, index) => {
            // Add random movement
            setInterval(() => {
                const x = Math.random() * 100;
                const y = Math.random() * 100;
                orb.style.transform = `translate(${x}px, ${y}px)`;
            }, 3000 + index * 1000);
        });
    }
    
    setupMobileMenu() {
        // Add mobile menu toggle if screen is small
        if (window.innerWidth <= 768) {
            // Mobile menu implementation would go here
            console.log('📱 Mobile view detected');
        }
    }
    
    handleNewMessage(data) {
        console.log('💬 New message received:', data);
        
        // Show notification for new messages
        if (data.sender === 'assistant') {
            this.showNotification('New message from NEXUS', 'info');
        }
    }
    
    updateSystemStatus(data) {
        console.log('⚙️ System status update:', data);
        
        if (data.status === 'interrupted') {
            this.showNotification('System interrupted', 'warning');
        }
    }
    
    refreshDashboardStats(data) {
        // Update stat cards with new data
        console.log('📊 Refreshing dashboard stats:', data);
    }
}

// CSS for notifications
const notificationStyles = `
@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOut {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

.notification-content {
    display: flex;
    align-items: center;
    gap: 12px;
}

.notification-content i {
    font-size: 1.2rem;
}
`;

// Add notification styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.nexusApp = new NEXUSWebApp();
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (window.nexusApp && window.nexusApp.socket) {
        window.nexusApp.socket.disconnect();
    }
});