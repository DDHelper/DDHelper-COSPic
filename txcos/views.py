import warnings

from django.core.exceptions import BadRequest
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import requests
import random

from qcloud_cos.cos_exception import CosException, CosServiceError

from .cos import client, bucket
from . import cos
import re

pattern = re.compile(r'^(http:|https:)?//i[0-9].hdslb.com/([a-zA-Z0-9/.@-_]+)$')


def parse_url(url: str):
    match = pattern.match(url)
    if match:
        path = match.groups()[1]
        return 'hdslb/' + path, path
    else:
        return None


def get_download_url(path):
    return f"http://i{random.randint(0, 2)}.hdslb.com/{path}"


def pic(request):
    try:
        url = request.GET['url']
    except KeyError or ValueError:
        raise BadRequest()

    result = parse_url(url)
    if result is None:
        return JsonResponse({"msg": "无效的url"}, status=400)
    key, path = result
    try:
        client.head_object(Bucket=bucket, Key=key)
    except CosServiceError as e:
        # 对象不存在，创建并存储
        rqs = requests.get(get_download_url(path))
        if rqs.status_code != 200:
            warnings.warn(f"原始url错误：{rqs.status_code}")
            return JsonResponse({"msg": f"原始url错误：{rqs.status_code}"}, status=400)
        if e.get_digest_msg()['code'] == 'NoSuchResource':
            client.put_object(
                Bucket=bucket,
                Key=key,
                Body=rqs
            )
        else:
            warnings.warn(f"未知cos错误：{e}")
            return JsonResponse({"msg": "未知错误"}, status=400)
    return HttpResponseRedirect(client.get_object_url(Bucket=bucket, Key=key))




