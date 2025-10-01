#!/usr/bin/env python3
"""
NEXUS Modern GUI Interface
Ultra-modern, sleek interface with glassmorphism effects, animations, and comprehensive dashboard
"""

import sys
import os
import pathlib
import queue
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# PyQt5 Imports for Modern UI
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QLabel, QPushButton, QTextEdit, QLineEdit,
    QFrame, QScrollArea, QGridLayout, QProgressBar, QTabWidget,
    QSplitter, QFileDialog, QGraphicsOpacityEffect, QButtonGroup
)
from PyQt5.QtGui import (
    QFont, QIcon, QPixmap, QPainter, QPainterPath, QLinearGradient, 
    QColor, QBrush, QPen, QMovie, QFontMetrics, QCursor
)
from PyQt5.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize,
    QThread, pyqtSignal, pyqtProperty, QParallelAnimationGroup
)

# Backend Integration
from Backend.InterruptService import set_interrupt
from Backend.SharedServices import gui_queue, backend_queue

# Personal Assistant Integration  
try:
    from personal_assistant_manager import PersonalAssistantManager
    PERSONAL_ASSISTANT_AVAILABLE = True
except ImportError:
    PERSONAL_ASSISTANT_AVAILABLE = False

# Enhanced Dashboard Components
try:
    from Interface.DashboardComponents import (
        StatCard, ActivityFeed, HealthDashboard, QuickInsights, ModernProgressBar
    )
    DASHBOARD_COMPONENTS_AVAILABLE = True
except ImportError:
    DASHBOARD_COMPONENTS_AVAILABLE = False

# Personal Assistant Interface
try:
    from Interface.PersonalAssistantInterface import ModernPersonalAssistantInterface
    PA_INTERFACE_AVAILABLE = True
except ImportError:
    PA_INTERFACE_AVAILABLE = False

# Quick Actions Components
try:
    from Interface.QuickActionsComponents import SmartQuickActions, VoiceControlWidget
    QUICK_ACTIONS_AVAILABLE = True
except ImportError:
    QUICK_ACTIONS_AVAILABLE = False

# Audio-Visual Components
try:
    from Interface.AudioVisualComponents import (
        EnhancedVoiceControl, AnimatedJarvisWidget, SoundManager, EnhancedButtonFactory
    )
    AUDIO_VISUAL_AVAILABLE = True
except ImportError:
    AUDIO_VISUAL_AVAILABLE = False

# --- MODERN DESIGN SYSTEM ---
class ModernColors:
    """Modern color palette with glassmorphism and gradient support"""
    
    # Primary Colors
    PRIMARY = "#6C63FF"
    PRIMARY_LIGHT = "#8B82FF"
    PRIMARY_DARK = "#5750E6"
    
    # Background Colors
    BG_PRIMARY = "rgba(15, 15, 23, 0.95)"
    BG_SECONDARY = "rgba(25, 25, 35, 0.85)"
    BG_TERTIARY = "rgba(35, 35, 45, 0.75)"
    
    # Glass Colors
    GLASS_BG = "rgba(255, 255, 255, 0.05)"
    GLASS_BORDER = "rgba(255, 255, 255, 0.1)"
    GLASS_HIGHLIGHT = "rgba(255, 255, 255, 0.2)"
    
    # Accent Colors
    SUCCESS = "#00D4AA"
    WARNING = "#FF9500"
    ERROR = "#FF5E5B"
    INFO = "#00C9FF"
    
    # Text Colors
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B8B8B8"
    TEXT_MUTED = "#666666"
    
    # Gradients
    GRADIENT_PRIMARY = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6C63FF, stop:1 #8B82FF)"
    GRADIENT_SUCCESS = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00D4AA, stop:1 #00F5CC)"
    GRADIENT_DANGER = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF5E5B, stop:1 #FF3B30)"
    GRADIENT_GLASS = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255,255,255,0.1), stop:1 rgba(255,255,255,0.05))"

