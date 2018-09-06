# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Boolean

from Linjia.commons.base_model import Base


class City(Base):
    """省市"""
    __tablename__ = 'city'
    Cityid = Column(String(64), primary_key=True)
    Citynum = Column(String(64), nullable=False, comment=u"城市编号")
    Cityname = Column(String(64), nullable=False, comment=u'城市名字')
    Cityprovincename = Column(String(64), nullable=False, comment=u'所在省份')
    Cityprovincenum = Column(String(64), nullable=False, comment=u'所在省份编号')
