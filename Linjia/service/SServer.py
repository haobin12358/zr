# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import ServersMoveSelector, ServersMoveSelectorPrice, UserMoveTrade, ServerCleanSelector, \
    UserCleanTrade


class SServer(SBase):
    @close_session
    def get_mover_serverlist(self):
        """获取搬家服务列表信息"""
        return self.session.query(ServersMoveSelector).filter_by(SMStatus=0).order_by(ServersMoveSelector.SMSshowprice).all()

    @close_session
    def update_mover_server(self, smsid, data):
        """更新搬家服务选项"""
        return self.session.query(ServersMoveSelector).filter(ServersMoveSelector.SMSid == smsid).update(data)

    @close_session
    def get_mover_serverlistby_city_id(self, cityid):
        """根据城市获取搬家服务列表信息"""
        return self.session.query(ServersMoveSelector).filter_by(SMScity=cityid).order_by(ServersMoveSelector.SMSshowprice).all()

    @close_session
    def get_mover_by_smsid(self, smsid):
        return self.session.query(ServersMoveSelector).filter(ServersMoveSelector.SMSid==smsid).first()

    @close_session
    def get_mover_price_by_smsid(self, smsid):
        """获取搬家服务的价格详情"""
        return self.session.query(ServersMoveSelectorPrice).filter_by(SMSid=smsid).first()

    @close_session
    def get_clearerserver_list(self):
        """获取清洁服务列表"""
        return self.session.query(ServerCleanSelector).filter(ServerCleanSelector.SCMstatus==0).order_by(ServerCleanSelector.SCprice).all()

    @close_session
    def get_cleanerserver_by_sceid(self, sceid):
        """根据id获取清洁服务"""
        return self.session.query(ServerCleanSelector).filter(ServerCleanSelector.SCEid==sceid).first()

    @close_session
    def update_cleanserver(self, sceid, data):
        """更新保洁服务"""
        return self.session.query(ServerCleanSelector).filter(ServerCleanSelector.SCEid==sceid).update(data)