class ModernStyles:
    """Modern CSS-like styles for Qt widgets"""
    
    @staticmethod
    def glass_card(width="auto", height="auto", padding="20px"):
        return f"""
            QWidget {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                backdrop-filter: blur(10px);
                padding: {padding};
                width: {width};
                height: {height};
            }}
            QWidget:hover {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }}
        """
    
    @staticmethod
    def modern_button(gradient=ModernColors.GRADIENT_PRIMARY):
        return f"""
            QPushButton {{
                background: {gradient};
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                font-size: 14px;
                padding: 12px 24px;
                text-align: center;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7B72FF, stop:1 #9B92FF);
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5C52E6, stop:1 #7C72E6);
            }}
            QPushButton:disabled {{
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }}
        """
    
    @staticmethod
    def modern_input():
        return """
            QLineEdit {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                color: white;
                font-size: 14px;
                padding: 12px 16px;
                selection-background-color: rgba(108, 99, 255, 0.3);
            }
            QLineEdit:focus {
                border: 2px solid rgba(108, 99, 255, 0.5);
                background: rgba(255, 255, 255, 0.12);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.4);
            }
        """
    
    @staticmethod
    def modern_text_area():
        return """
            QTextEdit {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                color: white;
                font-size: 14px;
                padding: 16px;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border: 1px solid rgba(108, 99, 255, 0.3);
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """

# --- ANIMATED COMPONENTS ---
class AnimatedCard(QWidget):
    """Glass card with hover animations"""
    
    def __init__(self, title="", content="", parent=None):
        super().__init__(parent)
        self.setFixedHeight(200)
        self.setup_ui(title, content)
        self.setup_animation()
    
    def setup_ui(self, title, content):
        self.setStyleSheet(ModernStyles.glass_card())
        layout = QVBoxLayout(self)
        
        # Title
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 10px;")
            layout.addWidget(title_label)
        
        # Content
        if content:
            content_label = QLabel(content)
            content_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; line-height: 1.5;")
            content_label.setWordWrap(True)
            layout.addWidget(content_label)
        
        layout.addStretch()
    
    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def enterEvent(self, event):
        self.animate_hover(True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.animate_hover(False)
        super().leaveEvent(event)
    
    def animate_hover(self, hover):
        current_rect = self.geometry()
        if hover:
            # Slightly expand on hover
            new_rect = QRect(current_rect.x() - 5, current_rect.y() - 5, 
                           current_rect.width() + 10, current_rect.height() + 10)
        else:
            # Return to original size
            new_rect = QRect(current_rect.x() + 5, current_rect.y() + 5,
                           current_rect.width() - 10, current_rect.height() - 10)
        
        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(new_rect)
        self.animation.start()

class StatusIndicator(QWidget):
    """Animated status indicator with pulse effect"""
    
    def __init__(self, status="ready", parent=None):
        super().__init__(parent)
        self.status = status
        self.setFixedSize(12, 12)
        self.setup_animation()
    
    def setup_animation(self):
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.3)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutSine)
        self.animation.setLoopCount(-1)  # Infinite loop
        self.animation.start()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        color_map = {
            "ready": ModernColors.SUCCESS,
            "listening": ModernColors.INFO,
            "processing": ModernColors.WARNING,
            "error": ModernColors.ERROR
        }
        
        color = QColor(color_map.get(self.status, ModernColors.SUCCESS))
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 12, 12)
    
    def set_status(self, status):
        self.status = status
        self.update()

