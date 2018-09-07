# -*-LJ_DB_PWi coding: utf-8 -*-
import datetime
from collections import namedtuple

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request

from Linjia.commons.error_response import AUTHORITY_ERROR

User = namedtuple('User', ('id', 'model', 'level'))


def usid_to_token(id, model='User', level=0, expiration=''):
    """生成令牌
    id: 用户id
    model: 用户类型(User 或者 SuperUser)
    expiration: 过期时间, 在appcommon/setting中修改
    """
    if not expiration:
        expiration = current_app.config['TOKEN_EXPIRATION']
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'id': id,
        'model': model,
        'level': level
    })


def token_to_usid(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature as e:
        print('不合法的token')
        return
    except SignatureExpired as e:
        print('token is expired')
        return
    except Exception as e:
        raise e
    id = data['id']
    return id


def token_decorator(func):
    """
    验证token装饰器, 并将用户对象放入request.user中
    """
    def inner(self, *args, **kwargs):
        parameter = request.args.to_dict()
        token = parameter.get('token')
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature as e:
            # 签名出错的token
            return func(self, *args, **kwargs)
        except SignatureExpired as e:
            # 过期的token
            return func(self, *args, **kwargs)
        except Exception as e:
            # 无法解析的token
            return func(self, *args, **kwargs)
        id = data['id']
        model = data['model']
        level = data['level']
        user = User(id, model, level)
        request.user = user
        return func(self, *args, **kwargs)
    return inner


def is_admin():
    """是否是管理员"""
    return hasattr(request, 'user') and request.user.model == u'Admin'


def is_tourist():
    """是否是游客"""
    return not hasattr(request, 'user')