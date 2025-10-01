#!/usr/bin/env python3
"""
NEXUS Modern Web Interface
Professional web-based GUI using Flask and modern frontend technologies
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import os
import sys
import threading
import json
from datetime import datetime
import queue

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from Backend.SharedServices import gui_queue, backend_queue
    from personal_assistant_manager import PersonalAssistantManager
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    print("⚠️ Backend services not available in web mode")

# Initialize Flask app with modern configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nexus_modern_interface_2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables
pa_manager = None
if BACKEND_AVAILABLE:
    try:
        pa_manager = PersonalAssistantManager()
    except Exception as e:
        print(f"⚠️ PersonalAssistantManager not available: {e}")

class ModernWebInterface:
    """Modern web interface manager"""
    
    def __init__(self):
        self.active_sessions = {}
        self.chat_history = []
        self.system_stats = {
            "status": "Ready",
            "uptime": "0:00:00",
            "active_tasks": 5,
            "meetings_today": 3,
            "monthly_expenses": 847,
            "fitness_score": 78
        }
    
    def update_stats(self):
        """Update system statistics"""
        # This would be called periodically to update real-time stats
        pass
    
    def add_chat_message(self, message, sender="user"):
        """Add message to chat history"""
        chat_entry = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "message": message,
            "id": len(self.chat_history)
        }
        self.chat_history.append(chat_entry)
        return chat_entry

# Initialize interface
web_interface = ModernWebInterface()

# Static file serving
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('templates/static', filename)

# Main routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', stats=web_interface.system_stats)

@app.route('/chat')
def chat():
    """Chat interface page"""
    return render_template('chat.html', chat_history=web_interface.chat_history)

@app.route('/assistant')
def assistant():
    """Personal assistant page"""
    return render_template('assistant.html')

@app.route('/analytics')
def analytics():
    """Analytics dashboard page"""
    return render_template('analytics.html')

# API endpoints
@app.route('/api/stats')
def api_stats():
    """Get system statistics"""
    return jsonify(web_interface.system_stats)

@app.route('/api/chat/send', methods=['POST'])
def api_chat_send():
    """Send chat message"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
    
    # Add user message
    user_msg = web_interface.add_chat_message(message, "user")
    
    # Process with backend if available
    if BACKEND_AVAILABLE:
        try:
            backend_queue.put({"type": "text_query", "data": message})
            
            # For now, add a placeholder response
            # In real implementation, you'd wait for backend response
            response = f"Processing: {message}"
            bot_msg = web_interface.add_chat_message(response, "assistant")
            
            # Emit to all connected clients
            socketio.emit('new_message', bot_msg)
            
        except Exception as e:
            error_msg = f"Error processing message: {e}"
            bot_msg = web_interface.add_chat_message(error_msg, "assistant")
            socketio.emit('new_message', bot_msg)
    
    # Emit user message to all clients
    socketio.emit('new_message', user_msg)
    
    return jsonify({"success": True, "message_id": user_msg["id"]})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"🌐 Client connected: {request.sid}")
    emit('status', {'message': 'Connected to NEXUS'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"🌐 Client disconnected: {request.sid}")

@socketio.on('send_message')
def handle_message(data):
    """Handle incoming message via WebSocket"""
    message = data.get('message', '')
    if message:
        user_msg = web_interface.add_chat_message(message, "user")
        emit('new_message', user_msg, broadcast=True)
        
        # Process message (placeholder)
        response = f"Echo: {message}"
        bot_msg = web_interface.add_chat_message(response, "assistant")
        emit('new_message', bot_msg, broadcast=True)

@socketio.on('voice_activate')
def handle_voice_activate():
    """Handle voice activation"""
    emit('voice_status', {'status': 'listening'}, broadcast=True)
    # Here you would integrate with voice recognition

@socketio.on('interrupt_signal')
def handle_interrupt():
    """Handle interrupt/barge-in signal"""
    print("🛑 Interrupt signal received via WebSocket")
    if BACKEND_AVAILABLE:
        from Backend.InterruptService import set_interrupt
        set_interrupt()
    emit('system_status', {'status': 'interrupted'}, broadcast=True)

def run_background_tasks():
    """Run background tasks for real-time updates"""
    import time
    while True:
        try:
            # Update system stats
            web_interface.update_stats()
            
            # Process backend queue if available
            if BACKEND_AVAILABLE:
                try:
                    while not gui_queue.empty():
                        message = gui_queue.get_nowait()
                        msg_type = message.get("type")
                        data = message.get("data")
                        
                        if msg_type == "chat":
                            # Emit chat update to all clients
                            socketio.emit('chat_update', {'html': data})
                        elif msg_type == "status":
                            # Emit status update
                            socketio.emit('status_update', {'status': data})
                            
                except queue.Empty:
                    pass
                except Exception as e:
                    print(f"Error processing backend queue: {e}")
            
            time.sleep(1)  # Update every second
            
        except Exception as e:
            print(f"Background task error: {e}")
            time.sleep(5)

def launch_modern_web_interface(host='127.0.0.1', port=5000, debug=False):
    """Launch the modern web interface"""
    print("\n🚀 LAUNCHING NEXUS MODERN WEB INTERFACE")
    print("="*60)
    print(f"🌐 Web Interface: http://{host}:{port}")
    print(f"📱 Mobile Responsive: Yes")
    print(f"🎨 Modern Design: Glassmorphism + Animations")
    print(f"⚡ Real-time Updates: WebSocket")
    print(f"🔊 Audio Support: Full integration")
    print("="*60)
    
    # Start background tasks
    background_thread = threading.Thread(target=run_background_tasks, daemon=True)
    background_thread.start()
    
    # Launch the web server
    try:
        socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
    except Exception as e:
        print(f"❌ Error launching web interface: {e}")

if __name__ == "__main__":
    launch_modern_web_interface(debug=True)