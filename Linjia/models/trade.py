# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Float, Boolean

from Linjia.commons.base_model import Base


# 房屋托管
class ProvideHouseApply(Base):
    """提供房源申请"""
    __tablename__ = 'provideroomapply'
    PHAid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment=u'用户(业主)id')
    PHAname = Column(String(8), nullable=False, comment=u'用户(业主)姓名')
    PHAphone = Column(String(16), nullable=False, comment=u'电话')
    PHAcity = Column(String(64), nullable=False, comment=u'城市编号')
    PHAcreatetime = Column(String(16), nullable=False, comment=u'申请时间')


class ProprietorHouse(Base):
    """业主-房源签约信息"""
    __tablename__ = 'proprietorroom'
    PHid = Column(String(64), primary_key=True)
    USid = Column(String(64), comment=u'业主用户id')
    ROid = Column(String(64), comment=u'房源id')
    PHprice = Column(Float, comment=u'签约价格')
    PHpriceuit = Column(Integer, default=0, comment=u'计费周期: 0: 月, 1 季, 2 半年, 3 一年')
    # PHprice = Column(Integer, default=0, comment=u'计费周期: 0: 月, 1 季, 2 半年, 3 一年')
    PHstarttime = Column(String(16), comment=u'签约时间')
    PHendtime = Column(String(16), comment=u'到期时间')
    # todo 具体合同信息


class UserRoom(Base):
    """租客住房"""
    __tablename__ = 'userroom'
    URid = Column(String(64), primary_key=True)
    USid = Column(String(64), comment=u'租户id')
    ROid = Column(String(64), comment=u'房源id')
    URstarttime = Column(String(16), nullable=False, comment=u'起始时间')
    URendtime = Column(String(16), nullable=False, comment=u'结束时间')
    # todo 其他具体信息


class UserSubslease(Base):
    """转租-转租者"""
    __tablename__ = 'usesubslease'
    Subsleaseid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment=u'转租者')
    Subsleasephone = Column(String(11), nullable=False, comment=u'转租者电话')
    Subsleasetime = Column(String(16), comment=u'转租时间')
    Subsleasereason = Column(String(255), comment=u'转租理由')
    Subsleaseisdelete = Column(Boolean, default=False, comment=u'是否删除, 当转租出去之后会删除')


class UserApartment(Base):
    """租客公寓住房"""
    __tablename__ = 'userapartment'
    UAid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment=u'住户id')
    APid = Column(String(64), nullable=False, comment=u'公寓id')
    UAstarttime = Column(String(16), nullable=False, comment=u'起始时间')
    UAendtime = Column(String(16), nullable=False, comment=u'结束时间')
    # todo 其他具体信息


class UserHomeStay(Base):
    """租客住民宿"""
    __tablename__ = 'userhomestay'
    UHid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment=u'住户id')
    HSid = Column(String(64), nullable=False, comment=u'民宿id')
    UHstarttime = Column(String(16), nullable=False, comment=u'起始时间')
    UHendtime = Column(String(16), nullable=False, comment=u'结束时间')
    # todo 其他具体信息


class UserMoveTrade(Base):
    """用户服务信息"""
    __tablename__ = 'usermovetrade'
    UMTid = Column(String(64), primary_key=True)
    SMSid = Column(String(64), nullable=False, comment=u'服务规模id')
    UMTstarttime = Column(String(16), nullable=False, comment=u'预约搬家时间')
    UMTmoveoutaddr = Column(String(64), nullable=False, comment=u'搬出地址')
    UMTmoveinaddr = Column(String(64), nullable=False, comment=u'搬入地址')
    UMTdistance = Column(String(64), comment=u'里程')
    UMTphone = Column(String(64), nullable=False, comment=u'电话')
    UMTspecialwish = Column(String(64), comment=u'特殊请求')
    # UMTcoupo = Column(String(64), comment=u'优惠券id') todo
    UMTpreviewprice = Column(Float, comment=u'估算价格')
    UMTstatus = Column(Integer, default=0, comment=u'状态, 0: 已预约, 1: 正在配送, 2: 完成')
    UMTtruestarttime = Column(String(16), comment=u'实际搬出时间')
    UMTtrueendtime = Column(String(16), comment=u'订单完成时间')
    STFid = Column(String(64), comment=u'搬家师傅')
    UMTtrueprice = Column(Float, comment=u'实收价格')


class UserCleanTrade(Base):
    """用户保洁服务"""
    __tablename__ = 'usercleantrace'
    UCTid = Column(String(64), primary_key=True)
    SCEid = Column(String(64), nullable=False, comment=u'保洁规模id')
    UCTaddr = Column(String(125), nullable=False, comment=u'地址')
    UCTpreviewstarttime = Column(String(16), nullable=False, comment=u'预约上门时间')
    UCTspecialwish = Column(String(255), comment=u'特殊需求')
    UCTpreviewlastingtime = Column(Float, comment=u'预约服务时长')
    # UCTcoupo = Column(String(64), comment=u'优惠券id')
    UCTstatus = Column(Integer, default=0, comment=u'订单状态, 0: 已预约, 1: 正在进行, 2: 完成')
    UCTtruestarttime = Column(String(16), comment=u'实际上门时间')
    UCTtrueendtime = Column(String(16), comment=u'工作人员离开时间')
    UCTtrueprice = Column(Float, comment=u'实际价格')


class HomeStayComment(Base):
    """公寓评论和评分"""
    __tablename__ = 'homestaycomment'
    HSCid = Column(String(64), primary_key=True)
    HSid = Column(String(64), nullable=False, comment=u'民宿id')
    USid = Column(String(64), nullable=False, comment=u'评论用户')
    USname = Column(String(16), nullable=False, comment=u'评论用户昵称')
    HSCsleeptime = Column(String(16), comment=u'入住时间')
    HSCcleanscore = Column(Float, default=5.0, comment=u'整洁卫生评分')
    HSCdescripscore = Column(Float, default=5.0, comment=u'描述相符')
    HSCimpressionscore = Column(Float, default=5.0, comment=u'房东印象评分')
    HSCtrafficscore = Column(Float, default=5.0, comment=u'交通位置评分')
    HSCperformancescore = Column(Float, default=5.0, comment=u'性价比评分')
    HStext = Column(String(255), comment=u'评论内容')

