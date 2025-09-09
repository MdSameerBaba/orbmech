# In Backend/InterruptService.py

# This simple dictionary serves as a thread-safe flag
# because dictionary updates in Python are atomic.
_interrupt_flag = {'triggered': False}

def set_interrupt():
    """Sets the interrupt flag to True. Called by the GUI."""
    print("🛑 UI Interrupt signal received!")
    _interrupt_flag['triggered'] = True

def is_interrupted():
    """Checks the status of the interrupt flag. Called by backend modules."""
    return _interrupt_flag['triggered']

def reset_interrupt():
    """Resets the interrupt flag to False. Called before an action."""
    if _interrupt_flag['triggered']:
        print("🔄 Resetting interrupt flag.")
    _interrupt_flag['triggered'] = False