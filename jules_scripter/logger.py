import logging
import sys

DEFAULT_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(funcName)s - %(message)s'
DEFAULT_LOG_LEVEL = logging.INFO
LOG_FILE = 'jules_scripter.log'

def setup_logger(name='jules_scripter', level=DEFAULT_LOG_LEVEL, log_format=DEFAULT_LOG_FORMAT, log_file=LOG_FILE):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if logger is already configured
    if logger.hasHandlers():
        return logger

    # Console Handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch_formatter = logging.Formatter(log_format)
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)

    # File Handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    fh_formatter = logging.Formatter(log_format)
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    return logger

# Default logger instance for easy import
log = setup_logger()

if __name__ == '__main__':
    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    log.critical("This is a critical message.")
