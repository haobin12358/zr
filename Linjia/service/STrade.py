# -*- coding: utf-8 -*-
import math
from datetime import datetime

from flask import request

from Linjia.commons.base_service import SBase, close_session
from Linjia.configs.timeformat import format_for_db
from Linjia.models import ProvideHouseApply, UserMoveTrade, UserCleanTrade, UserFixerTrade, UserComplaint


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

    @close_session
    def get_mover_serverlist_by_usid(self, usid, args=None):
        if args:
            mover_order_list = self.session.query(UserMoveTrade).filter(UserMoveTrade.USid==usid)
            page_num = args.get('page_num')
            page_size = args.get('page_size')
            all_count = mover_order_list.count()
            page_count = math.ceil(float(all_count) / page_size)
            request.page_count = page_count  # wf...
            request.all_count = all_count
            return mover_order_list.order_by(UserMoveTrade.UMTcreatetime.desc()).offset((page_num - 1) * page_size).limit(page_size).all()
        return self.session.query(UserMoveTrade).order_by(UserMoveTrade.UMTcreatetime.desc()).all()

    @close_session
    def get_clean_serverlist_by_usid(self, usid, args=None):
        if args:
            cleanserver_order_list = self.session.query(UserCleanTrade).filter(UserCleanTrade.USid == usid)
            page_num = args.get('page_num')
            page_size = args.get('page_size')
            all_count = cleanserver_order_list.count()
            page_count = math.ceil(float(all_count) / page_size)
            request.page_count = page_count  # wf...
            request.all_count = all_count
            return cleanserver_order_list.order_by(UserCleanTrade.UCTcreatetime.desc()).offset(
                (page_num - 1) * page_size).limit(page_size).all()
        return self.session.query(UserCleanTrade).order_by(UserCleanTrade.UCTcreatetime.desc()).all()

    @close_session
    def get_fixer_serverlist_by_usid(self, usid, args=None):
        if args:
            fixer_order_list = self.session.query(UserFixerTrade).filter(UserFixerTrade.USid==usid)
            page_num = args.get('page_num')
            page_size = args.get('page_size')
            all_count = fixer_order_list.count()
            page_count = math.ceil(float(all_count) / page_size)
            request.page_count = page_count  # wf...
            request.all_count = all_count
            return fixer_order_list.filter(UserFixerTrade.USid==usid).order_by(UserFixerTrade.UFTcreatetime.desc()).offset((page_num - 1) * page_size).limit(page_size).all()
        return self.session.query(UserFixerTrade).order_by(UserFixerTrade.UFTcreatetime.desc()).all()

    @close_session
    def get_complaint_list(self, page, count, status=None):
        """查看投诉列表"""
        all_complaint = self.session.query(UserComplaint)
        if status:
            all_complaint = all_complaint.filter(UserComplaint.UserComplaintstatus==status)
        all_count = all_complaint.count()
        request.page_count = math.ceil(float(all_count) / count)
        request.all_count = all_count
        return all_complaint.order_by(UserComplaint.UserComplaintcreatetime.desc()).offset((page - 1) * count).limit(count).all()

    @close_session
    def get_complaint_by_complaintid(self, compid):
        """根据投诉id获取投诉"""
        return self.session.query(UserComplaint).filter(UserComplaint.UserComplaintid==compid).first()

    @close_session
    def update_somplaint_by_complaintid(self, compid, status):
        """更新投诉处理状态"""
        return self.session.query(UserComplaint).filter(UserComplaint.UserComplaintid==compid).update(status)

    @close_session
    def get_provideapply_list(self, page, count, status=None, **kwargs):
        """管理员获取业主申请房源列表"""
        provide_list = self.session.query(ProvideHouseApply)
        if status:
            provide_list = provide_list.filter(ProvideHouseApply.PAHstatus==status)
        all_count = provide_list.count()
        request.page_count = math.ceil(float(all_count) / count)
        request.all_count = all_count
        return provide_list.order_by(ProvideHouseApply.PHAcreatetime).offset((page - 1) * count).limit(count).all()



