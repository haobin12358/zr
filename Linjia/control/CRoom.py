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
        # 类型  如: type=0-0|1-0|2-1  => [[0, 0], [1, 0], ...]
        args_dict['filter_type_list'] = map(lambda x: x.split('-'),
                                            args.get('type').split('|')) if 'type' in args else None
        # 租金
        args_dict['lowprice'] = args.get('lowprice')
        args_dict['highprice'] = args.get('highprice')
        # 朝向 face=1|2|3 ==> [1, 2, 3]
        args_dict['face_args'] = args.get('face').split('|') if 'face' in args else None
        # 签约时长 sign=1
        sign_args = args.get('sign')
        args_dict['sign_args'] = sign_args
        # 绿化率高 green_rate = 1
        args_dict['green_rate'] = args.get('green_rate')
        # 面积 area=40,80
        args_dict['lowarea'] = args.get('lowarea')
        args_dict['hignarea'] = args.get('hignarea')
        # 房源状态:
        args_dict['status'] = args.get('status')
        # 特色 feature = '1|3|5'  ==>  [1, 3, 5]
        args_dict['feature'] = args.get('feature').split('|') if 'feature' in args else None
        # 搜索词 多个关键词使用空格隔开
        args_dict['kw'] = args.get('kw').split() if 'kw' in args else None
        # 过滤None
        args_dict = {
            k: v for k, v in args_dict.items() if v is not None
        }
        room_detail_list = self.sroom.get_room_list_filter(args_dict)
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



