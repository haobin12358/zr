# -*- coding: utf-8 -*-
from flask import request

from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.configs.enums import FACE_CONFIG, PAY_PERIOD, HYTING_TYPE, GENDER_CONFIG, RENT_TYPE
from Linjia.configs.messages import get_room_list_success
from Linjia.service import SRoom, SUser


class CRoom(object):
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
        room.ROface = FACE_CONFIG[int(room.ROface)]
        room.ROrenttype = RENT_TYPE.get(int(room.ROrenttype), u'未知')
        self._fill_price_detail(room)
        self._fill_features(room)
        self._fill_subdiary_info(room)
        self._fill_house_info(room)
        self._fill_roomate_info(room)
        return Success('获取房源信息成功', room)

    def _fill_detail_for_list(self, room):
        """调整返回列表的格式"""
        room_respose_fields = ['ROid', 'ROname', 'ROarea', 'face',
                               'ROdistance', 'ROshowpriceunit',
                               'ROprice', 'ROimage', 'ROrenttype', 'ROpersoncount']
        room.fields = room_respose_fields
        room.face = FACE_CONFIG.get(int(room.ROface), u'未知')
        room.ROrenttype = RENT_TYPE.get(int(room.ROrenttype), u'未知')
        if room.ROstatus == 3:
            room.ROname = u'转' + room.ROname
        # 价格
        self._fill_show_price(room)
        return room

    def _fill_features(self, room):
        roid = room.ROid
        features = self.sroom.get_features_by_roid(roid)
        features.hide('ROid', 'RFid')
        features.RFhytingtype = HYTING_TYPE[int(features.RFhytingtype)]
        room.ROfeatures = features
        room.add('ROfeatures')
        return room

    def _fill_show_price(self, room):
        roompayprice = self.sroom.get_price_by_roidandperid(room.ROid, room.ROshowpricetype)
        room.ROprice = str(room.ROshowprice) + u'元' + room.ROshowpriceunit \
            if room.ROshowprice else str(roompayprice.RPPprice) + \
                                     roompayprice.RPPpriceUnit
        room.add('ROprice')
        return room

    def _fill_price_detail(self, room):
        roid = room.ROid
        price_list = self.sroom.get_price_by_roid(roid)
        map(lambda x: x.hide('ROid', 'RPPid'), price_list)
        map(lambda x: setattr(x, 'RPPperiod', PAY_PERIOD[int(x.RPPperiod)]), price_list)
        room.price_list = price_list
        room.add('price_list')
        return room

    def _fill_house_info(self, room):
        hoid = room.HOid
        house = self.sroom.get_house_by_hoid(hoid)
        house.size = str(house.HObedroomcount) + u'室' + str(house.HOparlorcount) + u'厅'
        house.floor = str(house.HOfloor) + '/' + str(house.HOtotalfloor) + u'层'
        house.fields = ['size', 'floor']
        room.fill(house, 'house')  # room.house = house
        return room

    def _fill_subdiary_info(self, room):
        """填充配套信息(包括图片获取)"""
        hoid = room.HOid
        roid = room.ROid
        subdiary_list = self.sroom.get_subdiaryinfo_by_hoid(hoid)
        map(lambda x: setattr(x, 'RSIface', FACE_CONFIG[int(x.RSIface)]), subdiary_list)
        map(lambda x: x.fill(self.sroom.get_subdiaryequirment_by_hsiid(x.HSIid), 'equirment'), subdiary_list)
        # 如果是合租
        if room.ROrenttype == 0:
            # img, area, face
            first_subdiary = {}
            first_subdiary['HSIimage'] = room.ROimage
            first_subdiary['HSIarea'] = room.ROarea
            first_subdiary['RSIface'] = room.ROface
            first_subdiary['equirment'] = self.sroom.get_room_equirment_by_roid(roid)
            subdiary_list.insert(0, first_subdiary)
        else:
            pass
        room.fill(subdiary_list, 'subdiary')
        roid = room.ROid
        house = self.sroom.get_house_by_hoid(hoid)
        house.size = str(house.HObedroomcount) + u'室' + str(house.HOparlorcount) + u'厅'
        house.floor = str(house.HOfloor) + '/' + str(house.HOtotalfloor) + u'层'
        room.add('house').house = house
        return room

    def _fill_release_info(self, room):
        """填充轉租"""
        if room.ROstatus == 3:
            room.ROname = u'转' + room.ROname

    def _fill_roomate_info(self, room):
        """填充室友信息(合租)"""
        hoid = room.HOid
        if room.ROstatus != 0:
            return
        # 该house下的所有room
        rooms_in_same_house = self.sroom.get_bedroom_by_hoid(hoid)
        for room_in_same_house in rooms_in_same_house:
            # 如果未租出(或者正在转租), 参数有: 卧室名,价格,状态
            # 如果已经租出, 参数有: 卧室名, 性别, 状态, 星座.
            if room_in_same_house.ROstatus <= 3:  # 0: 待审核, 1: 配置中(可预订), 2: 可入住, 3: 转租
                room_in_same_house.fields = ['ROid', 'ROnum', 'ROshowprice', 'ROshowpriceunit']
                self._fill_show_price(room_in_same_house)
            elif room_in_same_house.ROstatus == 5: # 已经租出
                room_in_same_house.fields = ['ROnum']
                user = self.suser.get_user_by_roid(room_in_same_house.ROid)
                user.fields = ['USgender', 'USstar']
                user.USgender = GENDER_CONFIG[int(user.USgender)]
                room_in_same_house.fill(user, 'user')
            room.fill(rooms_in_same_house, 'rooms_in_same_house')


