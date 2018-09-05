# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, orm


from Linjia.commons.base_model import Base


class Room(Base):
    """房源(合租/整租)"""
    __tablename__ = 'room'
    ROid = Column(String(64), primary_key=True)
    HOid = Column(String(64), comment=u'所属房子id')
    ROname = Column(String(64), nullable=False, comment=u'名字')  # 标题: 自如友家·建明里小区·3居室-01卧, 在添加的时候可以后台生成, 也可以自定义
    ROimage = Column(String(255), comment=u'主图')
    ROarea = Column(Float, nullable=False, comment=u'面积')
    ROface = Column(Integer, default=u'未知', comment=u'朝向{1-8分别代表东,东南,南,西南...')
    ROdistance = Column(String(32), comment=u'交通设施距离描述')
    ROshowpricetype = Column(Integer, default=1, comment=u'显示价格标准 0: 月付, 1 季付, 2 半年付, 3 年付')  # 根据这个标准去价格表中查价格
    ROshowpriceunit = Column(String(2), default=u'月', comment=u'显示价格单位')
    ROshowprice = Column(Float, comment=u'显示价格')
    ROrenttype = Column(Integer, default=0, comment=u'房源类型, 0: 合租, 1: 整租, 2: 精选, 3: 豪宅')
    ROsubwayaround = Column(Boolean, default=False, comment=u'离地铁近')   # 冗余
    ROnum = Column(Integer, comment=u'卧室号')  # 合租才有值
    ROpersoncount = Column(Integer, comment=u'可居几人, x居室')
    ROintro = Column(String(64), comment=u'房源介绍')
    ROstatus = Column(Integer, default=0, comment=u'房源状态, 0: 待审核, 1: 配置中(可预订), 2: 可入住, 3: 转租, 4: 实习, 5, 已租出')
    ROisdelete = Column(Boolean, default=False, comment=u'是否删除')
    ROcreatetime = Column(String(16), comment=u'创建时间')
    ROcitynum = Column(String(64), comment=u'城市编号, 冗余字段')

    @orm.reconstructor
    def __init__(self):
        self.fields = '__all__'


class House(Base):
    """房子信息"""
    __tablename__ = 'house'
    HOid = Column(String(64), primary_key=True)
    HOfloor = Column(Integer, comment=u'所在楼层')
    HOtotalfloor = Column(Integer, comment=u'总楼层')
    HObedroomcount = Column(Integer, default=1, comment=u'卧室数目')
    HOparlorcount = Column(Integer, default=1, comment=u'客厅数量')
    VIid = Column(String(64), comment=u'小区id')

    @orm.reconstructor
    def __init__(self):
        self.fields = '__all__'


class RoomFeature(Base):
    """房源特色"""
    __tablename__ = 'roomfeature'
    RFid = Column(String(64), primary_key=True)
    ROid = Column(String(64), nullable=False, comment=u'房源id')
    RFbalcony = Column(Boolean, default=False, comment=u'独立阳台')
    RFhytingtype = Column(Integer, nullable=False, comment=u'供暖方式 0 不供暖 1 集体 2独立 3 中央')
    RFfirstrent = Column(Boolean, nullable=False, comment=u'首次出租')
    RFtwotoilet = Column(Boolean, default=False, comment=u'两个卫生间')
    RFcanpet = Column(Boolean, default=False, comment=u'可养宠物')
    RFlock = Column(Boolean, default=False, comment=u'智能锁')
    RFelevator = Column(Boolean, default=False, comment=u'有电梯')
    RFtimeservice = Column(Boolean, default=False, comment=u'及时维修')
    RFwifi = Column(Boolean, default=False, comment=u'wifi覆盖')
    RFmonthclean = Column(Integer, default=1, comment=u'月度清洁次数')
    RFstyle = Column(String(8), comment=u'装修风格')  # 比如友家2.0 { }
    RFhotfeaturelist = Column(String(32), comment=u'详情显示标红的特色')

    @orm.reconstructor
    def __init__(self):
        self.fields = '__all__'


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


class HouseSubsidiaryInfo(Base):
    """房源配套信息, 图片显示在详情页上方, 朝向等信息显示在详情页户型配套中"""
    __tablename__ = 'roomsubsidiaryinfo'
    HSIid = Column(String(64), primary_key=True)
    HOid = Column(String(64), comment=u'房信息id')
    HSIname = Column(String(64), comment=u'名字, 比如起居室')  # 比如:户型, 公共卫生间, 起居室, 厨房...
    HSIarea = Column(Float, nullable=False, comment=u'面积')
    RSIface = Column(String(2), nullable=False, comment=u'朝向')
    HSIimage = Column(String(255), nullable=False, comment=u'图片')  #
    HRIsort = Column(Integer, comment=u'显示顺序标志')


