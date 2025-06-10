# Jules Scripter: Web Interaction Scripting System

## 1. Introduction

Jules Scripter is a Python-based system designed to simplify scripting interactions with web pages, particularly for use in environments like a fresh Ubuntu 24.04 desktop VM. It provides a high-level API wrapper around Selenium WebDriver, making it easier to write robust browser automation scripts. This system was devised to script interactions with `jules.google.com` (hypothetical).

## 2. Features

*   Simplified API for common web interactions (navigation, clicks, typing, text extraction).
*   Automatic browser driver management (for Chrome, Firefox, Edge) via `webdriver-manager`.
*   Built-in explicit waits to improve script reliability.
*   Configurable logging to console and file.
*   Custom exceptions for clearer error handling.
*   Support for headless browser execution.
*   Easy screenshot capture.
*   Selector strategy parsing (e.g., "id:element-id", "css:.my-class").

## 3. Prerequisites

*   Ubuntu 24.04 Desktop VM (or any system that can run Python and modern browsers).
*   Python 3.8+ and Pip.
*   A supported web browser installed (Firefox or Chrome recommended). The system will attempt to download the correct driver.

## 4. Installation

1.  **Clone the Repository (if applicable)**
    If this project is hosted in a Git repository:
    ```bash
    git clone <repository_url>
    cd jules_scripter_project
    ```
    Otherwise, ensure you have the `jules_scripter` library directory and the `examples` directory.

2.  **Set up a Virtual Environment (Recommended)**
    Navigate to the project root directory (e.g., `jules_scripter_project`).
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    To deactivate: `deactivate`

3.  **Install Dependencies**
    With the virtual environment activated, install the required packages:
    ```bash
    pip install -r jules_scripter/requirements.txt
    ```
    This will install `selenium` and `webdriver-manager`.

4.  **Browser Drivers**
    The `webdriver-manager` library will attempt to automatically download and cache the correct driver (e.g., `geckodriver` for Firefox, `chromedriver` for Chrome) when a script is first run. Ensure you have internet access for this initial download.

## 5. Directory Structure

```
jules_scripter_project/
├── jules_scripter/          # The core library package
│   ├── __init__.py          # Makes it a package, exports key components
│   ├── browser.py           # Contains the main JulesScripter class
│   ├── config.py            # Default configurations
│   ├── driver_manager.py    # Handles WebDriver setup
│   ├── exceptions.py        # Custom exception classes
│   ├── logger.py            # Logging setup
│   └── requirements.txt     # Python dependencies for the library
├── examples/                # Example scripts demonstrating usage
│   └── jules_demo_script.py
└── README.md                # This file
```

## 6. Core Concepts

### The `JulesScripter` Class
This is the main class you'll use to interact with browsers. You instantiate it, optionally specifying the browser type and headless mode, and then call its methods to perform actions.

It's recommended to use it as a context manager to ensure the browser is properly closed:
```python
from jules_scripter import JulesScripter

with JulesScripter(browser_type='firefox', headless=True) as bot:
    bot.goto("https://example.com")
    # ... more actions
```

### Selector Strategies
When finding elements, you can specify the selector strategy directly in the selector string or by using the `strategy_key` parameter.

Supported strategies (keys for `strategy_key` or prefixes in selector string):
*   `id`: Find by element ID. (e.g., `bot.find_element("id:my-button")`)
*   `name`: Find by element `name` attribute. (e.g., `bot.find_element("name:username")`)
*   `xpath`: Find by XPath expression. (e.g., `bot.find_element("xpath://div[@id='main']/p")`)
*   `css`: Find by CSS selector. (e.g., `bot.find_element("css:.my-class > a")`)
*   `class`: Find by class name. (e.g., `bot.find_element("class:submit-button")`)
*   `tag`: Find by tag name. (e.g., `bot.find_element("tag:h1")`)
*   `link_text`: Find by exact link text. (e.g., `bot.find_element("link_text:Click Here")`)
*   `partial_link_text`: Find by partial link text. (e.g., `bot.find_element("partial_link_text:Click")`)

