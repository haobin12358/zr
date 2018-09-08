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


