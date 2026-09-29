import logging

from enum import Enum

class LogLevel(Enum):
    DEBUG = logging.DEBUG  # 10
    INFO = logging.INFO  # 20
    WARNING = logging.WARNING  # 30
    ERROR = logging.ERROR  # 40
    CRITICAL = logging.CRITICAL  # 50


def console_logger(name: str, level: LogLevel) -> logging.Logger:
    # Create a named logger
    logger = logging.getLogger(f"__{name}__")
    # Set logger level using enum value
    logger.setLevel(level.value)

    # Create a console handler and set its level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.value)

    # Set the formatter for the console handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger
