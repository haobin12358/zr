# -*- coding: utf-8 -*-
from Linjia.extensions import msg


# @msg.all
# def all(**kwargs):
#     return msg.reply(kwargs['sender'], sender=kwargs['receiver'], content='all')


@msg.text()
def hello(**kwargs):
    """
    监听所有文本消息
    """
    return "hello too"


@msg.text("help")
def world(**kwargs):
    """
    监听help消息
    """
    return dict(content="hello world!")


@msg.subscribe
def subscribe(**kwargs):
    """
    监听订阅消息
    """
    print kwargs
    return "欢迎订阅我们的公众号"