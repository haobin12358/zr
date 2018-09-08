# -*- coding: utf-8 -*-
from datetime import datetime

from Linjia.commons.base_service import SBase, close_session
from Linjia.configs.timeformat import format_for_db
from Linjia.models import ProvideHouseApply


class STrade(SBase):
    @close_session
    def get_provide_appy_by_usid_village(self, usid, villege):
        """根据电话或小区查询提交记录, 防止短时间重复提交"""
        apply = self.session.query(ProvideHouseApply).\
            filter(ProvideHouseApply.USid==usid, ProvideHouseApply.PHAvillege==villege).first()
        if apply:
            last_applytime = datetime.strptime(apply.PHAcreatetime, format_for_db)
            seconds = (datetime.now() - last_applytime).total_seconds()
            if seconds < 600:
                return apply
