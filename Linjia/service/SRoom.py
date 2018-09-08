# -*- coding: utf-8 -*-
from flask import current_app
from sqlalchemy import or_, and_

from Linjia.commons.base_service import SBase, close_session
from Linjia.models import Room, House, UserSubslease, RoomEquirment, RoomMedia, RoomTag, Icon


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
        # todo 离地铁近
        all_room = self.session.query(Room).filter(Room.ROstatus >= 1, Room.ROisdelete==False)
        if 'type' in kwargs:
            all_room = all_room.filter(Room.ROrenttype == int(kwargs.get('type')))
        if 'style' in kwargs:
            all_room = all_room.filter(or_(Room.ROdecorationstyle == int(v) for v in kwargs.get('style')))
        if 'lowprice' in kwargs:
            all_room = all_room.filter(Room.ROshowprice > float(kwargs.get('lowprice')))
        if 'highprice' in kwargs:
            all_room = all_room.filter(Room.ROshowprice < float(kwargs.get('highprice')))
        if 'face_args' in kwargs:
            all_room = all_room.filter(or_(Room.ROface == int(v) for v in kwargs.get('face_args')))
        if 'show_type' in kwargs:
            all_room = all_room.join(RoomMedia, RoomMedia.ROid == Room.ROid).filter(RoomMedia.REtype == kwargs.get('show_type'))
        if 'bed_count' in kwargs:
            all_room = all_room.join(House, House.HOid==Room.HOid).filter(or_(House.HObedroomcount == int(v) for v in kwargs.get('bed_count')))
        page_num = kwargs.get('page')
        page_size = kwargs.get('count')
        return all_room.offset((page_num - 1) * page_size).limit(page_size).all()

    @close_session
    def get_house_by_hoid(self, hoid):
        """获取house"""
        return self.session.query(House).filter_by(HOid=hoid).first()

    @close_session
    def get_room_media_by_roid(self, roid):
        """获取房源的显示图片或视频信息"""
        return self.session.query(RoomMedia).filter_by(ROid=roid).all()

    @close_session
    def get_reaseinfo_by_roid(self, roid):
        """通过roid获取转租信息"""
        self.session.query(UserSubslease).filter_by(ROid=roid, Subsleaseisdelete=False).first()

    @close_session
    def get_tags_by_roid(self, roid):
        """"""
        return self.session.query(RoomTag).filter_by(ROid=roid).all()

    @close_session
    def get_room_equirment_by_roid(self, roid):
        return self.session.query(Icon).join(RoomEquirment, Icon.IConid==RoomEquirment.IConid).filter(RoomEquirment.ROid==roid).all()

    @close_session
    def get_house_by_roid(self, roid):
        """获取house"""
        return self.session.query(House).filter_by(ROid=roid).all()

    @close_session
    def get_bedroom_by_hoid(self, hoid):
        """获取通过house下的room, (仅用于合租)"""
        return self.session.query(Room).filter_by(HOid=hoid).all()



'''

 待删除
        if 'filter_type_list' in kwargs:
            filter_type_list = kwargs.get('filter_type_list')
            renttype_list = [and_(
                    Room.ROrenttype == int(ROrenttype),
                    *filter(lambda x: x.right.value != 0, [Room.ROpersoncount == int(ROpersoncount)])

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
        

'''
