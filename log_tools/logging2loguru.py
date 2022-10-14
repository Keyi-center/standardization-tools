import logging

from logging_handler import InterceptHandler


class Logging2Loguru():

    def __init__(self, xml_path=''):
        self.xml_path = xml_path

    def get_logger(self, name=None):
        logging.basicConfig(handlers=[InterceptHandler(self.xml_path)], level=0, force=True)
        log = logging.getLogger(name)

        return log
