# -*- coding: utf-8 -*-
from sqlalchemy import or_, and_

from Linjia.commons.base_service import SBase, close_session
from Linjia.models import Room, House, UserSubslease, RoomEquirment, RoomMedia, RoomTag, Icon, JoinRoomBanner, \
    HomeStayBanner, BedroomBehindRoom, UserBedroomBehindRoom, VillegeInfoAndSubway, CustomerGuide


class SRoom(SBase):
    @close_session
    def get_joint_room_list(self):
        """获取合租列表"""
        return self.session.query(Room).filter_by(ROrenttype=0, ROisdelete=False).all()

    @close_session
    def get_room_by_roid(self, roid):
        """根据id获取房源"""
        return self.session.query(Room).filter_by(ROid=roid, ROisdelete=False).first()

    @close_session
    def delete_room_by_roid(self, roid):
        """删除房源"""
        return self.session.query(Room).filter_by(ROid=roid).update({
            'ROisdelete': True
        })

    @close_session
    def update_room_by_roid(self, roid, data):
        """根据房源信息"""
        return self.session.query(Room).filter(Room.ROid == roid).update(data)

    @close_session
    def get_room_list_filter(self, kwargs, admin=False, style=[], face_args=[]):
        """获取所有(合租和整租"""
        all_room = self.session.query(Room).filter(Room.ROisdelete == False)
        all_room = all_room.filter_ignore_none_args(Room.ROrenttype == kwargs.get('type'),
                                                    Room.ROcitynum == kwargs.get('city_id'),
                                                    Room.ROareanum == kwargs.get('area_id')). \
            gt(Room.ROshowprice == kwargs.get('lowprice')).\
            lt(Room.ROshowprice == kwargs.get('highprice')).\
            filter(or_(Room.ROdecorationstyle == v for v in style)).\
            filter(or_(Room.ROface == v for v in face_args))
        if 'show_type' in kwargs:
            all_room = all_room.join(RoomMedia, RoomMedia.ROid == Room.ROid).filter(
                RoomMedia.REtype == kwargs.get('show_type'))
        if 'bed_count' in kwargs:
            all_room = all_room.join(House, House.HOid == Room.HOid).filter(
                or_(House.HObedroomcount == int(v) for v in kwargs.get('bed_count')))

        if 'subway' in kwargs:
            all_room = all_room.join(House, House.HOid == Room.HOid).join(VillegeInfoAndSubway, House.VIid == VillegeInfoAndSubway.id).contain(VillegeInfoAndSubway.subway == kwargs.get('subway'))
        if 'villege' in kwargs:
            all_room = all_room.join(House, House.HOid == Room.HOid).join(VillegeInfoAndSubway, House.VIid == VillegeInfoAndSubway.id).contain(VillegeInfoAndSubway.name == kwargs.get('villege'))

        return all_room.all_with_page(kwargs.get('page'), kwargs.get('count'))

    @close_session
    def get_house_by_hoid(self, hoid):
        """获取house"""
        return self.session.query(House).filter_by(HOid=hoid).first()

    @close_session
    def get_villege_info_by_hoid(self, hoid):
        """通过hoid获取小区信息"""
        return self.session.query(VillegeInfoAndSubway).join(House, House.VIid == VillegeInfoAndSubway.id).filter(House.HOid==hoid).first()

    @close_session
    def update_house_by_hoid(self, hoid, data):
        """更新house"""
        return self.session.query(House).filter_by(HOid=hoid).update(data)

    @close_session
    def get_room_media_by_roid(self, roid):
        """获取房源的显示图片或视频信息"""
        return self.session.query(RoomMedia).filter_by(ROid=roid).all()

    @close_session
    def get_room_media_by_link(self, link):
        """根据图片或视频链接获得"""
        return self.session.query(RoomMedia).filter(RoomMedia.REpic == link).first()

    @close_session
    def delete_room_media_by_link(self, link):
        return self.session.query(RoomMedia).filter(RoomMedia.REpic == link).delete()

    @close_session
    def delete_room_media_by_roid(self, roid):
        return self.session.query(RoomMedia).filter(RoomMedia.ROid == roid).delete()
    
    @close_session
    def get_reaseinfo_by_roid(self, roid):
        """通过roid获取转租信息"""
        self.session.query(UserSubslease).filter_by(ROid=roid, Subsleaseisdelete=False).first()

    @close_session
    def get_tags_by_roid(self, roid):
        """"""
        return self.session.query(RoomTag).filter_by(ROid=roid).all()

    @close_session
    def delete_tag_by_roid(self, roid):
        """删除某个房源的tag"""
        return self.session.query(RoomTag).filter_by(ROid=roid).delete()

    @close_session
    def get_room_equirment_by_roid(self, roid):
        return self.session.query(RoomEquirment).filter(RoomEquirment.ROid == roid).first()

    @close_session
    def delete_room_equirment_by_roid(self, roid):
        """删除某个房源的设备信息"""
        return self.session.query(RoomEquirment).filter(RoomEquirment.ROid == roid).delete()

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
        return self.session.query(BedroomBehindRoom).filter(BedroomBehindRoom.ROid == roid, BedroomBehindRoom.BBRisdelete == False).order_by(
            BedroomBehindRoom.BBRnum).all()

    # 2018年09月12日 调整
    @close_session
    def get_roomates_info_by_bbrid(self, bbrid):
        """获取卧室的入住情况"""
        return self.session.query(UserBedroomBehindRoom).filter(UserBedroomBehindRoom.BBRid == bbrid, UserBedroomBehindRoom.UBBRstatus == 0).first()
    
    @close_session
    def update_roomates_info_by_bbrid(self, bbrid, data):
        return self.session.query(UserBedroomBehindRoom).filter(UserBedroomBehindRoom.BBRid == bbrid).update(data)

    @close_session
    def get_bedroom_by_bbrid(self, bbrid):
        """根据卧室id获取卧室"""
        return self.session.query(BedroomBehindRoom).filter_by(BBRid=bbrid, BBRisdelete=False).first()

    @close_session
    def update_bedroom_by_bbrid(self, bbrid, data):
        """根据卧室id更新卧室"""
        return self.session.query(BedroomBehindRoom).filter_by(BBRid=bbrid, BBRisdelete=False).update(data)

    @close_session
    def get_joinroom_banner_list(self):
        """获取友家页的轮播图"""
        return self.session.query(JoinRoomBanner).order_by(JoinRoomBanner.JRBsort).all()

    @close_session
    def delete_joinroom_banner(self, jrbid):
        """删除友家页的轮播图"""
        return self.session.query(JoinRoomBanner).filter(JoinRoomBanner.JRBid == jrbid).delete()

    @close_session
    def get_homestay_banner_list(self):
        """获取民宿页的轮播图"""
        return self.session.query(HomeStayBanner).order_by(HomeStayBanner.HSBsort).all()

    @close_session
    def delete_homestay_banner(self, hsbid):
        """删除民宿页的轮播图"""
        return self.session.query(HomeStayBanner).filter(HomeStayBanner.HSBid == hsbid).delete()

    @close_session
    def get_villege_info_by_name(self, name):
        """根据公寓名字获取小区地铁信息"""
        return self.session.query(VillegeInfoAndSubway).filter(VillegeInfoAndSubway.name.contains(name)).all()

    @close_session
    def get_villege_info_by_id(self, viid):
        """根据id获取小区"""
        return self.session.query(VillegeInfoAndSubway).filter(VillegeInfoAndSubway.id == viid).first()

    @close_session
    def update_villege_info(self, viid, data):
        """更新小区信息"""
        return self.session.query(VillegeInfoAndSubway).filter(VillegeInfoAndSubway.id==viid).update(data)
    
    @close_session
    def get_guide_list(self):
        """获取入住指南"""
        return self.session.query(CustomerGuide).filter_by(CGisdelete=False).all()

    @close_session
    def update_guide(self, cgid, data):
        """更新入住指南"""
        return self.session.query(CustomerGuide).filter_by(CGid=cgid).update(data)

    @close_session
    def get_guide_by_cgid(self, cgid):
        """获取guide"""
        return self.session.query(CustomerGuide).filter_by(CGid=cgid).first()

