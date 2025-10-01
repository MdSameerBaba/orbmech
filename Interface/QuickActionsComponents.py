#!/usr/bin/env python3
"""
NEXUS Quick Actions Components
Smart shortcuts and quick actions for common personal assistant tasks
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGridLayout, QScrollArea, QProgressBar, QLineEdit, QComboBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

# Try to import personal assistant
try:
    from personal_assistant_manager import PersonalAssistantManager
    PERSONAL_ASSISTANT_AVAILABLE = True
except ImportError:
    PERSONAL_ASSISTANT_AVAILABLE = False

class QuickActionButton(QPushButton):
    """Enhanced button with modern styling and hover effects"""
    
    def __init__(self, icon, title, subtitle="", action_callback=None):
        super().__init__()
        self.icon = icon
        self.title = title
        self.subtitle = subtitle
        self.action_callback = action_callback
        
        self.setup_ui()
        
        if action_callback:
            self.clicked.connect(action_callback)
    
    def setup_ui(self):
        """Setup the button UI"""
        self.setFixedSize(160, 120)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Create layout for button content
        self.setText("")  # Clear default text
        
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(255, 255, 255, 0.05), 
                    stop:1 rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                color: white;
                font-weight: 500;
                padding: 15px;
                text-align: left;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(108, 99, 255, 0.2), 
                    stop:1 rgba(139, 130, 255, 0.1));
                border: 1px solid rgba(108, 99, 255, 0.3);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(108, 99, 255, 0.3), 
                    stop:1 rgba(139, 130, 255, 0.2));
            }
        """)
        
        # Set tooltip
        if self.subtitle:
            self.setToolTip(f"{self.title}\n{self.subtitle}")
        else:
            self.setToolTip(self.title)
    
    def paintEvent(self, event):
        """Custom paint event to draw icon and text"""
        super().paintEvent(event)
        
        from PyQt5.QtGui import QPainter, QFont
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw icon
        icon_font = QFont()
        icon_font.setPointSize(24)
        painter.setFont(icon_font)
        painter.setPen(Qt.white)
        
        icon_rect = self.rect()
        icon_rect.setHeight(50)
        painter.drawText(icon_rect, Qt.AlignCenter, self.icon)
        
        # Draw title
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setWeight(QFont.Bold)
        painter.setFont(title_font)
        
        title_rect = self.rect()
        title_rect.setTop(55)
        title_rect.setHeight(25)
        painter.drawText(title_rect, Qt.AlignCenter, self.title)
        
        # Draw subtitle if exists
        if self.subtitle:
            subtitle_font = QFont()
            subtitle_font.setPointSize(9)
            painter.setFont(subtitle_font)
            painter.setPen(Qt.lightGray)
            
            subtitle_rect = self.rect()
            subtitle_rect.setTop(80)
            subtitle_rect.setHeight(30)
            painter.drawText(subtitle_rect, Qt.AlignCenter | Qt.TextWordWrap, self.subtitle)


