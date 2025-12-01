import pytest
import os
from datetime import datetime
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver

from utilities.driver_factory import DriverFactory
from utilities.helpers import take_screenshot
from config.config import Config
from pages import HomePage, FlightsPage, PurchasePage, ConfirmationPage


# Ensure directories exist
Config.ensure_directories()


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )


@pytest.fixture(scope="session")
def browser(request) -> str:
    """Get browser from command line option."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request) -> bool:
    """Get headless mode from command line option."""
    return request.config.getoption("--headless")


@pytest.fixture(scope="function")
def driver(browser: str, headless: bool) -> Generator[WebDriver, None, None]:
    """
    Create and yield a WebDriver instance for each test.

    The driver is automatically quit after the test completes.
    """
    driver = DriverFactory.get_driver(browser=browser, headless=headless)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def home_page(driver: WebDriver) -> HomePage:
    """Create and return a HomePage instance."""
    page = HomePage(driver)
    page.open_home_page()
    return page


@pytest.fixture(scope="function")
def flights_page(driver: WebDriver) -> FlightsPage:
    """Create and return a FlightsPage instance."""
    return FlightsPage(driver)


@pytest.fixture(scope="function")
def purchase_page(driver: WebDriver) -> PurchasePage:
    """Create and return a PurchasePage instance."""
    return PurchasePage(driver)


@pytest.fixture(scope="function")
def confirmation_page(driver: WebDriver) -> ConfirmationPage:
    """Create and return a ConfirmationPage instance."""
    return ConfirmationPage(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result and take screenshot on failure.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            test_name = item.name
            screenshot_path = take_screenshot(driver, f"FAILED_{test_name}")
            print(f"\nScreenshot saved: {screenshot_path}")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "flights: mark test as flight selection related")
    config.addinivalue_line("markers", "purchase: mark test as purchase related")
    config.addinivalue_line("markers", "booking: mark test as booking flow related")


def pytest_html_report_title(report):
    """Set custom title for HTML report."""
    report.title = "BlazeDemo Automation Test Report"
