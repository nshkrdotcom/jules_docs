import sys
import os

# Adjust path to import jules_scripter if running from examples dir
# This assumes 'jules_scripter' directory is at the same level as 'examples'
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from jules_scripter import JulesScripter, log, ElementNotFoundException, TimeoutException

def main():
    log.info("Starting Jules.google.com interaction demo script.")

    # Use a try-except-finally block to ensure browser cleanup
    # Initialize with Chrome, headless mode for this example
    # In a real VM, ensure Chrome and ChromeDriver are available/installable by webdriver-manager
    bot = None
    try:
        with JulesScripter(browser_type='chrome', headless=True) as bot:
            log.info("JulesScripter initialized with Chrome (headless).")

            # 1. Navigate to jules.google.com
            target_url = "http://jules.google.com" # Hypothetical URL
            log.info(f"Navigating to {target_url}...")
            bot.goto(target_url)
            log.info(f"Successfully navigated to {target_url}. Page title: {bot.driver.title}")

            # 2. Find a search input field and type a query
            # Assuming a search input with id 'search-query-input'
            search_input_selector = "id:search-query-input"
            search_query = "how to script interactions"
            log.info(f"Typing '{search_query}' into input field '{search_input_selector}'...")
            bot.type_into(search_input_selector, search_query)
            log.info("Successfully typed into search input.")

            # 3. Click a search button
            # Assuming a search button with id 'search-submit-button'
            search_button_selector = "id:search-submit-button"
            log.info(f"Clicking search button '{search_button_selector}'...")
            bot.click(search_button_selector)
            log.info("Successfully clicked search button.")

            # 4. Wait for results and extract some text
            # Assuming results are in a div with id 'search-results-container'
            # or a 'no-results-message' p tag if nothing is found.
            results_container_selector = "id:search-results-container"
            no_results_selector = "css:.no-results-message" # Example CSS selector

            log.info("Waiting for search results...")
            try:
                # Wait for either the results container or a no results message
                # This requires a more complex wait condition not directly in the prototype,
                # so we'll try to find the results container first with a standard wait.
                # A real implementation might add wait_for_any_element()

                # For now, let's assume we expect results. If not, it will raise ElementNotFoundException.
                bot.wait.until(lambda driver: driver.find_element(bot.SELECTOR_STRATEGIES['id'], "search-results-container") or \
                                             driver.find_element(bot.SELECTOR_STRATEGIES['css'], ".no-results-message"))
                log.info("Results area is present.")

                # Try to get text from results container
                try:
                    results_text = bot.get_text(results_container_selector)
                    log.info(f"Results found: {results_text[:200]}...") # Log first 200 chars
                except ElementNotFoundException:
                    # If results_container_selector wasn't the one that appeared, try no_results_selector
                    try:
                        no_results_text = bot.get_text(no_results_selector)
                        log.info(f"No results: {no_results_text}")
                    except ElementNotFoundException:
                        log.warning("Neither results container nor no-results message found.")

            except TimeoutException:
                log.warning("Timed out waiting for search results or no results message.")
            except ElementNotFoundException:
                log.warning("Could not find the primary search results container after initial wait.")


            # 5. Take a screenshot
            screenshot_file = "jules_interaction_snapshot.png"
            log.info(f"Taking screenshot: {screenshot_file}...")
            bot.take_screenshot(screenshot_file)
            log.info(f"Screenshot saved to {os.path.join(bot.config.SCREENSHOT_DIR, screenshot_file)}")

            log.info("Demo script interaction steps completed.")

    except ElementNotFoundException as e:
        log.error(f"Demo script failed: Element not found - {e}")
    except TimeoutException as e:
        log.error(f"Demo script failed: Operation timed out - {e}")
    except Exception as e:
        log.error(f"Demo script failed with an unexpected error: {e}", exc_info=True)
    finally:
        log.info("Jules.google.com interaction demo script finished.")

if __name__ == "__main__":
    main()
