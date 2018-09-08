# -*- coding: utf-8 -*-
from flask import request, current_app
from raven.contrib import flask

from Linjia.commons.error_response import NOT_FOUND
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.configs.enums import FACE_CONFIG, RENT_TYPE
from Linjia.control.base_control import BaseRoomControl
from Linjia.service import SRoom, SUser, SCity


class CRoom(BaseRoomControl):
    def __init__(self):
        self.sroom = SRoom()
        self.suser = SUser()
        self.scity = SCity()

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
        print(args_dict)
        # 地址 区, 附近 todo
        args_dict = {
            k: v for k, v in args_dict.items() if v is not None
        }
        room_detail_list = self.sroom.get_room_list_filter(args_dict)
        map(self._fill_detail_for_list, room_detail_list)
        map(self._fill_house_info, room_detail_list)  # 楼层和规格
        map(lambda x: x.fill(self.sroom.get_tags_by_roid(x.ROid), 'tags', hide=('ROid', )), room_detail_list)  # 填充tag信息
        page_count = getattr(request, 'page_count')
        all_count = getattr(request, 'all_count')
        data = Success(u'获取房源列表成功', data=room_detail_list, page_count=page_count, all_count=all_count)
        return data

    def get_detail(self):
        data = parameter_required('roid')
        roid = data.get('roid')
        room = self.sroom.get_room_by_roid(roid)
        if not room:
            raise NOT_FOUND(u'房源不存在')
        self._fill_house_info(room)  # 楼层和规格
        self._fill_roomate_info(room)  # 室友信息
        room.fill(self.sroom.get_room_equirment_by_roid(room.ROid), 'equirment', hide=('IConid', ))
        room.fill(self.sroom.get_room_media_by_roid(room.ROid), 'media')
        room.fill(self.scity.get_city_by_cityid(room.ROcitynum), 'city')
        room.ROface = FACE_CONFIG.get(room.ROface, u'未知')
        room.ROrenttype = RENT_TYPE.get(room.ROrenttype, u'未知')
        room.add('ROisdelete', 'ROcreatetime', 'ROcitynum')
        flask.current_app.logger.error('ttest信息')
        return Success('获取房源信息成功', room)

