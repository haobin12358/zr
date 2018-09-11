# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask.views import MethodView

from Linjia.commons.error_response import APIS_WRONG


class Resource(MethodView):

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method
        apis = meth(*args, **kwargs)  # 字典
        for kwarg in kwargs.values():
            if kwarg not in apis:
                raise APIS_WRONG()
            return jsonify(apis[kwarg]())
        return meth(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise APIS_WRONG()

    def post(self, *args, **kwargs):
        raise APIS_WRONG()

    def option(self, *args, **kwargs):
        raise APIS_WRONG()

    def put(self, *args, **kwargs):
        raise APIS_WRONG()

    def delete(self, *args, **kwargs):
        raise APIS_WRONG()


