# -*- coding: utf-8 -*-
import math

from flask import request
from sqlalchemy import and_
from werkzeug.security import check_password_hash

from Linjia.commons.page_handler import page_handler
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import User, UserRoom, Admin, Staff


class SUser(SBase):
    @close_session
    def get_user_by_openid(self, openid):
        return self.session.query(User).filter_by(WXopenid=openid).first()

    @close_session
    def get_user_by_usid(self, usid):
        return self.session.query(User).filter_by(USid=usid).all()

    @close_session
    def get_user_by_phone(self, phone):
        return self.session.query(User).filter_by(USphone=phone).first()

    # 2018-09-12 不再使用
    @close_session
    def get_user_by_roid(self, roid):
        """获取房间的租户"""
        return self.session.query(User).join(UserRoom, User.USid==UserRoom.USid).filter_by(ROid=roid).first()

    @close_session
    def verify_admin_login(self, username, password):
        """验证管理员登录帐号和密码"""
        admin = self.session.query(Admin).filter_by(ADusername=username).first()
        if admin and check_password_hash(admin.ADpassword, password):
            return admin

    @close_session
    def get_staff_list(self, level=None, page=None, count=None, gender=None, kw=None):
        """获取工作人员列表"""
        filter_list = [Staff.STFgender == gender, Staff.STFlevel == level]
        staff_list = self.session.query(Staff).filter(and_(*filter(lambda x: hasattr(x.right, 'value'), filter_list)))
        if kw is not None:
            staff_list = staff_list.filter(Staff.STFname.contains(kw))
        page_handler(staff_list.count(), count)
        return staff_list.offset((page - 1) * page).limit(count).all()

    @close_session
    def update_staff_info(self, stfid):
        """修改工作人员"""
        return self.session.query(Staff).filter(Staff.STFid==stfid).update()







