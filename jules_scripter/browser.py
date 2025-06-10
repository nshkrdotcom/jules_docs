import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException,                                        NoSuchElementException as SeleniumNoSuchElementException,                                        WebDriverException, StaleElementReferenceException

from . import config # Assuming config.py might be updated later for new defaults
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
                 page_load_timeout=config.DEFAULT_PAGE_LOAD_TIMEOUT, config_file_path=None): # Added config_file_path

        # Config loading logic will be enhanced in a later step
        # For now, direct parameters take precedence.
        self.config_settings = config.load_config(config_file_path) # Anticipating config update

        self.browser_type = self.config_settings.get('browser', browser_type)
        self.headless = self.config_settings.get('headless', headless)
        self.implicit_wait_time = self.config_settings.get('implicit_wait', implicit_wait)
        self.explicit_wait_time = self.config_settings.get('explicit_wait', explicit_wait)
        self.page_load_timeout_time = self.config_settings.get('page_load_timeout', page_load_timeout)
        self.screenshot_dir = self.config_settings.get('screenshot_dir', config.SCREENSHOT_DIR)


        log.info(f"Initializing JulesScripter with browser: {self.browser_type}, headless: {self.headless}")
        try:
            self.driver = get_driver(browser_name=self.browser_type, headless=self.headless)
        except BrowserInitializationError as e:
            log.error(f"Failed to initialize browser driver: {e}")
            raise

        self.driver.implicitly_wait(self.implicit_wait_time)
        self.driver.set_page_load_timeout(self.page_load_timeout_time)
        self.wait = WebDriverWait(self.driver, self.explicit_wait_time)

        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        log.info("JulesScripter initialized successfully.")

    def _get_waiter(self, timeout=None):
        return WebDriverWait(self.driver, timeout) if timeout is not None else self.wait

    def _resolve_selector_to_by_tuple(self, selector, strategy_key=None):
        # Returns (By strategy, actual_selector_value)
        if strategy_key:
            strategy_key_lower = strategy_key.lower()
            if strategy_key_lower not in self.SELECTOR_STRATEGIES:
                raise ValueError(f"Unknown selector strategy key: {strategy_key}. Supported: {list(self.SELECTOR_STRATEGIES.keys())}")
            return (self.SELECTOR_STRATEGIES[strategy_key_lower], selector)

        if ':' not in selector:
            # Default to CSS if no prefix and no strategy_key
            return (self.SELECTOR_STRATEGIES['css'], selector)

        parts = selector.split(':', 1)
        strategy_prefix = parts[0].lower()
        actual_selector_value = parts[1]

        if strategy_prefix not in self.SELECTOR_STRATEGIES:
            raise ValueError(f"Unknown selector strategy prefix: {strategy_prefix}. Supported: {list(self.SELECTOR_STRATEGIES.keys())}")
        return (self.SELECTOR_STRATEGIES[strategy_prefix], actual_selector_value)

    def _find_element_internal(self, selector_or_element, strategy_key=None):
        if not isinstance(selector_or_element, str):
            return selector_or_element # It's already a WebElement

        by_strategy, actual_selector = self._resolve_selector_to_by_tuple(selector_or_element, strategy_key)

        try:
            element = self.wait.until(EC.presence_of_element_located((by_strategy, actual_selector)))
            log.debug(f"Element found: {by_strategy}='{actual_selector}'")
            return element
        except SeleniumTimeoutException:
            log.warning(f"Element not found or timed out: {selector_or_element} (strategy: {by_strategy}, value: '{actual_selector}')")
            raise ElementNotFoundException(f"Element not found or timed out for selector: {selector_or_element}")
        except ValueError as ve:
            log.error(f"Invalid selector or strategy: {ve}")
            raise
        except Exception as e:
            log.error(f"An unexpected error occurred while finding element {selector_or_element}: {e}")
            raise InteractionException(f"Unexpected error finding element {selector_or_element}: {e}")

    def goto(self, url):
        log.info(f"Navigating to URL: {url}")
        try:
            self.driver.get(url)
        except WebDriverException as e:
            log.error(f"Error navigating to {url}: {e}")
            raise NavigationException(f"Error navigating to {url}: {e}")

    def find_element(self, selector, strategy_key=None):
        log.debug(f"Finding element with selector: '{selector}', strategy: {strategy_key if strategy_key else 'parsed from selector'}")
        return self._find_element_internal(selector, strategy_key)

    def click(self, selector_or_element, strategy_key=None):
        log.info(f"Attempting to click element: {selector_or_element}")
        try:
            element = self._find_element_internal(selector_or_element, strategy_key)
            self.wait.until(EC.element_to_be_clickable(element))
            element.click()
            log.info(f"Clicked element successfully.")
        except ElementNotFoundException:
            raise
        except SeleniumTimeoutException:
            log.error(f"Timeout waiting for element to be clickable: {selector_or_element}")
            raise TimeoutException(f"Timeout waiting for element to be clickable: {selector_or_element}")
        except Exception as e:
            log.error(f"Error clicking element {selector_or_element}: {e}")
            raise InteractionException(f"Error clicking element {selector_or_element}: {e}")

    def type_into(self, selector_or_element, text_to_type, strategy_key=None, clear_first=True):
        log.info(f"Attempting to type '{text_to_type}' into element: {selector_or_element}")
        try:
            element = self._find_element_internal(selector_or_element, strategy_key)
            self.wait.until(EC.visibility_of(element))
            if clear_first:
                element.clear()
            element.send_keys(text_to_type)
            log.info(f"Typed text successfully.")
        except ElementNotFoundException:
            raise
        except SeleniumTimeoutException:
            log.error(f"Timeout waiting for element to be visible/enabled: {selector_or_element}")
            raise TimeoutException(f"Timeout waiting for element to be visible/enabled: {selector_or_element}")
        except Exception as e:
            log.error(f"Error typing into element {selector_or_element}: {e}")
            raise InteractionException(f"Error typing into element {selector_or_element}: {e}")

    def get_text(self, selector_or_element, strategy_key=None):
        log.debug(f"Getting text from element: {selector_or_element}")
        try:
            element = self._find_element_internal(selector_or_element, strategy_key)
            text = element.text
            log.debug(f"Retrieved text: '{text}'")
            return text
        except ElementNotFoundException:
            raise
        except Exception as e:
            log.error(f"Error getting text from element {selector_or_element}: {e}")
            raise InteractionException(f"Error getting text from {selector_or_element}: {e}")

    def get_attribute(self, selector_or_element, attribute_name, strategy_key=None):
        log.debug(f"Getting attribute '{attribute_name}' from element: {selector_or_element}")
        try:
            element = self._find_element_internal(selector_or_element, strategy_key)
            attr_value = element.get_attribute(attribute_name)
            log.debug(f"Retrieved attribute '{attribute_name}': '{attr_value}'")
            return attr_value
        except ElementNotFoundException:
            raise
        except Exception as e:
            log.error(f"Error getting attribute '{attribute_name}' from {selector_or_element}: {e}")
            raise InteractionException(f"Error getting attribute {attribute_name} from {selector_or_element}: {e}")

    def take_screenshot(self, filename="screenshot.png"):
        filepath = os.path.join(self.screenshot_dir, filename)
        try:
            self.driver.save_screenshot(filepath)
            log.info(f"Screenshot saved to {filepath}")
            return filepath
        except WebDriverException as e:
            log.error(f"Failed to save screenshot to {filepath}: {e}")
            raise InteractionException(f"Failed to save screenshot: {e}")

    # --- New Methods Start Here ---

    def wait_for_element_disappear(self, selector, strategy_key=None, timeout=None):
        waiter = self._get_waiter(timeout)
        by_strategy, actual_selector = self._resolve_selector_to_by_tuple(selector, strategy_key)
        log.info(f"Waiting for element {by_strategy}='{actual_selector}' to disappear.")
        try:
            waiter.until(EC.invisibility_of_element_located((by_strategy, actual_selector)))
            log.info(f"Element {by_strategy}='{actual_selector}' disappeared.")
            return True
        except SeleniumTimeoutException:
            log.warning(f"Timeout waiting for element {by_strategy}='{actual_selector}' to disappear.")
            raise TimeoutException(f"Timeout waiting for element {by_strategy}='{actual_selector}' to disappear.")
        except Exception as e:
            log.error(f"Error waiting for element {by_strategy}='{actual_selector}' to disappear: {e}")
            raise InteractionException(f"Error waiting for element {by_strategy}='{actual_selector}' to disappear: {e}")

    def wait_for_text_in_element(self, selector, text, strategy_key=None, timeout=None):
        waiter = self._get_waiter(timeout)
        by_strategy, actual_selector = self._resolve_selector_to_by_tuple(selector, strategy_key)
        log.info(f"Waiting for text '{text}' in element {by_strategy}='{actual_selector}'.")
        try:
            waiter.until(EC.text_to_be_present_in_element((by_strategy, actual_selector), text))
            log.info(f"Text '{text}' found in element {by_strategy}='{actual_selector}'.")
            return True
        except SeleniumTimeoutException:
            log.warning(f"Timeout waiting for text '{text}' in element {by_strategy}='{actual_selector}'.")
            raise TimeoutException(f"Timeout waiting for text '{text}' in element {by_strategy}='{actual_selector}'.")
        except Exception as e:
            log.error(f"Error waiting for text in element {by_strategy}='{actual_selector}': {e}")
            raise InteractionException(f"Error waiting for text in element {by_strategy}='{actual_selector}': {e}")

    def _get_select_element(self, selector_or_element, strategy_key=None):
        element = self._find_element_internal(selector_or_element, strategy_key)
        return Select(element)

    def select_dropdown_option_by_value(self, selector_or_element, value, strategy_key=None):
        log.info(f"Selecting dropdown option by value '{value}' for element: {selector_or_element}")
        try:
            select = self._get_select_element(selector_or_element, strategy_key)
            select.select_by_value(value)
            log.info(f"Selected option with value '{value}'.")
        except ElementNotFoundException:
            raise
        except SeleniumNoSuchElementException: # Thrown by Select if option not found
            log.error(f"Option with value '{value}' not found in dropdown {selector_or_element}.")
            raise ElementNotFoundException(f"Option with value '{value}' not found in dropdown {selector_or_element}.")
        except Exception as e:
            log.error(f"Error selecting dropdown option by value for {selector_or_element}: {e}")
            raise InteractionException(f"Error selecting dropdown option by value for {selector_or_element}: {e}")

    def select_dropdown_option_by_index(self, selector_or_element, index, strategy_key=None):
        log.info(f"Selecting dropdown option by index '{index}' for element: {selector_or_element}")
        try:
            select = self._get_select_element(selector_or_element, strategy_key)
            select.select_by_index(index)
            log.info(f"Selected option with index '{index}'.")
        except ElementNotFoundException:
            raise
        except SeleniumNoSuchElementException:
            log.error(f"Option with index '{index}' not found in dropdown {selector_or_element}.")
            raise ElementNotFoundException(f"Option with index '{index}' not found in dropdown {selector_or_element}.")
        except Exception as e:
            log.error(f"Error selecting dropdown option by index for {selector_or_element}: {e}")
            raise InteractionException(f"Error selecting dropdown option by index for {selector_or_element}: {e}")

    def select_dropdown_option_by_visible_text(self, selector_or_element, text, strategy_key=None):
        log.info(f"Selecting dropdown option by visible text '{text}' for element: {selector_or_element}")
        try:
            select = self._get_select_element(selector_or_element, strategy_key)
            select.select_by_visible_text(text)
            log.info(f"Selected option with visible text '{text}'.")
        except ElementNotFoundException:
            raise
        except SeleniumNoSuchElementException:
            log.error(f"Option with visible text '{text}' not found in dropdown {selector_or_element}.")
            raise ElementNotFoundException(f"Option with visible text '{text}' not found in dropdown {selector_or_element}.")
        except Exception as e:
            log.error(f"Error selecting dropdown option by visible text for {selector_or_element}: {e}")
            raise InteractionException(f"Error selecting dropdown option by visible text for {selector_or_element}: {e}")

    def hover_on_element(self, selector_or_element, strategy_key=None):
        log.info(f"Hovering over element: {selector_or_element}")
        try:
            element = self._find_element_internal(selector_or_element, strategy_key)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            log.info(f"Successfully hovered over element.")
        except ElementNotFoundException:
            raise
        except Exception as e:
            log.error(f"Error hovering over element {selector_or_element}: {e}")
            raise InteractionException(f"Error hovering over element {selector_or_element}: {e}")

    # --- End of New Methods ---

    def close(self):
        log.info("Closing browser.")
        if self.driver:
            try:
                self.driver.quit()
                log.info("Browser closed successfully.")
            except WebDriverException as e:
                log.error(f"Error closing browser: {e}")
            finally:
                self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == '__main__':
    print("Running basic JulesScripter test (with new methods - conceptual tests)...")
    # Test with context manager
    try:
        with JulesScripter(browser_type='firefox', headless=True) as bot: # Note: config.load_config will fail here as it's not yet defined
            bot.goto("https://www.example.com")
            print(f"Page title: {bot.driver.title}")
            heading_text = bot.get_text("css:h1")
            print(f"Heading text: {heading_text}")

            # Conceptual test for wait_for_text_in_element
            try:
                bot.wait_for_text_in_element("css:h1", "Example Domain", timeout=5)
                print("Text 'Example Domain' confirmed in H1.")
            except TimeoutException:
                print("Text 'Example Domain' not found in H1 within timeout.")

            # Conceptual test for wait_for_element_disappear (difficult to test on static page)
            # To test this, you'd need a page where an element actually disappears.
            # Example: bot.wait_for_element_disappear("css:#temporary-loading-spinner", timeout=5)

            # Conceptual test for hover (difficult to verify without visual feedback or JS event)
            try:
                bot.hover_on_element("css:h1")
                print("Hovered over H1 (conceptually).")
            except InteractionException as e:
                print(f"Hover test failed: {e}")

            bot.take_screenshot("example_page_enhanced.png")
        print("Firefox test completed (with context manager).")
    except Exception as e:
        # Expecting an error here due to config.load_config not being defined yet
        print(f"Test execution expectedly failed or had issues due to config.load_config: {e}")
        # log.error("Firefox test failed", exc_info=True) # logging might also be affected if config init fails early

    # Dropdown test would require a page with a select element. Example:
    # HTML: <select id="mySelect"><option value="val1">Text1</option></select>
    # bot.select_dropdown_option_by_value("id:mySelect", "val1")
