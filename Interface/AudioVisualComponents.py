#!/usr/bin/env python3
"""
NEXUS Enhanced Audio-Visual Components
Advanced components with sound effects, animations, and visual feedback using Graphics assets
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGraphicsOpacityEffect, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor, QMovie
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# Get the graphics path
GRAPHICS_PATH = os.path.join(os.path.dirname(__file__), "Graphics")

class SoundManager:
    """Manager for handling sound effects"""
    
    def __init__(self):
        self.player = QMediaPlayer()
        self.activate_sound = os.path.join(GRAPHICS_PATH, "activate.wav")
        self.player.setVolume(70)  # 70% volume
    
    def play_activation_sound(self):
        """Play the activation sound"""
        try:
            if os.path.exists(self.activate_sound):
                url = QUrl.fromLocalFile(self.activate_sound)
                content = QMediaContent(url)
                self.player.setMedia(content)
                self.player.play()
                print("🔊 Playing activation sound")
            else:
                print("❌ Activation sound file not found")
        except Exception as e:
            print(f"❌ Error playing activation sound: {e}")
    
    def set_volume(self, volume):
        """Set the sound volume (0-100)"""
        self.player.setVolume(volume)


class AnimatedJarvisWidget(QWidget):
    """Animated NEXUS assistant with Jarvis.gif"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.jarvis_gif_path = os.path.join(GRAPHICS_PATH, "Jarvis.gif")
        self.setup_ui()
        self.setup_animation()
    
    def setup_ui(self):
        """Setup the animated widget UI"""
        self.setFixedSize(200, 200)
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                border-radius: 100px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        
        # Create the animated label
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignCenter)
        self.animation_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border-radius: 100px;
                border: 2px solid rgba(108, 99, 255, 0.3);
            }
        """)
        self.animation_label.setFixedSize(180, 180)
        
        layout.addWidget(self.animation_label)
        
        # Status label
        self.status_label = QLabel("NEXUS Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                font-weight: 500;
                background: transparent;
                border: none;
                margin-top: 10px;
            }
        """)
        
        layout.addWidget(self.status_label)
    
    def setup_animation(self):
        """Setup the GIF animation"""
        try:
            if os.path.exists(self.jarvis_gif_path):
                self.movie = QMovie(self.jarvis_gif_path)
                self.movie.setScaledSize(self.animation_label.size())
                self.animation_label.setMovie(self.movie)
                
                # Don't start automatically - start when activated
                print("✅ Jarvis animation loaded successfully")
            else:
                print("❌ Jarvis.gif not found, using placeholder")
                self.show_placeholder()
        except Exception as e:
            print(f"❌ Error loading Jarvis animation: {e}")
            self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder when GIF is not available"""
        self.animation_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(108, 99, 255, 0.3), 
                    stop:1 rgba(139, 130, 255, 0.2));
                border: 2px solid rgba(108, 99, 255, 0.5);
                border-radius: 90px;
                color: white;
                font-size: 48px;
                font-weight: 600;
            }
        """)
        self.animation_label.setText("🤖")
        self.animation_label.setAlignment(Qt.AlignCenter)
    
    def start_animation(self):
        """Start the Jarvis animation"""
        try:
            if hasattr(self, 'movie'):
                self.movie.start()
                self.status_label.setText("NEXUS Active")
                self.animation_label.setStyleSheet("""
                    QLabel {
                        background: transparent;
                        border-radius: 90px;
                        border: 2px solid rgba(108, 99, 255, 0.8);
                    }
                """)
                print("🎬 Jarvis animation started")
            else:
                # Animate placeholder
                self.animate_placeholder()
        except Exception as e:
            print(f"❌ Error starting animation: {e}")
    
    def stop_animation(self):
        """Stop the Jarvis animation"""
        try:
            if hasattr(self, 'movie'):
                self.movie.stop()
                self.status_label.setText("NEXUS Ready")
                self.animation_label.setStyleSheet("""
                    QLabel {
                        background: transparent;
                        border-radius: 90px;
                        border: 2px solid rgba(108, 99, 255, 0.3);
                    }
                """)
                print("⏹️ Jarvis animation stopped")
        except Exception as e:
            print(f"❌ Error stopping animation: {e}")
    
    def animate_placeholder(self):
        """Animate the placeholder when GIF is not available"""
        self.animation_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(108, 99, 255, 0.6), 
                    stop:1 rgba(139, 130, 255, 0.4));
                border: 2px solid rgba(108, 99, 255, 0.8);
                border-radius: 90px;
                color: white;
                font-size: 48px;
                font-weight: 600;
            }
        """)
        self.status_label.setText("NEXUS Active")
    
    def set_status(self, status):
        """Update the status label"""
        self.status_label.setText(status)


class EnhancedVoiceControl(QWidget):
    """Enhanced voice control with sound effects and visual feedback"""
    
    voice_activated = pyqtSignal()
    voice_deactivated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sound_manager = SoundManager()
        self.is_listening = False
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the enhanced voice control UI"""
        self.setFixedHeight(100)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(255, 255, 255, 0.08), 
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                color: white;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(20)
        
        # Jarvis animation widget
        self.jarvis_widget = AnimatedJarvisWidget()
        self.jarvis_widget.setFixedSize(70, 70)
        layout.addWidget(self.jarvis_widget)
        
        # Voice control section
        voice_section = QVBoxLayout()
        
        # Microphone button with custom icons
        self.mic_button = QPushButton()
        self.mic_button.setFixedSize(60, 60)
        self.setup_mic_button()
        self.mic_button.clicked.connect(self.toggle_voice_listening)
        self.mic_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Status and instructions
        self.voice_status = QLabel("🎙️ Voice Control Ready")
        self.voice_status.setStyleSheet("""
            color: white; 
            font-size: 16px; 
            font-weight: 600;
            background: transparent;
            border: none;
            padding: 0px;
        """)
        
        self.voice_instruction = QLabel("Click microphone or say 'Hey NEXUS' to activate")
        self.voice_instruction.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7); 
            font-size: 12px;
            background: transparent;
            border: none;
            padding: 0px;
        """)
        
        voice_section.addWidget(self.voice_status)
        voice_section.addWidget(self.voice_instruction)
        
        # Control buttons layout
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.mic_button)
        controls_layout.addLayout(voice_section)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Volume control
        volume_section = self.create_volume_control()
        layout.addWidget(volume_section)
    
    def setup_mic_button(self):
        """Setup microphone button with custom graphics"""
        mic_on_path = os.path.join(GRAPHICS_PATH, "Mic_on.png")
        mic_off_path = os.path.join(GRAPHICS_PATH, "Mic_off.png")
        
        try:
            if os.path.exists(mic_off_path):
                # Load mic off icon
                pixmap = QPixmap(mic_off_path)
                scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QIcon(scaled_pixmap)
                self.mic_button.setIcon(icon)
                self.mic_button.setIconSize(scaled_pixmap.size())
                print("✅ Microphone icons loaded")
            else:
                # Fallback to emoji
                self.mic_button.setText("🎤")
                self.mic_button.setStyleSheet("""
                    QPushButton {
                        font-size: 24px;
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #00D4AA, stop:1 #00B894);
                        border: none;
                        border-radius: 30px;
                        color: white;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #00E6C3, stop:1 #00D4AA);
                    }
                """)
                print("⚠️ Using fallback microphone button")
        except Exception as e:
            print(f"❌ Error setting up mic button: {e}")
            self.mic_button.setText("🎤")
    
    def create_volume_control(self):
        """Create volume control section"""
        volume_widget = QWidget()
        volume_widget.setFixedWidth(120)
        
        volume_layout = QVBoxLayout(volume_widget)
        volume_layout.setContentsMargins(0, 0, 0, 0)
        volume_layout.setSpacing(8)
        
        volume_label = QLabel("🔊 Volume")
        volume_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            font-weight: 500;
            background: transparent;
            border: none;
        """)
        volume_label.setAlignment(Qt.AlignCenter)
        
        # Volume buttons
        volume_buttons = QHBoxLayout()
        volume_buttons.setSpacing(5)
        
        vol_down = QPushButton("🔉")
        vol_down.setFixedSize(30, 30)
        vol_down.clicked.connect(lambda: self.adjust_volume(-10))
        
        vol_up = QPushButton("🔊")
        vol_up.setFixedSize(30, 30)
        vol_up.clicked.connect(lambda: self.adjust_volume(10))
        
        for btn in [vol_down, vol_up]:
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    color: white;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                }
            """)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
        
        volume_buttons.addWidget(vol_down)
        volume_buttons.addWidget(vol_up)
        
        volume_layout.addWidget(volume_label)
        volume_layout.addLayout(volume_buttons)
        
        return volume_widget
    
    def toggle_voice_listening(self):
        """Toggle voice listening with sound effects"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start voice listening with effects"""
        try:
            self.is_listening = True
            
            # Play activation sound
            self.sound_manager.play_activation_sound()
            
            # Update UI
            self.update_mic_button_state(True)
            self.voice_status.setText("🔴 Listening...")
            self.voice_instruction.setText("Speak now or click to stop listening")
            
            # Start Jarvis animation
            self.jarvis_widget.start_animation()
            self.jarvis_widget.set_status("Listening...")
            
            # Emit signal
            self.voice_activated.emit()
            
            # Auto-stop after 15 seconds
            QTimer.singleShot(15000, self.stop_listening)
            
            print("🎙️ Voice listening started with sound effects")
            
        except Exception as e:
            print(f"❌ Error starting voice listening: {e}")
    
    def stop_listening(self):
        """Stop voice listening"""
        try:
            self.is_listening = False
            
            # Update UI
            self.update_mic_button_state(False)
            self.voice_status.setText("🎙️ Voice Control Ready")
            self.voice_instruction.setText("Click microphone or say 'Hey NEXUS' to activate")
            
            # Stop Jarvis animation
            self.jarvis_widget.stop_animation()
            self.jarvis_widget.set_status("NEXUS Ready")
            
            # Emit signal
            self.voice_deactivated.emit()
            
            print("⏹️ Voice listening stopped")
            
        except Exception as e:
            print(f"❌ Error stopping voice listening: {e}")
    
    def update_mic_button_state(self, listening):
        """Update microphone button appearance based on state"""
        mic_on_path = os.path.join(GRAPHICS_PATH, "Mic_on.png")
        mic_off_path = os.path.join(GRAPHICS_PATH, "Mic_off.png")
        
        try:
            if listening and os.path.exists(mic_on_path):
                pixmap = QPixmap(mic_on_path)
                scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QIcon(scaled_pixmap)
                self.mic_button.setIcon(icon)
                self.mic_button.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #FF5E5B, stop:1 #FF3B30);
                        border: none;
                        border-radius: 30px;
                        border: 2px solid rgba(255, 255, 255, 0.3);
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #FF7A77, stop:1 #FF5E5B);
                    }
                """)
            elif not listening and os.path.exists(mic_off_path):
                pixmap = QPixmap(mic_off_path)
                scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QIcon(scaled_pixmap)
                self.mic_button.setIcon(icon)
                self.mic_button.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #00D4AA, stop:1 #00B894);
                        border: none;
                        border-radius: 30px;
                        border: 2px solid rgba(255, 255, 255, 0.2);
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #00E6C3, stop:1 #00D4AA);
                    }
                """)
        except Exception as e:
            print(f"❌ Error updating mic button state: {e}")
    
    def adjust_volume(self, delta):
        """Adjust sound volume"""
        current_volume = self.sound_manager.player.volume()
        new_volume = max(0, min(100, current_volume + delta))
        self.sound_manager.set_volume(new_volume)
        print(f"🔊 Volume adjusted to {new_volume}%")
    
    def activate_voice_command(self, command):
        """Handle voice command activation"""
        self.jarvis_widget.set_status(f"Processing: {command[:20]}...")
        # Process the command here
        QTimer.singleShot(2000, lambda: self.jarvis_widget.set_status("NEXUS Ready"))


