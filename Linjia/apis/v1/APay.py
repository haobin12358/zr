# -*- coding: utf-8 -*-
from Linjia.commons.base_resource import Resource
from Linjia.control.Cpay import CPay


class APay(Resource):
    def __init__(self):
        self.cpay = CPay()

    def post(self, pay):
        apis = {
            'pay_for_service': self.cpay.pay_for_service,
            'pay_notify': self.cpay.pay_notify
        }
        return apis

    def get(self, pay):
        apis = {
            'check_refund': self.cpay.check_refund,
        }
        return apis