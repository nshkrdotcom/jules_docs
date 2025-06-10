# This file makes Python treat the directory as a package.
# You can also expose parts of your library here for easier imports.

from .browser import JulesScripter
from .exceptions import * # Import all custom exceptions
from .logger import log # Expose the default logger instance

__version__ = "0.1.0"