If no strategy prefix is provided in the selector string and `strategy_key` is not used, it defaults to CSS selector (e.g., `bot.find_element(".my-class")` is treated as a CSS selector).

## 7. Basic Usage

The `examples/jules_demo_script.py` file provides a comprehensive example. Here's a simpler one:

```python
import sys
import os

# Adjust path (if running script from a different directory than project root)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir) # Assuming script is in 'examples'
sys.path.insert(0, project_root)

from jules_scripter import JulesScripter, log, ElementNotFoundException

def simple_example():
    log.info("Starting simple example.")
    try:
        with JulesScripter(browser_type='firefox', headless=True) as bot:
            bot.goto("https://example.com")
            log.info(f"Page title: {bot.driver.title}")

            heading_text = bot.get_text("css:h1") # Explicit CSS selector
            log.info(f"Heading (H1): {heading_text}")

            paragraph_text = bot.get_text("p") # Defaults to CSS selector for 'p' tag
            log.info(f"First paragraph: {paragraph_text[:50]}...")

            bot.take_screenshot("simple_example.png")
            log.info("Screenshot taken.")

    except ElementNotFoundException as e:
        log.error(f"Element was not found: {e}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}", exc_info=True)
    finally:
        log.info("Simple example finished.")

if __name__ == "__main__":
    simple_example()
```

