import os
import json
from datetime import datetime
from typing import Any, Dict
from config.config import Config


def take_screenshot(driver, name: str) -> str:
    """
    Take a screenshot and save it to the screenshots directory.

    Args:
        driver: WebDriver instance
        name: Screenshot name

    Returns:
        Path to the saved screenshot
    """
    Config.ensure_directories()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(Config.SCREENSHOTS_DIR, filename)
    driver.save_screenshot(filepath)
    return filepath


def load_test_data(filename: str) -> Dict[str, Any]:
    """
    Load test data from a JSON file.

    Args:
        filename: Name of the JSON file in test_data directory

    Returns:
        Dictionary containing the test data
    """
    filepath = os.path.join(Config.TEST_DATA_DIR, filename)
    with open(filepath, "r") as f:
        return json.load(f)


def generate_random_email() -> str:
    """Generate a random email address for testing."""
    from faker import Faker
    fake = Faker()
    return fake.email()


def generate_random_user() -> Dict[str, str]:
    """Generate random user data for registration tests."""
    from faker import Faker
    fake = Faker()
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "telephone": fake.phone_number()[:15],
        "password": fake.password(length=12)
    }
