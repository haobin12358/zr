# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import City, RoomCity, MoverCity, Area, CleanerCity, FixerCity, SubwayLine, SubwayPosition


class SCity(SBase):
    # @close_session
    # def get_city_by_cityid(self, cityid):
    #     return self.session.query(City).filter_by(_id=cityid).first()

    @close_session
    def get_city_by_city_id(self, city_id):
        """根据编号查找城市"""
        return self.session.query(City).filter_by(city_id=city_id).first()

    @close_session
    def get_areainfo_by_id(self, id):
        """根据id获取地区"""
        return self.session.query(Area).filter(Area.area_id == id).first()

    @close_session
    def get_citylist_by_provinceid(self, province_id):
        """根据省份编号获取城市列表"""
        return self.session.query(City).filter_by(province_id=province_id).all()

    @close_session
    def get_roomoppencitylist(self):
        """获取房源开放城市"""
        return self.session.query(RoomCity).all()

    @close_session
    def is_room_open_city(self, city_id):
        """判断城市是否是房源开放城市"""
        return self.session.query(RoomCity).filter(RoomCity.city_id == city_id).first()

    @close_session
    def update_room_open_city(self, city_id, data):
        return self.session.query(RoomCity).filter(RoomCity.city_id == city_id).update(data)

    @close_session
    def delete_roomoppencity(self, city_id):
        return self.session.query(RoomCity).filter(RoomCity.city_id == city_id).delete()

    @close_session
    def delete_roomoppencity(self, city_id):
        """取消城市房源开放"""
        return self.session.query(RoomCity).filter_by(city_id=city_id).delete()

    @close_session
    def get_moveroppencitylist(self):
        """搬家服务开放城市列表"""
        return self.session.query(MoverCity).all()

    @close_session
    def delete_moveroppen(self, city_id):
        """取消搬家服务开放"""
        return self.session.query(MoverCity).filter(MoverCity.city_id == city_id).delete()

    @close_session
    def get_area_list_by_cityid(self, cityid):
        """获取城市下的所有地区"""
        return self.session.query(Area).filter_by(city_id=cityid).all()

    @close_session
    def is_move_oppener(self, city_id):
        """城市是否开通搬家"""
        return self.session.query(MoverCity).filter(MoverCity.city_id==city_id).first()

    @close_session
    def get_cleaneroppencitylist(self):
        """获取开通清洁服务的城市"""
        return self.session.query(CleanerCity).all()

    @close_session
    def delete_cleanoppen(self, city_id):
        """取消保洁服务的城市"""
        return self.session.query(CleanerCity).filter_by(city_id=city_id).delete()

    @close_session
    def is_clean_oppener(self, city_id):
        """城市是否开通清洁"""
        return self.session.query(CleanerCity).filter(CleanerCity.city_id==city_id).first()

    @close_session
    def get_fixeroppencitylist(self):
        """获取开通维修服务的城市"""
        return self.session.query(FixerCity).all()

    @close_session
    def delete_fixeroppencity(self, city_id):
        """取消维修服务城市"""
        return self.session.query(FixerCity).filter_by(city_id=city_id).delete()

    @close_session
    def is_fixer_oppener(self, city_id):
        """是否开通维修服务"""
        return self.session.query(FixerCity).filter_by(city_id=city_id).first()

    @close_session
    def get_subwayline_by_city_id(self, city_id):
        """获取城市内的地铁线路"""
        return self.session.query(SubwayLine).filter(SubwayLine.city_id==city_id).all()

    @close_session
    def get_subwayline_by_lineid(self, lineid):
        """获取线路 根据id"""
        return self.session.query(SubwayLine).filter(SubwayLine.subwaylineid==lineid).first()

    @close_session
    def get_subwayposition_by_line_id(self, lineid):
        """获取该地铁线路的所有站点"""
        return self.session.query(SubwayPosition).filter(SubwayPosition.subwaylineid==lineid).all()

