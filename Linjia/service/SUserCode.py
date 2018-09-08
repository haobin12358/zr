# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import User, UserRoom, Admin, UserCode


class SUserCode(SBase):
    @close_session
    def get_usercode_by_phone_code(self, codenum, phone):
        self.session.query(UserCode).filter_by(codenum=codenum, phone=phone).first()

