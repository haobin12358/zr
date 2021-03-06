# -*- coding: utf-8 -*-
import logging
import os
import traceback
from datetime import datetime

from flask import request, current_app

from Linjia.commons.base_error import BaseError
from Linjia.commons.error_response import SYSTEM_ERROR, APIS_WRONG
from Linjia.commons.success_response import Success
from Linjia.configs.appsettings import BASEDIR


def error_handler(app):

    @app.errorhandler(404)
    def error404(e):
        generic_log(e)
        return APIS_WRONG(u'接口未注册' + request.path)

    # @app.errorhandler(ValueError)
    # def error_value_error(e):
    #     generic_log(e)
    #     return APIS_WRONG(u'类型错误' + str(request.args.to_dict()))

    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, Success):
            return e
        generic_log(e)
        print('dddddddddd')
        if isinstance(e, BaseError):
            return e
        else:
            # if not app.debug:
            return SYSTEM_ERROR()
            # raise Exception(traceback.format_exc())


def generic_log(data):
    logger_file_name = datetime.now().strftime("%Y-%m-%d") + u'.log'
    logger_dir = os.path.join(BASEDIR, 'logs')
    if not os.path.isdir(logger_dir):
        os.makedirs(logger_dir)
    logger_dir = os.path.join(logger_dir, logger_file_name)
    handler = logging.FileHandler(logger_dir)
    if isinstance(data, Exception):
        data = traceback.format_exc()
    logging_format = logging.Formatter(
        # "%(asctime)s - %(levelname)s - %(filename)s \n- %(funcName)s - %(lineno)s - %(message)s"
        "%(asctime)s - %(levelname)s - %(filename)s \n %(message)s"
        )
    handler.setFormatter(logging_format)
    current_app.logger.addHandler(handler)
    current_app.logger.error(u'>>>>>>>>>>>>>>>>>>bug<<<<<<<<<<<<<<<<<<<')
    current_app.logger.error(data)
    current_app.logger.error(request.detail)
    # current_app.logger.error(request.data)
    # current_app.logger.error(request.args)
    # current_app.logger.error(request.method)
    current_app.logger.removeHandler(handler)

