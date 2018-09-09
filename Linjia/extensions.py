# -*- coding: utf-8 -*-
from weixin import Weixin
weixin = Weixin()


def reigster_extensions(app):
    weixin.init_app(app)
    from Linjia.configs.wxconfig import APPID, APPSECRET
    app.config.from_object(dict(WEIXIN_APP_ID=APPID, WEIXIN_APP_SECRET=APPSECRET, WEIXIN_TOKEN='token111'))
    app.add_url_rule("/wechat", view_func=weixin.view_func)