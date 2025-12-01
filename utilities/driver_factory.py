from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config


class DriverFactory:
    """Factory class for creating WebDriver instances."""

    @staticmethod
    def get_driver(browser: str = None, headless: bool = None) -> webdriver.Remote:
        """
        Create and return a WebDriver instance.

        Args:
            browser: Browser type ('chrome' or 'firefox')
            headless: Run browser in headless mode

        Returns:
            WebDriver instance
        """
        browser = browser or Config.BROWSER
        headless = headless if headless is not None else Config.HEADLESS

        if browser.lower() == "chrome":
            return DriverFactory._get_chrome_driver(headless)
        elif browser.lower() == "firefox":
            return DriverFactory._get_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _get_chrome_driver(headless: bool) -> webdriver.Chrome:
        """Create Chrome WebDriver instance."""
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        # Suppress logging
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Use system ChromeDriver if available, otherwise use webdriver-manager
        import os
        chromedriver_path = os.path.expanduser('~/bin/chromedriver')
        if os.path.exists(chromedriver_path):
            service = ChromeService(chromedriver_path)
        else:
            service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        return driver

    @staticmethod
    def _get_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Create Firefox WebDriver instance."""
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        return driver
