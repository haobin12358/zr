# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import City, Province


class SCity(SBase):
    # @close_session
    # def get_city_by_cityid(self, cityid):
    #     return self.session.query(City).filter_by(_id=cityid).first()

    @close_session
    def get_city_by_cityid(self, city_id):
        """根据编号查找城市"""
        return self.session.query(City).filter_by(city_id=city_id).first()

    @close_session
    def get_citylist_by_provinceid(self, province_id):
        """根据省份编号获取城市列表"""
        return self.session.query(City).filter_by(province_id=province_id).all()