class HouseSubsidiaryEquirment(Base):
    """配套中的设备信息"""
    __tablename__ = 'housesubsidiaryquirment'
    HSEid = Column(String(64), primary_key=True)
    HSIid = Column(String(64), comment=u'')
    HSEsn = Column(String(32), comment=u'设备编号')  # 有一个icon与之对应
    HSEname = Column(String(8), comment=u'设备名称') # 为空则显示默认
    HSEsort = Column(Integer, comment=u'顺序标志')


class RoomEquirment(Base):
    """房间的设备信息, 当房间为合租的时候会对应此表"""
    __tablename__ = 'roomrequirment'
    REid = Column(String(64), primary_key=True)
    ROid = Column(String(64), comment=u'房间id')
    REsn = Column(String(32), comment=u'设备编号')  # 有一个icon与之对应
    REname = Column(String(8), comment=u'设备名称') # 为空则显示默认
    REsort = Column(Integer, comment=u'顺序标志')


class RoomIndexShow(Base):
    """首页展示中的房源(整租/合租)列表"""
    __tablename__ = 'roomindexshow'
    RISid = Column(String(64), primary_key=True)
    ROid = Column(String(64), nullable=False, comment=u'房源id')
    ROtype = Column(Integer, comment=u'显示位置 0: 合租, 1: 整租')
    ROsort = Column(Integer, comment=u'位置标志')


class RoomPayPrice(Base):
    """价格信息"""
    __tablename__ = 'roomprice'
    RPPid = Column(String(64), primary_key=True)
    ROid = Column(String(64), nullable=False, comment=u'房间id')
    RPPperiod = Column(Integer, default=0, comment=u'付费周期')  # (0, 月付), (1, 季付), (2, 半年), (3, 一年), (4, 自如客分期)
    RPPdeposit = Column(Float, nullable=False, comment=u'押金')
    RPPservice = Column(Float, nullable=False, comment=u'服务费')
    RPPserviceUnit = Column(String(8), default=u'元/年', comment=u'服务费价格单位')
    RPPprice = Column(Float, nullable=False, comment=u'价格')
    RPPpriceUnit = Column(String(8), default=u'元/月', comment=u'房租价格单位')
    RPPstageurl = Column(String(125), comment=u'分期网址')  # 分期网址, 可以为空

    @orm.reconstructor
    def __init__(self):
        self.fields = '__all__'


class RoomTag(Base):
    """详情页显示的其他tag"""
    __tablename__ = 'roomtag'
    RTid = Column(String(64), primary_key=True)
    ROid = Column(String(64), nullable=False, comment=u'房源id')
    RTname = Column(String(8), nullable=False, comment=u'tag文字')
    RTsort = Column(Integer, comment=u'顺序标志')


class SubwayStationInfo(Base):
    """地铁距离信息"""
    __tablename__ = 'subwaystationinfo'
    SSIid = Column(String(64), primary_key=True)
    VIid = Column(String(64), comment=u'小区id')
    # todo subway


# 公寓
class Apartment(Base):
    """公寓"""
    __tablename__ = 'apartment'
    APid = Column(String(64), primary_key=True)
    APname = Column(String(32), nullable=False, comment=u'公寓名')
    APaddr = Column(String(32), nullable=False, comment=u'公寓地址')
    APcity = Column(String(64), nullable=False, comment=u'城市编号')
    APheadpic = Column(String(125), nullable=False, comment=u'主图')
    APopeningtime = Column(String(16), comment=u'开放时间')
    APhousenum = Column(Integer, comment=u'房间数')
    APhousetypenum = Column(Integer, comment=u"房型数")
    APminprice = Column(Float, comment=u'最低价')
    APmaxprice = Column(Float, comment=u'最高价')
    APlatitude = Column(Float, comment=u'纬度')
    APlongtitude = Column(Float, comment=u'经度')
    APprojectinfo = Column(Text, comment=u'项目简介')
    APstatus = Column(Integer, default=1, comment=u'开放状态 0: 未开放, 1 已开放')


class ApartmentPic(Base):
    """公寓图片"""
    __tablename__ = 'apartmentpic'
    APicid = Column(String(64), primary_key=True)
    APicname = Column(String(8), nullable=False, comment=u'图片名字')
    APicurl = Column(String(255), nullable=False, comment=u'图片链接')
    APicsort = Column(Integer, comment=u'顺序标志')


class ApartmentRoom(Base):
    """公寓房间"""
    __tablename__ = 'apartmentroom'
    ARid = Column(String(64), primary_key=True)
    APid = Column(String(64), comment=u'公寓id')
    ARtype = Column(String(64), comment=u'房型')
    ARstatus = Column(Integer, comment=u'在租状态 1. 可预约 2. 已租出')
    ARarea = Column(Float, comment=u'面积')


