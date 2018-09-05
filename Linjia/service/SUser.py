# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import User, UserRoom


class SUser(SBase):
    @close_session
    def get_user_by_openid(self, openid):
        return self.session.query(User).filter_by(WXopenid=openid).first()

    @close_session
    def get_user_by_usid(self, usid):
        return self.session.query(User).filter_by(USid=usid).all()

    @close_session
    def get_user_by_roid(self, roid):
        """获取房间的租户"""
        return self.session.query(User).join(UserRoom, User.USid==UserRoom.USid).filter_by(ROid=roid).first()
        # return self.session.query(UserRoom).filter_by(ROid=roid).first()

