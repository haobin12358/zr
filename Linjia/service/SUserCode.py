# -*- coding: utf-8 -*-
from collections import namedtuple
from datetime import datetime

from Linjia.commons.base_service import SBase, close_session
from Linjia.configs.timeformat import format_for_db
from Linjia.models import User, UserRoom, Admin, UserCode


class SUserCode(SBase):
    @close_session
    def get_usercode_by_phone_code(self, codenum, phone):
        """通过手机和验证码获取记录"""
        return self.session.query(UserCode).filter_by(Codenum=codenum, Phone=phone).order_by(UserCode.Createtime.desc()).first()

    @close_session
    def get_active_usercode_by_phone_code(self, phone, codenum):
        """获取十分钟以内的有效验证码记录
        万能验证码, 123456"""
        code = self.session.query(UserCode).filter_by(Codenum=codenum, Phone=phone).order_by(UserCode.Createtime.desc()).first()
        if code:
            code_time = datetime.strptime(code.Createtime, format_for_db)
            seconds = (datetime.now() - code_time).total_seconds()
            if seconds < 600:
                return code
        elif codenum == 123456:
            Code = namedtuple('Code', ['Phone'])
            res = Code(phone)
            return res
