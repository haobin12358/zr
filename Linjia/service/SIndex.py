# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import IndexBanner, RoomIndexShow, ServerIndexShow


class SIndex(SBase):
    @close_session
    def get_banner_list(self):
        """获取论波图"""
        return self.session.query(IndexBanner).filter_by(IBisdelete=False).order_by(IndexBanner.IBsort).all()

    @close_session
    def get_rooms_index_show(self):
        """获取主页显示的房源
        type: 0: 合租, 1: 整租, 2: 公寓, 4: 民
        """
        return self.session.query(RoomIndexShow).order_by(RoomIndexShow.ROsort).all()

    @close_session
    def get_index_server(self):
        """获取首页的服务列表"""
        return self.session.query(ServerIndexShow).order_by(ServerIndexShow.SISsort).all()

    @close_session
    def delete_banner_show_by_ibid(self, ibid):
        """根据id删除首页的banner图"""
        return self.session.query(IndexBanner).filter_by(IBid=ibid).delete()

    @close_session
    def delete_room_show_by_risid(self, risid):
        """删首页显示的显示的房源"""
        return self.session.query(RoomIndexShow).filter_by(RISid=risid).delete()

    @close_session
    def delete_apartment_show_by_aisid(self, aisid):
        """删除首页显示的公寓"""
        return self.session.query(APartmentIndexShow).delete()

    @close_session
    def delete_homestay_show_by_hsiid(self, hsiid):
        """删除首页显示的民宿"""
        return self.session.query(HomeStayIndexShow).filter_by(HSIid=hsiid).delete()
    
    @close_session
    def delete_server_index_show(self, sisid):
        """删除首页服务显示"""
        return self.session.query(ServerIndexShow).filter_by(SISid=sisid).delete()

