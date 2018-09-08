# -*- coding: utf-8 -*-
from collections import namedtuple

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request
User = namedtuple('User', ('id', 'model', 'level'))


def request_first_handler(app):
    @app.before_request
    def get_main_url():
        args = request.args.to_dict()
        if args and 'token' in args:
            token = args.get('token')
            s = Serializer(current_app.config['SECRET_KEY'])
            try:
                data = s.loads(token)
                id = data['id']
                model = data['model']
                level = data['level']
                user = User(id, model, level)
                request.user = user
            except BadSignature as e:
                # 签名出错的token
                pass
            except SignatureExpired as e:
                # 过期的token
                pass
            except Exception as e:
                # 无法解析的token
                pass
