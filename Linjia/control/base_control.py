# -*- coding: utf-8 -*-
from Linjia.configs.enums import FACE_CONFIG, RENT_TYPE, GENDER_CONFIG, DECORATOR_STYLE, ROSTATUS
from Linjia.commons.error_response import NOT_FOUND


class BaseRoomControl(object):
    def _fill_detail_for_list(self, room):
        """调整返回列表的格式"""
        room.fields = ['ROid', 'ROname', 'ROarea', 'face',
                        'ROdistance', 'ROshowprice', 'ROshowpriceunit',
                        'ROimage', 'ROrenttype', 'ROdecorationstyle']
        room.face = FACE_CONFIG.get(int(room.ROface), u'未知')
        room.ROrenttype = RENT_TYPE.get(int(room.ROrenttype), u'未知')
        room.ROdecorationstyle = DECORATOR_STYLE.get(int(room.ROdecorationstyle), u'未知')
        # room.ROstatus = ROSTATUS.get(int(room.ROstatus), u'未知')
        return self

    def _fill_house_info(self, room):
        hoid = room.HOid
        house = self.sroom.get_house_by_hoid(hoid)
        if not house:
            house = {
                'size': '',
                'floor': ''
            }
            room.fill(house, 'house')
            return self
        house.size = str(house.HObedroomcount) + u'室' + str(house.HOparlorcount) + u'厅'
        house.floor = str(house.HOfloor) + '/' + str(house.HOtotalfloor) + u'层'
        house.fields = ['size', 'floor']
        room.fill(house, 'house')  # room.house = house
        return self

    def _fill_release_info(self, room):
        """填充轉租"""
        if room.ROstatus == 3:
            room.ROname = u'转' + room.ROname
        return self

    def _fill_roomate_info(self, room):
        """填充室友信息(合租)"""
        roid = room.ROid
        # 不是合租则直接返回
        if room.ROrenttype != 0:
            return
        # 该house下的所有room
        rooms_in_same_house = self.sroom.get_bedroom_entryinfo_by_roid(roid)
        for room_in_same_house in rooms_in_same_house:
            # 如果未租出(或者正在转租), 参数有: 卧室名,价格,状态
            # 如果已经租出, 参数有: 卧室名, 性别, 状态, 星座.
            if room_in_same_house.BBRstatus <= 3:  # 0: 待审核, 1: 配置中(可预订), 2: 可入住, 3: 转租
                room_in_same_house.fields = ['BBRid', 'BBRnum', 'BBRshowprice', 'BBRshowpriceunit']
                room_in_same_house.fill(u'未租出', 'status')
            elif room_in_same_house.BBRstatus == 5:  # 已经租出
                room_in_same_house.fields = ['BBRnum']
                user = self.sroom.get_roomates_info_by_bbrid(room_in_same_house.BBRid)
                user.fields = ['USgender' ]
                user.USgender = GENDER_CONFIG[int(user.USgender)]
                room_in_same_house.fill(user, 'user')
                room_in_same_house.fill(u'已租出', 'status')
        room.fill(rooms_in_same_house, 'rooms_in_same_house')
        return self


class BaseIndexControl(object):
    def _fill_index_room_detail(self, index_room):
        room = self.sroom.get_room_by_roid(index_room.ROid)  # 与首页显示项目关联的room
        self._fill_house_info(room)
        fields = ['ROid', 'ROname', 'ROimage', 'ROshowprice', 'ROshowpriceunit', 'ROrenttype', 'ROdecorationstyle', 'house']
        map(lambda x: index_room.fill(getattr(room, x), x), fields)
        index_room.ROrenttype = RENT_TYPE.get(int(index_room['ROrenttype']))
        index_room.ROdecorationstyle = DECORATOR_STYLE.get(int(index_room['ROdecorationstyle']))
        # index_room.fill(room, 'room')
        return self
