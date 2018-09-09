# -*- coding: utf-8 -*-
from flask import jsonify

from Linjia.commons.base_resource import Resource
from Linjia.control import CRoom


class ARoom(Resource):
    def __init__(self):
        self.croom = CRoom()

    def get(self, room):
        print(room)
        apis = {
            'get_list': self.croom.get_list,
            'get_detail': self.croom.get_detail,
            'get_city': self.croom.get_oppener_city,
        }
        return jsonify(apis[room]())
