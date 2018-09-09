# -*- coding: utf-8 -*-
import re

from flask import request

from Linjia.commons.error_response import PARAMS_ERROR


def parameter_required(required, others='allow', filter_none=True):
    """验证请求中必需的参数
    others: 如果是allow, 则代表不会清除其他参数
    filter_none: True表示会过滤到空值(空列表, 空字符串, None)
    """
    data = request.json or request.args.to_dict() or {}
    if filter_none:
        data = filter(lambda x: x or x == 0, required)
    missed = filter(lambda x: x not in data, required)
    if missed:
        raise PARAMS_ERROR(u'必要参数缺失: ' + ', '.join(missed))
    if others != 'allow':
        data = {
            k: v for k, v in data.items() if k in required
        }
    return data


def validate_phone(arg):
    regex_phone = "^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$"
    return validate_arg(regex_phone, arg, str(arg) + u'不是手机号码')


def validate_arg(regex, arg, msg=None):
    res = re.match(regex, str(arg))
    if not res:
        raise PARAMS_ERROR(msg)
    return arg
