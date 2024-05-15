from fastapi import Depends
from loguru import logger
from typing import Any
from Helpers.config_logger import LoggerFactory

def get_logger_factory() -> LoggerFactory:
    return LoggerFactory()

class ConsoleLoggerDependency:
    def __init__(self, logger_factory: LoggerFactory = Depends(get_logger_factory)):
        self.logger_factory = logger_factory

    def __call__(self):
        return self.logger_factory.setup_console_logger()
    

class FileLoggerDependency:
    def __init__(self, logger_factory: LoggerFactory = Depends(get_logger_factory)):
        self.logger_factory = logger_factory

    def __call__(self):
        return self.logger_factory.setup_file_logger()
    

class FileConsoleLoggerDependency:
    def __init__(self, logger_factory: LoggerFactory = Depends(get_logger_factory)):
        self.logger_factory = logger_factory

    def __call__(self):
        return self.logger_factory.setup_file_console_logger()


