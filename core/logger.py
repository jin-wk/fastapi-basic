import os
import socket
import logging
from core.setting import get_setting

setting = get_setting(os.getenv("APP_ENV"))


class Filter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record: logging.LogRecord) -> bool:
        record.hostname = self.hostname
        return True


class Logger:
    def __init__(self) -> None:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = "{}/logs".format(root_dir)
        log_filename = "{}/{}.log".format(log_dir, setting.APP_NAME)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logger = logging.getLogger(setting.APP_NAME)
        logger.setLevel(logging.DEBUG)

        filter = Filter()
        formatter = logging.Formatter(
            '[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(hostname)s] [%(module)s] [%(funcName)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=log_filename, when="midnight", interval=1
        )
        file_handler.setLevel(setting.LOG_LEVEL)
        file_handler.addFilter(filter)
        file_handler.setFormatter(formatter)
        file_handler.suffix = '%Y%m%d'
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(setting.LOG_LEVEL)
        console_handler.addFilter(filter)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logger = logger
