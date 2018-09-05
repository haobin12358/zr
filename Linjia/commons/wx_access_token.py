# -*- coding: utf-8 -*-
import time

import requests

from Linjia.configs.wxconfig import APPID, APPSECRET
appid = APPID
appsecret = APPSECRET


class AccessToken(object):
    _access_token = None
    _create_time = 0
    _expire_in = 0

    @classmethod
    def get_access_token(cls):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, appsecret)
        if time.time() - cls._create_time > cls._expire_in - 200:
            print('开始获取accesstoken')
            response = requests.get(url).json()
            if 'errcode' in response:
                raise Exception('errorcode')
            else:
                cls._access_token = response.get('access_token')
                cls._create_time = time.time()
                cls._expire_in = response.get('expires_in')
        return cls._access_token


if __name__ == '__main__':
    res = AccessToken.get_access_token()
    print(res)
