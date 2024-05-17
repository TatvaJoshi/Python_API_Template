import functools
import os
import smtplib
import sys
from email.message import EmailMessage
from loguru import logger
# from notifiers import GetNotifier
from notifiers.logging import NotificationHandler
import notifiers
from DAL.Database.DbConnection import GetDb

class LoggerFactory:
   def __init__(self):
       self.consoleLogger = logger
       self.fileLogger = logger
       self.fileConsoleLogger = logger
       self.emailLogger = logger
       self.dbLogger = logger

   def SetupConsoleLogger(self):
       logLevel = os.environ.get("LOG_LEVEL", "DEBUG")
       logFormat = os.environ.get("LOG_FORMAT", "<green><level>{level: <8}</level></green>| {time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{message}</level>")
       self.consoleLogger.add(
           sys.stdout, level=logLevel, format=logFormat, colorize=True, backtrace=True, diagnose=True,
       )
       return self.consoleLogger

   def SetupFileLogger(self):
       logLevel = os.environ.get("LOG_LEVEL", "INFO")
       logFormat = os.environ.get("LOG_FORMAT", "<green><level>{level: <8}</level></green>| {time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{message}</level>")
       self.fileLogger.add(
           r"C:\\app\\Logs\\app.log", level=logLevel, format=logFormat,
       )
       return self.fileLogger

   def SetupFileConsoleLogger(self):
       logLevel = os.environ.get("LOG_LEVEL", "DEBUG")
       logFormat = os.environ.get("LOG_FORMAT", "<green><level>{level: <8}</level></green>| {time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{message}</level>")
       self.fileConsoleLogger.add(
           sys.stdout, level=logLevel, format=logFormat, colorize=True, backtrace=True, diagnose=True,
       )
       self.fileConsoleLogger.add(
           r"C:\\app\\Logs\\app.log", level=logLevel, format=logFormat,
       )
       return self.fileConsoleLogger

   def SetupDbLogger(self):
       logLevel = os.environ.get("LOG_LEVEL", "INFO")
       logFormat = os.environ.get("LOG_FORMAT", "{time} {level} {message}")

       async def dbLoggerHandler(message):
           async with GetDb() as conn:
               await conn.execute("INSERT INTO logs (message) VALUES ($1)", message)

       self.dbLogger.add(
           dbLoggerHandler, level=logLevel, format=logFormat,
       )
       return self.dbLogger

   @staticmethod
   def GetEmailHandler(username: str, password: str, to: str):
       notifier = notifiers.GetNotifier("gmail")
       notifier.notify = functools.partial(notifier.notify, username=username, password=password, to=to)
       handler = NotificationHandler(notifier)
       return handler