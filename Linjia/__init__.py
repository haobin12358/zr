# -*- coding: utf-8 -*-
from datetime import date

from flask import Flask as _Flask, Response
from werkzeug.exceptions import HTTPException

from Linjia.apis.v1 import AUser, ARoom
from Linjia.apis.v1.verify_wechat import register_blueprint
from flask.json import JSONEncoder as _JSONEncoder
from Linjia.commons.error_response import error_handler
from Linjia.commons.request_handler import request_first_handler


class JSONEncoder(_JSONEncoder):
    """重写对象序列化, 当默认jsonify无法序列化对象的时候将调用这里的default"""
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            res = dict(o)
            for k in res.keys():
                if k[0].isupper():
                    # 字段转小写
                    res[k.lower()] = res[k]
                    res.pop(k)
            return res
        if isinstance(o, Response):
            return o
        if isinstance(o, date):
            # 也可以序列化时间类型的对象
            return o.strftime('%Y-%m-%d')
        if isinstance(o, type):
            raise o()
        if isinstance(o, HTTPException):
            raise o
        raise Exception()


class Flask(_Flask):
    json_encoder = JSONEncoder


def register_route(app):
    # register_blueprint(app)
    app.add_url_rule('/user/<string:user>/', view_func=AUser.as_view('user'))
    app.add_url_rule('/room/<string:room>/', view_func=ARoom.as_view('room'))


def create_app():
    app = Flask(__name__)
    app.config.from_object('Linjia.configs.appsettings')
    register_route(app)
    print(app.debug)
    if not app.debug:
        error_handler(app)
    request_first_handler(app)
    return app