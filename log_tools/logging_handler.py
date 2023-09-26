import sys
import logging
from loguru import logger

from .loguru_assembly import LoguruAssembly


class InterceptHandler(logging.Handler):
    def __init__(self, xml_path):
        super().__init__()
        self.logger = LoguruAssembly(xml_path).get_logger()

    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = self.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
