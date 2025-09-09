# In interface/GUI.py

# --- IMPORTS ---
import sys
import os
import pathlib
import queue # Required for the queue.Empty exception

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QWidget, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QCursor, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer

from Backend.InterruptService import set_interrupt
# --- FINAL ARCHITECTURE: Import the two shared queues ---
from Backend.SharedServices import gui_queue, backend_queue

# --- HELPERS ---
def get_env_variable(key, default=""): return os.environ.get(key, default)
def GraphicsDirectoryPath(Filename): return os.path.join(os.getcwd(), 'interface', 'Graphics', Filename)
def get_gif_uri(): gif_path = GraphicsDirectoryPath('Jarvis.gif'); return pathlib.Path(gif_path).as_uri()

mic_status = "False"
def SetMicrophoneStatus(status: str): global mic_status; mic_status = status
def GetMicrophoneStatus(): global mic_status; return mic_status

# --- MODE 1: HOME SCREEN ---
class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 0, 0, 50)
        self.gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif')); movie.setScaledSize(QSize(500, 500))
        self.gif_label.setMovie(movie); self.gif_label.setAlignment(Qt.AlignCenter); movie.start()
        self.status_label = QLabel("Initializing..."); self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #AAAAAA; font-size: 16px; font-weight: bold;")
        self.mic_button = QPushButton(); self.mic_button.setIcon(QIcon(GraphicsDirectoryPath('Mic_on.png'))); self.mic_button.setIconSize(QSize(70, 70)); self.mic_button.setFixedSize(100, 100)
        self.mic_button.setCursor(QCursor(Qt.PointingHandCursor)); self.mic_button.setStyleSheet("QPushButton { background-color: #333; border-radius: 50px; } QPushButton:hover { background-color: #444; }")
        self.mic_button.clicked.connect(self.activate_microphone)
        layout.addStretch(); layout.addWidget(self.gif_label); layout.addWidget(self.status_label); layout.addWidget(self.mic_button, alignment=Qt.AlignCenter); layout.addStretch()
    def activate_microphone(self): self.mic_button.setStyleSheet("QPushButton { background-color: #777; border-radius: 50px; }"); SetMicrophoneStatus("True")
    def update_status(self, text):
        self.status_label.setText(text)
        if "Listening..." not in text and "Answering..." not in text: self.mic_button.setStyleSheet("QPushButton { background-color: #333; border-radius: 50px; }")

