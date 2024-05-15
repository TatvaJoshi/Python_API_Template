import functools
import os
import smtplib
import sys
from email.message import EmailMessage
from loguru import logger
from notifiers import get_notifier
from notifiers.logging import NotificationHandler
import notifiers 
from DAL.Database.db_connection import get_db

class LoggerFactory:
    def __init__(self):
        self.console_logger = logger
        self.file_logger = logger  # Remove any existing handlers
        self.file_console_logger = logger  # Remove any existing handlers
        self.email_logger = logger
        self.db_logger=logger

    def setup_console_logger(self):
        log_level = os.environ.get("LOG_LEVEL", "DEBUG")
        log_format = os.environ.get("LOG_FORMAT", "<green><level>{level: <8}</level></green>| {time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{message}</level>")

        self.console_logger.add(
            sys.stdout,
            level=log_level,
            format=log_format,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
        return self.console_logger

    def setup_file_logger(self):
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        log_format = os.environ.get("LOG_FORMAT", "<green><level>{level: <8}</level></green>| {time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{message}</level>")

        self.file_logger.add(
            r"C:\app\Logs\app.log",
            level=log_level,
            format=log_format,
        )
        return self.file_logger
    def setup_file_console_logger(self):
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        log_format = os.environ.get("LOG_FORMAT", "<green><level>{level: <8}</level></green>| {time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{message}</level>")

        self.file_console_logger.add(
            sys.stdout,
            level=log_level,
            format=log_format,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )
        self.file_console_logger.add(
            r"C:\app\Logs\app.log",
            level=log_level,
            format=log_format,
        )
        return self.file_console_logger
    def setup_db_logger(self):
        log_level = os.environ.get("LOG_LEVEL", "INFO")
        log_format = os.environ.get("LOG_FORMAT", "{time} {level} {message}")

        async def db_logger_handler(message):
            async with get_db() as conn:
                await conn.execute("INSERT INTO logs (message) VALUES ($1)", message)
        self.db_logger.add(
            db_logger_handler,
            level=log_level,
            format=log_format,
        )
        return self.db_logger
    @staticmethod
    def get_email_handler(username: str, password: str, to: str):
        notifier = notifiers.get_notifier("gmail")
        notifier.notify = functools.partial(notifier.notify, username=username, password=password, to=to)
        handler = NotificationHandler(notifier)
        return handler