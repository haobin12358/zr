# -*- coding: utf-8 -*-
import uuid

from Linjia.commons.error_response import AUTHORITY_ERROR
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_required import is_admin
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
        """新建轮播图, 必要的参数: 图片地址, 顺序标志, 链接"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('ibimage', 'iblink', 'ibsort')
        data['IBid'] = str(uuid.uuid4())
        self.sindex.add_model('IndexBanner', **data)
        return Success(u'添加成功', {
            'ibid': data['IBid']
        })

    def add_room_show(self):
        """新建首页显示的合租整租, 必要的参数 房源id, type, 和顺序: """
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('roid', 'rotype', 'rosort')
        data['RISid'] = str(uuid.uuid4())
        self.sindex.add_model('RoomIndexShow', **data)
        return Success(u'添加成功', {
            'risid': data['RISid']
        })

    def add_apartment_show(self):
        """新建首页显示的公寓, 必要的参数有:公寓id, 顺序标志, 非必需参数有: 描述 """
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('apid', 'aisort')
        data['AISid'] = str(uuid.uuid4())
        self.sindex.add_model('APartmentIndexShow', **data)
        return Success(u'添加成功', {
            'aisid': data['AISid']
        })

    def add_homestay_show(self):
        """新建首页显示民宿, 必要的参数有民宿id和顺序标志"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('hsid', 'hsisort')
        data['HSIid'] = str(uuid.uuid4())
        self.sindex.add_model('HomeStayIndexShow', **data)
        return Success(u'添加成功', {
            'hsiid': data['HSIid']
        })







