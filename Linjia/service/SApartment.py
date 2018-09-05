# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session


class SApartment(SBase):
    @close_session
    def get_apartment_by_apid(self, apid):
        pass
