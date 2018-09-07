# -*- coding: utf-8 -*-
from flask import request

from Linjia.commons.error_response import NOT_FOUND
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.configs.enums import FACE_CONFIG, RENT_TYPE
from Linjia.configs.messages import get_room_list_success
from Linjia.control.base_control import BaseRoomControl
from Linjia.service import SRoom, SUser


class CRoom(BaseRoomControl):
    def __init__(self):
        self.sroom = SRoom()
        self.suser = SUser()

    def get_list(self):
        args = request.args.to_dict()
        args_dict = {}
        if not args:
            args = {}
        args_dict['page'] = int(args.get('page', 1))  # 页码
        args_dict['count'] = int(args.get('count', 15))  # 取出条数
        # 租赁方式, 合租整租
        args_dict['type'] = args.get('type')
        # 装修风格 0 毛坯, 1简装, 2: 精装, 3: 豪华
        args_dict['style'] = args.get('style').split('|') if 'style' in args else None
        # 租金
        args_dict['lowprice'] = args.get('lowprice')
        args_dict['highprice'] = args.get('highprice')
        # 朝向 face=1|2|3 ==> [1, 2, 3]
        args_dict['face_args'] = args.get('face').split('|') if 'face' in args else None
        # 展现方式
        args_dict['show_type'] = args.get('show_type')
        # 房型 一室,二室,三室,五室以上
        args_dict['bed_count'] = args.get('bed_count').aplit('|') if 'bed_count' in args else None
        # 地址 区, 附近 todo
        args_dict = {
            k: v for k, v in args_dict.items() if v is not None
        }
        room_detail_list = self.sroom.get_room_list_filter(args_dict)
        import ipdb
        ipdb.set_trace()
        map(self._fill_detail_for_list, room_detail_list)
        map(self._fill_features, room_detail_list)
        map(self._fill_house_info, room_detail_list)
        data = Success(get_room_list_success, data=room_detail_list)
        return data

    def get_detail(self):
        data = parameter_required('roid')
        roid = data.get('roid')
        room = self.sroom.get_room_by_roid(roid)
        if not room:
            raise NOT_FOUND()
        room.ROface = FACE_CONFIG[int(room.ROface)]
        room.ROrenttype = RENT_TYPE.get(int(room.ROrenttype), u'未知')
        self._fill_price_detail(room)
        self._fill_features(room)
        self._fill_subdiary_info(room)
        self._fill_house_info(room)
        self._fill_roomate_info(room)
        return Success('获取房源信息成功', room)