class SmartQuickActions(QWidget):
    """Smart quick actions widget with AI-powered suggestions"""
    
    action_executed = pyqtSignal(str, str)  # action_type, details
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pa_manager = None
        if PERSONAL_ASSISTANT_AVAILABLE:
            try:
                self.pa_manager = PersonalAssistantManager()
            except Exception as e:
                print(f"Error initializing PersonalAssistantManager: {e}")
        
        self.setup_ui()
        self.setup_timer()
    
    def setup_ui(self):
        """Setup the quick actions UI"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(255, 255, 255, 0.05), 
                    stop:1 rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                color: white;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header
        header = QLabel("⚡ Quick Actions")
        header.setStyleSheet("""
            color: white; 
            font-size: 20px; 
            font-weight: 600;
            margin-bottom: 10px;
            padding: 0px;
            background: transparent;
            border: none;
        """)
        layout.addWidget(header)
        
        # Actions grid
        actions_scroll = QScrollArea()
        actions_scroll.setWidgetResizable(True)
        actions_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.5);
            }
        """)
        
        actions_widget = QWidget()
        self.actions_layout = QGridLayout(actions_widget)
        self.actions_layout.setSpacing(15)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create action buttons
        self.create_action_buttons()
        
        actions_scroll.setWidget(actions_widget)
        layout.addWidget(actions_scroll)
        
        # Smart suggestions
        suggestions_label = QLabel("💡 Smart Suggestions")
        suggestions_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 14px; 
            font-weight: 500;
            margin-top: 10px;
            padding: 0px;
            background: transparent;
            border: none;
        """)
        layout.addWidget(suggestions_label)
        
        self.suggestions_widget = QWidget()
        self.suggestions_layout = QVBoxLayout(self.suggestions_widget)
        self.suggestions_layout.setSpacing(8)
        self.suggestions_layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.suggestions_widget)
        
        # Load smart suggestions
        self.load_smart_suggestions()
    
    def create_action_buttons(self):
        """Create the action buttons grid"""
        actions = [
            # Row 1
            ("📅", "Schedule", "Quick event", self.quick_schedule),
            ("📋", "Add Task", "To-do item", self.quick_task),
            ("💰", "Log Expense", "Track spending", self.quick_expense),
            
            # Row 2
            ("👥", "Add Contact", "New person", self.quick_contact),
            ("🏃", "Log Health", "Fitness data", self.quick_health),
            ("📊", "Check Stats", "View analytics", self.quick_stats),
            
            # Row 3
            ("🔍", "Smart Search", "Find anything", self.smart_search),
            ("🎯", "Set Goal", "New objective", self.quick_goal),
            ("📱", "Quick Note", "Save thought", self.quick_note),
        ]
        
        row = 0
        col = 0
        for icon, title, subtitle, callback in actions:
            button = QuickActionButton(icon, title, subtitle, callback)
            self.actions_layout.addWidget(button, row, col)
            
            col += 1
            if col >= 3:  # 3 columns
                col = 0
                row += 1
    
    def quick_schedule(self):
        """Quick schedule action"""
        self.action_executed.emit("schedule", "Opening quick schedule...")
        if self.pa_manager:
            result = self.pa_manager.process_personal_assistant_query("schedule quick meeting tomorrow 2pm")
            print(f"Quick schedule result: {result}")
    
    def quick_task(self):
        """Quick task action"""
        self.action_executed.emit("task", "Adding quick task...")
        if self.pa_manager:
            result = self.pa_manager.process_personal_assistant_query("add task review code priority high")
            print(f"Quick task result: {result}")
    
    def quick_expense(self):
        """Quick expense action"""
        self.action_executed.emit("expense", "Logging quick expense...")
        if self.pa_manager:
            result = self.pa_manager.process_personal_assistant_query("add expense $15 coffee")
            print(f"Quick expense result: {result}")
    
    def quick_contact(self):
        """Quick contact action"""
        self.action_executed.emit("contact", "Adding quick contact...")
        if self.pa_manager:
            result = self.pa_manager.process_personal_assistant_query("show contacts")
            print(f"Quick contact result: {result}")
    
    def quick_health(self):
        """Quick health action"""
        self.action_executed.emit("health", "Logging health data...")
        if self.pa_manager:
            result = self.pa_manager.process_personal_assistant_query("log 8000 steps today")
            print(f"Quick health result: {result}")
    
    def quick_stats(self):
        """Quick stats action"""
        self.action_executed.emit("stats", "Checking statistics...")
        if self.pa_manager:
            result = self.pa_manager.process_personal_assistant_query("show my stats")
            print(f"Quick stats result: {result}")
    
    def smart_search(self):
        """Smart search action"""
        self.action_executed.emit("search", "Opening smart search...")
        # This could open a search dialog or interface
        print("Smart search activated")
    
    def quick_goal(self):
        """Quick goal action"""
        self.action_executed.emit("goal", "Setting new goal...")
        if self.pa_manager:
            result = self.pa_manager.process_personal_assistant_query("set goal exercise 5 times this week")
            print(f"Quick goal result: {result}")
    
    def quick_note(self):
        """Quick note action"""
        self.action_executed.emit("note", "Saving quick note...")
        # This could open a note input dialog
        print("Quick note activated")
    
    def load_smart_suggestions(self):
        """Load AI-powered smart suggestions"""
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime("%A")
        
        # Time-based suggestions
        suggestions = []
        
        if 6 <= current_hour < 12:
            suggestions.append("🌅 Good morning! Don't forget to log your morning routine")
            suggestions.append("☕ Log your breakfast and morning coffee")
        elif 12 <= current_hour < 17:
            suggestions.append("🍽️ Time to log your lunch expense")
            suggestions.append("📊 Check your daily progress")
        elif 17 <= current_hour < 22:
            suggestions.append("🏃 Log your evening workout")
            suggestions.append("📝 Review today's tasks")
        else:
            suggestions.append("😴 Time to log your sleep hours")
            suggestions.append("📋 Plan tomorrow's tasks")
        
        # Day-based suggestions
        if current_day == "Monday":
            suggestions.append("📅 Plan your week ahead")
        elif current_day == "Friday":
            suggestions.append("📊 Review this week's achievements")
        elif current_day in ["Saturday", "Sunday"]:
            suggestions.append("🎬 Add weekend entertainment to your list")
        
        # Add suggestion items
        for suggestion in suggestions[:3]:  # Show top 3 suggestions
            self.add_suggestion_item(suggestion)
    
    def add_suggestion_item(self, suggestion):
        """Add a suggestion item to the widget"""
        suggestion_item = QWidget()
        suggestion_item.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 5px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(108, 99, 255, 0.3);
            }
        """)
        suggestion_item.setFixedHeight(40)
        suggestion_item.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QHBoxLayout(suggestion_item)
        layout.setContentsMargins(10, 5, 10, 5)
        
        suggestion_label = QLabel(suggestion)
        suggestion_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            background: transparent;
            border: none;
            padding: 0px;
        """)
        
        layout.addWidget(suggestion_label)
        layout.addStretch()
        
        self.suggestions_layout.addWidget(suggestion_item)
    
    def setup_timer(self):
        """Setup timer for periodic updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_suggestions)
        self.update_timer.start(300000)  # Update every 5 minutes
    
    def update_suggestions(self):
        """Update smart suggestions periodically"""
        # Clear existing suggestions
        for i in reversed(range(self.suggestions_layout.count())):
            child = self.suggestions_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Reload suggestions
        self.load_smart_suggestions()


