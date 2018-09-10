# -*- coding: utf-8 -*-
from datetime import datetime

from flask.wrappers import Request as _Request
from flask_cors import CORS
from flask import Flask as _Flask, Response, current_app, json
from werkzeug.exceptions import HTTPException, BadRequest

from Linjia.apis.v1 import AUser, ARoom, AIndex, ATrade, AServer, AMover
from Linjia.apis.v1.verify_wechat import register_blueprint
from flask.json import JSONEncoder as _JSONEncoder

from Linjia.commons.error_response import PARAMS_ERROR
from Linjia.commons.logger_handler import error_handler
from Linjia.commons.request_handler import request_first_handler
from Linjia.extensions import reigster_extensions


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
        if isinstance(o, datetime):
            # 也可以序列化时间类型的对象
            return o.strftime('%Y%m%d%H%M%S')
        if isinstance(o, type):
            raise o()
        if isinstance(o, HTTPException):
            raise o
        raise TypeError(repr(o) + " is not JSON serializable")


class Request(_Request):
    def on_json_loading_failed(self, e):
        if current_app is not None and current_app.debug:
            raise BadRequest('Failed to decode JSON object: {0}'.format(e))
        raise PARAMS_ERROR(u'参数异常')

    def get_json(self, force=False, silent=False, cache=True):
        data = self.data
        if not data:
            return
        try:
            rv = json.loads(data)
        except ValueError as e:
            if silent:
                rv = None
                if cache:
                    normal_rv, _ = self._cached_json
                    self._cached_json = (normal_rv, rv)
            else:
                rv = self.on_json_loading_failed(e)
                if cache:
                    _, silent_rv = self._cached_json
                    self._cached_json = (rv, silent_rv)
        else:
            if cache:
                self._cached_json = (rv, rv)
        return rv


class Flask(_Flask):
    json_encoder = JSONEncoder
    request_class = Request


def register_route(app):
    # register_blueprint(app)
    app.add_url_rule('/user/<string:user>/', view_func=AUser.as_view('user'))
    app.add_url_rule('/room/<string:room>/', view_func=ARoom.as_view('room'))
    app.add_url_rule('/index/<string:index>/', view_func=AIndex.as_view('index'))
    app.add_url_rule('/trade/<string:trade>/', view_func=ATrade.as_view('trade'))
    app.add_url_rule('/mover/<string:server>/', view_func=AMover.as_view('mover'))  # 搬家


def create_app():
    app = Flask(__name__)
    app.config.from_object('Linjia.configs.appsettings')
    register_route(app)
    reigster_extensions(app)
    print(app.debug)
    error_handler(app)
    CORS(app, supports_credentials=True)
    request_first_handler(app)
    return app