# --- DASHBOARD WIDGETS ---
class PersonalAssistantWidget(QWidget):
    """Personal Assistant dashboard widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        self.setStyleSheet(ModernStyles.glass_card())
        layout = QVBoxLayout(self)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("🤖 Personal Assistant")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: 600;")
        header.addWidget(title)
        header.addStretch()
        
        # Quick stats
        stats_layout = QGridLayout()
        
        self.tasks_label = QLabel("0")
        self.tasks_label.setStyleSheet("color: #00D4AA; font-size: 24px; font-weight: bold;")
        tasks_title = QLabel("Active Tasks")
        tasks_title.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        
        self.appointments_label = QLabel("0")
        self.appointments_label.setStyleSheet("color: #6C63FF; font-size: 24px; font-weight: bold;")
        appointments_title = QLabel("Today's Meetings")
        appointments_title.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        
        self.expenses_label = QLabel("$0")
        self.expenses_label.setStyleSheet("color: #FF9500; font-size: 24px; font-weight: bold;")
        expenses_title = QLabel("This Month")
        expenses_title.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        
        stats_layout.addWidget(self.tasks_label, 0, 0)
        stats_layout.addWidget(tasks_title, 1, 0)
        stats_layout.addWidget(self.appointments_label, 0, 1)
        stats_layout.addWidget(appointments_title, 1, 1)
        stats_layout.addWidget(self.expenses_label, 0, 2)
        stats_layout.addWidget(expenses_title, 1, 2)
        
        layout.addLayout(header)
        layout.addLayout(stats_layout)
        layout.addStretch()
    
    def load_data(self):
        """Load personal assistant data"""
        if PERSONAL_ASSISTANT_AVAILABLE:
            try:
                pa = PersonalAssistantManager()
                # This would need to be implemented in the PersonalAssistantManager
                # For now, using placeholder data
                self.tasks_label.setText("5")
                self.appointments_label.setText("3")
                self.expenses_label.setText("$847")
            except:
                pass

class SystemStatsWidget(QWidget):
    """System statistics widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.start_timer()
    
    def setup_ui(self):
        self.setStyleSheet(ModernStyles.glass_card())
        layout = QVBoxLayout(self)
        
        # Header
        title = QLabel("⚡ System Status")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: 600; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Status indicators
        self.create_status_row("NEXUS Core", "ready", layout)
        self.create_status_row("Personal Assistant", "ready", layout)
        self.create_status_row("DSA Engine", "ready", layout)
        self.create_status_row("Project Manager", "ready", layout)
        self.create_status_row("Stock Analyzer", "ready", layout)
        
        layout.addStretch()
    
    def create_status_row(self, name, status, layout):
        row = QHBoxLayout()
        
        name_label = QLabel(name)
        name_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 14px;")
        
        indicator = StatusIndicator(status)
        
        status_label = QLabel(status.capitalize())
        status_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        
        row.addWidget(name_label)
        row.addStretch()
        row.addWidget(indicator)
        row.addWidget(status_label)
        
        layout.addLayout(row)
    
    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(5000)  # Update every 5 seconds
    
    def update_stats(self):
        # Update system statistics
        pass

