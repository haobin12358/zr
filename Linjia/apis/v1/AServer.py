# -*- coding: utf-8 -*-
from flask import jsonify

from Linjia.commons.base_resource import Resource
from Linjia.control import CServer


class AMover(Resource):
    """搬家相关"""
    def __init__(self):
        self.cserver = CServer()

    def get(self, server):
        apis = {
            'city_list': self.cserver.get_moveercity_list,
            'move_list': self.cserver.get_mover_list_by_city,
        }
        res = apis[server]()
        return jsonify(res)
