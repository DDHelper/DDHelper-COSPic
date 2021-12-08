# 使用方式

## 前端
```html
<img src="http://服务部署域名/txcos/pic/?url=原始url">
```

## 后端

### 对象存储相关配置
按照[txcos/cos.py](txcos/cos.py)中需求的环境变量配置即可

### 服务相关配置
按照[COSPic/settings.py](COSPic/settings.py)中的环境变量配置即可

修改环境变量 SECRET_KEK, DEBUG, ALLOWED_HOSTS 即可

### Docker
docker中默认端口为8008
