# -*- coding: utf-8 -*-
from flask import json
from werkzeug.exceptions import HTTPException


class BaseError(HTTPException):
    message = '系统错误'
    status = 404
    status_code = 405001

    def __init__(self, message=None, status=None, status_code=None, header=None):
        self.code = 200
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        if status:
            self.status = status
        super(BaseError, self).__init__(message, None)

    def get_body(self, environ=None):
        body = dict(
            status=self.status,
            message=self.message,
            status_code=self.status_code
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]
