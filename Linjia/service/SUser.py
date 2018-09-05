# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import User


class SUser(SBase):
    @close_session
    def get_user_by_openid(self, openid):
        return self.session.query(User).filter_by(WXopenid=openid).first()

    @close_session
    def get_user_by_usid(self, usid):
        return self.session.query(User).filter_by(USid=usid)

