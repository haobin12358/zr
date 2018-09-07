# -*- coding: utf-8 -*-
import logging

from flask import request

from Linjia.commons.base_error import BaseError
from Linjia.commons.success_response import Success


class DB_ERROR(BaseError):
    message = '系统错误'
    status = 404

class PARAMS_MISS(BaseError):
    status = 405
    status_code = 405001
    message = '参数缺失'


class TOKEN_ERROR(BaseError):
    status = 405
    status_code = 405001
    message = "未登录"


class MethodNotAllowed(BaseError):
    status = 405
    status_code = 405002
    message = "方法不支持"


class AUTHORITY_ERROR(BaseError):
    status = 405
    status_code = 405001
    message = "无权限"


class NOT_FOUND(BaseError):
    status = 404
    status_code = 405001
    message = '无此项目'

class SYSTEM_ERROR(BaseError):
    status_code = 200
    message = '系统错误'
    status = 404


class APIS_WRONG(BaseError):
    status = 405
    status_code = 405002
    message = "接口未注册"

class TIME_ERROR(BaseError):
    status = 405
    status_code = 405003
    message = "敬请期待"


def error_handler(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, Success):
            return e
        ge_log(e)
        if isinstance(e, BaseError):
            return e
        if not app.debug:
            raise BaseError(e.msg)
        raise e

    def ge_log(e):
        handler = logging.FileHandler('app.log', encoding='UTF-8')
        if hasattr(e , 'get_body'):
            logging_format = logging.Formatter(
                "[%(asctime)s] {%(pathname)s: \n"
                "%(lineno)d} %(levelname)s - %(message)s " + request.path + e.get_body())
        else:
            logging_format = logging.Formatter(
                "[%(asctime)s] {%(pathname)s: \n"
                "%(lineno)d} %(levelname)s - %(message)s " + request.path)
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)
        app.logger.error(e)
