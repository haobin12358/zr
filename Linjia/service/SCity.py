# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import City


class SCity(SBase):
    @close_session
    def get_city_by_cityid(self, cityid):
        return self.session.query(City).filter_by(Cityid=cityid).first()

    @close_session
    def get_city_by_citynum(self, citynum):
        """根据编号查找城市"""
        return self.session.query(City).filter_by(Citynum=citynum).first()

    @close_session
    def get_citylist_by_provincenum(self, provincenum):
        """根据省份编号获取城市列表"""
        return self.session.query(City).filter_by(Cityprovincenum=provincenum).all()
