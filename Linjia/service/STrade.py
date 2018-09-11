# -*- coding: utf-8 -*-
from datetime import datetime

from Linjia.commons.base_service import SBase, close_session
from Linjia.configs.timeformat import format_for_db
from Linjia.models import ProvideHouseApply, UserMoveTrade, UserCleanTrade, UserFixerTrade


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
            page_num = args.get('page_num')
            page_size = args.get('page_size')
            return self.session.query(UserMoveTrade).filter(UserMoveTrade.USid==usid).order_by(UserMoveTrade.UMTcreatetime.desc()).offset((page_num - 1) * page_size).limit(page_size).all()
        return self.session.query(UserMoveTrade).order_by(UserMoveTrade.UMTcreatetime.desc()).all()

    @close_session
    def get_clean_serverlist_by_usid(self, usid, args=None):
        if args:
            page_num = args.get('page_num')
            page_size = args.get('page_size')
            return self.session.query(UserCleanTrade).filter(UserCleanTrade.USid == usid).order_by(UserCleanTrade.UCTcreatetime.desc()).offset(
                (page_num - 1) * page_size).limit(page_size).all()
        return self.session.query(UserCleanTrade).order_by(UserCleanTrade.UCTcreatetime.desc()).all()

    @close_session
    def get_fixer_serverlist_by_usid(self, usid, args=None):
        if args:
            page_num = args.get('page_num')
            page_size = args.get('page_size')
            return self.session.query(UserFixerTrade).filter(UserFixerTrade.USid==usid).order_by(UserFixerTrade.UFTcreatetime.desc()).offset((page_num - 1) * page_size).limit(page_size).all()
        return self.session.query(UserFixerTrade).order_by(UserFixerTrade.UFTcreatetime.desc()).all()

