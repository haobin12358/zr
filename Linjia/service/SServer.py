# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import ServersMoveSelector, ServersMoveSelectorPrice, UserMoveTrade


class SServer(SBase):
    @close_session
    def get_mover_serverlist(self):
        """获取搬家服务列表信息"""
        return self.session.query(ServersMoveSelector).filter_by(SMstatus=0).all()

    @close_session
    def get_mover_serverlistby_city_id(self, cityid):
        """根据城市获取搬家服务列表信息"""
        return self.session.query(ServersMoveSelector).filter_by(SMScity=cityid).all()

    @close_session
    def get_mover_serverlist_by_usid(self, usid, args):
        page_num = args.get('page_num')
        page_size = args.get('page_size')
        return self.session.query(UserMoveTrade).filter(UserMoveTrade.USid==usid).offset((page_num - 1) * page_size).limit(page_size).all()

    @close_session
    def get_mover_by_smsid(self, smsid):
        return self.session.query(ServersMoveSelector).filter(ServersMoveSelector.SMSid==smsid).first()

    @close_session
    def get_mover_price_by_smsid(self, smsid):
        """获取搬家服务的价格详情"""
        return self.session.query(ServersMoveSelectorPrice).filter_by(SMSid=smsid).first()
