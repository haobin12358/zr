# -*- coding: utf-8 -*-
from weixin import Weixin, WeixinMsg

msg = WeixinMsg('token')


def reigster_extensions(app):
    app.add_url_rule("/wechat", view_func=msg.view_func)
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