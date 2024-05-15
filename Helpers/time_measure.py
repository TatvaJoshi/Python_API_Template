import time
from contextlib import ContextDecorator

from Helpers.old_utility.logger import get_console_logger,get_file_logger

class TimerContextManager(ContextDecorator):
    """A context manager that logs the time taken for a block of code to execute."""

    def __init__(self, name, request=None):
        self.name = name
        self.file_logger = get_file_logger()
        self.console_logger = get_console_logger()
        self.request = request

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        # Format the log message
        log_message = f"{self.name} took {execution_time:.6f} seconds"
        # Log to console with custom formatting and IP address
        self.console_logger.debug(log_message)

        if self.request:
            try:
        # Log to file with IP address
                self.file_logger.debug(log_message,extra={"request": self.request})
            except Exception as e:
                print(f"Logging to file failed: {e}")

        else:
            self.file_logger.debug(log_message)

        return False