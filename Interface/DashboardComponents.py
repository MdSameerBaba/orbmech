#!/usr/bin/env python3
"""
NEXUS Enhanced Dashboard Components
Advanced dashboard widgets with real-time data and interactive visualizations
"""

import sys
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, 
    QFrame, QScrollArea, QGridLayout, QPushButton, QGraphicsOpacityEffect
)
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect

# Try to import personal assistant
try:
    from personal_assistant_manager import PersonalAssistantManager
    PERSONAL_ASSISTANT_AVAILABLE = True
except ImportError:
    PERSONAL_ASSISTANT_AVAILABLE = False

class ModernProgressBar(QWidget):
    """Custom modern progress bar with gradient and animation"""
    
    def __init__(self, value=0, max_value=100, color="#6C63FF", parent=None):
        super().__init__(parent)
        self.value = value
        self.max_value = max_value
        self.color = color
        self.setFixedHeight(8)
        self.setMinimumWidth(200)
        
        # Animation setup
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(1000)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.setBrush(QBrush(QColor(255, 255, 255, 20)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 4, 4)
        
        # Progress
        if self.value > 0:
            progress_width = int((self.value / self.max_value) * self.width())
            
            # Gradient
            gradient = QLinearGradient(0, 0, progress_width, 0)
            gradient.setColorAt(0, QColor(self.color))
            gradient.setColorAt(1, QColor(self.color).lighter(120))
            
            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(0, 0, progress_width, self.height(), 4, 4)
    
    def set_value(self, value):
        self.animation.setStartValue(self.value)
        self.animation.setEndValue(value)
        self.animation.start()
        self.value = value

class StatCard(QWidget):
    """Modern statistics card with icon and trend"""
    
    def __init__(self, title, value, subtitle="", icon="📊", trend=0, parent=None):
        super().__init__(parent)
        self.setFixedSize(280, 140)
        self.setup_ui(title, value, subtitle, icon, trend)
        self.setup_animation()
    
    def setup_ui(self, title, value, subtitle, icon, trend):
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 16px;
                padding: 20px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with icon and trend
        header = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px; color: rgba(255, 255, 255, 0.9);")
        
        trend_color = "#00D4AA" if trend >= 0 else "#FF5E5B"
        trend_symbol = "↗" if trend >= 0 else "↘"
        trend_label = QLabel(f"{trend_symbol} {abs(trend):.1f}%")
        trend_label.setStyleSheet(f"color: {trend_color}; font-size: 12px; font-weight: 600;")
        
        header.addWidget(icon_label)
        header.addStretch()
        header.addWidget(trend_label)
        
        # Main value
        value_label = QLabel(str(value))
        value_label.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: 700;
            margin: 10px 0;
        """)
        
        # Title and subtitle
        title_label = QLabel(title)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 16px; font-weight: 600;")
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
        
        layout.addLayout(header)
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        if subtitle:
            layout.addWidget(subtitle_label)
        layout.addStretch()
    
    def setup_animation(self):
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def enterEvent(self, event):
        current = self.geometry()
        expanded = QRect(current.x() - 2, current.y() - 2, current.width() + 4, current.height() + 4)
        self.hover_animation.setStartValue(current)
        self.hover_animation.setEndValue(expanded)
        self.hover_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        current = self.geometry()
        normal = QRect(current.x() + 2, current.y() + 2, current.width() - 4, current.height() - 4)
        self.hover_animation.setStartValue(current)
        self.hover_animation.setEndValue(normal)
        self.hover_animation.start()
        super().leaveEvent(event)

class ActivityFeed(QWidget):
    """Real-time activity feed widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.activities = []
        self.setup_ui()
        self.load_recent_activities()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("⚡ Recent Activity")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(30, 30)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 15px;
                color: white;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        refresh_btn.clicked.connect(self.refresh_activities)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        # Scroll area for activities
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 3px;
                min-height: 20px;
            }
        """)
        
        self.activity_widget = QWidget()
        self.activity_layout = QVBoxLayout(self.activity_widget)
        self.activity_layout.setContentsMargins(0, 0, 0, 0)
        self.activity_layout.setSpacing(10)
        
        scroll_area.setWidget(self.activity_widget)
        layout.addWidget(scroll_area)
    
    def add_activity(self, icon, title, subtitle, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()
        
        activity_item = QWidget()
        activity_item.setFixedHeight(60)
        activity_item.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 10px;
            }
            QWidget:hover {
                background: rgba(255, 255, 255, 0.06);
            }
        """)
        
        layout = QHBoxLayout(activity_item)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedSize(30, 30)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 16px; color: rgba(255, 255, 255, 0.8);")
        
        # Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: 500;")
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(subtitle_label)
        
        # Timestamp
        time_label = QLabel(timestamp.strftime("%H:%M"))
        time_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 11px;")
        
        layout.addWidget(icon_label)
        layout.addLayout(content_layout)
        layout.addStretch()
        layout.addWidget(time_label)
        
        self.activity_layout.insertWidget(0, activity_item)  # Insert at top
        
        # Keep only last 10 activities
        if self.activity_layout.count() > 10:
            item = self.activity_layout.takeAt(10)
            if item.widget():
                item.widget().deleteLater()
    
    def load_recent_activities(self):
        # Sample activities - in real implementation, load from database/logs
        sample_activities = [
            ("📅", "Calendar Event Added", "Team meeting scheduled for 3 PM"),
            ("✅", "Task Completed", "Finished presentation preparation"),
            ("💰", "Expense Logged", "$25.50 for lunch at downtown cafe"),
            ("📚", "DSA Practice", "Completed 3 array problems"),
            ("📈", "Stock Analysis", "Analyzed AAPL performance trends"),
        ]
        
        for i, (icon, title, subtitle) in enumerate(sample_activities):
            timestamp = datetime.now() - timedelta(minutes=i*15)
            self.add_activity(icon, title, subtitle, timestamp)
    
    def refresh_activities(self):
        # Clear existing activities
        while self.activity_layout.count():
            item = self.activity_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Reload activities
        self.load_recent_activities()

