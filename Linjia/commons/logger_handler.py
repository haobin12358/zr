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
        if isinstance(e, HTTPException):
            raise e
        else:
            ge_log(e)
            if not app.debug:
                return SYSTEM_ERROR('k')
            raise e

    def ge_log(e):
        handler = logging.FileHandler('app.log', encoding='UTF-8')

        logging_format = logging.Formatter(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
            "%(asctime)s] {%(pathname)s: \n"
            "%(lineno)d} %(levelname)s - %(message)s   \n path is: " + request.path + \
            '\n more info:' + repr(traceback.format_exc()))
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)
        app.logger.error(e)
