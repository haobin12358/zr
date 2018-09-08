# -*- coding: utf-8 -*-
import uuid

from Linjia.commons.error_response import AUTHORITY_ERROR, NOT_FOUND
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_admin
from Linjia.configs.enums import RENT_TYPE
from Linjia.control.base_control import BaseRoomControl, BaseIndexControl
from Linjia.service import SIndex, SRoom, SCity


class CIndex(BaseRoomControl, BaseIndexControl):
    def __init__(self):
        self.sindex = SIndex()
        self.sroom = SRoom()
        self.scity = SCity()

    def get_banner(self):
        banner_list = self.sindex.get_banner_list()
        return Success('获取成功', banner_list)

    def get_index_room_list(self):
        index_shows = self.sindex.get_rooms_index_show()
        map(self._fill_index_room_detail, index_shows)
        # 分类
        data = dict(
            join_rent=filter(lambda x: x.ROrenttype == RENT_TYPE[0], index_shows),
            whole_rent=filter(lambda x: x.ROrenttype == RENT_TYPE[1], index_shows),
            apartment=filter(lambda x: x.ROrenttype == RENT_TYPE[2], index_shows),
            homestay=filter(lambda x: x.ROrenttype == RENT_TYPE[3], index_shows),
        )
        return Success(u'获取首页信息成功', data)


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

    def delete_banner_show(self):
        """删除轮播"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('ibid')
        banner = self.sindex.delete_banner_show_by_ibid(data.get('ibid'))
        message = u'删除成功' if banner else u'要删除的元素不存在'
        return Success(message, {
            'ibid': data.get('ibid')     
        })

    def delete_room_show(self):
        """删除首页显示的整租或合租房源"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('risid')
        room_index_show = self.sindex.delete_room_show_by_risid(data.get('risid'))
        message = u'删除成功' if room_index_show else u'要删除的对象不存在'
        return Success(message, {
            'risid': data.get('risid')
        })

    def delete_apartment_show(self):
        """删除首页显示的公寓"""
        if not is_admin():
            raise AUTHORITY_ERROR("请使用管理员登录")
        data = parameter_required('aisid')
        apartment_index_show = self.sindex.delete_apartment_show_by_aisid(data.get('aisid'))
        message = u'删除成功' if apartment_index_show else u'要删除的对象不存在'
        return Success(message, {
            'aisid': data.get('aisid')     
        })

    def delete_homestay_show(self):
        """删除首页显示的民宿"""
        if not is_admin():
            raise AUTHORITY_ERROR("请使用管理员登录")
        data = parameter_required('hsiid')
        homestay_index_show = self.sindex.delete_homestay_show_by_hsiid(data.get('hsiid'))
        message = u'删除成功' if homestay_index_show else u'要删除的对象不存在'
        return Success(message, {
            'hsiid': data.get('hsiid')
        })

    def delete_server_index_show(self):
        """删除首页显示的服务"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('sisid')
        server_index_show = self.sindex.delete_server_index_show(data.get('sisid'))
        message = u'删除成功' if server_index_show else u'要删除的对象不存在'
        return Success(message, {
            'sisid': data.get('sisid')
        })
