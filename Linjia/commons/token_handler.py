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

def is_admin():
    """是否是管理员"""
    return hasattr(request, 'user') and request.user.model == u'Admin'


def is_tourist():
    """是否是游客"""
    return not hasattr(request, 'user')


def common_user():
    """是否是普通用户, 不包括管理员"""
    return hasattr(request, 'user') and request.user.model == u'user'


def is_hign_level_admin():
    """高级管理员, 包括高级和超级"""
    return is_admin() and request.user.level > 0



