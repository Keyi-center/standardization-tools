from setuptools import setup, find_packages

setup(
    name="standardization-tools",
    version="1.0",
    author="liuzhen",
    author_email="liuzhen@zhejianglab.com",
    description="工程标准化工具包",

    # 项目主页
    url="http://gitlab.sci-art.zhejianglab.com/sci_art_common/standardization-tools/-/blob/main/README.md",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(),

    # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    data_files=[
        ('', ['conf/*.conf']),
        ('/usr/lib/systemd/system/', ['bin/*.service']),
    ],

    # 不打包某些文件
    exclude_package_data={
        'log': 'log.*',
        'test': 'test.*',
        'bandwidth_reporter': ['*.txt', '*.log']
    }
)
