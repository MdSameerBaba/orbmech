# In Backend/WebDriverService.py

import atexit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

_driver_instance = None
_service_instance = None

def get_webdriver_service():
    """
    Ensures that the ChromeDriver service is started only once per application run.
    This prevents file access conflicts.
    """
    global _service_instance
    if _service_instance is None:
        try:
            print("🔧 Initializing WebDriver Service...")
            _service_instance = Service(ChromeDriverManager().install())
            print("✅ WebDriver Service is running.")
        except Exception as e:
            print(f"❌ Critical Error: Failed to start WebDriver Service: {e}")
            raise
    return _service_instance

def get_new_driver_instance():
    """Gets a new, clean browser instance using the shared service."""
    try:
        service = get_webdriver_service()
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--use-fake-device-for-media-stream")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Critical Error: Failed to create new driver instance: {e}")
        return None

def shutdown_webdriver_service():
    """Stops the shared WebDriver service."""
    global _service_instance
    if _service_instance and _service_instance.is_connectable():
        print("🔧 Shutting down WebDriver Service...")
        _service_instance.stop()
        _service_instance = None
        print("✅ WebDriver Service stopped.")

# Register the shutdown function to be called when the Python interpreter exits
atexit.register(shutdown_webdriver_service)