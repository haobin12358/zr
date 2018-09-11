# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, orm


from Linjia.commons.base_model import Base


class Room(Base):
    """房源(合租/整租/公寓/民宿)"""
    __tablename__ = 'room'
    ROid = Column(String(64), primary_key=True)
    HOid = Column(String(64), comment=u'所属房子id')
    ROname = Column(String(64), nullable=False, comment=u'名字')  # 标题: 自如友家·建明里小区·3居室-01卧, 在添加的时候可以后台生成, 也可以自定义
    ROimage = Column(String(255), comment=u'主图')
    ROarea = Column(Float, nullable=False, comment=u'面积')
    ROface = Column(Integer, default=u'未知', comment=u'朝向{1-8分别代表东,东南,南,西南...')
    ROdistance = Column(String(32), comment=u'交通设施距离描述')
    # ROshowpricetype = Column(Integer, default=1, comment=u'显示价格标准 0: 月付, 1 季付, 2 半年付, 3 年付')  # 根据这个标准去价格表中查价格
    ROshowprice = Column(Float, comment=u'显示价格')
    ROshowpriceunit = Column(String(64), default=u'month', comment=u'价格单位,month,night')
    ROrenttype = Column(Integer, default=0, comment=u'租赁方式, 0: 合租, 1: 整租, 2: 公寓, 3: 民宿')
    ROdecorationstyle = Column(Integer, default=2, comment=u'装修风格, 0: 毛坯, 1: 简装, 2: 精装, 3: 豪华')
    ROnum = Column(Integer, comment=u'卧室号')  # 合租才有值
    ROstatus = Column(Integer, default=0, comment=u'房源状态, 0: 待审核, 1: 配置中(可预订), 2: 可入住, 3: 转租, 4: 实习, 5, 已租出')
    ROisdelete = Column(Boolean, default=False, comment=u'是否删除')
    ROcreatetime = Column(String(16), comment=u'创建时间')
    ROshowtime = Column(String(16), comment=u'发布时间')
    ROcitynum = Column(String(64), comment=u'城市编号, 冗余字段')
    ROareanum = Column(String(64), comment=u'区编号')
    ROsubwayaround = Column(Boolean, default=False, comment=u'地铁附近')
    ROaroundequirment = Column(Text, comment=u'周边设施介绍')
    # 类型为民宿的时候需要用到的字段
    ROentertime  = Column(String(16), comment=u'入住时间')  # 入住时间
    ROleavetime = Column(String(16), comment=u'离开时间')  # 离开时间


class House(Base):
    """房子信息"""
    __tablename__ = 'house'
    HOid = Column(String(64), primary_key=True)
    HOfloor = Column(Integer, comment=u'所在楼层')
    HOtotalfloor = Column(Integer, comment=u'总楼层')
    HObedroomcount = Column(Integer, default=1, comment=u'卧室数目')
    HOparlorcount = Column(Integer, default=1, comment=u'客厅数量')
    VIid = Column(String(64), comment=u'小区id')


class RoomTag(Base):
    """列表页显示的tag"""
    __tablename__ = 'roomtag'
    RTid = Column(String(64), primary_key=True)
    ROid = Column(String(64), nullable=False)
    RTname = Column(String(16), nullable=False, comment=u'tag文字')
    RTsort = Column(Integer, comment=u'tag顺序')


class RoomMedia(Base):
    """房源展示多媒体(图片或视频)"""
    __tablename__ = 'roomimage'
    REid = Column(String(61), primary_key=True)
    ROid = Column(String(64), nullable=False, comment=u'房源id')
    REpic = Column(String(255), nullable=False, comment=u'图片链接')
    REtype = Column(String(8), default=u'image', comment=u'展示类型, image, video')
    RIsort = Column(Integer, comment=u'显示顺序标志')


