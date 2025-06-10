import configparser
import os
from .logger import log # Assuming logger is in the same directory or proper path is set

# Default configuration values (used as fallback and for structure)
DEFAULT_SETTINGS = {
    'General': {
        'browser': 'firefox',
        'headless': 'False', # Stored as strings, converted on load
        'screenshot_dir': 'screenshots',
    },
    'Timeouts': {
        'implicit_wait': '10', # seconds
        'explicit_wait': '20', # seconds
        'page_load_timeout': '30', # seconds
    }
}

DEFAULT_CONFIG_FILENAME = 'jules_config.ini'

def _get_type_converted_value(section, key, value_str):
    """ Helper to convert string values from INI to appropriate types. """
    # General section
    if section == 'General':
        if key == 'headless':
            return value_str.lower() in ['true', '1', 'yes', 'on']
    # Timeouts section
    elif section == 'Timeouts':
        if key in ['implicit_wait', 'explicit_wait', 'page_load_timeout']:
            try:
                return int(value_str)
            except ValueError:
                log.warning(f"Config: Invalid integer value '{value_str}' for {section}.{key}. Using default.")
                # Fallback to default for this specific key if conversion fails
                return int(DEFAULT_SETTINGS[section][key])
    # Default: return as string if no specific conversion
    return value_str

def load_config(config_file_path=None):
    """
    Loads configuration from an INI file.
    Defaults are taken from DEFAULT_SETTINGS.
    File settings override defaults.
    """
    parser = configparser.ConfigParser()

    # Load default settings into the parser first
    # This ensures all sections and keys are present, even if not in the file
    for section, options in DEFAULT_SETTINGS.items():
        parser[section] = {} # Ensure section exists
        for key, value in options.items():
            parser[section][key] = str(value) # Store defaults as strings initially

    # Determine which config file to use
    actual_config_file_path = config_file_path or DEFAULT_CONFIG_FILENAME

    loaded_from_file = False
    if os.path.exists(actual_config_file_path):
        try:
            parser.read(actual_config_file_path)
            log.info(f"Configuration loaded from: {actual_config_file_path}")
            loaded_from_file = True
        except configparser.Error as e:
            log.warning(f"Error parsing configuration file {actual_config_file_path}: {e}. Using default settings.")
    else:
        if config_file_path: # User specified a file but it wasn't found
            log.warning(f"Specified configuration file not found: {config_file_path}. Using default settings.")
        else: # Default file not found, which is fine, just use defaults
            log.info(f"Default configuration file '{DEFAULT_CONFIG_FILENAME}' not found. Using default settings.")

    # Prepare the final configuration dictionary with type conversions
    final_config = {}
    # Consolidate settings from parser (which now contains defaults + file overrides)
    # into a simpler dictionary for the application, with type conversions.
    for section in parser.sections():
        for key in parser[section]:
            value_str = parser.get(section, key) # Get value from parser (could be default or from file)
            # Use a more specific key for the final_config dict if sections are simple
            # e.g., 'browser' instead of 'General.browser'
            config_key = key
            if section == 'General' and key == 'browser': # Example of direct key
                final_config['browser'] = value_str
            elif section == 'General' and key == 'headless':
                final_config['headless'] = _get_type_converted_value(section, key, value_str)
            elif section == 'General' and key == 'screenshot_dir':
                final_config['screenshot_dir'] = value_str
            elif section == 'Timeouts':
                 final_config[key] = _get_type_converted_value(section, key, value_str)
            # Add other specific keys as needed or a generic way to handle them:
            # else:
            #    final_config[f"{section.lower()}_{key}"] = _get_type_converted_value(section, key, value_str)


    # Ensure all default keys are present in final_config, even if not in file or if file was empty
    # This structure is a bit simplified; a more robust merge might be needed for complex configs
    # The current approach relies on parser being pre-filled with defaults.
    # Let's refine final_config structure to match what browser.py expects:

    # Re-build final_config from DEFAULT_SETTINGS structure to ensure all keys are there,
    # then update with values from parser (which includes file overrides).
    processed_config = {}
    for section_name, section_defaults in DEFAULT_SETTINGS.items():
        for key, default_value_str in section_defaults.items():
            # Determine the key for processed_config (e.g., 'browser', 'headless', 'implicit_wait')
            output_key = key
            # Get value from parser (could be default or from file)
            value_from_parser_str = parser.get(section_name, key, fallback=default_value_str)
            processed_config[output_key] = _get_type_converted_value(section_name, key, value_from_parser_str)

    if loaded_from_file:
        log.debug(f"Final merged configuration: {processed_config}")
    else:
        log.debug(f"Using default configuration: {processed_config}")

    return processed_config


# For direct access to default values if needed elsewhere (though load_config is primary)
# These are the string versions before type conversion.
DEFAULT_BROWSER = DEFAULT_SETTINGS['General']['browser']
DEFAULT_HEADLESS_MODE_STR = DEFAULT_SETTINGS['General']['headless'] # String version
SCREENSHOT_DIR = DEFAULT_SETTINGS['General']['screenshot_dir']
DEFAULT_IMPLICIT_WAIT_STR = DEFAULT_SETTINGS['Timeouts']['implicit_wait'] # String version
DEFAULT_EXPLICIT_WAIT_STR = DEFAULT_SETTINGS['Timeouts']['explicit_wait'] # String version
DEFAULT_PAGE_LOAD_TIMEOUT_STR = DEFAULT_SETTINGS['Timeouts']['page_load_timeout'] # String version


if __name__ == '__main__':
    log.info("Testing configuration loading...")

    # Test 1: No config file present (or default name)
    print("\n--- Test 1: Default settings (no jules_config.ini) ---")
    cfg = load_config()
    print(f"Browser: {cfg.get('browser')}, Headless: {cfg.get('headless')}")
    print(f"Implicit Wait: {cfg.get('implicit_wait')}, Screenshot Dir: {cfg.get('screenshot_dir')}")

    # Test 2: Create a dummy config file and test loading it
    print("\n--- Test 2: Custom settings from dummy_config.ini ---")
    dummy_config_content = """
[General]
browser = chrome
headless = True

[Timeouts]
explicit_wait = 25
# implicit_wait will use default
"""
    dummy_file = 'dummy_config.ini'
    with open(dummy_file, 'w') as f:
        f.write(dummy_config_content)

    cfg_custom = load_config(config_file_path=dummy_file)
    print(f"Browser: {cfg_custom.get('browser')}, Headless: {cfg_custom.get('headless')}")
    print(f"Explicit Wait: {cfg_custom.get('explicit_wait')}, Implicit Wait (default): {cfg_custom.get('implicit_wait')}")
    print(f"Page Load Timeout (default): {cfg_custom.get('page_load_timeout')}")

    os.remove(dummy_file)

    print("\n--- Test 3: Non-existent specified config file ---")
    cfg_non_existent = load_config(config_file_path='non_existent_config.ini')
    print(f"Browser: {cfg_non_existent.get('browser')} (should be default)")
