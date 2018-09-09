# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import ServersMoveSelector, ServersMoveSelectorPrice


class SServer(SBase):
    @close_session
    def get_mover_serverlist(self):
        """获取搬家服务列表信息"""
        return self.session.query(ServersMoveSelector).filter_by(SMstatus=0).all()

    @close_session
    def get_mover_serverlist(self, city_id):
        """根据城市获取搬家服务列表"""
        return self.session.query(ServersMoveSelector, )

    @close_session
    def get_mover_serverlistby_city_id(self, cityid):
        """根据城市获取搬家服务列表信息"""
        return self.session.query(ServersMoveSelector).filter_by(SMScity=cityid).all()

    @close_session
    def get_mover_price_by_smsid(self, smsid):
        """获取搬家服务的价格详情"""
        return self.session.query(ServersMoveSelectorPrice).filter_by(SMSid=smsid).first()
