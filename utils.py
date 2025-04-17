# utils.py

import config

def debug_log(msg: str):
    """
        Prints a debug message if debugging is enabled.

        :param msg: Message to be printed.
    """

    if config.DEBUG:
        print(f"[DEBUG] {msg}")

def log(msg: str):
    """
        Prints a log message if logging is enabled.

        :param msg: Message to be printed.
    """

    if config.LOGGING_ENABLED:
        print(f"[LOG] {msg}")

