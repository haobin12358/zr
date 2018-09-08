# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Boolean

from Linjia.commons.base_model import Base

'''
class City(Base):
    """省市"""
    __tablename__ = 'city'
    Cityid = Column(String(64), primary_key=True)
    Citynum = Column(String(64), nullable=False, comment=u"城市编号")
    Cityname = Column(String(64), nullable=False, comment=u'城市名字')
    Cityprovincename = Column(String(64), nullable=False, comment=u'所在省份')
    Cityprovincenum = Column(String(64), nullable=False, comment=u'所在省份编号')
'''


class Province(Base):
    """省"""
    __tablename__ = 'province'
    _id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    province_id = Column(String(8), nullable=False)

class City(Base):
    __tablename__ = 'city'
    _id = Column(Integer, primary_key=True)
    city_id = Column(String(8), nullable=False)
    name = Column(String(20), nullable=False)
    province_id = Column(String(8), nullable=False)

class Area(Base):
    __tablename__ = 'area'
    _id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    area_id = Column(String(8), nullable=False)
    city_id = Column(String(8), nullable=False)


