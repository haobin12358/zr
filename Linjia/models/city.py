# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Boolean

from Linjia.commons.base_model import Base


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


class RoomCity(Base):
    """开放租房服务城市"""
    __tablename__ = 'roomcity'
    RCid = Column(String(64), primary_key=True)
    city_id = Column(String(8), nullable=False)
    ishot = Column(Boolean, default=False, comment=u'是否热门')


class MoverCity(Base):
    """开放搬家的城市"""
    __tablename__ = 'movercity'
    MCid = Column(String(64), primary_key=True)
    city_id = Column(String(8), nullable=False)


class CleanerCity(Base):
    """开通清洁的城市"""
    __tablename__ = 'cleanercity'
    CCid = Column(String(64), primary_key=True)
    city_id = Column(String(8), nullable=False)

class FixerCity(Base):
    """开通维修的服务"""
    __tablename__ = 'fixercity'
    FCid = Column(String(64), primary_key=True)
    city_id = Column(String(8), nullable=False)