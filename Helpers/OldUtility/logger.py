import logging
from logging import FileHandler, StreamHandler
from datetime import datetime

class IPAddressLogFilter(logging.Filter):
    def filter(self, record):
        request = getattr(record, "request", None)
        if request is not None:
            record.ip_address = request.client.host
        else:
            record.ip_address = "Server"
        return True

class IPAddressLogFormatter(logging.Formatter):
    def format(self, record):
        ip_address = getattr(record, "ip_address", "Server")
        record.msg = f"[{datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S,%f')}][{ip_address}][{record.msg}]"
        return super().format(record)

def configure_loggers():
    file_handler = FileHandler(r'C:\app\Logs\app.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S,%f')
    file_handler.setFormatter(file_formatter)

    file_logger = logging.getLogger('file_logger')
    file_logger.setLevel(logging.DEBUG)
    file_logger.addHandler(file_handler)
    file_handler.addFilter(IPAddressLogFilter())
    file_handler.setFormatter(IPAddressLogFormatter())

    console_logger = logging.getLogger('console_logger')
    console_logger.setLevel(logging.DEBUG)
    console_handler = StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('\033[92m%(levelname)s:    %(message)s\033[0m')
    console_handler.setFormatter(console_formatter)
    console_logger.addHandler(console_handler)

    return file_logger, console_logger

def get_file_logger():
    return logging.getLogger('file_logger')

def get_console_logger():
    return logging.getLogger('console_logger')
