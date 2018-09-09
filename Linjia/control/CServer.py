# -*- coding: utf-8 -*-
from Linjia.commons.success_response import Success
from Linjia.service import SServer, SCity


class CServer(object):
    def __init__(self):
        self.sserver = SServer()
        self.scity = SCity()

    def get_move_list(self):
        """hau"""
        move_list = self.sserver.get_mover_serverlist()
        return Success(u'获取列表成功', {
            'servers': move_list
        })

    def get_moveercity_list(self):
        """获取开通搬家服务的城市"""
        city_list = self.scity.get_moveroppencitylist()
        if city_list:
            map(lambda x: x.fill(self.scity.get_city_by_city_id(x.city_id).name, 'name'), city_list)
        return Success(u'获取列表成功', {
            'servers': city_list
        })



