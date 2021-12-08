import os

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 正常情况日志级别使用INFO，需要定位时可以修改为DEBUG，此时SDK会打印和服务端的通信信息
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 1. 设置用户属性, 包括 secret_id, secret_key, region等。Appid 已在CosConfig中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
secret_id = os.environ.get('COS_SecretId')
secret_key = os.environ.get('COS_SecretKey')
region = os.environ.get('COS_Region')

bucket = os.environ.get('COS_Bucket')

token = None
scheme = 'https'

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)

# 2. 获取客户端对象
client = CosS3Client(config)
