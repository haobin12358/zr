# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, Boolean

from Linjia.commons.base_model import Base


class User(Base):
    """用户(业主或租客)"""
    __tablename__ = 'user'
    USid = Column(String(64), primary_key=True)
    USnickname = Column(String(16), nullable=False, comment=u'用户昵称')
    USphone = Column(String(12), comment=u'用户手机号')
    USpassword = Column(String(255), comment=u'密码')
    USgender = Column(Integer, comment=u'性别, 0: 男, 1: 女')
    USheader = Column(String(125), comment=u'头像')
    USemail = Column(String(64), comment=u'用户邮箱')
    UShobby = Column(String(64), comment=u'用户爱好')
    USstar = Column(String(8), comment=u'星座')
    USaddr = Column(String(125), comment=u'地址')
    USisdelete = Column(Boolean, default=False, comment=u'是否删除')
    WXopenid = Column(String(125), comment=u'微信openid')
    WXnickname = Column(String(32), comment=u'微信用户名')
    WXprovice = Column(String(16), comment=u'微信')
    WXheader = Column(String(125), comment=u'微信头像')
    WXprivilege = Column(String(125), comment=u'微信用户特权信息, 比如微信沃卡用户为（chinaunicom）')


class UserSecurity(Base):
    """用户身份信息"""
    __tablename__ = 'usersecurity'
    Securityid = Column(String(64), primary_key=True)
    USid = Column(String(64), comment=u'用户id')
    Securitytype = Column(String(8), nullable=False, comment=u'证件类型')
    Securitynum = Column(String(64), nullable=False, comment=u'证件号码')


class UserSecurityPic(Base):
    """证件照"""
    __tablename__ = 'usersecuritypic'
    USPid = Column(String(64), primary_key=True)
    Securityid = Column(String(64), nullable=False, comment=u'UserSecurityid')
    USPpic = Column(String(125), nullable=False, comment=u'图片路径')
    USPtype = Column(Integer, nullable=False, comment=u'图片类型0: 正面, 1 反面, 2 手持')


class Admin(Base):
    """管理员"""
    __tablename__ = 'admin'
    ADid = Column(String(64), primary_key=True)
    ADname = Column(String(16), nullable=False, comment=u'姓名')
    ADusername = Column(String(16), nullable=False, comment=u'登录名')
    ADpassword = Column(String(255), nullable=False, comment=u'登录密码')
    ADheader = Column(String(255), comment=u'头像')
    ADlevel = Column(Integer, default=0, comment=u'用户等级 0: 普通管理员, 1 高级管理员, 2 超管')
    ADmobiel = Column(String(16), comment=u'手机')
    ADphone = Column(String(16), comment=u'电话')
    ADaddress = Column(String(16), comment=u'地址')
    ADdesc = Column(Text, comment=u'个人简述')
    ADisfreeze = Column(Boolean, default=False, comment=u'是否被冻结')


class Staff(Base):
    """公司员工"""
    __tablename__ = 'staff'
    STFid = Column(String(64), primary_key=True)
    STFmobiel = Column(String(16), comment=u'手机')
    STFphone = Column(String(16), comment=u'电话')
    STFaddress = Column(String(16), comment=u'地址')
    STFgender = Column(Integer, comment=u'性别, 0 男, 1 女')
    STFlevel = Column(Integer, default=0, comment=u'员工类型, 0 管家, 1 搬家工, 2清洁工, 3维修')
    ADaddressnum = Column(String(16), comment=u'负责区域编号')
    APid = Column(String(64), comment=u'单独负责某个公寓')  # 不存在则为空
    ADdesc = Column(Text, comment=u'个人简述')


# 以下可能会需要
class ZOStaff(Base):
    """管家"""
    __tablename__ = 'zostaff'
    ZOSid = Column(String(64), primary_key=True)


# 其他信息
class MoverStaff(Base):
    """搬家工"""
    __tablename__ = 'moverstaff'
    MSid = Column(String(64), primary_key=True)


class ClearnerStaff(Base):
    """清洁工"""
    __tablename__ = 'clearnerstaff'
    CSid = Column(String(64), primary_key=True)


class FixerStaff(Base):
    """修理工"""
    __tablename__ = 'fixerstaff'
    FSid = Column(String(64), primary_key=True)


if __name__ == '__main__':
    pass
