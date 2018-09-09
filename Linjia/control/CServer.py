# -*- coding: utf-8 -*-
from Linjia.commons.success_response import Success
from Linjia.service import SServer, SCity


class CServer(object):
    def __init__(self):
        self.sserver = SServer()
        self.scity = SCity()

    def get_move_list(self):
        move_list = self.sserver.get_mover_serverlist()
        return Success(u'获取列表成功', {
            'servers': move_list
        })

    def get_moveercity_list(self):
        pass
