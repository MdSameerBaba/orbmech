# In a new file: Backend/SignalService.py
from PyQt5.QtCore import QObject, pyqtSignal

class SignalService(QObject):
    # Define the signals that the backend can emit
    status_updated = pyqtSignal(str)
    chat_updated = pyqtSignal(str)
    summary_updated = pyqtSignal(str)
    exit_signal = pyqtSignal()
    interrupt_signal = pyqtSignal()

# Create a single, global instance of the service
# This ensures the entire application uses the exact same signal object
signal_service = SignalService()