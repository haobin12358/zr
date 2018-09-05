# -*- coding: utf-8 -*-
from flask import request

from Linjia.commons.success_response import Success
from Linjia.control.base_control import BaseRoomControl
from Linjia.service import SIndex, SRoom


class CIndex(BaseRoomControl):
    def __init__(self):
        self.sindex = SIndex()
        self.sroom = SRoom()

    def get_banner(self):
        banner_list = self.sindex.get_banner_list()
        return Success('获取成功', banner_list)

    def get_index_room_list(self):

        join_rent_show_list = self.sindex.get_index_room()
        whole_rent_show_list = self.sindex.get_index_room(1)
        map(self._fill_room_simple, join_rent_show_list)
        map(self._fill_room_simple, whole_rent_show_list)
        data = dict(
            join_rent=join_rent_show_list,  # 合租
            whole_rent=whole_rent_show_list,  # 整租
            apartment=self.sindex.get_index_apartment(),  # 公寓
            homestay=self.sindex.get_index_homestay(),  # 民宿
            server=self.sindex.get_index_server()
        )
        return Success('获取成功', data)

    def _fill_room_simple(self, rent_show):
        """需要房源的id, 名字, 图片, 价格, 地址"""
        roid = rent_show.ROid
        room = self.sroom.get_room_by_roid(roid)
        self._fill_show_price(room)
        show_fields = ['ROid', 'ROname', 'ROimage', 'ROdistance', 'ROprice']
        # 下一句等同于: rent_show.ROid = room.ROid; rent_show.ROname = room.ROname....
        map(lambda x: setattr(rent_show, x, getattr(room, x)), show_fields)
        rent_show.fields = show_fields
        return room

    def _fill_apartment_simple(self, apartment_show):
        """需要公寓的id, 名字, 图片"""