class HealthDashboard(QWidget):
    """Health and wellness dashboard"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_health_data()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        title = QLabel("🏃 Health & Wellness")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Health metrics grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(15)
        
        # Steps progress
        steps_widget = self.create_health_metric("👟", "Steps Today", "8,247", "10,000", 82)
        metrics_grid.addWidget(steps_widget, 0, 0)
        
        # Water intake
        water_widget = self.create_health_metric("💧", "Water Intake", "6 glasses", "8 glasses", 75)
        metrics_grid.addWidget(water_widget, 0, 1)
        
        # Sleep
        sleep_widget = self.create_health_metric("😴", "Sleep", "7.5 hrs", "8 hrs", 94)
        metrics_grid.addWidget(sleep_widget, 1, 0)
        
        # Workout
        workout_widget = self.create_health_metric("💪", "Workout", "45 min", "60 min", 75)
        metrics_grid.addWidget(workout_widget, 1, 1)
        
        layout.addLayout(metrics_grid)
        layout.addStretch()
    
    def create_health_metric(self, icon, title, current, target, percentage):
        metric_widget = QWidget()
        metric_widget.setFixedHeight(100)
        metric_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(metric_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px;")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 12px; font-weight: 500;")
        
        header.addWidget(icon_label)
        header.addWidget(title_label)
        header.addStretch()
        
        # Values
        current_label = QLabel(current)
        current_label.setStyleSheet("color: white; font-size: 18px; font-weight: 600;")
        
        target_label = QLabel(f"of {target}")
        target_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 11px;")
        
        # Progress bar
        progress = ModernProgressBar(percentage, 100, "#00D4AA")
        
        layout.addLayout(header)
        layout.addWidget(current_label)
        layout.addWidget(target_label)
        layout.addWidget(progress)
        
        return metric_widget
    
    def load_health_data(self):
        # Load actual health data from personal assistant database
        if PERSONAL_ASSISTANT_AVAILABLE:
            try:
                pa = PersonalAssistantManager()
                # Would load real health data here
                pass
            except:
                pass

class QuickInsights(QWidget):
    """Quick insights and recommendations widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_insights()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        title = QLabel("🧠 Smart Insights")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Insights list
        self.insights_layout = QVBoxLayout()
        self.insights_layout.setSpacing(10)
        layout.addLayout(self.insights_layout)
        
        layout.addStretch()
    
    def add_insight(self, icon, text, action_text="", action_callback=None):
        insight_widget = QWidget()
        insight_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout(insight_widget)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 16px; color: rgba(255, 255, 255, 0.8);")
        
        # Text
        text_label = QLabel(text)
        text_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 13px; line-height: 1.4;")
        text_label.setWordWrap(True)
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        
        # Action button
        if action_text and action_callback:
            action_btn = QPushButton(action_text)
            action_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(108, 99, 255, 0.2);
                    border: 1px solid rgba(108, 99, 255, 0.3);
                    border-radius: 6px;
                    color: #6C63FF;
                    font-size: 11px;
                    font-weight: 600;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background: rgba(108, 99, 255, 0.3);
                }
            """)
            action_btn.clicked.connect(action_callback)
            layout.addWidget(action_btn)
        
        self.insights_layout.addWidget(insight_widget)
    
    def load_insights(self):
        # Sample insights - would be generated based on user data
        insights = [
            ("💡", "You have 3 high-priority tasks due today. Consider tackling them first!", "View Tasks"),
            ("📊", "Your productivity peaked at 2 PM yesterday. Schedule important work then!", ""),
            ("🎯", "You've completed 67% of this week's fitness goals. Great progress!", "Log Workout"),
            ("📈", "AAPL stock you're tracking is up 3.2% today. Consider reviewing your portfolio.", "Analyze"),
            ("🔔", "You have a meeting in 30 minutes. Don't forget to prepare!", "Open Calendar"),
        ]
        
        for icon, text, action in insights:
            self.add_insight(icon, text, action if action else "")

if __name__ == "__main__":
    # This file is meant to be imported, not run directly
    pass