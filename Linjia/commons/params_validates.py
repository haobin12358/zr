# -*- coding: utf-8 -*-
from flask import request

from Linjia.commons.error_response import PARAMS_MISS


def parameter_required(required, others='allow'):
    """验证请求中必需的参数
    others: 如果是allow, 则代表不会清除其他参数
    """
    data = request.json or request.args.to_dict() or {}
    if required:
        missed = filter(lambda x: x not in data, required)
        if missed:
            raise PARAMS_MISS('必要参数缺失: ' + ', '.join(missed))
    if others != 'allow':
        data = {
            k: v for k, v in data.items() if k in required
        }
    return data