class VoiceControlWidget(QWidget):
    """Voice control interface with visual feedback"""
    
    voice_activated = pyqtSignal()
    voice_command = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_listening = False
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the voice control UI"""
        self.setFixedHeight(80)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(255, 255, 255, 0.05), 
                    stop:1 rgba(255, 255, 255, 0.02));
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                color: white;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Voice button
        self.voice_button = QPushButton("🎤")
        self.voice_button.setFixedSize(50, 50)
        self.voice_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #00D4AA, stop:1 #00B894);
                border: none;
                border-radius: 25px;
                color: white;
                font-size: 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #00E6C3, stop:1 #00D4AA);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #00B894, stop:1 #00A085);
            }
        """)
        self.voice_button.clicked.connect(self.toggle_voice)
        self.voice_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Status and controls
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("🎙️ Voice Control Ready")
        self.status_label.setStyleSheet("""
            color: white; 
            font-size: 14px; 
            font-weight: 600;
            background: transparent;
            border: none;
            padding: 0px;
        """)
        
        self.instruction_label = QLabel("Click microphone or say 'Hey NEXUS'")
        self.instruction_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7); 
            font-size: 12px;
            background: transparent;
            border: none;
            padding: 0px;
        """)
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.instruction_label)
        
        layout.addWidget(self.voice_button)
        layout.addLayout(status_layout)
        layout.addStretch()
    
    def toggle_voice(self):
        """Toggle voice listening state"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start voice listening"""
        self.is_listening = True
        self.voice_button.setText("⏸️")
        self.status_label.setText("🔴 Listening...")
        self.instruction_label.setText("Speak now or click to stop")
        
        # Emit signal
        self.voice_activated.emit()
        
        # Auto-stop after 10 seconds (in real implementation)
        QTimer.singleShot(10000, self.stop_listening)
    
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.voice_button.setText("🎤")
        self.status_label.setText("🎙️ Voice Control Ready")
        self.instruction_label.setText("Click microphone or say 'Hey NEXUS'")


if __name__ == "__main__":
    # This file is meant to be imported, not run directly
    pass