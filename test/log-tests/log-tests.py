import datetime
import logging
import os
import unittest
from logging2loguru import Logging2Loguru


class TestLogTools(unittest.TestCase):
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = datetime.datetime.now().day

    def test_log_with_default(self):
        with self.assertLogs('loggers', level='INFO') as cm:
            log = Logging2Loguru().get_logger('loggers')
            log.info('first message')
            log.error('second message')
        self.assertEqual(cm.output, ['INFO:loggers:first message',
                                     'ERROR:loggers:second message'])

        with self.assertLogs('logger', level='DEBUG') as cm1:
            Logging2Loguru().get_logger('logger.debug').debug('debug message')
            Logging2Loguru().get_logger('logger.info').info('info message')
            Logging2Loguru().get_logger('logger.warning').warning('warning message')
            Logging2Loguru().get_logger('logger.error').error('error message')
        self.assertEqual(cm1.output, ['DEBUG:logger.debug:debug message',
                                      'INFO:logger.info:info message',
                                      'WARNING:logger.warning:warning message',
                                      'ERROR:logger.error:error message'])

        with self.assertLogs('logger', level='ERROR') as cm1:
            Logging2Loguru().get_logger('logger.debug').debug('debug message')
            Logging2Loguru().get_logger('logger.info').info('info message')
            Logging2Loguru().get_logger('logger.warning').warning('warning message')
            Logging2Loguru().get_logger('logger.error').error('error message')
        self.assertEqual(cm1.output, ['ERROR:logger.error:error message'])

    def test_log(self):
        with self.assertLogs('foo', level='INFO') as cm:
            log = Logging2Loguru(r'D:\PythonProjects\standardization-tools\test\log-tests\log.xml').get_logger('foo')
            log.info('first info message')
            log.warning('second warning message')
            log.error('third error message')
        print(cm.output)
        self.assertEqual(cm.output, ['INFO:foo:first info message',
                                     'WARNING:foo:second warning message',
                                     'ERROR:foo:third error message'])

        self.assertTrue(os.path.exists(r'D:\PythonProjects\standardization-tools\logfile\Default'))
        self.assertTrue(os.path.exists(r'D:\PythonProjects\standardization-tools\logfile\ERROR'))
        self.assertTrue(os.path.exists('D:\\PythonProjects\\standardization-tools\\logfile\\Default\\' +
                                       f'{TestLogTools.y}-{TestLogTools.m}-{TestLogTools.d}.log'))
        self.assertTrue(os.path.exists('D:\\PythonProjects\\standardization-tools\\logfile\\ERROR\\' +
                                       f'{TestLogTools.y}-{TestLogTools.m}-{TestLogTools.d}.log'))


if __name__ == '__main__':
    unittest.main()
