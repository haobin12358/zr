# -*- coding: utf-8 -*-
# *- coding:utf8 *-
from flask import jsonify

from Linjia.commons.base_resource import Resource
from Linjia.control import CTrade


class ATrade(Resource):
    def __init__(self):
        self.ctrade = CTrade()

    def post(self, trade):
        apis = {
            'add_providehouse_apply': self.ctrade.add_providehouse_apply,
        }
        res = apis[trade]()
        return jsonify(res)
