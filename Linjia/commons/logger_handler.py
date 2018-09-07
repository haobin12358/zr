# -*- coding: utf-8 -*-
import logging
import traceback

from flask import request
from werkzeug.exceptions import HTTPException

from Linjia.commons.error_response import SYSTEM_ERROR
from Linjia.commons.success_response import Success


def error_handler(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, Success):
            return e
        ge_log(e)
        if isinstance(e, HTTPException):
            return e
        else:
            if not app.debug:
                return SYSTEM_ERROR()
            raise Exception(traceback.format_exc().decode('unicode-escape'))

    def ge_log(e):
        handler = logging.FileHandler('app.log', encoding='UTF-8')
        data = traceback.format_exc()

        logging_format = logging.Formatter(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
            "%(asctime)s] {%(pathname)s: \n"
            "%(lineno)d} %(levelname)s - %(message)s   \n path is: " + request.path + \
            '\n more info:' + data.decode('unicode-escape'))
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)
        app.logger.error(e)
