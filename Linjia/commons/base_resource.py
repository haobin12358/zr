# -*- coding: utf-8 -*-
from flask.views import MethodView

from Linjia.commons.error_response import APIS_WRONG


class Resource(MethodView):
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
