# -*- coding: utf-8 -*-
from weixin import Weixin, WeixinMsg

msg = WeixinMsg('token')


def reigster_extensions(app):
    app.add_url_rule("/wechat", view_func=msg.view_func)