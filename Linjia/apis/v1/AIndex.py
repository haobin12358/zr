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
            'detail': self.cindex.get_index_room_list
        }
        res = apis[index]()
        return jsonify(res)
