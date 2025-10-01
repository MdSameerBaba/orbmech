// NEXUS Chat Interface - Enhanced Chat Functionality

class NEXUSChat {
    constructor() {
        this.messages = [];
        this.isTyping = false;
        this.recognition = null;
        this.socket = io();
        
        this.init();
    }
    
    init() {
        console.log('💬 NEXUS Chat Interface Initializing...');
        
        this.setupEventListeners();
        this.setupWebSocket();
        this.setupVoiceRecognition();
        this.setupAutoResize();
        this.loadChatHistory();
        
        console.log('✅ NEXUS Chat Interface Ready');
    }
    
    setupEventListeners() {
        // Send button
        const sendBtn = document.getElementById('sendBtn');
        const chatInput = document.getElementById('chatInput');
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send (Shift+Enter for new line)
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Voice input button
        const voiceInputBtn = document.getElementById('voiceInputBtn');
        voiceInputBtn.addEventListener('click', () => this.toggleVoiceInput());
        
        // Quick prompt buttons
        document.querySelectorAll('.prompt-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const prompt = btn.dataset.prompt;
                this.sendMessage(prompt);
            });
        });
        
        // Suggestion buttons
        document.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const suggestion = btn.textContent;
                chatInput.value = suggestion;
                chatInput.focus();
            });
        });
        
        // Clear chat button
        const clearChatBtn = document.getElementById('clearChatBtn');
        if (clearChatBtn) {
            clearChatBtn.addEventListener('click', () => this.clearChat());
        }
        
        // Export chat button
        const exportChatBtn = document.getElementById('exportChatBtn');
        if (exportChatBtn) {
            exportChatBtn.addEventListener('click', () => this.exportChat());
        }
        
        // Input focus effects
        chatInput.addEventListener('focus', () => {
            document.querySelector('.chat-input-wrapper').classList.add('focused');
        });
        
        chatInput.addEventListener('blur', () => {
            document.querySelector('.chat-input-wrapper').classList.remove('focused');
        });
    }
    
    setupWebSocket() {
        this.socket.on('connect', () => {
            console.log('🌐 Chat connected to NEXUS server');
            this.addSystemMessage('Connected to NEXUS', 'success');
        });
        
        this.socket.on('disconnect', () => {
            console.log('🌐 Chat disconnected from server');
            this.addSystemMessage('Disconnected from server', 'error');
        });
        
        this.socket.on('new_message', (data) => {
            this.receiveMessage(data);
        });
        
        this.socket.on('typing_start', () => {
            this.showTypingIndicator();
        });
        
        this.socket.on('typing_stop', () => {
            this.hideTypingIndicator();
        });
    }
    
    setupVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                console.log('🎤 Voice recognition started');
                this.updateVoiceInputButton(true);
            };
            
            this.recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                
                const chatInput = document.getElementById('chatInput');
                chatInput.value = transcript;
                
                if (event.results[event.resultIndex].isFinal) {
                    console.log('🗣️ Voice input complete:', transcript);
                    // Auto-send after voice input
                    setTimeout(() => this.sendMessage(), 500);
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('🎤 Voice recognition error:', event.error);
                this.updateVoiceInputButton(false);
                this.showNotification('Voice recognition error', 'error');
            };
            
            this.recognition.onend = () => {
                console.log('🎤 Voice recognition ended');
                this.updateVoiceInputButton(false);
            };
        }
    }
    
    setupAutoResize() {
        const chatInput = document.getElementById('chatInput');
        
        chatInput.addEventListener('input', () => {
            // Auto-resize textarea
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
            
            // Update send button state
            const sendBtn = document.getElementById('sendBtn');
            if (chatInput.value.trim()) {
                sendBtn.classList.add('has-content');
            } else {
                sendBtn.classList.remove('has-content');
            }
        });
    }
    
    sendMessage(text = null) {
        const chatInput = document.getElementById('chatInput');
        const message = text || chatInput.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        if (!text) {
            chatInput.value = '';
            chatInput.style.height = 'auto';
            document.getElementById('sendBtn').classList.remove('has-content');
        }
        
        // Send to server
        this.socket.emit('send_message', { message });
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Hide quick prompts after first message
        this.hideWelcomeMessage();
    }
    
    receiveMessage(data) {
        this.hideTypingIndicator();
        
        if (data.sender === 'assistant') {
            this.addMessage(data.message, 'assistant', data.timestamp);
        }
    }
    
    addMessage(text, sender, timestamp = null) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageElement = this.createMessageElement(text, sender, timestamp);
        
        messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
        
        // Store message
        this.messages.push({
            text,
            sender,
            timestamp: timestamp || new Date().toISOString()
        });
        
        // Animate message appearance
        setTimeout(() => {
            messageElement.classList.add('visible');
        }, 50);
    }
    
    createMessageElement(text, sender, timestamp = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;
        
        const time = timestamp ? new Date(timestamp) : new Date();
        const timeString = time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-text">${this.formatMessage(text)}</div>
                    <div class="message-time">${timeString}</div>
                </div>
                <div class="message-avatar">
                    <i class="fas fa-user"></i>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-text">${this.formatMessage(text)}</div>
                    <div class="message-time">${timeString}</div>
                    <div class="message-actions">
                        <button class="action-btn" onclick="nexusChat.copyMessage(this)" title="Copy">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button class="action-btn" onclick="nexusChat.speakMessage(this)" title="Speak">
                            <i class="fas fa-volume-up"></i>
                        </button>
                    </div>
                </div>
            `;
        }
        
        return messageDiv;
    }
    
    formatMessage(text) {
        // Basic markdown-like formatting
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');
        text = text.replace(/\n/g, '<br>');
        
        // Auto-link URLs
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        text = text.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener">$1</a>');
        
        return text;
    }
    
    addSystemMessage(text, type = 'info') {
        const messagesContainer = document.getElementById('chatMessages');
        const systemMessage = document.createElement('div');
        systemMessage.className = `system-message system-${type}`;
        systemMessage.innerHTML = `
            <div class="system-content">
                <i class="fas fa-${this.getSystemIcon(type)}"></i>
                <span>${text}</span>
            </div>
        `;
        
        messagesContainer.appendChild(systemMessage);
        this.scrollToBottom();
    }
    
    getSystemIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    showTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.style.display = 'flex';
            this.scrollToBottom();
            this.isTyping = true;
        }
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.style.display = 'none';
            this.isTyping = false;
        }
    }
    
    hideWelcomeMessage() {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.display = 'none';
        }
    }
    
    toggleVoiceInput() {
        if (!this.recognition) {
            this.showNotification('Voice recognition not supported', 'error');
            return;
        }
        
        if (this.recognition && this.recognition.state === 'listening') {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }
    
    updateVoiceInputButton(isListening) {
        const voiceBtn = document.getElementById('voiceInputBtn');
        if (voiceBtn) {
            if (isListening) {
                voiceBtn.classList.add('listening');
                voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
            } else {
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            }
        }
    }
    
    scrollToBottom() {
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
    
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.innerHTML = '';
            this.messages = [];
            
            // Show welcome message again
            const welcomeMessage = document.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.style.display = 'flex';
            }
            
            this.showNotification('Chat cleared', 'success');
        }
    }
    
    exportChat() {
        if (this.messages.length === 0) {
            this.showNotification('No messages to export', 'warning');
            return;
        }
        
        const chatData = {
            exportDate: new Date().toISOString(),
            messages: this.messages
        };
        
        const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `nexus-chat-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
        this.showNotification('Chat exported successfully', 'success');
    }
    
    loadChatHistory() {
        // Load chat history from server if available
        fetch('/api/chat/history')
            .then(response => response.json())
            .then(data => {
                if (data.messages && data.messages.length > 0) {
                    this.hideWelcomeMessage();
                    data.messages.forEach(msg => {
                        this.addMessage(msg.message, msg.sender, msg.timestamp);
                    });
                }
            })
            .catch(error => {
                console.log('No chat history available:', error);
            });
    }
    
    copyMessage(button) {
        const messageText = button.closest('.message-content').querySelector('.message-text').textContent;
        navigator.clipboard.writeText(messageText).then(() => {
            this.showNotification('Message copied to clipboard', 'success');
        });
    }
    
    speakMessage(button) {
        const messageText = button.closest('.message-content').querySelector('.message-text').textContent;
        
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(messageText);
            utterance.rate = 0.9;
            utterance.pitch = 1.0;
            utterance.volume = 0.8;
            
            speechSynthesis.speak(utterance);
            this.showNotification('Speaking message...', 'info');
        } else {
            this.showNotification('Text-to-speech not supported', 'error');
        }
    }
    
    showNotification(message, type = 'info') {
        // Reuse notification system from main app
        if (window.nexusApp) {
            window.nexusApp.showNotification(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.nexusChat = new NEXUSChat();
});

// Add chat-specific styles
const chatStyles = `
/* Chat-specific styles */
.chat-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 120px);
    background: var(--glass-primary);
    backdrop-filter: blur(20px);
    border-radius: var(--radius-xl);
    margin: var(--spacing-lg);
    border: 1px solid var(--glass-border);
    overflow: hidden;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-lg);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.chat-message {
    display: flex;
    gap: var(--spacing-md);
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.3s ease;
    margin-bottom: var(--spacing-md);
}

.chat-message.visible {
    opacity: 1;
    transform: translateY(0);
}

.user-message {
    flex-direction: row-reverse;
}

.message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 1.1rem;
}

.user-message .message-avatar {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    color: white;
}

.assistant-message .message-avatar {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    color: var(--primary-color);
}

.message-content {
    max-width: 70%;
    background: var(--glass-secondary);
    border-radius: var(--radius-lg);
    padding: var(--spacing-md);
    position: relative;
    border: 1px solid var(--glass-border);
}

.user-message .message-content {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    border: none;
}

.message-text {
    margin-bottom: var(--spacing-sm);
    line-height: 1.5;
}

.message-time {
    font-size: 0.75rem;
    opacity: 0.7;
    text-align: right;
}

.user-message .message-time {
    text-align: left;
}

.message-actions {
    display: flex;
    gap: var(--spacing-xs);
    margin-top: var(--spacing-sm);
    opacity: 0;
    transition: opacity 0.2s ease;
}

.message-content:hover .message-actions {
    opacity: 1;
}

.action-btn {
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    padding: var(--spacing-xs);
    border-radius: var(--radius-sm);
    transition: all 0.2s ease;
}

.action-btn:hover {
    color: var(--primary-color);
    background: var(--glass-secondary);
}

.welcome-message {
    display: flex;
    gap: var(--spacing-lg);
    padding: var(--spacing-xl);
    background: var(--glass-secondary);
    border-radius: var(--radius-lg);
    border: 1px solid var(--glass-border);
    margin-bottom: var(--spacing-lg);
}

.welcome-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: white;
    flex-shrink: 0;
}

.welcome-content h3 {
    margin-bottom: var(--spacing-sm);
    color: var(--primary-color);
}

.welcome-content p {
    margin-bottom: var(--spacing-lg);
    opacity: 0.8;
}

.quick-prompts {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
}

.prompt-btn {
    background: var(--glass-primary);
    border: 1px solid var(--glass-border);
    color: white;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: 0.875rem;
}

.prompt-btn:hover {
    background: var(--primary-color);
    border-color: var(--primary-color);
    transform: translateY(-2px);
}

.typing-indicator {
    display: flex;
    gap: var(--spacing-md);
    align-items: center;
    padding: var(--spacing-md);
    opacity: 0.8;
}

.typing-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--primary-color);
}

.typing-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    background: var(--primary-color);
    border-radius: 50%;
    animation: typingDots 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typingDots {
    0%, 80%, 100% {
        transform: scale(0);
        opacity: 0.5;
    }
    40% {
        transform: scale(1);
        opacity: 1;
    }
}

.chat-input-container {
    border-top: 1px solid var(--glass-border);
    padding: var(--spacing-lg);
    background: var(--glass-secondary);
}

.chat-input-wrapper {
    display: flex;
    align-items: flex-end;
    gap: var(--spacing-sm);
    background: var(--glass-primary);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-sm);
    transition: all 0.2s ease;
}

.chat-input-wrapper.focused {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2);
}

.input-actions-left,
.input-actions-right {
    display: flex;
    gap: var(--spacing-xs);
}

.chat-input {
    flex: 1;
    background: none;
    border: none;
    color: white;
    padding: var(--spacing-sm);
    font-family: var(--font-primary);
    font-size: 0.9rem;
    resize: none;
    min-height: 20px;
    max-height: 120px;
    overflow-y: auto;
}

.chat-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.chat-input:focus {
    outline: none;
}

.input-action-btn {
    width: 36px;
    height: 36px;
    border: none;
    background: var(--glass-secondary);
    color: rgba(255, 255, 255, 0.7);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.input-action-btn:hover {
    background: var(--glass-primary);
    color: var(--primary-color);
}

.voice-input-btn.listening {
    background: var(--error-color);
    color: white;
    animation: pulse 1s infinite;
}

.send-btn {
    width: 36px;
    height: 36px;
    border: none;
    background: var(--glass-secondary);
    color: rgba(255, 255, 255, 0.5);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.send-btn.has-content {
    background: var(--primary-color);
    color: white;
}

.send-btn:hover {
    transform: scale(1.05);
}

.input-suggestions {
    display: flex;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-sm);
    flex-wrap: wrap;
}

.suggestion-btn {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    color: rgba(255, 255, 255, 0.7);
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.8rem;
}

.suggestion-btn:hover {
    background: var(--glass-primary);
    color: var(--primary-color);
    border-color: var(--primary-color);
}

.system-message {
    display: flex;
    justify-content: center;
    margin: var(--spacing-md) 0;
}

.system-content {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: 0.875rem;
    opacity: 0.8;
}

.system-success .system-content {
    border-color: var(--success-color);
    color: var(--success-color);
}

.system-error .system-content {
    border-color: var(--error-color);
    color: var(--error-color);
}

.chat-controls {
    display: flex;
    gap: var(--spacing-sm);
}

.control-btn {
    background: var(--glass-secondary);
    border: 1px solid var(--glass-border);
    color: rgba(255, 255, 255, 0.8);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: 0.875rem;
}

.control-btn:hover {
    background: var(--glass-primary);
    color: white;
    border-color: var(--primary-color);
}

/* Responsive */
@media (max-width: 768px) {
    .message-content {
        max-width: 85%;
    }
    
    .quick-prompts {
        flex-direction: column;
    }
}
`;

// Add chat styles to document
const chatStyleSheet = document.createElement('style');
chatStyleSheet.textContent = chatStyles;
document.head.appendChild(chatStyleSheet);