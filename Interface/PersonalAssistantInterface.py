#!/usr/bin/env python3
"""
NEXUS Personal Assistant Interface
Comprehensive personal assistant interface for the modern GUI
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, 
    QLineEdit, QTabWidget, QScrollArea, QGridLayout, QFrame, QSplitter,
    QProgressBar, QComboBox, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt, QTimer, QDate, QTime

# Try to import personal assistant
try:
    from personal_assistant_manager import PersonalAssistantManager
    PERSONAL_ASSISTANT_AVAILABLE = True
except ImportError:
    PERSONAL_ASSISTANT_AVAILABLE = False

from Backend.SharedServices import backend_queue

class ModernPersonalAssistantInterface(QWidget):
    """Complete personal assistant interface with all life management features"""
    
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
        """Setup the comprehensive personal assistant UI"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(15, 15, 23, 0.95), 
                    stop:1 rgba(25, 25, 35, 0.85));
                color: white;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content with tabs
        content_tabs = self.create_content_tabs()
        layout.addWidget(content_tabs)
    
    def create_header(self):
        """Create the header with title and quick stats"""
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 20px;
            }
        """)
        header_widget.setFixedHeight(120)
        
        layout = QHBoxLayout(header_widget)
        layout.setContentsMargins(25, 20, 25, 20)
        
        # Title section
        title_section = QVBoxLayout()
        
        title = QLabel("🤖 Personal Assistant")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: 700; margin-bottom: 5px;")
        
        subtitle = QLabel("Complete life management system")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        
        title_section.addWidget(title)
        title_section.addWidget(subtitle)
        title_section.addStretch()
        
        # Quick stats
        stats_section = QHBoxLayout()
        stats_section.setSpacing(30)
        
        # Tasks stat
        tasks_stat = self.create_stat_item("📋", "5", "Active Tasks")
        calendar_stat = self.create_stat_item("📅", "3", "Today's Events")
        expense_stat = self.create_stat_item("💰", "$847", "This Month")
        health_stat = self.create_stat_item("🏃", "78%", "Health Score")
        
        stats_section.addWidget(tasks_stat)
        stats_section.addWidget(calendar_stat)
        stats_section.addWidget(expense_stat)
        stats_section.addWidget(health_stat)
        
        layout.addLayout(title_section)
        layout.addStretch()
        layout.addLayout(stats_section)
        
        return header_widget
    
    def create_stat_item(self, icon, value, label):
        """Create a quick stat item"""
        stat_widget = QWidget()
        stat_widget.setFixedSize(100, 60)
        
        layout = QVBoxLayout(stat_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(5)
        
        # Icon and value
        top_row = QHBoxLayout()
        top_row.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px; margin-right: 5px;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #6C63FF; font-size: 18px; font-weight: 600;")
        
        top_row.addWidget(icon_label)
        top_row.addWidget(value_label)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 11px; text-align: center;")
        label_widget.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(top_row)
        layout.addWidget(label_widget)
        
        return stat_widget
    
    def create_content_tabs(self):
        """Create the main content tabs"""
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.03);
                padding: 10px;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.7);
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 500;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: rgba(108, 99, 255, 0.2);
                color: white;
                border-bottom: 2px solid #6C63FF;
            }
            QTabBar::tab:hover:!selected {
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.9);
            }
        """)
        
        # Calendar Tab
        calendar_tab = self.create_calendar_tab()
        tab_widget.addTab(calendar_tab, "📅 Calendar")
        
        # Tasks Tab
        tasks_tab = self.create_tasks_tab()
        tab_widget.addTab(tasks_tab, "📋 Tasks")
        
        # Expenses Tab
        expenses_tab = self.create_expenses_tab()
        tab_widget.addTab(expenses_tab, "💰 Expenses")
        
        # Health Tab
        health_tab = self.create_health_tab()
        tab_widget.addTab(health_tab, "🏃 Health")
        
        # Contacts Tab
        contacts_tab = self.create_contacts_tab()
        tab_widget.addTab(contacts_tab, "👥 Contacts")
        
        # Entertainment Tab
        entertainment_tab = self.create_entertainment_tab()
        tab_widget.addTab(entertainment_tab, "🎬 Entertainment")
        
        return tab_widget
    
    def create_calendar_tab(self):
        """Create the calendar management tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)
        
        # Left side - Add appointment form
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        form_widget.setFixedWidth(350)
        
        form_layout = QVBoxLayout(form_widget)
        
        form_title = QLabel("📅 Schedule New Event")
        form_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        form_layout.addWidget(form_title)
        
        # Form fields
        self.event_title_input = QLineEdit()
        self.event_title_input.setPlaceholderText("Event title...")
        self.event_title_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.event_title_input)
        
        date_time_layout = QHBoxLayout()
        self.event_date = QDateEdit()
        self.event_date.setDate(QDate.currentDate())
        self.event_date.setStyleSheet(self.get_input_style())
        
        self.event_time = QTimeEdit()
        self.event_time.setTime(QTime.currentTime())
        self.event_time.setStyleSheet(self.get_input_style())
        
        date_time_layout.addWidget(self.event_date)
        date_time_layout.addWidget(self.event_time)
        form_layout.addLayout(date_time_layout)
        
        self.event_location_input = QLineEdit()
        self.event_location_input.setPlaceholderText("Location (optional)...")
        self.event_location_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.event_location_input)
        
        add_event_btn = QPushButton("Add Event")
        add_event_btn.setStyleSheet(self.get_button_style())
        add_event_btn.clicked.connect(self.add_calendar_event)
        form_layout.addWidget(add_event_btn)
        
        form_layout.addStretch()
        
        # Right side - Calendar view
        calendar_view = QWidget()
        calendar_view.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        calendar_layout = QVBoxLayout(calendar_view)
        
        calendar_title = QLabel("📆 Upcoming Events")
        calendar_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        calendar_layout.addWidget(calendar_title)
        
        # Events list
        self.events_scroll = QScrollArea()
        self.events_scroll.setWidgetResizable(True)
        self.events_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self.events_widget = QWidget()
        self.events_layout = QVBoxLayout(self.events_widget)
        self.events_layout.setAlignment(Qt.AlignTop)
        
        self.events_scroll.setWidget(self.events_widget)
        calendar_layout.addWidget(self.events_scroll)
        
        # Load existing events
        self.load_calendar_events()
        
        layout.addWidget(form_widget)
        layout.addWidget(calendar_view)
        
        return widget
    
    def create_tasks_tab(self):
        """Create the task management tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)
        
        # Left side - Add task form
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        form_widget.setFixedWidth(350)
        
        form_layout = QVBoxLayout(form_widget)
        
        form_title = QLabel("📋 Add New Task")
        form_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        form_layout.addWidget(form_title)
        
        # Task form fields
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Task description...")
        self.task_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.task_input)
        
        priority_layout = QHBoxLayout()
        priority_label = QLabel("Priority:")
        priority_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px;")
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setCurrentText("Medium")
        self.priority_combo.setStyleSheet(self.get_input_style())
        
        priority_layout.addWidget(priority_label)
        priority_layout.addWidget(self.priority_combo)
        form_layout.addLayout(priority_layout)
        
        self.task_due_date = QDateEdit()
        self.task_due_date.setDate(QDate.currentDate().addDays(1))
        self.task_due_date.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.task_due_date)
        
        add_task_btn = QPushButton("Add Task")
        add_task_btn.setStyleSheet(self.get_button_style())
        add_task_btn.clicked.connect(self.add_task)
        form_layout.addWidget(add_task_btn)
        
        form_layout.addStretch()
        
        # Right side - Tasks view
        tasks_view = QWidget()
        tasks_view.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        tasks_layout = QVBoxLayout(tasks_view)
        
        tasks_title = QLabel("✅ Active Tasks")
        tasks_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        tasks_layout.addWidget(tasks_title)
        
        # Tasks list
        self.tasks_scroll = QScrollArea()
        self.tasks_scroll.setWidgetResizable(True)
        self.tasks_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self.tasks_widget = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_layout.setAlignment(Qt.AlignTop)
        
        self.tasks_scroll.setWidget(self.tasks_widget)
        tasks_layout.addWidget(self.tasks_scroll)
        
        # Load existing tasks
        self.load_tasks()
        
        layout.addWidget(form_widget)
        layout.addWidget(tasks_view)
        
        return widget
    
    def create_expenses_tab(self):
        """Create the expense tracking tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)
        
        # Left side - Add expense form
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        form_widget.setFixedWidth(350)
        
        form_layout = QVBoxLayout(form_widget)
        
        form_title = QLabel("💰 Add Expense")
        form_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        form_layout.addWidget(form_title)
        
        # Expense form fields
        amount_layout = QHBoxLayout()
        amount_label = QLabel("$")
        amount_label.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        
        self.expense_amount = QDoubleSpinBox()
        self.expense_amount.setRange(0.01, 99999.99)
        self.expense_amount.setDecimals(2)
        self.expense_amount.setValue(0.00)
        self.expense_amount.setStyleSheet(self.get_input_style())
        
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.expense_amount)
        form_layout.addLayout(amount_layout)
        
        self.expense_description = QLineEdit()
        self.expense_description.setPlaceholderText("What was this expense for?")
        self.expense_description.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.expense_description)
        
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        category_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px;")
        
        self.expense_category = QComboBox()
        self.expense_category.addItems([
            "Food & Dining", "Transportation", "Shopping", "Entertainment", 
            "Bills & Utilities", "Healthcare", "Education", "Other"
        ])
        self.expense_category.setStyleSheet(self.get_input_style())
        
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.expense_category)
        form_layout.addLayout(category_layout)
        
        add_expense_btn = QPushButton("Add Expense")
        add_expense_btn.setStyleSheet(self.get_button_style())
        add_expense_btn.clicked.connect(self.add_expense)
        form_layout.addWidget(add_expense_btn)
        
        form_layout.addStretch()
        
        # Right side - Expenses view
        expenses_view = QWidget()
        expenses_view.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        expenses_layout = QVBoxLayout(expenses_view)
        
        expenses_title = QLabel("💳 Recent Expenses")
        expenses_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        expenses_layout.addWidget(expenses_title)
        
        # Monthly summary
        summary_widget = QWidget()
        summary_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
            }
        """)
        summary_widget.setFixedHeight(80)
        
        summary_layout = QHBoxLayout(summary_widget)
        
        month_total = QLabel("This Month: $847.50")
        month_total.setStyleSheet("color: #FF9500; font-size: 20px; font-weight: 600;")
        
        budget_progress = QLabel("Budget: 70% used")
        budget_progress.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px;")
        
        summary_layout.addWidget(month_total)
        summary_layout.addStretch()
        summary_layout.addWidget(budget_progress)
        
        expenses_layout.addWidget(summary_widget)
        
        # Expenses list
        self.expenses_scroll = QScrollArea()
        self.expenses_scroll.setWidgetResizable(True)
        self.expenses_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self.expenses_widget = QWidget()
        self.expenses_layout = QVBoxLayout(self.expenses_widget)
        self.expenses_layout.setAlignment(Qt.AlignTop)
        
        self.expenses_scroll.setWidget(self.expenses_widget)
        expenses_layout.addWidget(self.expenses_scroll)
        
        # Load existing expenses
        self.load_expenses()
        
        layout.addWidget(form_widget)
        layout.addWidget(expenses_view)
        
        return widget
    
    def create_health_tab(self):
        """Create the health tracking tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Header with health summary
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        header.setFixedHeight(120)
        
        header_layout = QHBoxLayout(header)
        
        # Health metrics
        metrics = [
            ("👟", "Steps", "8,247", "#00D4AA"),
            ("💧", "Water", "6 glasses", "#00C9FF"),
            ("😴", "Sleep", "7.5 hrs", "#6C63FF"),
            ("💪", "Workouts", "3 this week", "#FF9500")
        ]
        
        for icon, title, value, color in metrics:
            metric_widget = QWidget()
            metric_layout = QVBoxLayout(metric_widget)
            metric_layout.setAlignment(Qt.AlignCenter)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 24px; margin-bottom: 5px;")
            icon_label.setAlignment(Qt.AlignCenter)
            
            value_label = QLabel(value)
            value_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: 600;")
            value_label.setAlignment(Qt.AlignCenter)
            
            title_label = QLabel(title)
            title_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
            title_label.setAlignment(Qt.AlignCenter)
            
            metric_layout.addWidget(icon_label)
            metric_layout.addWidget(value_label)
            metric_layout.addWidget(title_label)
            
            header_layout.addWidget(metric_widget)
        
        layout.addWidget(header)
        
        # Quick log buttons
        quick_log = QHBoxLayout()
        
        log_steps_btn = QPushButton("👟 Log Steps")
        log_water_btn = QPushButton("💧 Log Water")
        log_workout_btn = QPushButton("💪 Log Workout")
        log_sleep_btn = QPushButton("😴 Log Sleep")
        
        for btn in [log_steps_btn, log_water_btn, log_workout_btn, log_sleep_btn]:
            btn.setStyleSheet(self.get_button_style())
            btn.setFixedHeight(40)
            quick_log.addWidget(btn)
        
        layout.addLayout(quick_log)
        layout.addStretch()
        
        return widget
    
    def create_contacts_tab(self):
        """Create the contacts management tab"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)
        
        # Left side - Add contact form
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        form_widget.setFixedWidth(350)
        
        form_layout = QVBoxLayout(form_widget)
        
        form_title = QLabel("👥 Add Contact")
        form_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        form_layout.addWidget(form_title)
        
        # Contact form fields
        self.contact_name = QLineEdit()
        self.contact_name.setPlaceholderText("Full name...")
        self.contact_name.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.contact_name)
        
        self.contact_phone = QLineEdit()
        self.contact_phone.setPlaceholderText("Phone number...")
        self.contact_phone.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.contact_phone)
        
        self.contact_email = QLineEdit()
        self.contact_email.setPlaceholderText("Email address...")
        self.contact_email.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.contact_email)
        
        add_contact_btn = QPushButton("Add Contact")
        add_contact_btn.setStyleSheet(self.get_button_style())
        add_contact_btn.clicked.connect(self.add_contact)
        form_layout.addWidget(add_contact_btn)
        
        form_layout.addStretch()
        
        # Right side - Contacts list
        contacts_view = QWidget()
        contacts_view.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        contacts_layout = QVBoxLayout(contacts_view)
        
        contacts_title = QLabel("📞 Contacts")
        contacts_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        contacts_layout.addWidget(contacts_title)
        
        # Search
        self.contact_search = QLineEdit()
        self.contact_search.setPlaceholderText("Search contacts...")
        self.contact_search.setStyleSheet(self.get_input_style())
        contacts_layout.addWidget(self.contact_search)
        
        # Contacts list
        self.contacts_scroll = QScrollArea()
        self.contacts_scroll.setWidgetResizable(True)
        self.contacts_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        self.contacts_widget = QWidget()
        self.contacts_layout = QVBoxLayout(self.contacts_widget)
        self.contacts_layout.setAlignment(Qt.AlignTop)
        
        self.contacts_scroll.setWidget(self.contacts_widget)
        contacts_layout.addWidget(self.contacts_scroll)
        
        # Load existing contacts
        self.load_contacts()
        
        layout.addWidget(form_widget)
        layout.addWidget(contacts_view)
        
        return widget
    
    def create_entertainment_tab(self):
        """Create the entertainment recommendations tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("🎬 Entertainment & Recommendations")
        header.setStyleSheet("color: white; font-size: 24px; font-weight: 600; margin-bottom: 20px;")
        layout.addWidget(header)
        
        # Entertainment categories
        categories_layout = QHBoxLayout()
        
        movie_btn = QPushButton("🎬 Movies")
        tv_btn = QPushButton("📺 TV Shows")
        music_btn = QPushButton("🎵 Music")
        books_btn = QPushButton("📚 Books")
        
        for btn in [movie_btn, tv_btn, music_btn, books_btn]:
            btn.setStyleSheet(self.get_button_style())
            btn.setFixedHeight(50)
            categories_layout.addWidget(btn)
        
        layout.addLayout(categories_layout)
        
        # Recommendations area
        recommendations_widget = QWidget()
        recommendations_widget.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        recommendations_layout = QVBoxLayout(recommendations_widget)
        
        recs_title = QLabel("🔥 Trending Recommendations")
        recs_title.setStyleSheet("color: white; font-size: 18px; font-weight: 600; margin-bottom: 15px;")
        recommendations_layout.addWidget(recs_title)
        
        # Sample recommendations
        recommendations = [
            ("🎬", "The Crown", "Netflix • Historical Drama • 9.1★"),
            ("📺", "Wednesday", "Netflix • Comedy/Horror • 8.6★"),
            ("🎵", "Spotify Discover Weekly", "Your personalized playlist updated"),
            ("📚", "Atomic Habits", "Self-improvement • James Clear • 4.8★"),
        ]
        
        for icon, title, subtitle in recommendations:
            rec_item = QWidget()
            rec_item.setStyleSheet("""
                QWidget {
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 10px;
                }
                QWidget:hover {
                    background: rgba(255, 255, 255, 0.06);
                }
            """)
            rec_item.setFixedHeight(60)
            
            rec_layout = QHBoxLayout(rec_item)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 20px;")
            icon_label.setFixedSize(30, 30)
            
            content_layout = QVBoxLayout()
            
            title_label = QLabel(title)
            title_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")
            
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
            
            content_layout.addWidget(title_label)
            content_layout.addWidget(subtitle_label)
            
            rec_layout.addWidget(icon_label)
            rec_layout.addLayout(content_layout)
            rec_layout.addStretch()
            
            recommendations_layout.addWidget(rec_item)
        
        layout.addWidget(recommendations_widget)
        layout.addStretch()
        
        return widget
    
    def get_input_style(self):
        """Get the standard input field style"""
        return """
            QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                padding: 10px 12px;
                margin-bottom: 10px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, 
            QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid rgba(108, 99, 255, 0.5);
                background: rgba(255, 255, 255, 0.12);
            }
        """
    
    def get_button_style(self):
        """Get the standard button style"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6C63FF, stop:1 #8B82FF);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                font-size: 14px;
                padding: 10px 20px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7B72FF, stop:1 #9B92FF);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5C52E6, stop:1 #7C72E6);
            }
        """
    
    def setup_timer(self):
        """Setup timer for periodic updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(30000)  # Update every 30 seconds
    
    def add_calendar_event(self):
        """Add a new calendar event"""
        title = self.event_title_input.text().strip()
        date = self.event_date.date().toString("yyyy-MM-dd")
        time = self.event_time.time().toString("HH:mm")
        location = self.event_location_input.text().strip()
        
        if not title:
            return
        
        if self.pa_manager:
            try:
                query = f"schedule {title} on {date} at {time}"
                if location:
                    query += f" at {location}"
                result = self.pa_manager.process_personal_assistant_query(query)
                print(f"Calendar event added: {result}")
            except Exception as e:
                print(f"Error adding calendar event: {e}")
        
        # Clear form
        self.event_title_input.clear()
        self.event_location_input.clear()
        
        # Refresh events
        self.load_calendar_events()
    
    def add_task(self):
        """Add a new task"""
        task_text = self.task_input.text().strip()
        priority = self.priority_combo.currentText().lower()
        due_date = self.task_due_date.date().toString("yyyy-MM-dd")
        
        if not task_text:
            return
        
        if self.pa_manager:
            try:
                query = f"add task {task_text} priority {priority} due {due_date}"
                result = self.pa_manager.process_personal_assistant_query(query)
                print(f"Task added: {result}")
            except Exception as e:
                print(f"Error adding task: {e}")
        
        # Clear form
        self.task_input.clear()
        
        # Refresh tasks
        self.load_tasks()
    
    def add_expense(self):
        """Add a new expense"""
        amount = self.expense_amount.value()
        description = self.expense_description.text().strip()
        category = self.expense_category.currentText()
        
        if amount <= 0 or not description:
            return
        
        if self.pa_manager:
            try:
                query = f"add expense ${amount:.2f} {description} category {category}"
                result = self.pa_manager.process_personal_assistant_query(query)
                print(f"Expense added: {result}")
            except Exception as e:
                print(f"Error adding expense: {e}")
        
        # Clear form
        self.expense_amount.setValue(0.00)
        self.expense_description.clear()
        
        # Refresh expenses
        self.load_expenses()
    
    def add_contact(self):
        """Add a new contact"""
        name = self.contact_name.text().strip()
        phone = self.contact_phone.text().strip()
        email = self.contact_email.text().strip()
        
        if not name:
            return
        
        if self.pa_manager:
            try:
                query = f"add contact {name}"
                if phone:
                    query += f" phone {phone}"
                if email:
                    query += f" email {email}"
                result = self.pa_manager.process_personal_assistant_query(query)
                print(f"Contact added: {result}")
            except Exception as e:
                print(f"Error adding contact: {e}")
        
        # Clear form
        self.contact_name.clear()
        self.contact_phone.clear()
        self.contact_email.clear()
        
        # Refresh contacts
        self.load_contacts()
    
    def load_calendar_events(self):
        """Load and display calendar events"""
        # Clear existing events
        for i in reversed(range(self.events_layout.count())):
            self.events_layout.itemAt(i).widget().setParent(None)
        
        # Sample events - in real implementation, load from database
        sample_events = [
            ("📅", "Team Meeting", "Today 3:00 PM", "Conference Room A"),
            ("📅", "Doctor Appointment", "Tomorrow 10:00 AM", "Medical Center"),
            ("📅", "Project Deadline", "Friday 6:00 PM", ""),
        ]
        
        for icon, title, time, location in sample_events:
            event_widget = self.create_list_item(icon, title, f"{time}\n{location}" if location else time)
            self.events_layout.addWidget(event_widget)
    
    def load_tasks(self):
        """Load and display tasks"""
        # Clear existing tasks
        for i in reversed(range(self.tasks_layout.count())):
            self.tasks_layout.itemAt(i).widget().setParent(None)
        
        # Sample tasks - in real implementation, load from database
        sample_tasks = [
            ("📋", "Prepare presentation", "Due: Today", "high"),
            ("📋", "Review code changes", "Due: Tomorrow", "medium"),
            ("📋", "Update documentation", "Due: Friday", "low"),
        ]
        
        for icon, title, due, priority in sample_tasks:
            priority_colors = {"high": "#FF5E5B", "medium": "#FF9500", "low": "#00D4AA"}
            task_widget = self.create_list_item(icon, title, due, priority_colors.get(priority, "#FF9500"))
            self.tasks_layout.addWidget(task_widget)
    
    def load_expenses(self):
        """Load and display expenses"""
        # Clear existing expenses
        for i in reversed(range(self.expenses_layout.count())):
            self.expenses_layout.itemAt(i).widget().setParent(None)
        
        # Sample expenses - in real implementation, load from database
        sample_expenses = [
            ("💰", "Lunch at downtown cafe", "$25.50", "Food & Dining"),
            ("💰", "Gas station", "$45.00", "Transportation"),
            ("💰", "Netflix subscription", "$15.99", "Entertainment"),
        ]
        
        for icon, description, amount, category in sample_expenses:
            expense_widget = self.create_list_item(icon, description, f"{amount} • {category}")
            self.expenses_layout.addWidget(expense_widget)
    
    def load_contacts(self):
        """Load and display contacts"""
        # Clear existing contacts
        for i in reversed(range(self.contacts_layout.count())):
            self.contacts_layout.itemAt(i).widget().setParent(None)
        
        # Sample contacts - in real implementation, load from database
        sample_contacts = [
            ("👤", "John Smith", "📱 555-0123 • ✉️ john@email.com"),
            ("👤", "Sarah Johnson", "📱 555-0456 • ✉️ sarah@company.com"),
            ("👤", "Mike Wilson", "📱 555-0789"),
        ]
        
        for icon, name, details in sample_contacts:
            contact_widget = self.create_list_item(icon, name, details)
            self.contacts_layout.addWidget(contact_widget)
    
    def create_list_item(self, icon, title, subtitle, accent_color="#6C63FF"):
        """Create a standardized list item widget"""
        item_widget = QWidget()
        item_widget.setStyleSheet(f"""
            QWidget {{
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-left: 3px solid {accent_color};
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 8px;
            }}
            QWidget:hover {{
                background: rgba(255, 255, 255, 0.06);
            }}
        """)
        item_widget.setFixedHeight(70)
        
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px; color: rgba(255, 255, 255, 0.8);")
        icon_label.setFixedSize(30, 30)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Content
        content_layout = QVBoxLayout()
        content_layout.setSpacing(3)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600;")
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(subtitle_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(content_layout)
        layout.addStretch()
        
        return item_widget
    
    def update_data(self):
        """Update all data periodically"""
        # In a real implementation, this would refresh data from the database
        pass

if __name__ == "__main__":
    # This file is meant to be imported, not run directly
    pass