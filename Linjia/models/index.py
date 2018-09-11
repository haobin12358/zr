# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Boolean

from Linjia.commons.base_model import Base


class RoomIndexShow(Base):
    """首页展示中的房源(整租/合租)列表"""
    __tablename__ = 'roomindexshow'
    RISid = Column(String(64), primary_key=True)
    ROid = Column(String(64), nullable=False, comment=u'房源id')
    ROtype = Column(Integer, comment=u'0: 合租, 1: 整租, 2: 公寓, 民宿')
    ROsort = Column(Integer, comment=u'顺序标志')


# class APartmentIndexShow(Base):
#     """公寓首页显示"""
#     __tablename__ = 'apartmentindexshow'
#     AISid = Column(String(64), primary_key=True)
#     APid = Column(String(64), nullable=False, comment=u'公寓id')
#     AISsort = Column(Integer, comment=u'顺序标志')
#     AIsubtitle = Column(String(64), comment=u'描述,比如欢乐工厂lof之寓')
#
#
# class HomeStayIndexShow(Base):
#     """显示在首页的民宿"""
#     __tablename__ = 'homestayindexshow'
#     HSIid = Column(String(64), primary_key=True)
#     HSid = Column(String(64), nullable=False, comment=u'民宿id')
#     HSIsort = Column(Integer, comment=u'顺序标志')


class ServerIndexShow(Base):
    """首页显示的服务"""
    __tablename__ = 'serverindexshow'
    SISid = Column(String(64), primary_key=True)
    SISimage = Column(String(255), nullable=False, comment=u'图片')
    SISlink = Column(String(255), nullable=False, comment=u'链接')
    SISsort = Column(Integer, comment=u'顺序标志')


class IndexBanner(Base):
    """首頁论波图"""
    __tablename__ = 'indexbanner'
    IBid = Column(String(64), primary_key=True)
    IBimage = Column(String(255), nullable=False)
    IBlink = Column(String(255), comment=u'跳转链接')
    IBsort = Column(Integer, comment=u'顺序标志')
    IBisdelete = Column(Boolean, default=False, comment=u'是否删除')



# class HomeStayBanner(Base):
#     """民宿"""
#