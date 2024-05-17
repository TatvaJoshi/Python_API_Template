import time
from contextlib import ContextDecorator
from Helpers.ConfigLogger import LoggerFactory

class TimerContextManager(ContextDecorator):
   """A context manager that logs the time taken for a block of code to execute."""
   def __init__(self, name, request=None):
       self.name = name
       self.fileLogger = LoggerFactory().SetupFileLogger()
       self.consoleLogger = LoggerFactory().SetupConsoleLogger()
       self.request = request

   def __enter__(self):
       self.startTime = time.perf_counter()
       return self

   def __exit__(self, excType, excValue, traceback):
       endTime = time.perf_counter()
       executionTime = endTime - self.startTime
       # Format the log message
       logMessage = f"{self.name} took {executionTime:.6f} seconds"
       # Log to console with custom formatting and IP address
       self.consoleLogger.debug(logMessage)
       if self.request:
           try:
               # Log to file with IP address
               self.fileLogger.debug(logMessage, extra={"request": self.request})
           except Exception as e:
               print(f"Logging to file failed: {e}")
       else:
           self.fileLogger.debug(logMessage)
       return False