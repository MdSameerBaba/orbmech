# Backend/SharedServices.py
import queue

# Messages intended *for* the GUI (backend posts here; GUI consumes)
gui_queue = queue.Queue()

# Messages intended *for* the backend (GUI posts here; backend consumes)
backend_queue = queue.Queue()