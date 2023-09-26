from .logging2loguru import Logging2Loguru

log = Logging2Loguru().get_logger()
log.info("this is a info message!")
log.error("this is a error message!")

# Logging2Loguru(r'D:\PythonProjects\standardization-tools\test\log-tests\log.xml').get_logger('foo').info('first message')
# Logging2Loguru(r'D:\PythonProjects\standardization-tools\test\log-tests\log.xml').get_logger('foo.bar').error('second message')
# Logging2Loguru(r'D:\PythonProjects\standardization-tools\test\log-tests\log.xml').get_logger('bar').error('bar message')

log2 = Logging2Loguru(r'D:\PythonProjects\standardization-tools\test\log-tests\log.xml').get_logger()
log2.error('bar message')