To run this (assuming it's saved as `examples/simple_test.py`):
```bash
# Ensure your virtual environment is active
# Ensure you are in the project_root directory
python examples/simple_test.py
```

## 8. API Overview (Key Methods)

Refer to the `jules_scripter/browser.py` file for full details and method signatures.

*   **`JulesScripter(browser_type='firefox', headless=False, implicit_wait=10, explicit_wait=20, page_load_timeout=30, config_file_path=None)`**
    *   Initializes the scripter. `browser_type` can be 'firefox', 'chrome', or 'edge'.
    *   Settings can be overridden by a `jules_config.ini` file (see Configuration section).
    *   `config_file_path`: Optionally specify a path to an INI configuration file. If None, looks for `jules_config.ini` in the current working directory.

*   **`goto(url: str)`**: Navigates the browser to the given URL.

*   **`find_element(selector: str, strategy_key: str = None)`**: Finds a single web element.
    *   Returns a Selenium WebElement.
    *   Raises `ElementNotFoundException` if not found within the explicit wait time.

*   **`get_attribute(selector_or_element, attribute_name: str, strategy_key: str = None)`**: Gets the value of an element's attribute.

*   **`click(selector_or_element, strategy_key: str = None)`**: Clicks an element.
    *   `selector_or_element` can be a selector string or a WebElement instance.

*   **`type_into(selector_or_element, text_to_type: str, strategy_key: str = None, clear_first: bool = True)`**: Types text into an input field.
    *   `clear_first`: If True (default), clears the field before typing.

*   **`get_text(selector_or_element, strategy_key: str = None)`**: Gets the visible text of an element.

*   **`take_screenshot(filename: str = "screenshot.png")`**: Saves a screenshot of the current page to the `screenshots` directory (configurable in `config.py`).

*   **`wait_for_element_disappear(selector: str, strategy_key: str = None, timeout: int = None)`**: Waits for an element to become invisible or stale.
    *   `timeout`: Specific timeout for this wait, otherwise uses default explicit wait.

*   **`wait_for_text_in_element(selector: str, text: str, strategy_key: str = None, timeout: int = None)`**: Waits for the given text to be present in the specified element.

*   **`select_dropdown_option_by_value(selector_or_element, value: str, strategy_key: str = None)`**: Selects a dropdown (`<select>`) option by its `value` attribute.

*   **`select_dropdown_option_by_index(selector_or_element, index: int, strategy_key: str = None)`**: Selects a dropdown option by its numerical index.

*   **`select_dropdown_option_by_visible_text(selector_or_element, text: str, strategy_key: str = None)`**: Selects a dropdown option by its visible text.

*   **`hover_on_element(selector_or_element, strategy_key: str = None)`**: Performs a mouse hover action on an element.

*   **`close()`**: Closes the browser and quits the driver. Automatically called if using a context manager.

*   **`driver`**: The underlying Selenium WebDriver instance, for advanced use if needed.

*   **`wait`**: The Selenium `WebDriverWait` instance, for custom explicit wait conditions.

## 9. Logging

*   Logs are output to both the console and a file named `jules_scripter.log` in the directory where the script is run.
*   Log level and format can be configured in `jules_scripter/logger.py`.
*   Import the `log` object for use in your scripts: `from jules_scripter import log`.

## 10. Configuration

Jules Scripter allows configuration through a file or via constructor parameters.

### Configuration File (`jules_config.ini`)

You can customize the behavior of Jules Scripter by creating a `jules_config.ini` file in the directory where your script is run, or by providing a path to a custom INI file via the `config_file_path` parameter in the `JulesScripter` constructor.

A template file named `jules_scripter/jules_config.ini.template` is provided in the library. Copy this template to `jules_config.ini` (or your custom path) and modify it as needed.

**Example `jules_config.ini`:**
```ini
[General]
browser = chrome
headless = True
screenshot_dir = custom_screenshots

[Timeouts]
explicit_wait = 25
implicit_wait = 5
```

**Priority of Settings:**
1.  Values explicitly passed to the `JulesScripter` constructor (e.g., `JulesScripter(browser='chrome')`).
2.  Values from the configuration file (if `config_file_path` is used or `jules_config.ini` is found).
3.  Default values defined in `jules_scripter/config.py`.

*(Self-correction: The above priority is how it *should* ideally work. The current implementation of `browser.py` __init__ and `config.py` `load_config` is: `load_config` provides a base dictionary from file/defaults, and then `browser.py` constructor parameters override these if provided. This means constructor parameters have the highest priority. The README should reflect current implementation)*

**Corrected Priority of Settings (as per current implementation):**
1.  Values explicitly passed to the `JulesScripter` constructor (e.g., `JulesScripter(browser='chrome')`) take the highest precedence.
2.  If a constructor parameter is not provided, the value is taken from the configuration loaded via `config_file_path` (or default `jules_config.ini`).
3.  If not in the INI file or the INI file is not found, the hardcoded default values from `jules_scripter/config.py` are used.

### Constructor Parameters
You can also override default settings or file settings by passing parameters directly to the `JulesScripter` constructor:
```python
bot = JulesScripter(browser_type='chrome', headless=True, explicit_wait=30)
```
Refer to the API overview for the `JulesScripter` constructor for all available parameters.

## 11. Error Handling

The library uses custom exceptions (defined in `jules_scripter/exceptions.py`) to indicate issues:
*   `BrowserInitializationError`: Problem setting up the browser.
*   `ElementNotFoundException`: Element could not be located.
*   `TimeoutException`: An operation timed out (often waiting for an element).
*   `NavigationException`: Error during page navigation (e.g., `goto`).
*   `InteractionException`: Generic error during element interaction.

Wrap your script actions in `try...except` blocks to handle these.

## 12. Running Examples

1.  Ensure you have followed the Installation steps.
2.  Activate your virtual environment: `source .venv/bin/activate`
3.  Navigate to the project root directory.
4.  Run an example script:
    ```bash
    python examples/jules_demo_script.py
    # or
    python examples/simple_test.py # If you saved the example from section 7
    ```
    Screenshots will be saved in a `screenshots/` directory created in the project root. Logs will be in `jules_scripter.log`.

## 13. Contributing

This project is currently a conceptual design. For future development:
*   Follow standard Python coding conventions (PEP 8).
*   Add unit tests for new features or bug fixes.
*   Update documentation as needed.
