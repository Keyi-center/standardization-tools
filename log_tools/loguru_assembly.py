import os
from lxml import etree
from loguru import logger


class LoguruAssembly:

    def __init__(self, xml_path) -> logger:
        if xml_path != '':

            root = etree.parse(xml_path).getroot()

            log_path = './log' if root.find('logpath') is None else root.find('logpath').text

            log_retention = '15 days' if root.find('logretention') is None else root.find('logretention').text

            log_rotation = '00:00' if root.find('logrotation') is None else root.find('logrotation').text

            log_format = '' if root.find('logformat') is None else root.find('logformat').text

            log_level = 'INFO' if root.find('loglevel') is None else root.find('loglevel').text

            log_filter = None if root.find('logfilter') is None else root.find('logfilter').text

            log_enqueue = False if root.find('logenqueue') is None else root.find('logenqueue').text

            log_catch = True if root.find('logcatch') is None else root.find('logcatch').text

            # 错误日志
            if log_format == '':
                logger.add(
                    os.path.join(log_path, "ERROR/{time:YYYY-MM-DD}.log"),
                    filter=lambda x: True if x["level"].name == "ERROR" else False,
                    rotation=log_rotation, retention=log_retention, level='ERROR', encoding='utf-8',
                    enqueue=log_enqueue, catch=log_catch, compression='tar.gz'
                )
                logger.add(
                    os.path.join(log_path, "Default/{time:YYYY-MM-DD}.log"),
                    filter=log_filter,
                    rotation="00:00", retention=log_retention, level=log_level, encoding='utf-8',
                    enqueue=log_enqueue, catch=log_catch, compression='tar.gz'
                )
            else:
                logger.add(
                    os.path.join(log_path, "ERROR/{time:YYYY-MM-DD}.log"),
                    format=log_format,
                    filter=lambda x: True if x["level"].name == "ERROR" else False,
                    rotation="00:00", retention=log_retention, level='ERROR', encoding='utf-8',
                    enqueue=log_enqueue, catch=log_catch, compression='tar.gz'
                )
                # Default日志
                logger.add(
                    os.path.join(log_path, "Default/{time:YYYY-MM-DD}.log"),
                    filter=log_filter,
                    format=log_format, rotation="00:00", retention=log_retention, level="INFO",
                    encoding='utf-8', compression='tar.gz'
                )
        else:
            logger.add(
                "log/ERROR/{time:YYYY-MM-DD}.log",
                filter=lambda x: True if x["level"].name == "ERROR" else False,
                rotation="00:00", retention="15 days", level='ERROR', encoding='utf-8',
                compression='tar.gz'
            )

            logger.add(
                "log/Default/{time:YYYY-MM-DD}.log",
                rotation="00:00", retention="15 days", level="INFO", encoding='utf-8',
                compression='tar.gz'
            )

        self.logger = logger

    def get_logger(self):
        return self.logger
