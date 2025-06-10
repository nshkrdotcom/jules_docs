from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .logger import log
from .exceptions import BrowserInitializationError

def get_driver(browser_name='firefox', headless=False):
    """
    Initializes and returns a Selenium WebDriver instance.
    Uses webdriver-manager to download/manage drivers.
    """
    browser_name = browser_name.lower()
    log.info(f"Initializing {browser_name} driver. Headless: {headless}")

    try:
        if browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        elif browser_name == 'chrome':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox") # Often needed in CI/Docker
            options.add_argument("--disable-dev-shm-usage") # Often needed in CI/Docker
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        elif browser_name == 'edge':
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless")
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
        else:
            raise BrowserInitializationError(f"Unsupported browser: {browser_name}. Supported browsers are: firefox, chrome, edge.")

        log.info(f"{browser_name.capitalize()} driver initialized successfully.")
        return driver
    except Exception as e:
        log.error(f"Failed to initialize {browser_name} driver: {e}", exc_info=True)
        raise BrowserInitializationError(f"Failed to initialize {browser_name} driver: {e}")

if __name__ == '__main__':
    # Test calls (these will attempt to download drivers)
    try:
        log.info("Attempting to get Firefox driver...")
        ff_driver = get_driver('firefox', headless=True)
        if ff_driver:
            log.info("Firefox driver obtained. Closing.")
            ff_driver.quit()
    except BrowserInitializationError as e:
        log.error(f"Firefox test failed: {e}")

    try:
        log.info("Attempting to get Chrome driver...")
        chrome_driver = get_driver('chrome', headless=True)
        if chrome_driver:
            log.info("Chrome driver obtained. Closing.")
            chrome_driver.quit()
    except BrowserInitializationError as e:
        log.error(f"Chrome test failed: {e}")