# --- MODE 2: CHAT SCREEN ---
class ChatScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #212121;")
        layout = QVBoxLayout(self); layout.setContentsMargins(10, 10, 10, 10); layout.setSpacing(10)
        self.chat_display = QTextEdit(); self.chat_display.setReadOnly(True); self.chat_display.setStyleSheet("QTextEdit { background-color: #2C2C2C; color: #FFFFFF; font-size: 14px; border: 1px solid #444; border-radius: 8px; padding: 15px; }")
        self.status_label = QLabel("Initializing..."); self.status_label.setFixedHeight(25); self.status_label.setStyleSheet("color: #AAAAAA; padding-left: 15px;")
        self.input_area = self.create_input_area()
        layout.addWidget(self.chat_display); layout.addWidget(self.status_label); layout.addWidget(self.input_area)
    def create_input_area(self):
        input_widget = QWidget(); input_widget.setFixedHeight(60); layout = QHBoxLayout(input_widget); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(10)
        self.reset_button = QPushButton(); self.reset_button.setIcon(QIcon(GraphicsDirectoryPath("Reset.png"))); self.reset_button.setToolTip("Start a new chat session"); self.reset_button.clicked.connect(self.reset_chat)
        self.stop_button = QPushButton(); self.stop_button.setIcon(QIcon(GraphicsDirectoryPath("Stop.png"))); self.stop_button.setToolTip("Stop the assistant's speech"); self.stop_button.clicked.connect(self.send_interrupt_signal); self.stop_button.hide()
        self.text_input = QLineEdit(); self.text_input.setPlaceholderText("Type your message or click the mic..."); self.text_input.returnPressed.connect(self.send_text_query)
        self.send_button = QPushButton(); self.send_button.setIcon(QIcon(GraphicsDirectoryPath("Send.png"))); self.send_button.setToolTip("Send typed message"); self.send_button.clicked.connect(self.send_text_query)
        self.mic_button = QPushButton(); self.mic_button.setIcon(QIcon(GraphicsDirectoryPath("Mic_on.png"))); self.mic_button.setToolTip("Activate voice input"); self.mic_button.clicked.connect(self.activate_microphone)
        for btn in [self.reset_button, self.stop_button, self.send_button, self.mic_button]:
            btn.setFixedSize(45, 45); btn.setIconSize(QSize(22, 22)); btn.setCursor(QCursor(Qt.PointingHandCursor)); btn.setStyleSheet("QPushButton { background-color: #444; border-radius: 22px; } QPushButton:hover { background-color: #555; }")
        self.text_input.setStyleSheet("QLineEdit { background-color: #444; color: white; border-radius: 22px; padding-left: 15px; font-size: 14px; height: 45px; }")
        layout.addWidget(self.reset_button); layout.addWidget(self.stop_button); layout.addWidget(self.text_input); layout.addWidget(self.send_button); layout.addWidget(self.mic_button)
        return input_widget
    def send_text_query(self):
        query = self.text_input.text().strip()
        if query:
            backend_queue.put({"type": "text_query", "data": query})
            self.text_input.clear()
    def activate_microphone(self): self.mic_button.setStyleSheet("QPushButton { background-color: #777; border-radius: 22px; }"); SetMicrophoneStatus("True")
    def reset_chat(self): backend_queue.put({"type": "reset_chat"})
    def send_interrupt_signal(self): set_interrupt(); self.stop_button.hide()
    def update_chat_history(self, html): self.chat_display.setHtml(html); self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())
    def update_status(self, text):
        self.status_label.setText(text)
        if "Answering" in text: self.stop_button.show()
        else: self.stop_button.hide()
        if "Listening..." in text: self.mic_button.setStyleSheet("QPushButton { background-color: #777; border-radius: 22px; }")
        else: self.mic_button.setStyleSheet("QPushButton { background-color: #444; border-radius: 22px; }")

# --- MODE 3: ANALYSIS SCREEN ---
class AnalysisScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #212121;")
        layout = QVBoxLayout(self); layout.setContentsMargins(15, 15, 15, 15); layout.setSpacing(10)
        control_layout = QHBoxLayout(); self.upload_button = QPushButton("  Upload PDF"); self.upload_button.setIcon(QIcon(GraphicsDirectoryPath("Upload.png")))
        self.upload_button.setStyleSheet("QPushButton { background-color: #005C4B; color: white; font-weight: bold; border-radius: 5px; padding: 10px; text-align: left; }")
        self.upload_button.setCursor(QCursor(Qt.PointingHandCursor)); self.file_label = QLabel("No file selected."); self.file_label.setStyleSheet("color: #AAAAAA; padding-left: 10px; font-size: 14px;")
        control_layout.addWidget(self.upload_button); control_layout.addWidget(self.file_label); control_layout.addStretch()
        self.summary_display = QTextEdit(); self.summary_display.setReadOnly(True); self.summary_display.setPlaceholderText("Upload a PDF to see its summary here...")
        self.summary_display.setStyleSheet("QTextEdit { background-color: #2C2C2C; color: #FFFFFF; font-size: 14px; border: 1px solid #444; border-radius: 8px; padding: 15px; }")
        layout.addLayout(control_layout); layout.addWidget(self.summary_display)
    def display_summary(self, summary_html: str):
        print(f"GUI: Received request to display summary. Content: '{summary_html[:50]}...'"); self.summary_display.clear()
        self.summary_display.setHtml(summary_html); self.summary_display.repaint(); self.file_label.setText("Analysis Complete.")
        print("GUI: Summary display updated.")

