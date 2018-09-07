# -*- coding: utf-8 -*-
import hashlib
import json
import string
import time
import random

import requests

# from Linjia.configs.wxconfig import APPID, APPSECRET
# appid = APPID
# appsecret = APPSECRET


class Sign:
    def __init__(self, appId, appSecret, url):
        self.appId = appId
        self.appSecret = appSecret

        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': self.getJsApiTicket(),
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

    def getJsApiTicket(self):
        data = json.loads(open('jsapi_ticket.json').read())
        jsapi_ticket = data['jsapi_ticket']
        if data['expire_time'] < time.time():
            url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=%s" % (getAccessToken(self.appId, self.appSecret))
            response = requests.get(url)
            jsapi_ticket = json.loads(response.text)['ticket']
            data['jsapi_ticket'] = jsapi_ticket
            data['expire_time'] = int(time.time()) + 7000
            fopen = open('jsapi_ticket.json', 'w')
            fopen.write(json.dumps(data))
            fopen.close()
        return jsapi_ticket

    def getAccessToken(self):
        data = json.loads(open('access_token.json').read())
        access_token = data['access_token']
        if data['expire_time'] < time.time():
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (self.appId, self.appSecret)
            response = requests.get(url)
            access_token = json.loads(response.text)['access_token']
            data['access_token'] = access_token
            data['expire_time'] = int(time.time()) + 7000
            fopen = open('access_token.json', 'w')
            fopen.write(json.dumps(data))
            fopen.close()
        return access_token



"""

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

"""


if __name__ == '__main__':
    # 注意 URL 一定要动态获取，不能 hardcode
    appId = 'wx9aaaaaaaaaaaaa'
    appSecret = 'a******************'
    sign = Sign(appId, appSecret, 'http://l.wkt.ooo:7443')
    print sign.sign()

    # res = AccessToken.get_access_token()
    # print(res)
