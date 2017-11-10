import time
import requests
from config import app_id, secret, url
from flask import Response
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


def code2session(code):
    args = {
        'app_id': app_id,
        'secret': secret,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    r = requests.get(url, **args)
    return r.json()


def json_response(obj):
    return Response(json.dumps(obj, ensure_ascii=False, indent=4), mimetype='application/json')


def douban_isbn(isbn):
    fields = "?fields=" + ','.join([
        'title',
        'summary',
        'image',
        'author',
        'publisher',
        'url',
        'price',

    ])
    url = "https://api.douban.com/v2/book/isbn/" + isbn + fields
    log(url)
    r = requests.get(url)
    log(json.dumps(r.json(), ensure_ascii=False, indent=4))
    return json.loads(json.dumps(r.json()))


if __name__ == '__main__':
    douban_isbn('9787802562547')
    # douban_isbn('9787502146788')
