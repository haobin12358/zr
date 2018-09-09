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
    def delete_room_show_by_roid(self, roid):
        """根据roid删除首页显示的房源"""
        return self.session.query(RoomIndexShow).filter(RoomIndexShow.ROid==roid).delete()

    @close_session
    def delete_server_index_show(self, sisid):
        """删除首页服务显示"""
        return self.session.query(ServerIndexShow).filter_by(SISid=sisid).delete()

    @close_session
    def is_room_showinindex_by_roid(self, roid):
        """判断是否在首页显示"""
        show = self.session.query(RoomIndexShow).filter_by(ROid=roid).first()
        return True if show else False