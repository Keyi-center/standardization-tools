import json
import os.path
import shutil
from pathlib import Path


def update_file(path, content):
    """
    @Param path: absolute path of file that been updated
    @Param content: full override file with this content
    """
    with open(path, 'w') as f:
        f.write(content)


def read_file(path,encoding='utf-8'):
    """
    @Param path: absolute path of file that been read
    """
    with open(path, 'r',encoding=encoding) as f:
        return f.read()


def read_json_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_config(config_path, config_dict):
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, ensure_ascii=False)


def update_json_config(config_path, config_dict):
    try:
        with open(config_path, 'r+', encoding='utf-8') as f:
            file_data = json.load(f)
            file_data.update(config_dict)
            f.seek(0)
            json.dump(file_data, f)
    except FileNotFoundError:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, ensure_ascii=False)


def copy_file(src_file_path, target_dir, filename_without_suffix=None):
    """文件拷贝

    将源文件拷贝到目标目录。
    使用示例：
        - copy_file('/home/x/test.json', '/data/x') -> /data/x/test.json
        - copy_file('/home/x/test.json', '/data/x', 'config') -> /data/x/config.json

    Args:
        src_file_path 源文件路径
        target_dir 目标目录
        filename_without_suffix 目标文件名，默认保留源文件名

    Returns:
        target_file_path 目标文件路径
        target_filename 目标文件名
    """
    src_file = Path(src_file_path)
    if src_file.is_dir():
        raise IsADirectoryError("directory copy not supported")

    if filename_without_suffix:
        suffixes = src_file.suffixes
        target_filename = f"{filename_without_suffix}{''.join(suffixes)}"
    else:
        target_filename = src_file.name

    target_file_path = os.path.join(target_dir, target_filename)
    shutil.copyfile(src_file_path, target_file_path)
    return target_file_path, target_filename
