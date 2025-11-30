import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the test framework."""

    # Base URL
    BASE_URL = "https://demo.opencart.com/"

    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

    # Timeouts (in seconds)
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    PAGE_LOAD_TIMEOUT = 30

    # Paths
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")
    REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
    TEST_DATA_DIR = os.path.join(ROOT_DIR, "test_data")

    # Create directories if they don't exist
    @classmethod
    def ensure_directories(cls):
        os.makedirs(cls.SCREENSHOTS_DIR, exist_ok=True)
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)
