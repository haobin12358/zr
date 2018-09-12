# -*- coding: utf-8 -*-
from sqlalchemy import or_, and_

from Linjia.commons.base_service import SBase, close_session
from Linjia.models import Room, House, UserSubslease, RoomEquirment, RoomMedia, RoomTag, Icon, JoinRoomBanner, \
    HomeStayBanner, BedroomBehindRoom, UserBedroomBehindRoom, VillegeInfoAndSubway


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
    def get_room_list_filter(self, kwargs, admin=False):
        """获取所有(合租和整租"""
        # todo 离地铁近
        all_room = self.session.query(Room).filter(Room.ROisdelete==False)
        if not admin:
            all_room = all_room.join(BedroomBehindRoom, Room.ROid==BedroomBehindRoom.ROid).filter(BedroomBehindRoom.BBRstatus >= 1, Room.ROisdelete==False)
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
        if 'city_id' in kwargs:
            all_room = all_room.filter(Room.ROcitynum==kwargs.get('city_id'))
        if 'area_id' in kwargs:
            all_room = all_room.filter(Room.ROareanum==kwargs.get('area_id'))
        return all_room.all_with_page(kwargs.get('page'), kwargs.get('count'))

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
        return self.session.query(RoomEquirment).filter(RoomEquirment.ROid==roid).first()

    @close_session
    def get_house_by_roid(self, roid):
        """获取house"""
        return self.session.query(House).filter_by(ROid=roid).all()

    # @close_session
    # 2018年09月12日 删除
    # def get_bedroom_by_hoid(self, hoid):
    #     """获取通过house下的room, (仅用于合租)"""
    #     return self.session.query(Room).filter_by(HOid=hoid).all()

    # 2018年09月12日 调整
    @close_session
    def get_bedroom_entryinfo_by_roid(self, roid):
        """获取房源下的卧室"""
        return self.session.query(BedroomBehindRoom).filter(BedroomBehindRoom.ROid==roid).order_by(BedroomBehindRoom.BBRnum).all()

    # 2018年09月12日 调整
    @close_session
    def get_roomates_info_by_bbrid(self, bbrid):
        """获取卧室的入住情况"""
        return self.session.query(UserBedroomBehindRoom).filter(UserBedroomBehindRoom.BBRid==bbrid).first()


    @close_session
    def get_joinroom_banner_list(self):
        """获取友家页的轮播图"""
        return self.session.query(JoinRoomBanner).order_by(JoinRoomBanner.JRBsort).all()

    @close_session
    def delete_joinroom_banner(self, jrbid):
        """删除友家页的轮播图"""
        return self.session.query(JoinRoomBanner).filter(JoinRoomBanner.JRBid==jrbid).delete()

    @close_session
    def get_homestay_banner_list(self):
        """获取民宿页的轮播图"""
        return self.session.query(HomeStayBanner).order_by(HomeStayBanner.HSBsort).all()

    @close_session
    def delete_homestay_banner(self, hsbid):
        """删除民宿页的轮播图"""
        return self.session.query(HomeStayBanner).filter(HomeStayBanner.HSBid==hsbid).delete()

    @close_session
    def get_villege_info_by_name(self, name):
        """根据公寓名字获取公寓地铁信息"""
        return self.session.query(VillegeInfoAndSubway).filter(VillegeInfoAndSubway.name.contains(name)).all()




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
