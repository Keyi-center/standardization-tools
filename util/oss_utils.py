'''
测试上传下载
https://cloud.tencent.com/document/product/436/12269
pip install -U cos-python-sdk-v5 -i https://mirrors.cloud.tencent.com/pypi/simple
'''

import logging
import sys

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
# 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
secret_id = 'AKIDzpSr67uUq9E6kiT0KQK0TirulQuCJG0Z'
# 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
secret_key = 'QcbOyLXXLxMfldHiz3uY1JPIyGRQIzUm'
# 已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
region = 'ap-shanghai'
bucket = "ai-painting-1254232194"
# 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
token = None
# 指定使用 http/https 协议来访问 COS，默认为 https，可不填
scheme = 'https'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


def upload_file(file_path, filename, prefix='media'):
    key = f'{prefix}/{filename}'
    with open(file_path, 'rb') as fp:
        response = client.put_object(
            Bucket=bucket,
            Body=fp,
            Key=key,
            StorageClass='STANDARD',
            EnableMD5=False
        )

    print(response['ETag'])
    return client.get_object_url(bucket, key)


if __name__ == '__main__':
    #### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
    # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
    upload_file('picture.jpg', )
    with open('picture.jpg', 'rb') as fp:
        response = upload_file('picture.jpg', fp)
    print(response)
    print(response['ETag'])
    print(response['url'])

    # https://sci-art-1254232194.cos.ap-shanghai.myqcloud.com/text2painting/picture.jpg
    # https://sci-art-1254232194.cos.ap-shanghai.myqcloud.com/picture.jpg
