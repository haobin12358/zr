# -*- coding: utf-8 -*-
from Linjia.commons.base_resource import Resource
from Linjia.control import CIndex


class AIndex(Resource):
    def __init__(self):
        self.cindex = CIndex()

    def get(self, index):
        apis = {
            'banner': self.cindex.get_banner,
            'detail': self.cindex.get_index_room_list,
            'index_server_show': self.cindex.get_index_server,
        }
        return apis

    def post(self, index):
        apis = {
            'add_banner': self.cindex.add_banner,
            'add_room_show': self.cindex.add_room_show,
            'add_server_show': self.cindex.add_server_index,
            'delete_banner_show': self.cindex.delete_banner_show,
            'delete_room_show': self.cindex.delete_room_show,
            'delete_room_show_byroid': self.cindex.delete_room_show_by_roid,
            'delete_server_show': self.cindex.delete_server_index_show,
            'upload_img': self.cindex.upload_img
        }
        return apis

