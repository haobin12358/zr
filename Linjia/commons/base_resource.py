# -*- coding: utf-8 -*-
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.wrappers import Response

from Linjia.commons.error_response import APIS_WRONG, MethodNotAllowed


class Resource(MethodView):

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method
        apis = meth(*args, **kwargs)
        if not isinstance(apis, dict):
            super(Resource, self).dispatch_request(*args, **kwargs)
        for kwarg in kwargs.values():
            if kwarg not in apis:
                raise APIS_WRONG()
            res = jsonify(apis[kwarg]())
            if isinstance(res, str) or isinstance(res, Response):
                return res
        return meth(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed()

    def post(self, *args, **kwargs):
        raise MethodNotAllowed()

    def option(self, *args, **kwargs):
        raise MethodNotAllowed()

    def put(self, *args, **kwargs):
        raise MethodNotAllowed()

    def delete(self, *args, **kwargs):
        raise APIS_WRONG(u'请求方法不支持')


