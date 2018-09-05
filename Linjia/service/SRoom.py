# -*- coding: utf-8 -*-
from sqlalchemy import or_, and_

from Linjia.commons.base_service import SBase, close_session
from Linjia.models import Room, RoomFeature, RoomSignInfo, House, RoomPayPrice, Villege, UserSubslease, \
    HouseSubsidiaryInfo, HouseSubsidiaryEquirment, RoomEquirment

FEATURE_CONFG = {  # args: value
    0: RoomFeature.RFfirstrent == True,
    1: RoomFeature.RFtwotoilet == True,
    2: RoomFeature.RFhytingtype == 1,
    3: RoomFeature.RFhytingtype == 2,
    4: RoomFeature.RFhytingtype == 3,
    5: RoomFeature.RFcanpet == True,
    6: RoomFeature.RFlock == True,
    7: RoomFeature.RFelevator == True,
    # 待会会添加装修风格的过滤
}


class SRoom(SBase):
    @close_session
    def get_joint_room_list(self):
        """获取合租列表"""
        return self.session.query(Room).filter_by(ROrenttype=0).all()

    @close_session
    def get_room_by_roid(self, roid):
        """根据id获取房间"""
        return self.session.query(Room).filter_by(ROid=roid).first()

    @close_session
    def get_room_list_filter(self, kwargs):
        """获取所有(合租和整租"""
        # todo 离地铁近, 装修风格..
        print(kwargs)
        all_room = self.session.query(Room). \
            join(House, Room.HOid == House.HOid). \
            join(RoomFeature, Room.ROid == RoomFeature.ROid). \
            join(RoomPayPrice, Room.ROid == RoomPayPrice.ROid). \
            filter(Room.ROisdelete == False, Room.ROshowpricetype == RoomPayPrice.RPPperiod)

        if 'filter_type_list' in kwargs:
            filter_type_list = kwargs.get('filter_type_list')
            renttype_list = [and_(
                *filter(lambda x: x.right.value != 0, [
                    Room.ROrenttype == int(ROrenttype),
                    Room.ROpersoncount == int(ROpersoncount)
                ])
            ) for ROrenttype, ROpersoncount in filter_type_list]
            all_room = all_room.filter(or_(*renttype_list))
        if 'lowprice' in kwargs:
            all_room.filter(RoomPayPrice.RPPprice > float(kwargs.get('lowprice')))
        if 'highprice' in kwargs:
            all_room.filter(RoomPayPrice.RPPprice < float(kwargs.get('highprice')))
        if 'faceargs' in kwargs:
            face_args = kwargs.get('faceargs')
            face_arg = or_(*[Room.ROface == x for x in face_args])
            all_room = all_room.filter(face_arg)
        if 'sign_args' in kwargs:
            all_room = all_room.join(RoomSignInfo, Room.ROid == RoomSignInfo.ROid)
            all_room = all_room.filter(RoomSignInfo.PSIsigntype == int(kwargs.get('Dbcreater')))
        if 'lowarea' in kwargs:
            all_room = all_room.filter(Room.ROarea > float(kwargs.get('lowarea')))
        if 'hignarea' in kwargs:
            all_room = all_room.filter(Room.ROarea < float(kwargs.get('hignarea')))
        if 'green_rate' in kwargs:
            all_room = all_room.join(Villege, House.VIid == Villege.VIid)
            all_room.filter(Villege.VIgreen > float(kwargs.get('green_rate')))
        if 'status' in kwargs:
            all_room = all_room.filter(Room.ROstatus == int(kwargs.get('status')))
        if 'feature' in kwargs:
            all_room = all_room.filter(or_(*[FEATURE_CONFG[int(k)] for k in kwargs.get('feature')]))
        if 'kw' in kwargs:
            all_room = all_room.filter(and_(*[Room.ROname.like('%' + w + '%') for w in kwargs.get('kw')]))
        page_num = kwargs.get('page')
        page_size = kwargs.get('count')
        return all_room.offset((page_num - 1) * page_size).limit(page_size).all()

    @close_session
    def get_features_by_roid(self, roid):
        """通过roid获取特色值"""
        return self.session.query(RoomFeature).filter_by(ROid=roid).first()

    @close_session
    def get_price_by_roidandperid(self, roid, showpricetype):
        """价格"""
        return self.session.query(RoomPayPrice).filter_by(ROid=roid, RPPperiod=showpricetype).first()

    @close_session
    def get_price_by_roid(self, roid):
        """价格"""
        return self.session.query(RoomPayPrice).filter_by(ROid=roid).all()

    @close_session
    def get_house_by_hoid(self, hoid):
        """获取house"""
        return self.session.query(House).filter_by(HOid=hoid).first()

    @close_session
    def get_reaseinfo_by_roid(self, roid):
        """通过roid获取转租信息"""
        self.session.query(UserSubslease).filter_by(ROid=roid, Subsleaseisdelete=False).first()

    @close_session
    def get_subdiaryinfo_by_hoid(self, hoid):
        """房源配套信息(图片就在这个表中)"""
        return self.session.query(HouseSubsidiaryInfo).filter_by(HOid=hoid).order_by(HouseSubsidiaryInfo.HRIsort).all()

    @close_session
    def get_subdiaryequirment_by_hsiid(self, hsiid):
        """配套中的设备信息"""
        return self.session.query(HouseSubsidiaryEquirment).filter_by(HSIid=hsiid).order_by(
            HouseSubsidiaryEquirment.HSEsort).all()

    @close_session
    def get_room_equirment_by_roid(self, roid):
        return self.session.query(RoomEquirment).filter_by(ROid=roid).all()

    @close_session
    def get_house_by_roid(self, roid):
        """获取house"""
        return self.session.query(House).filter_by(ROid=roid).all()