class RoomEquirment(Base):
    """房间的设备信息"""
    __tablename__ = 'roomrequirment'
    REid = Column(String(64), primary_key=True)
    ROid = Column(String(64), comment=u'房源id')
    # IConid = Column(String(64), comment=u'ico图标的id')
    # IContext = Column(String(64), comment=u'自定义的文字')  # 可以为空
    # IConsort = Column(Integer, comment=u'顺序标志')
    Clothesbox = Column(Boolean, default=False, comment=u'衣柜')
    Wifi = Column(Boolean, default=False)
    Washer = Column(Boolean, default=False, comment=u'洗衣机')
    Freezebox = Column(Boolean, default=False, comment=u'冰箱')
    TV = Column(Boolean, default=False)
    Aircondition = Column(Boolean, default=False, comment=u'空调')
    Heatwatter = Column(Boolean, default=False, comment=u'热水器')
    Desk = Column(Boolean, default=False, comment=u'桌椅')
    Shotbox = Column(Boolean, default=False, comment=u'鞋柜')


class RoomSignInfo(Base):
    """租房签约规定"""
    __tablename__ = 'roomsigninfo'
    RSIid = Column(String(64), primary_key=True)
    ROid = Column(String(64), nullable=False, comment=u'房源id')
    PSIsigntype = Column(Integer, default=0, comment=u'签约时长类型 0: 短租, 1: 年租')
    RSIshortest = Column(Integer, default=90, comment=u'最少租期')
    RSIlongest = Column(Integer, default=180, comment=u'最长租期')
    RSIdeadline = Column(String(16), comment=u'可签约至')
    RSIshow = Column(Boolean, default=False, comment=u'是否显示')


class Villege(Base):
    """小区"""
    __tablename__ = 'villege'
    VIid = Column(String(64), primary_key=True)
    VIyears = Column(String(4), comment=u'建筑年代')
    VItype = Column(String(8), comment=u'建筑类型')
    VIdesc = Column(String(255), comment=u'小区介绍')
    VIgreen = Column(Float, comment=u'绿化率')
    VIviolumetric = Column(Float, comment=u'容积率')
    VIcarrate = Column(Float, comment=u'车位配比')
    VIisclose = Column(Boolean, comment=u'是否封闭')
    VIcarpay = Column(Float, comment=u'停车费')
    VIcompany = Column(String(16), comment=u'物业公司')
    VIphone = Column(String(16), comment=u'物业电话')
    VILatitude = Column(Float, comment=u'纬度')
    VIlongitude = Column(Float, comment=u'经度')
    VIcitynum = Column(String(64), comment=u'城市编号')
    VIlocationnum = Column(String(64), comment=u'区域编号')  # todo 区域编号

# 代定
class SubwayStationInfo(Base):
    """地铁距离信息"""
    __tablename__ = 'subwaystationinfo'
    SSIid = Column(String(64), primary_key=True)
    VIid = Column(String(64), comment=u'小区id')
    # todo subway


class HomeStayReserve(Base):
    """预约须知"""
    __tablename__ = 'homestayreserve'
    HSRid = Column(String(64), primary_key=True)
    HSid = Column(String(64), nullable=False, comment=u'民宿id')
    HSRtype = Column(Integer, default=0, comment=u'预定类型: 0: 申请预定, 1:?')
    HSRdesposit = Column(String(16), comment=u'押金规则')
    HSRshortestliving = Column(Float, default=1, comment=u'最少入住天数')
    HSRcleanprice = Column(Float, default=0, comment=u'清洁费')
    HSRstartliveingtime = Column(String(16), comment=u'入住时间')
    HSRleavingtime = Column(String(16), default=u'12点之前', comment=u'退房时间')
    HSRservice = Column(String(32), comment=u'服务, 如可做饭')


class Icon(Base):
    __tablename__ = 'ico'
    IConid = Column(String(64), primary_key=True)
    IConurl = Column(String(255), nullable=False)
    IConame = Column(String(16), nullable=False)

class Question(Base):
    """问题"""
    __tablename__ = 'question'
    QUid = Column(String(64), primary_key=True)
    QUtitle = Column(String(255), nullable=False, comment=u'问题')
    QUanswer = Column(Text, nullable=False, comment=u'回答')
    QUisshow = Column(Boolean, default=True, comment=u'是否显示')
    QUsort = Column(Integer, comment=u'顺序标志')


class JoinRoomBanner(Base):
    """有家轮播图"""
    __tablename__ = 'joinroombanner'
    JRBid = Column(String(64), primary_key=True)
    JRBimage = Column(String(255), nullable=False)
    JRBsort = Column(Integer, comment=u'顺序标志')


if __name__ == '__main__':
    obj = globals()
    filte_obj = list(filter(lambda x: x[0].isupper(), obj))
    print(filte_obj)
