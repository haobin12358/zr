# -*- coding: utf-8 -*-
import uuid

from flask import request, redirect
from weixin import WeixinLogin


from Linjia.commons.error_response import NOT_FOUND, SYSTEM_ERROR
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import usid_to_token
from Linjia.configs.url_config import HTTP_HOST
from Linjia.configs.wxconfig import APPID, WXSCOPE, APPSECRET
from Linjia.service import SUser


class CUser():
    def __init__(self):
        self.suser = SUser()

    def wechat_login(self):
        """获取微信跳转链接"""
        self.wxlogin = WeixinLogin(APPID, APPSECRET)
        url = self.wxlogin.authorize(HTTP_HOST + "/weixin/callback", "snsapi_base")
        return Success('获取跳转链接成功',  {'url': url}, status=302)

    def wexin_callback(self):
        """获取用户信息"""
        args = request.args.to_dict()
        code = args.get('code')
        data = self.wxlogin.access_token(code)
        print data.access_token
        print data.refresh_token
        print data.openid
        data = self.wxlogin.user_info(data.access_token)
        return data

    def admin_login(self):
        """管理员登录"""
        data = parameter_required('username', 'password')
        username = data.get('username')
        password = data.get('password')
        admin = self.suser.verify_admin_login(username, password)
        if not admin:
            raise NOT_FOUND(u'用户名或者密码错误')
        level = admin.ADlevel  # 管理员等级
        token = usid_to_token(admin.ADid, 'Admin')
        return Success(u'获取token成功', {
            'token': token,
            'level': level
        })


    def add_admin(self):
        pass

    def get_wx_config(self):
        from Linjia.configs.wxconfig import APPID, APPSECRET
        from weixin.mp import WeixinMP

        mp = WeixinMP(APPID, APPSECRET)
        data = {
            'config': mp.jsapi_sign(url=request.url)
        }
        response = Success(u'返回签名成功', data)
        return response

