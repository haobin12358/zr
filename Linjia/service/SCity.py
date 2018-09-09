# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import City, RoomCity, MoverCity, Area


class SCity(SBase):
    # @close_session
    # def get_city_by_cityid(self, cityid):
    #     return self.session.query(City).filter_by(_id=cityid).first()

    @close_session
    def get_city_by_city_id(self, city_id):
        """根据编号查找城市"""
        return self.session.query(City).filter_by(city_id=city_id).first()

    @close_session
    def get_citylist_by_provinceid(self, province_id):
        """根据省份编号获取城市列表"""
        return self.session.query(City).filter_by(province_id=province_id).all()

    @close_session
    def get_roomoppencitylist(self):
        """获取房源开放城市"""
        return self.session.query(RoomCity).all()

    @close_session
    def get_moveroppencitylist(self):
        """搬家服务开放城市列表"""
        return self.session.query(MoverCity).all()

    @close_session
    def get_area_list_by_cityid(self, cityid):
        """获取城市下的所有地区"""
        return self.session.query(Area).filter_by(city_id=cityid).all()

    @close_session
    def is_move_oppener(self, city_id):
        """是否开通搬家"""
        return self.session.query(MoverCity).filter(MoverCity.city_id==city_id).first()
