# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import HomeStay


class SHomeStay(SBase):
    @close_session
    def get_homestay_by_hsid(self, hsid):
        return self.session.query(HomeStay).filter_by(HSid=hsid).first()