class QuickActionsWidget(QWidget):
    """Quick action buttons widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(ModernStyles.glass_card())
        layout = QVBoxLayout(self)
        
        title = QLabel("🚀 Quick Actions")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: 600; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Action buttons
        actions = [
            ("📱 Voice Command", self.activate_voice),
            ("📅 Show Calendar", self.show_calendar),
            ("📋 Add Task", self.add_task),
            ("💰 Log Expense", self.log_expense),
            ("📚 DSA Practice", self.start_dsa),
            ("📈 Stock Analysis", self.analyze_stocks)
        ]
        
        for text, callback in actions:
            btn = QPushButton(text)
            btn.setStyleSheet(ModernStyles.modern_button())
            btn.clicked.connect(callback)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            layout.addWidget(btn)
        
        layout.addStretch()
    
    def activate_voice(self):
        backend_queue.put({"type": "activate_voice"})
    
    def show_calendar(self):
        backend_queue.put({"type": "text_query", "data": "show calendar"})
    
    def add_task(self):
        backend_queue.put({"type": "text_query", "data": "add task"})
    
    def log_expense(self):
        backend_queue.put({"type": "text_query", "data": "add expense"})
    
    def start_dsa(self):
        backend_queue.put({"type": "text_query", "data": "dsa practice"})
    
    def analyze_stocks(self):
        backend_queue.put({"type": "text_query", "data": "stock analysis"})

# --- MAIN SCREENS ---
class ModernDashboard(QWidget):
    """Modern dashboard with glassmorphism design"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Background gradient
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {ModernColors.BG_PRIMARY}, 
                    stop:1 {ModernColors.BG_SECONDARY});
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Welcome header
        header = self.create_header()
        layout.addWidget(header)
        
        # Dashboard grid
        dashboard_grid = self.create_dashboard_grid()
        layout.addWidget(dashboard_grid)
        
        layout.addStretch()
    
    def create_header(self):
        header_widget = QWidget()
        header_widget.setStyleSheet(ModernStyles.glass_card(height="80px"))
        layout = QHBoxLayout(header_widget)
        
        # NEXUS branding
        nexus_label = QLabel("NEXUS")
        nexus_label.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: 800;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #6C63FF, stop:1 #8B82FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        """)
        
        subtitle = QLabel("Complete AI Personal Assistant")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 16px; margin-left: 10px;")
        
        # Status indicator
        status_indicator = StatusIndicator("ready")
        status_text = QLabel("Ready")
        status_text.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; margin-left: 5px;")
        
        layout.addWidget(nexus_label)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(status_indicator)
        layout.addWidget(status_text)
        
        return header_widget
    
    def create_dashboard_grid(self):
        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(30)
        grid.setContentsMargins(20, 20, 20, 20)  # Add margins around entire grid
        
        # Top row - Statistics cards with proper spacing
        if DASHBOARD_COMPONENTS_AVAILABLE:
            stats_row = QHBoxLayout()
            stats_row.setSpacing(25)
            stats_row.setContentsMargins(0, 0, 0, 20)  # Add bottom margin
            
            # Personal Assistant Stats
            tasks_card = StatCard("Active Tasks", "5", "2 due today", "📋", 12.5)
            meetings_card = StatCard("Meetings", "3", "Today's schedule", "📅", -5.2)
            expenses_card = StatCard("Monthly Spend", "$847", "Budget: $1,200", "💰", 8.3)
            health_card = StatCard("Fitness Score", "78%", "Weekly average", "🏃", 15.7)
            
            # Set fixed heights to prevent collision
            for card in [tasks_card, meetings_card, expenses_card, health_card]:
                card.setFixedHeight(120)
                card.setMinimumWidth(280)
            
            stats_row.addWidget(tasks_card)
            stats_row.addWidget(meetings_card)
            stats_row.addWidget(expenses_card)
            stats_row.addWidget(health_card)
            
            stats_widget = QWidget()
            stats_widget.setLayout(stats_row)
            stats_widget.setFixedHeight(160)  # Set fixed height to prevent overlap
            grid.addWidget(stats_widget, 0, 0, 1, 2)  # Span 2 columns
        else:
            # Fallback to original widgets
            pa_widget = PersonalAssistantWidget()
            grid.addWidget(pa_widget, 0, 0)
            
            stats_widget = SystemStatsWidget()
            grid.addWidget(stats_widget, 0, 1)
        
        # Second row - Main dashboard widgets with improved spacing
        main_row = QHBoxLayout()
        main_row.setSpacing(30)
        main_row.setContentsMargins(0, 20, 0, 0)  # Add top margin
        
        # Left column
        left_column = QVBoxLayout()
        left_column.setSpacing(25)
        
        # Quick Actions
        if QUICK_ACTIONS_AVAILABLE:
            actions_widget = SmartQuickActions()
            actions_widget.action_executed.connect(self.handle_quick_action)
        else:
            actions_widget = QuickActionsWidget()
        left_column.addWidget(actions_widget)
        
        # Health Dashboard
        if DASHBOARD_COMPONENTS_AVAILABLE:
            health_widget = HealthDashboard()
            left_column.addWidget(health_widget)
        
        left_widget = QWidget()
        left_widget.setLayout(left_column)
        
        # Right column
        right_column = QVBoxLayout()
        right_column.setSpacing(25)
        
        # Activity Feed
        if DASHBOARD_COMPONENTS_AVAILABLE:
            activity_widget = ActivityFeed()
            right_column.addWidget(activity_widget)
            
            # Smart Insights
            insights_widget = QuickInsights()
            right_column.addWidget(insights_widget)
        else:
            # Fallback
            activity_widget = AnimatedCard(
                "📊 Recent Activity",
                "• Completed 3 DSA problems\n• Added 2 calendar events\n• Logged $45 in expenses\n• Analyzed AAPL stock"
            )
            right_column.addWidget(activity_widget)
        
        right_widget = QWidget()
        right_widget.setLayout(right_column)
        
        main_row.addWidget(left_widget, 1)  # 50% width
        main_row.addWidget(right_widget, 1)  # 50% width
        
        main_widget = QWidget()
        main_widget.setLayout(main_row)
        main_widget.setMinimumHeight(400)  # Set minimum height to prevent compression
        grid.addWidget(main_widget, 1, 0, 1, 2)  # Span 2 columns
        
        return grid_widget
    
    def handle_quick_action(self, action_type, details):
        """Handle quick action execution"""
        print(f"Quick action executed: {action_type} - {details}")
        
        # Play sound effect for actions
        if hasattr(self, 'parent') and AUDIO_VISUAL_AVAILABLE:
            try:
                parent_window = self.parent()
                if hasattr(parent_window, 'sound_manager'):
                    parent_window.sound_manager.play_activation_sound()
            except:
                pass
        
        # Here you could emit signals or call other methods to handle the action
        # For example, switch to relevant tab or show feedback
    
    def setup_enhanced_dashboard_section(self, layout):
        """Setup enhanced dashboard section with Jarvis animation"""
        if not AUDIO_VISUAL_AVAILABLE:
            return
        
        # Create Jarvis central widget
        jarvis_section = QWidget()
        jarvis_section.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(255, 255, 255, 0.08), 
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        jarvis_section.setFixedHeight(250)
        
        jarvis_layout = QHBoxLayout(jarvis_section)
        jarvis_layout.setSpacing(30)
        
        # Large Jarvis animation
        self.dashboard_jarvis = AnimatedJarvisWidget()
        self.dashboard_jarvis.setFixedSize(200, 200)
        
        # Status and controls
        status_section = QVBoxLayout()
        
        status_title = QLabel("NEXUS Assistant Status")
        status_title.setStyleSheet("""
            color: white; 
            font-size: 20px; 
            font-weight: 600;
            margin-bottom: 15px;
        """)
        
        self.assistant_status = QLabel("🟢 All systems operational")
        self.assistant_status.setStyleSheet("""
            color: #00D4AA; 
            font-size: 16px; 
            font-weight: 500;
            margin-bottom: 10px;
        """)
        
        status_details = QLabel("• Personal Assistant: Active\n• Voice Recognition: Ready\n• Data Sync: Complete")
        status_details.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 14px;
            line-height: 1.5;
        """)
        
        status_section.addWidget(status_title)
        status_section.addWidget(self.assistant_status)
        status_section.addWidget(status_details)
        status_section.addStretch()
        
        jarvis_layout.addWidget(self.dashboard_jarvis)
        jarvis_layout.addLayout(status_section)
        jarvis_layout.addStretch()
        
        layout.addWidget(jarvis_section)

class ModernChatInterface(QWidget):
    """Modern chat interface with enhanced design"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {ModernColors.BG_PRIMARY}, 
                    stop:1 {ModernColors.BG_SECONDARY});
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Chat header
        header = self.create_chat_header()
        layout.addWidget(header)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(ModernStyles.modern_text_area())
        layout.addWidget(self.chat_display)
        
        # Input area
        input_area = self.create_input_area()
        layout.addWidget(input_area)
        
        # Enhanced voice control with sound effects
        if AUDIO_VISUAL_AVAILABLE:
            self.enhanced_voice = EnhancedVoiceControl()
            self.enhanced_voice.voice_activated.connect(self.handle_voice_activation)
            self.enhanced_voice.voice_deactivated.connect(self.handle_voice_deactivation)
            self.enhanced_voice.setContentsMargins(0, 15, 0, 0)  # Add top margin
            layout.addWidget(self.enhanced_voice)
    
    def create_chat_header(self):
        header = QWidget()
        header.setStyleSheet(ModernStyles.glass_card(height="60px"))
        layout = QHBoxLayout(header)
        
        title = QLabel("💬 NEXUS Chat")
        title.setStyleSheet("color: white; font-size: 20px; font-weight: 600;")
        
        self.status_label = QLabel("Ready to assist...")
        self.status_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status_label)
        
        return header
    
    def create_input_area(self):
        input_widget = QWidget()
        input_widget.setStyleSheet(ModernStyles.glass_card(height="80px"))
        layout = QHBoxLayout(input_widget)
        
        # Text input
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Ask NEXUS anything...")
        self.text_input.setStyleSheet(ModernStyles.modern_input())
        self.text_input.returnPressed.connect(self.send_message)
        
        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet(ModernStyles.modern_button())
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Stop/Interrupt button (barge-in functionality)
        if AUDIO_VISUAL_AVAILABLE:
            self.stop_button = EnhancedButtonFactory.create_icon_button("Stop", (40, 40), "Stop NEXUS (Barge-in)")
        else:
            self.stop_button = QPushButton("⏹️")
            self.stop_button.setStyleSheet(ModernStyles.modern_button(ModernColors.GRADIENT_DANGER))
        
        self.stop_button.clicked.connect(self.send_interrupt_signal)
        self.stop_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_button.hide()  # Initially hidden
        
        # Voice button
        self.voice_button = QPushButton("🎤")
        self.voice_button.setStyleSheet(ModernStyles.modern_button(ModernColors.GRADIENT_SUCCESS))
        self.voice_button.clicked.connect(self.activate_voice)
        self.voice_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout.addWidget(self.text_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.voice_button)
        
        return input_widget
    
    def send_message(self):
        message = self.text_input.text().strip()
        if message:
            # Add message to chat display
            self.add_user_message(message)
            
            # Send to backend
            backend_queue.put({"type": "text_query", "data": message})
            self.text_input.clear()
            
            # Update status
            self.status_label.setText("Processing...")
    
    def add_user_message(self, message):
        """Add user message to chat display"""
        current_time = datetime.now().strftime("%H:%M")
        user_html = f"""
        <div style="margin: 10px 0; text-align: right;">
            <div style="background: linear-gradient(135deg, #6C63FF, #8B82FF); 
                        color: white; padding: 12px 16px; border-radius: 18px 18px 6px 18px; 
                        display: inline-block; max-width: 80%; font-size: 14px;">
                {message}
            </div>
            <div style="color: rgba(255,255,255,0.5); font-size: 11px; margin-top: 4px;">
                You • {current_time}
            </div>
        </div>
        """
        current_html = self.chat_display.toHtml()
        self.chat_display.setHtml(current_html + user_html)
        self.scroll_to_bottom()
    
    def add_assistant_message(self, message):
        """Add assistant message to chat display"""
        current_time = datetime.now().strftime("%H:%M")
        assistant_html = f"""
        <div style="margin: 10px 0; text-align: left;">
            <div style="background: rgba(255,255,255,0.1); color: white; 
                        padding: 12px 16px; border-radius: 18px 18px 18px 6px; 
                        display: inline-block; max-width: 80%; font-size: 14px;
                        border: 1px solid rgba(255,255,255,0.1);">
                {message}
            </div>
            <div style="color: rgba(255,255,255,0.5); font-size: 11px; margin-top: 4px;">
                NEXUS • {current_time}
            </div>
        </div>
        """
        current_html = self.chat_display.toHtml()
        self.chat_display.setHtml(current_html + assistant_html)
        self.scroll_to_bottom()
        
        # Reset status
        self.status_label.setText("Ready to assist...")
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def handle_voice_activation(self):
        """Handle voice control activation"""
        self.status_label.setText("🎙️ Voice activated - Listening...")
        # Could trigger speech recognition here
        print("🎙️ Voice control activated with sound effects")
    
    def handle_voice_deactivation(self):
        """Handle voice control deactivation"""
        self.status_label.setText("Ready to assist...")
        print("⏹️ Voice control deactivated")
    
    def send_interrupt_signal(self):
        """Send interrupt signal to stop NEXUS (barge-in functionality)"""
        set_interrupt()
        self.stop_button.hide()
        self.status_label.setText("🛑 Interrupted")
        
        # Add interrupted message to chat
        self.add_assistant_message("🛑 Stopped by user")
        
        # Play sound if available
        if hasattr(self, 'enhanced_voice') and AUDIO_VISUAL_AVAILABLE:
            try:
                # Brief feedback sound or visual indicator
                print("🛑 Barge-in activated - NEXUS interrupted")
            except:
                pass
        
        # Reset status after brief delay
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.status_label.setText("Ready to assist..."))
    
    def activate_voice(self):
        backend_queue.put({"type": "activate_voice"})
    
    def update_chat(self, html):
        self.chat_display.setHtml(html)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def update_status(self, status_text):
        """Update status and show/hide stop button based on activity"""
        self.status_label.setText(status_text)
        
        # Show stop button when NEXUS is answering/speaking
        if "Answering" in status_text or "Speaking" in status_text:
            self.stop_button.show()
        else:
            self.stop_button.hide()
    
    def update_status(self, status):
        self.status_label.setText(status)

