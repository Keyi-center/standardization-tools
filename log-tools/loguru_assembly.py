from lxml import etree
import os
import sys
from loguru import logger

class LoguruAssembly:

    def __init__(self, xml_path) -> logger:
        # 先读取XML文件中的配置数据
        # 由于config.xml放置在与当前文件相同的目录下，因此通过 __file__ 来获取XML文件的目录，然后再拼接成绝对路径
        if xml_path != '':
            # 这里利用了lxml库来解析XML
            root = etree.parse(xml_path).getroot()
            # 读取日志文件保存路径
            log_path = './log' if root.find('logpath') is None else root.find('logpath').text
            # 读取日志文件容量，转换为字节
            log_retention = '15 days' if root.find('logretention') is None else root.find('logretention').text
            # 读取日志文件保存个数
            log_rotation = '00:00' if root.find('logrotation') is None else root.find('logrotation').text
            # 读取日志文件保存格式
            log_format = '' if root.find('logformat') is None else root.find('logformat').text

            log_level = 'DEBUG' if root.find('loglevel') is None else root.find('loglevel').text

            log_filter = None if root.find('logfilter') is None else root.find('logfilter').text

            log_enqueue = False if root.find('logenqueue') is None else root.find('logenqueue').text

            log_catch = True if root.find('logcatch') is None else root.find('logcatch').text

            # 错误日志
            if log_format == '':
                logger.add(
                    os.path.join(log_path, "ERROR/{time:YYYY-MM-DD}.log"),
                    filter=lambda x: True if x["level"].name == "ERROR" else False,
                    rotation=log_rotation, retention=log_retention, level='ERROR', encoding='utf-8',
                    enqueue=log_enqueue, catch=log_catch
                )
                logger.add(
                    os.path.join(log_path, "Default/{time:YYYY-MM-DD}.log"),
                    rotation="00:00", retention=log_retention, level=log_level, encoding='utf-8',
                    enqueue=log_enqueue, catch=log_catch
                )
            else:
                logger.add(
                    os.path.join(log_path, "ERROR/{time:YYYY-MM-DD}.log"),
                    format=log_format,
                    filter=lambda x: True if x["level"].name == "ERROR" else False,
                    rotation="00:00", retention=log_retention, level='ERROR', encoding='utf-8',
                    enqueue=log_enqueue, catch=log_catch
                )
                # Default日志
                logger.add(
                    os.path.join(log_path, "Default/{time:YYYY-MM-DD}.log"),
                    format=log_format, rotation="00:00", retention=log_retention, level="INFO",
                    encoding='utf-8'
                )
        else:
            logger.add(
                "log/ERROR/{time:YYYY-MM-DD}.log",
                filter=lambda x: True if x["level"].name == "ERROR" else False,
                rotation="00:00", retention="15 days", level='ERROR', encoding='utf-8'
            )

            logger.add(
                "log/Default/{time:YYYY-MM-DD}.log",
                rotation="00:00", retention="15 days", level="INFO", encoding='utf-8'
            )

        self.logger = logger


    def get_logger(self):
        return self.logger
