# -*- coding: utf-8 -*-
from Linjia.configs.enums import FACE_CONFIG, RENT_TYPE, GENDER_CONFIG, DECORATOR_STYLE, ROSTATUS
from Linjia.commons.error_response import NOT_FOUND


class BaseRoomControl(object):
    def _fill_detail_for_list(self, room):
        """调整返回列表的格式"""
        room.fields = ['ROid', 'ROname', 'ROarea', 'face',
                        'ROdistance', 'ROshowprice', 'ROshowpriceunit',
                        'ROimage', 'ROrenttype']
        if room.ROstatus == 3:
            room.ROname = u'转' + room.ROname
        room.face = FACE_CONFIG.get(int(room.ROface), u'未知')
        room.ROrenttype = RENT_TYPE.get(int(room.ROrenttype), u'未知')
        room.ROdecorationstyle = DECORATOR_STYLE.get(int(room.ROdecorationstyle), u'未知')
        room.ROstatus = ROSTATUS.get(int(room.ROstatus), u'未知')
        return room

    def _fill_house_info(self, room):
        hoid = room.HOid
        house = self.sroom.get_house_by_hoid(hoid)
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
        hoid = room.HOid
        # 不是合租则直接返回
        if room.ROrenttype != 0:
            return
        # 该house下的所有room
        rooms_in_same_house = self.sroom.get_bedroom_by_hoid(hoid)
        for room_in_same_house in rooms_in_same_house:
            # 如果未租出(或者正在转租), 参数有: 卧室名,价格,状态
            # 如果已经租出, 参数有: 卧室名, 性别, 状态, 星座.
            if room_in_same_house.ROstatus <= 3:  # 0: 待审核, 1: 配置中(可预订), 2: 可入住, 3: 转租
                room_in_same_house.fields = ['ROid', 'ROnum', 'ROshowprice', 'ROshowpriceunit']
                room_in_same_house.fill(u'未租出', 'status')
            elif room_in_same_house.ROstatus == 5:  # 已经租出
                room_in_same_house.fields = ['ROnum']
                user = self.suser.get_user_by_roid(room_in_same_house.ROid)
                user.fields = ['USgender', 'USstar']
                user.USgender = GENDER_CONFIG[int(user.USgender)]
                room_in_same_house.fill(user, 'user')
                room_in_same_house.fill(u'已租出', 'status')
        room.fill(rooms_in_same_house, 'rooms_in_same_house')
        return self


class BaseIndexControl(object):
    def _fill_index_room_detail(self, index_room):
        room = self.sroom.get_room_by_roid(index_room.ROid)  # 与首页显示项目关联的room
        room.fields = ['ROid', 'ROname', 'ROimage', 'ROshowprice', 'ROshowpriceunit', 'ROrenttype']
        index_room.fill(room, 'room')
        self._fill_house_info(room)
        return self