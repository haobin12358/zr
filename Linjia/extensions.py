# -*- coding: utf-8 -*-
from flask import current_app, request
from weixin import Weixin, WeixinMsg, WeixinLogin
from weixin.login import WeixinLoginError
from werkzeug.utils import redirect

from Linjia import PARAMS_ERROR
from Linjia.commons.params_validates import parameter_required
from Linjia.configs.url_config import HTTP_HOST
from Linjia.configs.wxconfig import APPSECRET, APPID
from Linjia.service import SUser

msg = WeixinMsg('token')


def reigster_extensions(app):
    app.add_url_rule("/wechat", view_func=msg.view_func)
    wxlogin = WeixinLogin(APPID, APPSECRET)
    @msg.all
    def all_test(**kwargs):
        print kwargs
        # 或者直接返回
        # return "all"
        return msg.reply(
            kwargs['sender'], sender=kwargs['receiver'], content='all'
        )

    @msg.text()
    def hello(**kwargs):
        return dict(content="hello too!", type="text")

    @msg.text("world")
    def world(**kwargs):
        return msg.reply(
            kwargs['sender'], sender=kwargs['receiver'], content='hello world!'
        )

    @msg.image
    def image(**kwargs):
        print kwargs
        return ""

    @msg.subscribe
    def subscribe(**kwargs):
        print kwargs
        return ""

    @msg.unsubscribe
    def unsubscribe(**kwargs):
        print kwargs
        return "fdasfdsa"

    @app.route('/wechat/callback')
    def weixin_callback():
        """通过code, 获取用户信息"""
        args = parameter_required(('code', ))
        code = args.get('code')
        try:
            data = wxlogin.access_token(code)
            data = wxlogin.user_info(data.access_token, data.openid)
            state = args.get('state').split('P')
            usid = state[0]
            redirect_url = state[1]
            to_model = {
                'UScity': data.get('city'),
                'WXopenid': data.get('openid'),
                'WXnickname': data.get('nickname'),
                'USnickname': data.get('nickname'),
                'USheader': data.get('headimgurl'),
                'WXprovice': data.get('province')
            }
            to_model['USgender'] = 0 if data.get('sex') == 1 else 1
            suser = SUser()
            updated = suser.update_user_by_usid(usid, to_model)
            return redirect(redirect_url)
        except WeixinLoginError as e:
            current_app.logger.error(request.url)
            # raise PARAMS_ERROR(u'登录出现错误')
            return redirect(HTTP_HOST)
