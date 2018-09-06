# -*- coding: utf-8 -*-
from Linjia.commons.base_service import SBase, close_session
from Linjia.models import IndexBanner, RoomIndexShow, APartmentIndexShow, HomeStayIndexShow, ServerIndexShow


class SIndex(SBase):
    @close_session
    def get_banner_list(self):
        """获取论波图"""
        return self.session.query(IndexBanner).filter_by(IBisdelete=False).order_by(IndexBanner.IBsort).all()

    @close_session
    def get_index_room(self, type=0):
        """获取主页显示的房源
        type: 0 合租, 1 正租
        """
        return self.session.query(RoomIndexShow).filter_by(ROtype=type).order_by(RoomIndexShow.ROsort).all()

    @close_session
    def get_index_apartment(self):
        """获取主页显示的公寓"""
        return self.session.query(APartmentIndexShow).order_by(APartmentIndexShow.AISsort).all()

    @close_session
    def get_index_homestay(self):
        """民宿"""
        return self.session.query(HomeStayIndexShow).order_by(HomeStayIndexShow.HSIsort).all()

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
