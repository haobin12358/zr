# -*- coding: utf-8 -*-
from Linjia.extensions import weixin


@weixin.all
def all(**kwargs):
    return weixin.reply(kwargs['sender'], sender=kwargs['receiver'], content='all')


@weixin.text()
def hello(**kwargs):
    """
    监听所有文本消息
    """
    return "hello too"


@weixin.text("help")
def world(**kwargs):
    """
    监听help消息
    """
    return dict(content="hello world!")


@weixin.subscribe
def subscribe(**kwargs):
    """
    监听订阅消息
    """
    print kwargs
    return "欢迎订阅我们的公众号"