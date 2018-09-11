# -*- coding: utf-8 -*-
from Linjia.commons.base_resource import Resource
from Linjia.control import CServer


class Aserver(Resource):
    def __init__(self):
        self.cserver = CServer()


class AMover(Aserver):
    """搬家相关"""
    def get(self, mover):
        apis = {
            'city_list': self.cserver.get_moveercity_list,
            'move_list': self.cserver.get_mover_list_by_city,
            'get_detail': self.cserver.get_mover_detail
        }
        return apis


class Acleaner(Aserver):
    """清洁相关"""
    def get(self, cleaner):
        apis = {
            'city_list': self.cserver.get_cleanercity_list,
            'clean_list': self.cserver.get_clean_list_by_cityid
        }
        return apis

class AFixer(Aserver):
    def get(self, fixer):
        apis = {
            'city_list': self.cserver.get_fixercity_list, 
            'fixer_list': self.cserver.get_fixer_list_by_cityid,
        }
        return apis
