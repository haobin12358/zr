# -*- coding: utf-8 -*-
from flask import jsonify

from Linjia.commons.base_resource import Resource
from Linjia.control import CIndex


class AIndex(Resource):
    def __init__(self):
        self.cindex = CIndex()

    def get(self, index):
        apis = {
            'banner': self.cindex.get_banner,
            'detail': self.cindex.get_index_room_list,
        }
        res = apis[index]()
        return jsonify(res)

    def post(self, index):
        apis = {
            'add_banner': self.cindex.add_banner,
            'add_room_show': self.cindex.add_room_show,
            'add_apartment_show': self.cindex.add_apartment_show,
            'add_homestay_show': self.cindex.add_homestay_show,
        }
        res = apis[index]()
        return jsonify(res)
