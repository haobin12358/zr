# -*- coding: utf-8 -*-
from Linjia.commons.base_resource import Resource
from Linjia.control import CRoom


class ARoom(Resource):
    def __init__(self):
        self.croom = CRoom()

    def get(self, room):
        apis = {
            'get_list': self.croom.get_list,
            'get_detail': self.croom.get_detail,
            'get_city': self.croom.get_oppener_city,
            'get_area_by_cityid': self.croom.get_area_by_citynum,
            'get_subway': self.croom.get_subwayline_by_citynum,
            'get_position': self.croom.get_subway_potion_by_lineid,
            'get_joinroom_banner': self.croom.get_joinroom_banner,
            'get_homestay_banner': self.croom.get_homestay_banner,
            'get_villege_info': self.croom.get_villegeinfo_by_namekeyword,
        }
        return apis

    def post(self, room):
        apis = {
            'add_joinroom_banner': self.croom.add_joinroom_banner,
            'add_homestay_banner': self.croom.add_homestay_banner,
            'delete_join_room_banner': self.croom.delete_joinroom_banner,
            'delete_homestay_banner': self.croom.delete_homestay_banner,
            'add_room': self.croom.add_room,
            'add_villegetinfo': self.croom.add_villegetinfo,
            'update_villeginfo': self.croom.update_villeginfo,
            'add_bedroom': self.croom.add_bedroom,
            'update_bedroom': self.croom.update_bedroom,
            'delete_bedroom': self.croom.delete_bedroom,
        }
        return apis