# --- THE MAIN WINDOW ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{get_env_variable('Assistantname', 'AI')} Assistant")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet("background-color: black;")
        self.initUI()
        self.init_queue_checker()

    def initUI(self):
        self.setGeometry(100, 100, 850, 800)
        central_widget = QWidget(); self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget); main_layout.setContentsMargins(0,0,0,0); main_layout.setSpacing(0)
        self.top_bar = self.create_top_bar()
        self.stacked_widget = QStackedWidget()
        self.home_screen = HomeScreen(); self.chat_screen = ChatScreen(); self.analysis_screen = AnalysisScreen()
        self.analysis_screen.upload_button.clicked.connect(self.open_file_dialog)
        self.stacked_widget.addWidget(self.home_screen); self.stacked_widget.addWidget(self.chat_screen); self.stacked_widget.addWidget(self.analysis_screen)
        main_layout.addWidget(self.top_bar); main_layout.addWidget(self.stacked_widget)
        self.offset = None

    def open_file_dialog(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Select a PDF to Analyze", "", "PDF Files (*.pdf)", options=options)
        if filepath:
            filename = os.path.basename(filepath)
            self.analysis_screen.file_label.setText(f"Processing: {filename}...")
            self.analysis_screen.summary_display.setText("Analyzing document, please wait...")
            backend_queue.put({"type": "analyze_pdf", "data": filepath})

    def create_top_bar(self):
        top_bar = QWidget(); top_bar.setFixedHeight(50); top_bar.setStyleSheet("background-color: #333333; color: white;")
        layout = QHBoxLayout(top_bar)
        title = QLabel(f"{get_env_variable('Assistantname', 'AI').upper()} ASSISTANT"); title.setStyleSheet("font-weight: bold; font-size: 16px; padding-left: 10px;")
        home_btn = QPushButton("Full Mode"); home_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        chat_btn = QPushButton("Chat Mode"); chat_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        analysis_btn = QPushButton("Analysis Mode"); analysis_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        for btn in [home_btn, chat_btn, analysis_btn]: btn.setCursor(QCursor(Qt.PointingHandCursor)); btn.setStyleSheet("QPushButton { border: none; font-weight: bold; padding: 10px; } QPushButton:hover { background-color: #555; }")
        minimize_btn = QPushButton("—"); minimize_btn.clicked.connect(self.showMinimized)
        self.maximize_btn = QPushButton("☐"); self.maximize_btn.clicked.connect(self.toggle_maximize)
        close_btn = QPushButton("✕"); close_btn.clicked.connect(self.close)
        for btn in [minimize_btn, self.maximize_btn, close_btn]: btn.setFixedSize(40, 40); btn.setStyleSheet("QPushButton { border: none; font-size: 16px; } QPushButton:hover { background-color: #555; }")
        layout.addWidget(title); layout.addStretch(); layout.addWidget(home_btn); layout.addWidget(chat_btn); layout.addWidget(analysis_btn); layout.addWidget(minimize_btn); layout.addWidget(self.maximize_btn); layout.addWidget(close_btn)
        return top_bar
        
    def toggle_maximize(self):
        if self.isMaximized(): self.showNormal()
        else: self.showMaximized()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.y() < self.top_bar.height(): self.offset = event.pos()
    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton: self.move(self.pos() + event.pos() - self.offset)
    def mouseReleaseEvent(self, event): self.offset = None
    def init_queue_checker(self): self.queue_timer = QTimer(self); self.queue_timer.timeout.connect(self.process_queue); self.queue_timer.start(100)
    def process_queue(self):
        while not gui_queue.empty():
            try:
                message = gui_queue.get_nowait()
                msg_type, data = message.get("type"), message.get("data")
                if msg_type == "chat": self.chat_screen.update_chat_history(data)
                elif msg_type == "status": self.home_screen.update_status(data); self.chat_screen.update_status(data)
                elif msg_type == "pdf_summary": self.analysis_screen.display_summary(data)
                elif msg_type == "exit": self.close()
            except queue.Empty:
                pass
            except Exception as e: print(f"Error processing GUI queue message: {e}")

# --- ENTRY POINT ---
def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())