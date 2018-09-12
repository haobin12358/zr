# -*- coding: utf-8 -*-
import uuid

from flask import request, current_app
from raven.contrib import flask

from Linjia.commons.error_response import NOT_FOUND, TOKEN_ERROR
from Linjia.commons.params_validates import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_admin
from Linjia.configs.enums import FACE_CONFIG, RENT_TYPE
from Linjia.control.base_control import BaseRoomControl
from Linjia.service import SRoom, SUser, SCity, SIndex


class CRoom(BaseRoomControl):
    def __init__(self):
        self.sroom = SRoom()
        self.suser = SUser()
        self.scity = SCity()
        self.sindex = SIndex()

    def get_list(self):
        # todo 位置, 地铁, 附近
        args = request.args.to_dict()
        args_dict = {}
        if not args:
            args = {}
        args_dict['page'] = int(args.get('page', 1))  # 页码
        args_dict['count'] = int(args.get('count', 15))  # 取出条数
        # 租赁方式, 合租整租公寓民宿
        args_dict['type'] = args.get('type')
        # 装修风格 0 毛坯, 1简装, 2: 精装, 3: 豪华
        args_dict['style'] = args.get('style').split('|') if 'style' in args else None
        # 租金
        args_dict['lowprice'] = args.get('lowprice')
        args_dict['highprice'] = args.get('highprice')
        # 朝向 face=1|2|3 ==> [1, 2, 3]
        args_dict['face_args'] = args.get('face').split('|') if 'face' in args else None
        # 展现方式 image or video
        args_dict['show_type'] = args.get('show_type')
        # 房型 一室,二室,三室,五室以上
        args_dict['bed_count'] = args.get('bed_count').split('|') if 'bed_count' in args else None
        # 城市编号
        args_dict['city_id'] = args.get('city_id')
        # 区
        args_dict['area_id'] = args.get('area_id')
        print(args_dict)
        # 地址 区, 附近 todo
        args_dict = {
            k: v for k, v in args_dict.items() if v is not None
        }
        room_detail_list = self.sroom.get_room_list_filter(args_dict)
        map(self._fill_detail_for_list, room_detail_list)
        map(self._fill_house_info, room_detail_list)  # 楼层和规格
        map(lambda x: x.fill(self.sroom.get_tags_by_roid(x.ROid), 'tags', hide=('ROid', )), room_detail_list)  # 填充tag信息
        map(lambda x: x.fill(self.sindex.is_room_showinindex_by_roid(x.ROid), 'show_index'), room_detail_list)  # 是否显示在首页
        page_count = getattr(request, 'page_count')
        all_count = getattr(request, 'all_count')
        data = Success(u'获取房源列表成功', data=room_detail_list, page_count=page_count, all_count=all_count)
        return data

    def get_detail(self):
        """房源详细信息"""
        data = parameter_required(('roid', ))
        roid = data.get('roid')
        room = self.sroom.get_room_by_roid(roid)
        if not room:
            raise NOT_FOUND(u'房源不存在')
        self._fill_house_info(room)  # 楼层和规格
        self._fill_roomate_info(room)  # 室友信息
        room.fill(self.sroom.get_room_equirment_by_roid(room.ROid), 'equirment', hide=('IConid', 'REid', 'ROid'))
        room.fill(self.sroom.get_room_media_by_roid(room.ROid), 'media')
        room.fill(self.scity.get_city_by_city_id(room.ROcitynum), 'city')
        room.ROface = FACE_CONFIG.get(room.ROface, u'未知')
        room.ROrenttype = RENT_TYPE.get(room.ROrenttype, u'未知')
        room.add('ROisdelete', 'ROcreatetime', 'ROcitynum')
        return Success(u'获取房源信息成功', room)

    def get_oppener_city(self):
        """获取开放城市"""
        opnerlist = self.scity.get_roomoppencitylist()
        map(lambda x: x.fill(self.scity.get_city_by_city_id(x.city_id).name, 'name'), opnerlist)
        return Success(u'获取城市列表成功', {
            'citys': opnerlist
        })

    def get_area_by_citynum(self):
        args = parameter_required(('city_id', ))
        city_id = args.get('city_id')
        area_list = self.scity.get_area_list_by_cityid(city_id)
        map(lambda x: x.hide('_id'), area_list)
        return Success(u'获取城市成功', {
            'area_list': area_list
        })

    def get_subwayline_by_citynum(self):
        """获取城市内的地铁线路, 只获得线路, 暂不获得站点"""
        data = parameter_required(('city_id', ))
        city_id = data.get('city_id')
        subway_line = self.scity.get_subwayline_by_city_id(city_id)
        # map(lambda x: x.fill(
        #     self.scity.get_subwayposition_by_line_id(x.subwaylineid),
        #     'positions'
        # ), subway_line)
        return Success(u'获取地铁信息成功', subway_line)

    def get_subway_potion_by_lineid(self):
        """获取地铁线路的站点"""
        data = parameter_required(('line_id', ))
        line_id = data.get('line_id')
        line = self.scity.get_subwayline_by_lineid(line_id)
        if not line:
            raise NOT_FOUND(u'不存在的线路')
        positions = self.scity.get_subwayposition_by_line_id(line.subwaylineid)
        return Success(u'获取站点信息成功', positions)

    def add_joinroom_banner(self):
        """添加友家轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('jrbimage', 'jrbsort', ), others='ignore')
        data['jrbid'] = str(uuid.uuid4())
        model_bean = self.sroom.add_model('JoinRoomBanner', data, return_fields=('JRBid', 'JRBimage', 'JRBsort'))
        for k in model_bean.keys():
            if k[0].isupper():
                # 字段转小写
                model_bean[k.lower()] = model_bean[k]
                model_bean.pop(k)
        return Success(u'添加成功', model_bean)

    def get_joinroom_banner(self):
        """获取友家轮播图"""
        join_room_banner_list = self.sroom.get_joinroom_banner_list()
        return Success(u'获取轮播图成功', join_room_banner_list)

    def delete_joinroom_banner(self):
        """删除友家轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('jrbid', ))
        jrbid = data.get('jrbid')
        joinroom = self.sroom.delete_joinroom_banner(jrbid)
        msg = u'删除成功' if joinroom else u'要删除的对象不存在'
        return Success(msg, {
            'jrbid': jrbid
        })

    def get_homestay_banner(self):
        """获取民宿页的轮播图"""
        homestay_banner_list = self.sroom.get_homestay_banner_list()
        return Success(u'获取轮播图成功', homestay_banner_list)

    def add_homestay_banner(self):
        """添加民宿页的轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('hsbimage', 'hsbsort'), others='ignore')
        data['hsbid'] = str(uuid.uuid4())
        model_bean = self.sroom.add_model('HomeStayBanner', data)
        return Success(u'添加成功', {
            'hsbid': data['hsbid']
        })

    def delete_homestay_banner(self):
        """删除民宿页的轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('hsbid',))
        hsbid = data.get('hsbid')
        homestaybanner = self.sroom.delete_homestay_banner(hsbid)
        msg = u'删除成功' if homestaybanner else u'要删除的对象不存在'
        return Success(msg, {
            'hsbid': hsbid
        })

    def add_homestay_copywriting(self):
        """添加, 这个需要问前端, 怎么获取"""
        pass


