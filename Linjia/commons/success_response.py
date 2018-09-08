# -*- coding: utf-8 -*-
from flask import json

from Linjia.commons.base_error import BaseError


class Success(BaseError):
    """
    成功信息, 不要被基类迷惑
    """
    status = 200
    message = '获取成功'
    data = '获取成功'

    def __init__(self, message=None, data=None, page_count=None, all_count=None, *args, **kwargs):
        self.status_code = None
        if message is not None:
            self.message = message
        if data is not None:
            self.data = data
        if page_count is not None:
            self.page_count = page_count
        if all_count is not None:
            self.all_count = all_count
        super(Success, self).__init__(*args, **kwargs)

    def get_body(self, environ=None):
        body = dict(
            status=self.status,
            message=self.message,
            data=self.data
        )
        if hasattr(self, 'page_count'):
            body['page_count'] = self.page_count
        if hasattr(self, 'all_count'):
            body['all_count'] = self.all_count
        text = json.dumps(body)
        return text


