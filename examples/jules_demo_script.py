import sys
import os
import time # For demonstration purposes

# Adjust path to import jules_scripter if running from examples dir
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from jules_scripter import JulesScripter, log, ElementNotFoundException, TimeoutException

def main():
    log.info("Starting Jules.google.com interaction demo script (enhanced).")
    log.info("Note: This script might use settings from 'jules_config.ini' if present in the working directory.")

    bot = None
    try:
        # Initialize JulesScripter. It will look for 'jules_config.ini' by default.
        # Or specify a path: JulesScripter(config_file_path='my_custom_config.ini')
        # Constructor arguments will override INI settings e.g. JulesScripter(browser_type='edge')
        with JulesScripter(headless=True) as bot: # Let config file or defaults decide browser
            log.info(f"JulesScripter initialized. Browser: {bot.browser_type}, Headless: {bot.headless}, Explicit Wait: {bot.explicit_wait_time}s")

            target_url = "https://www.example.com" # Using example.com for actual interaction
            log.info(f"Navigating to {target_url}...")
            bot.goto(target_url)
            log.info(f"Successfully navigated to {target_url}. Page title: {bot.driver.title}")

            # Showcase get_attribute
            h1_selector = "css:h1"
            try:
                h1_tag_name = bot.find_element(h1_selector).tag_name # Get tag name of the element
                h1_text_content = bot.get_text(h1_selector)
                log.info(f"Found element '{h1_selector}'. Tag: '{h1_tag_name}', Text: '{h1_text_content}'")

                # Showcase wait_for_text_in_element
                log.info(f"Waiting for text '{h1_text_content}' to be in '{h1_selector}'...")
                bot.wait_for_text_in_element(h1_selector, h1_text_content, timeout=5)
                log.info("Text confirmed in element.")

            except (ElementNotFoundException, TimeoutException) as e:
                log.error(f"Error with H1 element: {e}")

            # Hypothetical search interaction (adapted from original script)
            # On example.com, these will fail, which can demonstrate error handling.
            search_input_selector = "id:search-query-input" # Does not exist on example.com
            search_query = "how to script interactions"

            log.info(f"Attempting to type '{search_query}' into non-existent input field '{search_input_selector}'...")
            try:
                bot.type_into(search_input_selector, search_query, clear_first=False) # showcase clear_first
                log.info("Successfully typed into search input.")
            except ElementNotFoundException:
                log.warning(f"As expected, element '{search_input_selector}' not found for typing.")

            # Hypothetical dropdown - imagine there's a language selector
            # <select id="lang-select"> <option value="en">English</option> <option value="es">Español</option> </select>
            lang_dropdown_selector = "id:lang-select" # Does not exist on example.com
            log.info(f"Attempting to select from non-existent dropdown '{lang_dropdown_selector}'...")
            try:
                bot.select_dropdown_option_by_visible_text(lang_dropdown_selector, "Español")
                log.info("Selected language (hypothetically).")
            except ElementNotFoundException:
                log.warning(f"As expected, dropdown '{lang_dropdown_selector}' not found.")

            # Showcase hover_on_element
            paragraph_selector = "css:p" # Hover over the first paragraph
            try:
                log.info(f"Hovering over element '{paragraph_selector}'...")
                bot.hover_on_element(paragraph_selector)
                log.info("Successfully hovered over paragraph.")
            except (ElementNotFoundException, InteractionException) as e:
                log.error(f"Could not hover over paragraph: {e}")

            # Showcase wait_for_element_disappear - this needs an element that actually disappears
            # For now, we'll just log the intent.
            disappearing_element_selector = "id:loading-spinner" # Hypothetical
            log.info(f"Conceptually waiting for '{disappearing_element_selector}' to disappear (will likely timeout if not present).")
            try:
                bot.wait_for_element_disappear(disappearing_element_selector, timeout=2) # Short timeout
                log.info(f"Element '{disappearing_element_selector}' disappeared.")
            except TimeoutException:
                log.info(f"Element '{disappearing_element_selector}' did not disappear within timeout (as expected).")


            # Take a screenshot
            screenshot_file = "example_com_snapshot_enhanced.png"
            log.info(f"Taking screenshot: {screenshot_file}...")
            # screenshot_dir is now read from config by JulesScripter
            # So, the path will be os.path.join(bot.screenshot_dir, screenshot_file)
            saved_at = bot.take_screenshot(screenshot_file)
            log.info(f"Screenshot saved to {saved_at}")

            log.info("Demo script interaction steps completed.")

    except ElementNotFoundException as e:
        log.error(f"Demo script failed: Element not found - {e}")
    except TimeoutException as e:
        log.error(f"Demo script failed: Operation timed out - {e}")
    except Exception as e:
        log.error(f"Demo script failed with an unexpected error: {e}", exc_info=True)
    finally:
        log.info("Jules.google.com interaction demo script (enhanced) finished.")

if __name__ == "__main__":
    main()
