# -*- coding: utf-8 -*-
import uuid

from Linjia.commons.error_response import NOT_FOUND
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.control.base_control import BaseRoomControl, BaseIndexControl
from Linjia.service import SIndex, SRoom, SApartment, SHomeStay, SCity


class CIndex(BaseRoomControl, BaseIndexControl):
    def __init__(self):
        self.sindex = SIndex()
        self.sroom = SRoom()
        self.sapartment = SApartment()
        self.shomestay = SHomeStay()
        self.scity = SCity()

    def get_banner(self):
        banner_list = self.sindex.get_banner_list()
        return Success('获取成功', banner_list)

    def get_index_room_list(self):
        join_rent_show_list = self.sindex.get_index_room()
        whole_rent_show_list = self.sindex.get_index_room(1)
        apartment_show_list = self.sindex.get_index_apartment()
        homestay_show_list = self.sindex.get_index_homestay()
        server_show_list = self.sindex.get_index_server()
        map(self._fill_room_simple, join_rent_show_list)
        map(self._fill_room_simple, whole_rent_show_list)
        map(self._fill_apartment_simple, apartment_show_list)
        map(self._fill_homestay_simple, homestay_show_list)
        map(lambda x: x.hide('SISid'), server_show_list)  # 隐藏无用id
        data = dict(
            join_rent=join_rent_show_list,  # 合租
            whole_rent=whole_rent_show_list,  # 整租
            apartment=apartment_show_list,  # 公寓
            homestay=homestay_show_list,  # 民宿
            server=server_show_list # 服务
        )
        return Success('获取成功', data)

    def add_banner(self):
        """新建轮播图, 需要图片地址, 顺序标志, 链接"""
        data = parameter_required('ibimage', 'iblink', 'ibsort')
        data['IBid'] = str(uuid.uuid4())
        self.sindex.add_model('IndexBanner', **data)
        return Success(u'添加成功', {
            'ibid': data['IBid']
        })






