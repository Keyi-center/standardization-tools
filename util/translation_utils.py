import hashlib
import json
import time
import uuid

import requests


YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '6ecde8517a197197'
APP_SECRET = '1OvhoKkskX0rG1sB8bUZhgtmNqZASLso'


def encrypt(sign_str):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(sign_str.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def translate(query, to_lan='en', from_lan='auto'):
    data = {'from': from_lan, 'to': to_lan, 'signType': 'v3'}
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    sign_str = APP_KEY + truncate(query) + salt + curtime + APP_SECRET
    sign = encrypt(sign_str)
    data['appKey'] = APP_KEY
    data['q'] = query
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    if not response.ok:
        raise RuntimeError('translation failed')
    response_content = json.loads(response.content)
    return response_content.get('translation', []).pop()


def chinese_to_english(query):
    result = translate(query, to_lan='en')
    return result


if __name__ == '__main__':
    chinese_to_english("白日依山尽，黄河入海流")
