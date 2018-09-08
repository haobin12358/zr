# *- coding:utf8 *-
from sqlalchemy import Column, String, Text, Float

from Linjia.commons.base_model import Base


# 搬家
class ServerMoveMain(Base):
    """搬家服务"""
    __tablename__ = 'servermovemain'
    SMiMd = Column(String(64), primary_key=True)
    SMMtitle = Column(String(16), nullable=False, comment=u'标题, 比如搬家.')
    SMMimage = Column(String(255), nullable=False, comment=u'顶部图')


class ServersMoveSelector(Base):
    """搬家服务的规模选择"""
    __tablename__ = 'servermoveselector'
    SMSid = Column(String(64), primary_key=True)
    SMMid = Column(String(64), nullable=False, comment=u'所属服务')
    SMStitlepic = Column(String(255), nullable=False, comment=u'封面图')
    SMStitle = Column(String(16), nullable=False, comment=u'标题, 比如小搬')
    SMSsubtitle = Column(String(255), nullable=False, comment=u'标题下方, 比如一句话说明适用范围')
    SMScity = Column(String(16), comment=u'城市')  # 不同的城市有不同的服务


class ServersMoveSelectorPrice(Base):
    """搬家服务规模价格"""
    __tablename__ = 'servermoveselectorprice'
    SMSPid = Column(String(64), primary_key=True)
    SMSid = Column(String(64), nullable=False, comment=u'搬家服务规模id')
    SMSPstartprice = Column(Float, nullable=False, comment=u'起步价')
    SMSPpricestartdeadline = Column(Float, default=10.0, comment=u'起步价里程范围')
    SMSPpricesoverstartperkg = Column(Float, comment=u'超出里程的单位价格')
    SMSPfloorprice = Column(Float, comment=u'楼层费')
    SMSPpersonprice = Column(Float, comment=u'加人费')
    SMSPtitle = Column(String(16), nullable=False, comment=u'价格标题')
    SMSPsubtitle = Column(String(125), comment=u'价格简易描述')
    SSPprice = Column(Float, nullable=False, comment=u'价格')
    SMSPpriceunit = Column(String(8), comment=u'价格单位,如元/人')


class ServerMoveTips(Base):
    """小贴士"""
    __tablename__ = 'servermovetips'
    STid = Column(String(64), primary_key=True)
    STmainpic = Column(String(255), comment=u'封面图')
    STbigtext = Column(String(32), comment=u'封面文字')
    STtitle = Column(String(32), nullable=False, comment=u'标题')
    STdatatime = Column(String(16), comment=u'文章时间')
    STtags = Column(String(32), comment=u'标签')
    STtext = Column(Text, nullable=False, comment=u'正文内容')


class ServerMoveComment(Base):
    """服务评价"""
    __tablename__ = 'servermovecomment'
    SMCid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment=u'评论用户')
    USheader = Column(String(255), comment=u'用户头像')
    USname = Column(String(8), comment=u'用户昵称')
    SMCcreatetime = Column(String(16), nullable=False, comment=u'评价时间')
    STFid = Column(String(64), nullable=False, comment=u'公司服务员工id')
    STFtitle = Column(String(8), default=u'搬家师傅', comment=u'服务员工称号,如:搬家师傅')
    STFname = Column(String(16), nullable=False, comment=u'服务员工姓名')
    # todo 评论标签


# 清洁
class ServerCleanMain(Base):
    """清洁服务"""
    __tablename__ = 'servercleanmain'
    SCMid = Column(String(64), primary_key=True)
    SCMtitle = Column(String(16), nullable=False, comment=u'标题, 比如清洁.')
    SCMimage = Column(String(255), nullable=False, comment=u'顶部图')


class ServerCleanSelector(Base):
    """清洁服务的规模选择"""
    __tablename__ = 'servercleanselector'
    SCEid = Column(String(64), primary_key=True)
    SCMid = Column(String(64), nullable=False, comment=u'所属服务')
    SCMtitlepic = Column(String(255), nullable=False, comment=u'封面图')
    SCMtitle = Column(String(16), nullable=False, comment=u'标题, 比如日常保洁')
    SCMsubtitle = Column(String(255), nullable=False, comment=u'标题下方, 比如一句话说明适用范围')
    SCMcity = Column(String(16), comment=u'城市')  # 不同的城市有不同的服务


class ServersCleanSelectorPrice(Base):
    """清洁服务规模价格"""
    __tablename__ = 'serverselectorprice'
    SCSPid = Column(String(64), primary_key=True)
    SCSid = Column(String(64), nullable=False, comment=u'清洁服务规模id')
    SCSPtitle = Column(String(16), nullable=False, comment=u'价格标题')
    SCSPsubtitle = Column(String(125), comment=u'价格简易描述')
    SCSPprice = Column(Float, nullable=False, comment=u'价格')
    SCSPpriceunit = Column(String(8), comment=u'价格单位,如元/人')


class ServerCleanTips(Base):
    """小贴士"""
    __tablename__ = 'servertips'
    STid = Column(String(64), primary_key=True)
    SCTmainpic = Column(String(255), comment=u'封面图')
    SCTbigtext = Column(String(32), comment=u'封面文字')
    SCTtitle = Column(String(32), nullable=False, comment=u'标题')
    SCTdatatime = Column(String(16), comment=u'文章时间')
    SCTtags = Column(String(32), comment=u'标签')
    SCTtext = Column(Text, nullable=False, comment=u'正文内容')


class ServerCleanComment(Base):
    """服务评价"""
    __tablename__ = 'servermaincomment'
    SCCid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment=u'评论用户')
    USheader = Column(String(255), comment=u'用户头像')
    USname = Column(String(8), comment=u'用户昵称')
    SCCcreatetime = Column(String(16), nullable=False, comment=u'评价时间')
    STFid = Column(String(64), nullable=False, comment=u'公司服务员工id')  # STF(staff)
    STFtitle = Column(String(8), default=u'保洁人员', comment=u'服务员工称号,如:搬家师傅')
    STFname = Column(String(16), nullable=False, comment=u'服务员工姓名')
    # todo 评论标签


# 维修 todo )

if __name__ == '__main__':
    obj = globals()
    filte_obj = list(filter(lambda x: x[0].isupper(), obj))
    print(filte_obj)