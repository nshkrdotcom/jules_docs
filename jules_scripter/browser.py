import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException,                                        NoSuchElementException as SeleniumNoSuchElementException,                                        WebDriverException

from . import config
from .logger import log
from .exceptions import ElementNotFoundException, TimeoutException, NavigationException, InteractionException, BrowserInitializationError
from .driver_manager import get_driver

class JulesScripter:
    DEFAULT_SELECTOR_STRATEGY = By.CSS_SELECTOR

    SELECTOR_STRATEGIES = {
        'id': By.ID,
        'name': By.NAME,
        'xpath': By.XPATH,
        'css': By.CSS_SELECTOR,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME,
        'link_text': By.LINK_TEXT,
        'partial_link_text': By.PARTIAL_LINK_TEXT
    }

    def __init__(self, browser_type=config.DEFAULT_BROWSER, headless=config.DEFAULT_HEADLESS_MODE,
                 implicit_wait=config.DEFAULT_IMPLICIT_WAIT, explicit_wait=config.DEFAULT_EXPLICIT_WAIT,
                 page_load_timeout=config.DEFAULT_PAGE_LOAD_TIMEOUT):

        self.browser_type = browser_type
        self.headless = headless
        self.implicit_wait_time = implicit_wait
        self.explicit_wait_time = explicit_wait
        self.page_load_timeout_time = page_load_timeout

        log.info(f"Initializing JulesScripter with browser: {browser_type}, headless: {headless}")
        try:
            self.driver = get_driver(browser_name=browser_type, headless=headless)
        except BrowserInitializationError as e:
            log.error(f"Failed to initialize browser driver: {e}")
            raise

        self.driver.implicitly_wait(self.implicit_wait_time)
        self.driver.set_page_load_timeout(self.page_load_timeout_time)
        self.wait = WebDriverWait(self.driver, self.explicit_wait_time)

        if not os.path.exists(config.SCREENSHOT_DIR):
            os.makedirs(config.SCREENSHOT_DIR)
        log.info("JulesScripter initialized successfully.")

    def _resolve_selector(self, selector_or_element):
        if isinstance(selector_or_element, str):
            # Assume it's a selector string, use default strategy if not specified
            if ':' not in selector_or_element:
                strategy_key = 'css' # Default to CSS
                actual_selector = selector_or_element
            else:
                parts = selector_or_element.split(':', 1)
                strategy_key = parts[0].lower()
                actual_selector = parts[1]

            if strategy_key not in self.SELECTOR_STRATEGIES:
                raise ValueError(f"Unknown selector strategy: {strategy_key}. Supported: {list(self.SELECTOR_STRATEGIES.keys())}")
            return (self.SELECTOR_STRATEGIES[strategy_key], actual_selector)
        return selector_or_element # Assume it's already a WebElement or (By, selector) tuple

    def goto(self, url):
        log.info(f"Navigating to URL: {url}")
        try:
            self.driver.get(url)
        except WebDriverException as e:
            log.error(f"Error navigating to {url}: {e}")
            raise NavigationException(f"Error navigating to {url}: {e}")

    def find_element(self, selector, strategy_key=None):
        # If strategy_key is provided, selector is just the value.
        # If strategy_key is None, selector can be "strategy:value" or just "value" (defaulting to CSS)
        log.debug(f"Finding element with selector: '{selector}', strategy: {strategy_key if strategy_key else 'parsed from selector'}")
        try:
            if strategy_key:
                if strategy_key.lower() not in self.SELECTOR_STRATEGIES:
                     raise ValueError(f"Unknown selector strategy: {strategy_key}")
                by_strategy = self.SELECTOR_STRATEGIES[strategy_key.lower()]
                actual_selector = selector
            else: # Parse from selector string
                resolved_item = self._resolve_selector(selector)
                if not isinstance(resolved_item, tuple) or len(resolved_item) != 2:
                    # This case should ideally not be hit if _resolve_selector is robust
                    raise ValueError("Selector could not be resolved to a (strategy, value) tuple.")
                by_strategy, actual_selector = resolved_item

            element = self.wait.until(EC.presence_of_element_located((by_strategy, actual_selector)))
            log.debug(f"Element found: {by_strategy}='{actual_selector}'")
            return element
        except SeleniumTimeoutException:
            log.warning(f"Element not found or timed out: {selector}")
            raise ElementNotFoundException(f"Element not found or timed out for selector: {selector}")
        except ValueError as ve:
            log.error(f"Invalid selector or strategy: {ve}")
            raise
        except Exception as e:
            log.error(f"An unexpected error occurred while finding element {selector}: {e}")
            raise InteractionException(f"Unexpected error finding element {selector}: {e}")

    def click(self, selector_or_element, strategy_key=None):
        log.info(f"Attempting to click element: {selector_or_element}")
        try:
            if isinstance(selector_or_element, str):
                element = self.find_element(selector_or_element, strategy_key=strategy_key)
            else: # Assuming it's a WebElement
                element = selector_or_element

            # Wait for element to be clickable
            self.wait.until(EC.element_to_be_clickable(element))
            element.click()
            log.info(f"Clicked element successfully.")
        except ElementNotFoundException:
            raise # Re-raise if find_element failed
        except SeleniumTimeoutException:
            log.error(f"Timeout waiting for element to be clickable: {selector_or_element}")
            raise TimeoutException(f"Timeout waiting for element to be clickable: {selector_or_element}")
        except Exception as e:
            log.error(f"Error clicking element {selector_or_element}: {e}")
            raise InteractionException(f"Error clicking element {selector_or_element}: {e}")

    def type_into(self, selector_or_element, text_to_type, strategy_key=None):
        log.info(f"Attempting to type '{text_to_type}' into element: {selector_or_element}")
        try:
            if isinstance(selector_or_element, str):
                element = self.find_element(selector_or_element, strategy_key=strategy_key)
            else: # Assuming it's a WebElement
                element = selector_or_element

            # Wait for element to be visible and enabled
            self.wait.until(EC.visibility_of(element))
            element.clear() # Clear existing text
            element.send_keys(text_to_type)
            log.info(f"Typed text successfully.")
        except ElementNotFoundException:
            raise # Re-raise if find_element failed
        except SeleniumTimeoutException:
            log.error(f"Timeout waiting for element to be visible/enabled: {selector_or_element}")
            raise TimeoutException(f"Timeout waiting for element to be visible/enabled: {selector_or_element}")
        except Exception as e:
            log.error(f"Error typing into element {selector_or_element}: {e}")
            raise InteractionException(f"Error typing into element {selector_or_element}: {e}")

    def get_text(self, selector_or_element, strategy_key=None):
        log.debug(f"Getting text from element: {selector_or_element}")
        try:
            if isinstance(selector_or_element, str):
                element = self.find_element(selector_or_element, strategy_key=strategy_key)
            else: # Assuming it's a WebElement
                element = selector_or_element

            text = element.text
            log.debug(f"Retrieved text: '{text}'")
            return text
        except ElementNotFoundException:
            raise
        except Exception as e:
            log.error(f"Error getting text from element {selector_or_element}: {e}")
            raise InteractionException(f"Error getting text from {selector_or_element}: {e}")

    def take_screenshot(self, filename="screenshot.png"):
        filepath = os.path.join(config.SCREENSHOT_DIR, filename)
        try:
            self.driver.save_screenshot(filepath)
            log.info(f"Screenshot saved to {filepath}")
            return filepath
        except WebDriverException as e:
            log.error(f"Failed to save screenshot to {filepath}: {e}")
            raise InteractionException(f"Failed to save screenshot: {e}")

    def close(self):
        log.info("Closing browser.")
        if self.driver:
            try:
                self.driver.quit()
                log.info("Browser closed successfully.")
            except WebDriverException as e:
                log.error(f"Error closing browser: {e}")
                # Don't raise here, just log, as we are trying to clean up.
            finally:
                self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == '__main__':
    # This is a basic test. It requires geckodriver (for firefox) or chromedriver to be in PATH
    # or for webdriver-manager to be able to install it.
    # In a real VM, you'd need a desktop environment for non-headless, or Xvfb for headless.

    print("Running basic JulesScripter test...")
    # Test with context manager
    try:
        with JulesScripter(browser_type='firefox', headless=True) as bot:
            bot.goto("https://www.example.com")
            print(f"Page title: {bot.driver.title}")
            heading_text = bot.get_text("css:h1") # Using "strategy:selector"
            print(f"Heading text: {heading_text}")
            bot.take_screenshot("example_page.png")
        print("Firefox test completed (with context manager).")
    except Exception as e:
        print(f"Firefox test failed: {e}")
        log.error("Firefox test failed", exc_info=True)

    # Test without context manager (manual close)
    bot_chrome = None
    try:
        bot_chrome = JulesScripter(browser_type='chrome', headless=True)
        bot_chrome.goto("https://www.example.com")
        print(f"Page title: {bot_chrome.driver.title}")
        # Example of finding element first, then interacting
        div_element = bot_chrome.find_element("css:div") # find first div
        print(f"Found a div with tag name: {div_element.tag_name}")
        bot_chrome.take_screenshot("example_page_chrome.png")
        print("Chrome test completed (manual close).")
    except Exception as e:
        print(f"Chrome test failed: {e}")
        log.error("Chrome test failed", exc_info=True)
    finally:
        if bot_chrome:
            bot_chrome.close()
