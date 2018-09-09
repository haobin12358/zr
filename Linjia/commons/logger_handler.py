# -*- coding: utf-8 -*-
import logging
import traceback

from flask import request, current_app
from werkzeug.exceptions import HTTPException

from Linjia.commons.error_response import SYSTEM_ERROR, APIS_WRONG
from Linjia.commons.success_response import Success


def error_handler(app):

    @app.errorhandler(404)
    def error404(e):
        return APIS_WRONG()

    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, Success):
            return e
        generic_log(e)
        if isinstance(e, HTTPException):
            return e
        else:
            if not app.debug:
                return SYSTEM_ERROR()
            raise Exception(traceback.format_exc().decode('unicode-escape'))

    def generic_log(e):
        handler = logging.FileHandler('app.log', encoding='UTF-8')
        data = traceback.format_exc()

        logging_format = logging.Formatter(
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
            "%(asctime)s] {%(pathname)s: \n"
            "%(lineno)d} %(levelname)s - %(message)s   \n path is: " + request.path + \
            '\n more info:' + data.decode('unicode-escape'))
        handler.setFormatter(logging_format)
        app.logger.addHandler(handler)
        app.logger.info(e)
