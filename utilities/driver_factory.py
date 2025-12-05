from selenium import webdriver
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

        # Selenium Manager will automatically handle driver download
        driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        return driver

    @staticmethod
    def _get_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Create Firefox WebDriver instance."""
        import os
        from selenium.webdriver.firefox.service import Service

        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")
            # Set environment variable for headless mode
            os.environ["MOZ_HEADLESS"] = "1"

        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        # Disable logging
        options.set_preference("devtools.console.stdout.content", False)

        # Set Firefox binary location (handles snap installations)
        # Check multiple possible Firefox binary locations
        firefox_paths = [
            "/snap/firefox/current/usr/lib/firefox/firefox",  # Snap package actual binary
            "/snap/bin/firefox",  # Snap wrapper
            "/usr/bin/firefox-esr",  # ESR installation
            "/usr/lib/firefox/firefox",  # Standard installation
        ]

        for path in firefox_paths:
            if os.path.exists(path):
                options.binary_location = path
                break

        # Create a service object to configure geckodriver
        service = Service()

        # Selenium Manager will automatically handle driver download
        driver = webdriver.Firefox(service=service, options=options)

        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        return driver
