import logging
import os
from utils.config import ConfigManager


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        config = ConfigManager().get_logging_config()
        log_level = getattr(logging, config.get('level', 'INFO'))
        log_format = config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = config.get('file_path', 'logs/test.log')

        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = logging.getLogger('ecommerce_test')
        self.logger.setLevel(log_level)

        formatter = logging.Formatter(log_format)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)