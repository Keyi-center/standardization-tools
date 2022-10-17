# Standardization Tools

用于支持项目的标准化

## log-tools 
log-tools
用于支持日志的标准化，可支持配置文件方式配置

### 日志配置项
| 配置项       | Description      | 默认值 |
| ----------- | ---------------- | -------------- |
| loglevel    | 应将已记录消息发送到接收器的最低严重级别             |  INFO      |
| logpath     | 日志文件保存路径                                |    ./log   |
|logretention | 日志文件保存路径                                |  15 days   |
|logrotation  | 分隔日志文件，何时关闭当前日志文件并启动一个新文件的条件|   00:00    |
|logformat    | 日志记录格式                                    | Loguru默认格式 |
|logenqueue   | 是否异步记录日志内容到文件                         |   False    | 
|logfilter    | 用于决定每个记录的消息是否应该发送到接收器            |   None    |
|logcatch     | 是否应该自动捕获接收器处理日志消息时发生的错误         |   True   |

### 接入方式
1）通过下述命令下载该工具包
```shell
python -m pip install git+http://gitlab.sci-art.zhejianglab.com/sci_art_common/standardization-tools.git@baseline-1.0#egg=log_toolsv
```
2) 导入该工具包
```python
from log_tools.logging2loguru import Logging2Loguru
```
3) 初始化日志类
```python
# config.py

my_log = Logging2Loguru().get_logger() #方式一，默认方式
my_log = Logging2Loguru().get_logger('flask_project') #方式二
my_log = Logging2Loguru(r'D:\PythonProjects\standardization-tools\test\log-tests\log.xml').get_logger('flask_project') #方式三
```
类Logging2Loguru初始化时可以加上日志xml配置的路径，get_logger初始化时可以加上日志的名字。日志xml配置建议放置在根目录下()，如果不加则使用日志默认的配置，日志文件默认保存在项目根目录下的log文件夹中，log文件夹分为Default和Error两个文件，Default保存的时默认日志级别及以上的日志，Error文件夹保存的是error级别的日志。
该日志类可以全局初始化一次，后续直接用即可，建议在全局配置文件config.py中进行初始化。
4) 使用
```python
from config import my_log

my_log.info('flask_gunicorn will be start!')

@app.route("/")
def init():
    my_log.info('gunicorn+flask web服务正常启动........')
    return u"gunicorn+flask web服务正常启动........"
```
### demo示例
#### 代码示例
```python
from logging2loguru import Logging2Loguru  # 导入工具包

log = Logging2Loguru().get_logger()
log.info("this is a info message!")   # info级别日志的打印
log.error("this is a error message!")  # error级别日志的打印

log2 = Logging2Loguru(r'D:\PythonProjects\standardization-tools\test\log-tests\log.xml').get_logger()
log2.info('info message')
log2.warning('warning message')
log2.error('bar message')
```

#### xml配置示例
```xml
<?xml version="1.0" encoding="utf-8"?>

<config>
    <!--  日志级别  -->
    <loglevel>INFO</loglevel>

    <!--  日志保存路径  -->
    <logpath>D:\PythonProjects\standardization-tools\logfile</logpath>

    <!-- 日志文件达到50MB,重新建立文件   -->
    <logrotation>50 MB</logrotation>

    <!--  日志保存天数  -->
    <logretention>10 days</logretention>

    <!-- 日志格式化配置，建议用默认配置   -->
    <logformat>{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}</logformat>
</config>
```


