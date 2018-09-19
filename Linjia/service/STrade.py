# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import ProvideHouseApply, UserMoveTrade, UserCleanTrade, UserFixerTrade, UserComplaint


class STrade(SBase):
    @close_session
    def get_provide_appy_by_usid_village(self, usid, villege):
        """根据电话或小区查询提交记录"""
        return self.session.query(ProvideHouseApply).\
            filter(ProvideHouseApply.USid==usid, ProvideHouseApply.PHAvillege==villege).first()

    @close_session
    def get_mover_serverlist_by_usid(self, usid=None, args={}):
        page_num = args.get('page_num')
        page_size = args.get('page_size')
        return self.session.query(UserMoveTrade).filter_ignore_none_args(UserMoveTrade.USid==usid, UserMoveTrade.UMTstatus==args.get('status')).order_by(UserMoveTrade.UMTcreatetime.desc()).all_with_page(page_num, page_size)

    @close_session
    def get_mover_order_by_umtid(self, umtid):
        """id获取单个订单"""
        return self.session.query(UserMoveTrade).filter(UserMoveTrade.UMTid==umtid).first()

    @close_session
    def get_clean_serverlist_by_usid(self, usid=None, args={}):
            return self.session.query(UserCleanTrade).filter_ignore_none_args(UserCleanTrade.USid == usid, UserCleanTrade.UCTstatus==args.get('status')).order_by(UserCleanTrade.UCTcreatetime.desc()).all_with_page(args.get('page_num'), args.get('page_size'))

    @close_session
    def get_clean_order_by_uctid(self, uctid):
        """"""
        return self.session.query(UserCleanTrade).filter(UserCleanTrade.UCTid==uctid).first()

    @close_session
    def get_fixer_serverlist_by_usid(self, usid=None, args={}):
        return self.session.query(UserFixerTrade).filter_ignore_none_args(UserFixerTrade.USid == usid, UserFixerTrade.UFTstatus==args.get('status')).order_by(UserFixerTrade.UFTcreatetime.desc()).all_with_page(args.get('page_num'), args.get('page_size'))

    @close_session
    def get_fixer_order_by_uftid(self, uftid):
        return self.session.query(UserFixerTrade).filter(UserFixerTrade.UFTid == uftid).first()

    @close_session
    def get_complaint_list(self, page, count, status=None):
        """查看投诉列表"""
        all_complaint = self.session.query(UserComplaint)
        if status:
            all_complaint = all_complaint.filter(UserComplaint.UserComplaintstatus == status, UserComplaint.UserComplaintisdelete == False)
        return all_complaint.order_by(UserComplaint.UserComplaintcreatetime.desc()).all_with_page(page, count)

    @close_session
    def get_complaint_by_complaintid(self, compid):
        """根据投诉id获取投诉"""
        return self.session.query(UserComplaint).filter(UserComplaint.UserComplaintid==compid).first()

    @close_session
    def update_somplaint_by_complaintid(self, compid, data):
        """更新投诉处理状态"""
        return self.session.query(UserComplaint).filter(UserComplaint.UserComplaintid==compid, UserComplaint.UserComplaintisdelete == False).update(data)

    @close_session
    def get_provideapply_list(self, page, count, status=None, **kwargs):
        """管理员获取业主申请房源列表"""
        provide_list = self.session.query(ProvideHouseApply).filter(ProvideHouseApply.PAHisdelete==False)
        if status:
            provide_list = provide_list.filter(ProvideHouseApply.PAHstatus==status)
        return provide_list.order_by(ProvideHouseApply.PHAcreatetime.desc()).all_with_page(page, count)

    @close_session
    def updaet_provideapply(self, phaid, data):
        """更新房源申请"""
        return self.session.query(ProvideHouseApply).filter(ProvideHouseApply.PHAid == phaid, ProvideHouseApply.PAHisdelete == False).update(data)
    
    @close_session
    def update_fixertrade_status_by_utfid(self, utfid, status):
        """根据订单id更新维修服务状态"""
        return self.session.query(UserFixerTrade).filter_by(UFTid=utfid).update({
            'UFTstatus': status     
        })

    @close_session
    def update_movertrade_status_by_umtid(self, umtid, status):
        """根据订单id更改状态, 搬家"""
        return self.session.query(UserMoveTrade).filter_by(UMTid=umtid).update({
            'UMTstatus': status     
        })

    @close_session
    def update_cleanertrade_status(self, uctid, status):
        """更改保洁订单维修状态"""
        return self.session.query(UserCleanTrade).filter_by(UCTid=uctid).update({
            'UCTstatus': status     
        })

    @close_session
    def update_fixerorder_detail_by_uftid(self, uftid, data):
        """更新维修订单任意"""
        return self.session.query(UserFixerTrade).filter(UserFixerTrade.UFTid==uftid).update(data)

    @close_session
    def update_cleanorder_detail_by_uctid(self, uctid, data):
        """更新保洁订单任意"""
        return self.session.query(UserCleanTrade).filter(UserCleanTrade.UCTid==uctid).update(data)

    @close_session
    def update_movertrade_detail_by_umtid(self, umtid, data):
        """更新搬家订单任意"""
        return self.session.query(UserMoveTrade).filter(UserMoveTrade.UMTid==umtid).update(data)

