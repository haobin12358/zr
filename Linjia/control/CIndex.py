# -*- coding: utf-8 -*-
from flask import request

from Linjia.commons.success_response import Success
from Linjia.service import SIndex, SRoom


class CIndex(object):
    def __init__(self):
        self.sindex = SIndex()
        self.sroom = SRoom()

    def get_banner(self):
        banner_list = self.sindex.get_banner_list()
        return Success('获取成功', banner_list)

    def get_index_room_list(self):
        join_rent = self.sindex.get_index_room()
        whole_rent = self.sindex.get_index_room(1)

        data = dict(
            join_rent=self.sindex.get_index_room(),  # 合租
            whole_rent=self.sindex.get_index_room(1),  # 整租
            apartment=self.sindex.get_index_apartment(),  # 公寓
            homestay=self.sindex.get_index_homestay(),  # 民宿
            server=self.sindex.get_index_server()
        )
        return Success('获取成功', data)

    def _fill_room_info(self, index_show):
        roid = index_show.ROid
        room = self.sroom.get_room_by_roid(roid)
        room.fields = ['HSid', 'HSname', '']
