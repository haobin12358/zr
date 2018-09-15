# -*- coding: utf-8 -*-
import logging
import os
import traceback
from datetime import datetime

from flask import request
from werkzeug.exceptions import HTTPException

from Linjia.commons.base_error import BaseError
from Linjia.commons.error_response import SYSTEM_ERROR, APIS_WRONG
from Linjia.commons.success_response import Success
from Linjia.configs.appsettings import BASEDIR


def error_handler(app):

    @app.errorhandler(404)
    def error404(e):
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
        if isinstance(e, BaseError):
            return e
        else:
            if not app.debug:
                return SYSTEM_ERROR()
            raise Exception(traceback.format_exc().decode('unicode-escape'))

    def generic_log(e):
        logger_file_name = datetime.now().strftime("%Y-%m-%d") + u'.log'
        logger_dir = os.path.join(BASEDIR, 'logs', logger_file_name)
        handler = logging.FileHandler(logger_dir, encoding='UTF-8')
        data = traceback.format_exc()
        logging_format = logging.Formatter(
            # "%(asctime)s - %(levelname)s - %(filename)s \n- %(funcName)s - %(lineno)s - %(message)s"
            "%(asctime)s - %(levelname)s - %(filename)s \n %(message)s"
            )
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)
        app.logger.info('>>>>>>>>>>>>>>>>>>bug<<<<<<<<<<<<<<<<<<<')
        app.logger.error(data.decode('unicode-escape'))
        app.logger.info('request.url is {}'.format(request.url))
        app.logger.info('request.data is {} '.format(request.data))
        app.logger.info('request.args is {} '.format(request.args))
        app.logger.info('method : {} '.format(request.method))

