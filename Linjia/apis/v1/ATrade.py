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
            'mover_appointment': self.ctrade.mover_appointment,
            'cleaner_apponintment': self.ctrade.cleaner_appiontment,
            'fixer_appointment': self.ctrade.fixer_appiontment,
            'add_complaint': self.ctrade.add_complaint
        }
        res = apis[trade]()
        return jsonify(res)

    def get(self, trade):
        apis = {
            'get_my_appiontlist': self.ctrade.get_my_oppintment,
        }
        res = apis[trade]()
        return jsonify(res)
