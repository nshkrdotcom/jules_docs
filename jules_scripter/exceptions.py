class JulesScripterException(Exception):
    """Base exception for the Jules Scripter library."""
    pass

class BrowserInitializationError(JulesScripterException):
    """Raised when the browser fails to initialize."""
    pass

class ElementNotFoundException(JulesScripterException):
    """Raised when an element cannot be found on the page."""
    pass

class TimeoutException(JulesScripterException):
    """Raised when an operation times out."""
    pass

class NavigationException(JulesScripterException):
    """Raised for errors during page navigation."""
    pass

class InteractionException(JulesScripterException):
    """Raised for errors during element interaction (e.g., click, type)."""
    pass