# Global status tracking
mic_status = "False"

def SetMicrophoneStatus(status: str):
    global mic_status
    mic_status = status

def GetMicrophoneStatus():
    global mic_status
    return mic_status

# --- MAIN WINDOW ---
class ModernNEXUSWindow(QMainWindow):
    """Ultra-modern NEXUS main window"""
    
    def __init__(self):
        super().__init__()
        self.drag_position = None
        
        # Initialize audio-visual components
        if AUDIO_VISUAL_AVAILABLE:
            self.sound_manager = SoundManager()
        
        self.setup_window()
        self.setup_ui()
        self.setup_queue_processor()
    
    def setup_window(self):
        self.setWindowTitle("NEXUS - Complete AI Personal Assistant")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # Window background
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {ModernColors.BG_PRIMARY}, 
                    stop:1 {ModernColors.BG_SECONDARY});
                border-radius: 20px;
            }}
        """)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)  # Add small margins
        layout.setSpacing(8)  # Add spacing between title bar and content
        
        # Custom title bar
        title_bar = self.create_title_bar()
        layout.addWidget(title_bar)
        
        # Main content area with tabs
        self.tab_widget = QTabWidget()
        self.setup_tabs()
        layout.addWidget(self.tab_widget)
        
        # Initialize drag variables
        self.drag_position = None
    
    def create_title_bar(self):
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_bar.setStyleSheet(f"""
            QWidget {{
                background: {ModernColors.GLASS_BG};
                border-bottom: 1px solid {ModernColors.GLASS_BORDER};
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
            }}
        """)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # App title and icon with Jarvis
        app_info = QHBoxLayout()
        
        # Add animated Jarvis widget to title bar
        if AUDIO_VISUAL_AVAILABLE:
            self.title_jarvis = AnimatedJarvisWidget()
            self.title_jarvis.setFixedSize(50, 50)
            app_info.addWidget(self.title_jarvis)
        
        title_section = QVBoxLayout()
        title = QLabel("NEXUS")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: 800;
            margin-right: 10px;
        """)
        
        subtitle = QLabel("Complete AI Assistant")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
        
        title_section.addWidget(title)
        title_section.addWidget(subtitle)
        
        app_info.addLayout(title_section)
        
        # Window controls with custom graphics
        controls = QHBoxLayout()
        controls.setSpacing(10)
        
        if AUDIO_VISUAL_AVAILABLE:
            minimize_btn = EnhancedButtonFactory.create_icon_button("Minimize", (30, 30), "Minimize Window")
            maximize_btn = EnhancedButtonFactory.create_icon_button("Maximize", (30, 30), "Maximize Window")
            close_btn = EnhancedButtonFactory.create_icon_button("Close", (30, 30), "Close Application")
        else:
            minimize_btn = self.create_window_button("—", self.showMinimized)
            maximize_btn = self.create_window_button("☐", self.toggle_maximize)
            close_btn = self.create_window_button("✕", self.close)
        
        # Connect actions
        minimize_btn.clicked.connect(self.showMinimized)
        maximize_btn.clicked.connect(self.toggle_maximize)
        close_btn.clicked.connect(self.close)
        
        controls.addWidget(minimize_btn)
        controls.addWidget(maximize_btn)
        controls.addWidget(close_btn)
        
        layout.addLayout(app_info)
        layout.addStretch()
        layout.addLayout(controls)
        
        return title_bar
    
    def create_window_button(self, text, callback):
        btn = QPushButton(text)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 15px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        btn.clicked.connect(callback)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        return btn
    
    def setup_tabs(self):
        # Style the tab widget
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.7);
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: rgba(108, 99, 255, 0.2);
                color: white;
                border-bottom: 2px solid #6C63FF;
            }
            QTabBar::tab:hover:!selected {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        
        # Dashboard tab
        self.dashboard = ModernDashboard()
        self.tab_widget.addTab(self.dashboard, "🏠 Dashboard")
        
        # Chat tab
        self.chat_interface = ModernChatInterface()
        self.tab_widget.addTab(self.chat_interface, "💬 Chat")
        
        # Personal Assistant tab
        if PA_INTERFACE_AVAILABLE:
            self.pa_interface = ModernPersonalAssistantInterface()
            self.tab_widget.addTab(self.pa_interface, "🤖 Assistant")
        else:
            pa_widget = QWidget()
            pa_widget.setStyleSheet(f"background: {ModernColors.BG_PRIMARY};")
            self.tab_widget.addTab(pa_widget, "🤖 Assistant")
        
        # Analytics tab (placeholder)
        analytics_widget = QWidget()
        analytics_widget.setStyleSheet(f"background: {ModernColors.BG_PRIMARY};")
        self.tab_widget.addTab(analytics_widget, "📊 Analytics")
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < 60:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        self.drag_position = None
    
    def setup_queue_processor(self):
        self.queue_timer = QTimer()
        self.queue_timer.timeout.connect(self.process_gui_queue)
        self.queue_timer.start(50)  # Process every 50ms for smooth updates
    
    def process_gui_queue(self):
        """Process messages from the backend"""
        while not gui_queue.empty():
            try:
                message = gui_queue.get_nowait()
                msg_type = message.get("type")
                data = message.get("data")
                
                if msg_type == "chat":
                    self.chat_interface.update_chat(data)
                elif msg_type == "status":
                    self.chat_interface.update_status(data)
                    # Also update title bar Jarvis if available
                    if hasattr(self, 'title_jarvis') and AUDIO_VISUAL_AVAILABLE:
                        if "Answering" in data or "Speaking" in data:
                            self.title_jarvis.start_animation()
                        else:
                            self.title_jarvis.stop_animation()
                elif msg_type == "exit":
                    self.close()
                    
            except queue.Empty:
                break
            except Exception as e:
                print(f"Error processing GUI queue: {e}")

# --- ENTRY POINT ---
def ModernGraphicalUserInterface():
    """Launch the modern NEXUS GUI"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("NEXUS")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("NEXUS AI")
    
    # Load custom fonts if available
    from PyQt5.QtGui import QFontDatabase
    font_db = QFontDatabase()
    
    # Create and show the main window
    window = ModernNEXUSWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    ModernGraphicalUserInterface()