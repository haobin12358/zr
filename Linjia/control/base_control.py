# -*- coding: utf-8 -*-
from Linjia.configs.enums import FACE_CONFIG, RENT_TYPE, GENDER_CONFIG
from Linjia.commons.error_response import NOT_FOUND


class BaseRoomControl(object):
    def _fill_detail_for_list(self, room):
        """调整返回列表的格式"""
        room_respose_fields = ['ROid', 'ROname', 'ROarea', 'face',
                               'ROdistance', 'ROshowpriceunit',
                               'ROshowprice',  'ROshowpriceunit'
                               'ROimage', 'ROrenttype']
        room.fields = room_respose_fields
        room.face = FACE_CONFIG.get(int(room.ROface), u'未知')
        room.ROrenttype = RENT_TYPE.get(int(room.ROrenttype), u'未知')
        if room.ROstatus == 3:
            room.ROname = u'转' + room.ROname
        return room

    def _fill_house_info(self, room):
        hoid = room.HOid
        house = self.sroom.get_house_by_hoid(hoid)
        house.size = str(house.HObedroomcount) + u'室' + str(house.HOparlorcount) + u'厅'
        house.floor = str(house.HOfloor) + '/' + str(house.HOtotalfloor) + u'层'
        house.fields = ['size', 'floor']
        room.fill(house, 'house')  # room.house = house
        return room

    def _fill_release_info(self, room):
        """填充轉租"""
        if room.ROstatus == 3:
            room.ROname = u'转' + room.ROname

    def _fill_roomate_info(self, room):
        """填充室友信息(合租)"""
        hoid = room.HOid
        # 不是合租则直接返回
        if room.ROstatus != 0:
            return
        # 该house下的所有room
        rooms_in_same_house = self.sroom.get_bedroom_by_hoid(hoid)
        for room_in_same_house in rooms_in_same_house:
            # 如果未租出(或者正在转租), 参数有: 卧室名,价格,状态
            # 如果已经租出, 参数有: 卧室名, 性别, 状态, 星座.
            if room_in_same_house.ROstatus <= 3:  # 0: 待审核, 1: 配置中(可预订), 2: 可入住, 3: 转租
                room_in_same_house.fields = ['ROid', 'ROnum', 'ROshowprice', 'ROshowpriceunit']
            elif room_in_same_house.ROstatus == 5:  # 已经租出
                room_in_same_house.fields = ['ROnum']
                user = self.suser.get_user_by_roid(room_in_same_house.ROid)
                user.fields = ['USgender', 'USstar']
                user.USgender = GENDER_CONFIG[int(user.USgender)]
                room_in_same_house.fill(user, 'user')
        room.fill(rooms_in_same_house, 'rooms_in_same_house')


class BaseIndexControl(object):
    def _fill_room_simple(self, rent_show):
        """添加显示房源的: id, 名字, 图片, 价格, 地址"""
        roid = rent_show.ROid
        room = self.sroom.get_room_by_roid(roid)
        self._fill_show_price(room)
        show_fields = ['ROid', 'ROname', 'ROimage', 'ROdistance', 'ROprice']
        # 下一句等同于: rent_show.ROid = room.ROid; rent_show.ROname = room.ROname....
        map(lambda x: setattr(rent_show, x, getattr(room, x)), show_fields)
        rent_show.fields = show_fields
        rent_show.add('RISid')
        return room

    def _fill_apartment_simple(self, apartment_show):
        """填充公寓的名字"""
        apid = apartment_show.APid
        apartment = self.sapartment.get_apartment_by_apid(apid)
        if not apartment:
            raise NOT_FOUND(u'没有这个公寓' + apid)
        apartment_show.fill(apartment.APname, 'name')

    def _fill_homestay_simple(self, homestay_show):
        """填充民宿的价格, 名字, 图片, 出租方式, 城市"""
        hsid = homestay_show.HSid
        homestay = self.shomestay.get_homestay_by_hsid(hsid)
        if not homestay:
            raise NOT_FOUND(u'没有这个民宿' + hsid)
        homestay_show.minprice = homestay.HSprice
        homestay_show.name = homestay.HSname
        homestay_show.headpic = homestay.HSimage
        homestay_show.city = homestay.HScitynum
        # 城市
        citynum = homestay.HScitynum
        city = self.scity.get_city_by_citynum(citynum)
        homestay_show.city = city.Cityname
        homestay_show.add('minprice', 'name', 'headpic', 'city')