class ApartmentFeature(Base):
    """公寓特色, tag标签"""
    __tablename__ = 'apartmentfeature'
    AFid = Column(String(64), primary_key=True)
    APid = Column(String(64), nullable=False, comment=u'公寓id')
    AFname = Column(String(16), nullable=False, comment=u'特色名字')
    AFtipcolor = Column(String(8), default='gold', comment=u'特色显示颜色')
    AFsort = Column(String(16), comment=u'顺序标志')
    AFshow = Column(Boolean, default=True, comment=u'是否显示')


class ApartmentAquirment(Base):
    """公寓公共设备"""
    __tablename__ = 'apartmentaquirment'
    AAid = Column(String(64), primary_key=True)
    APid = Column(String(64), nullable=False, comment=u'公寓id')
    AAsn = Column(Integer, comment=u'配套设备编号')
    AAname = Column(String(8), comment=u'配套设备显示文字')  # 为空则显示默认
    AAsort = Column(Integer, comment=u'顺序标志')


class APartmentIndexShow(Base):
    """公寓首页显示"""
    __tablename__ = 'apartmentindexshow'
    AISid = Column(String(64), primary_key=True)
    APid = Column(String(64), nullable=False, comment=u'公寓id')
    AISsort = Column(Integer, comment=u'顺序标志')


# 民宿
class HomeStay(Base):
    """民宿"""
    __tablename__ = 'homestay'
    HSid = Column(String(64), primary_key=True)
    HSname = Column(String(16), nullable=False, comment=u'名字')
    HScitynum = Column(String(16), comment=u'城市编号')
    Hsrentwayname = Column(String(16), default=u'独立房间', comment=u'出租方式')
    HSpersoncount = Column(Integer, default=2, comment=u'可住人数')
    HSroomcount = Column(Integer, comment=u'房间数')
    HStoiletCount = Column(Integer, default=1, comment=u'卫生间数量')
    HSbalconyCount = Column(Integer, default=0, comment=u'阳台数量')
    HSarea = Column(Float, nullable=False, comment=u'面积')
    USid = Column(String(16), comment=u'房东id')
    HSprice = Column(Float, comment=u'显示价格')
    HSoriginnalprice = Column(Float, comment=u'原价')
    HSpriceunit = Column(String(4), default=u'元/晚', comment=u'价格单位')
    HSaddress = Column(String(64), comment=u'一句话地址')
    HSevaluateScore = Column(Float, comment=u'自定义评分')
    HSrule = Column(Text, comment=u'房屋守则')
    HScircle = Column(Text, comment=u'周边情况')
    HSdesc = Column(Text, comment=u'房源描述')
    HSlongitude = Column(Float, comment=u'经度')
    HSlantitude = Column(Float, comment=u'纬度')
    HSstatus = Column(Integer, default=1, comment=u'状态 0: 不可用, 1: 正常')


class HomeStayBed(Base):
    """床"""
    __tablename__ = 'homestaybed'
    HSBid = Column(String(64), primary_key=True)
    HSid = Column(String(64), nullable=False, comment=u'民宿id')
    HSBnum = Column(Integer, default=1, comment=u'床数量')
    HSBname = Column(Integer, comment=u'床名字, 如: 双人床')
    HSBtype = Column(Integer, default=2, comment=u'床类型: 1: 单人床, 2: 双人床')


class HomeStayComment(Base):
    """评论和评分"""
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


class HomeStayPic(Base):
    __tablename__ = 'homestaypic'
    HSid = Column(String(64), primary_key=True)
    HSpicture = Column(String(255), nullable=False, comment=u'图片')
    HSPsort = Column(Integer, comment=u'顺序标志')
    HSPiamain = Column(Boolean, default=False, comment=u'是否主图')


class HomeStayAquirment(Base):
    """配套设施"""
    __tablename__ = 'homestayaquirment'
    HSAid = Column(String(64), primary_key=True)
    HSid = Column(String(64), nullable=False, comment=u'民宿id')
    HSAnums = Column(String(8), nullable=False, comment=u'设备编号')  # 会有一个默认名称和ico图标与之对应
    HSAname = Column(String(16), comment=u'设备名, 为空则显示默认')
    HSAsort = Column(Integer, comment=u'顺序标志')
    HScolor = Column(String(16), comment=u'图标特殊状态')


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


class Question(Base):
    """问题"""
    __tablename__ = 'question'
    QUid = Column(String(64), primary_key=True)
    QUtitle = Column(String(255), nullable=False, comment=u'问题')
    QUanswer = Column(Text, nullable=False, comment=u'回答')
    QUisshow = Column(Boolean, default=True, comment=u'是否显示')
    QUsort = Column(Integer, comment=u'顺序标志')



if __name__ == '__main__':
    obj = globals()
    filte_obj = list(filter(lambda x: x[0].isupper(), obj))
    print(filte_obj)