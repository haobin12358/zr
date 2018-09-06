# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import Apartment


class SApartment(SBase):
    @close_session
    def get_apartment_by_apid(self, apid):
        return self.session.query(Apartment).filter_by(APid=apid).first()