class EnhancedButtonFactory:
    """Factory for creating buttons with custom graphics"""
    
    @staticmethod
    def create_icon_button(icon_name, size=(40, 40), tooltip=""):
        """Create a button with custom icon from Graphics folder"""
        button = QPushButton()
        button.setFixedSize(*size)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        
        if tooltip:
            button.setToolTip(tooltip)
        
        # Try to load custom icon
        icon_path = os.path.join(GRAPHICS_PATH, f"{icon_name}.png")
        
        if os.path.exists(icon_path):
            try:
                pixmap = QPixmap(icon_path)
                scaled_pixmap = pixmap.scaled(size[0]-10, size[1]-10, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon = QIcon(scaled_pixmap)
                button.setIcon(icon)
                button.setIconSize(scaled_pixmap.size())
                
                button.setStyleSheet("""
                    QPushButton {
                        background: rgba(255, 255, 255, 0.1);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background: rgba(255, 255, 255, 0.2);
                        border: 1px solid rgba(108, 99, 255, 0.5);
                    }
                    QPushButton:pressed {
                        background: rgba(108, 99, 255, 0.3);
                    }
                """)
                
                print(f"✅ Created button with {icon_name}.png")
                return button
                
            except Exception as e:
                print(f"❌ Error creating icon button for {icon_name}: {e}")
        
        # Fallback to text
        fallback_text = {
            "Home": "🏠",
            "Settings": "⚙️",
            "Close": "❌",
            "Minimize": "➖",
            "Maximize": "⬜",
            "Send": "📤",
            "Stop": "⏹️",
            "Reset": "🔄"
        }
        
        button.setText(fallback_text.get(icon_name, "●"))
        button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(108, 99, 255, 0.5);
            }
            QPushButton:pressed {
                background: rgba(108, 99, 255, 0.3);
            }
        """)
        
        return button


if __name__ == "__main__":
    # This file is meant to be imported, not run directly
    pass