import os
import logging


def log_config(module="generic"):
    # Define log levels and their corresponding values
    log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
    }

    # Set up logger with module name
    logger = logging.getLogger(f'rabbitmq-{module}')

    # Set log level based on environment variable or default to 'info'
    log_level_option = os.environ.get('LOG_LEVEL', 'info').lower()
    log_level = log_levels.get(log_level_option, logging.INFO)
    logger.setLevel(log_level)

    # Configure logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
