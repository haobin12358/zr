# -*- coding: utf-8 -*-
import uuid

import requests
from flask import request, redirect

from Linjia.commons.success_response import Success
from Linjia.commons.token_required import usid_to_token
from Linjia.configs.messages import get_token_success
from Linjia.configs.url_config import HTTP_HOST
from Linjia.configs.wxconfig import APPID, WXSCOPE, APPSECRET
from Linjia.service import SUser


class CUser():
    def __init__(self):
        self.suser = SUser()

    def wechat_login(self):
        """获取微信跳转链接"""
        redirect_url = request.args.get('redirect_url', HTTP_HOST + '/user/get_wechat_info')
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
              'appid=%s&redirect_uri=%s&response_type=code' \
              '&scope=%s&state=STATE#wechat_redirect' % (APPID, redirect_url, WXSCOPE)
        return Success('获取跳转链接成功',  {'url': url}, status=302)

    def get_wechat_user_info(self):
        """获取用户信息"""
        args = request.args.to_dict()
        if not args:
            data = Success('跳转链接', {'url': '/user/wechat_login'}, status_code=302)
            return data
        code = args.get('code')
        if not code:
            return redirect('/user/wechat_login')
        access_token, oppenid = self.get_access_token(code)
        userinfo = self.get_info(access_token, oppenid)
        user = self.suser.get_user_by_openid(oppenid)
        # 如果没有使用微信登录过
        if not user:
            print('第一次登录')
            user_dict = self.generic_user_info_by_wechat(userinfo)
            self.suser.add_model('User', **user_dict)
            usid = user_dict.get('USid')
        else:
            # 如果使用微信登录过
            usid = user.USid
        token = usid_to_token(usid)
        # todo 绑定手机操作
        data = {
            'token': token
        }
        return Success(get_token_success, data)

    @staticmethod
    def generic_user_info_by_wechat(userinfo):
        user = {
            'USid': str(uuid.uuid4()),
            'USnickname': userinfo.get('nickname'),
            'USgender': userinfo.get('sex'),
            'USheader': userinfo.get('headimgurl'),
            'WXopenid': userinfo.get('openid'),
            'WXprivilege': str(userinfo.get('privilege')),
        }
        return user

    @staticmethod
    def get_access_token(code):
        """请求微信服务获取 access_token, oppenid"""
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
              'appid=%s&secret=%s&code=%s&' \
              'grant_type=authorization_code' % (APPID, APPSECRET, code)
        json_response = requests.get(url).json()
        access_token = json_response.get('access_token')
        oppenid = json_response.get('openid')
        return access_token, oppenid

    @staticmethod
    def get_info(access_token, opponid):
        url = 'https://api.weixin.qq.com/sns/userinfo?' \
              'access_token=%s&openid=%s&lang=zh_CN' % (access_token, opponid)
        json_res = requests.get(url).json()
        return json_res

