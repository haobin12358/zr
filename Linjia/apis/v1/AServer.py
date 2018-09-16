# -*- coding: utf-8 -*-
from Linjia.commons.base_resource import Resource
from Linjia.control import CServer


class Aserver(Resource):
    def __init__(self):
        self.cserver = CServer()
    
    def post(self, server):
        apis = {
            'add_city': self.cserver.add_city,
        }
        return apis


class AMover(Aserver):
    """搬家相关"""
    def get(self, mover):
        apis = {
            'city_list': self.cserver.get_moveercity_list,
            'move_list': self.cserver.get_mover_list_by_city,
            'get_detail': self.cserver.get_mover_detail,
            'mover_list_admin': self.cserver.get_moverlist,
        }
        return apis

    def post(self, mover):
        apis = {
            'add_moverselector': self.cserver.add_moverselector,
            'cancle_moverselector': self.cserver.cancle_moverselector,
            'add_mover_city': self.cserver.add_mover_oppencity,
            'delete_mover_city': self.cserver.del_mover_oppencity,
        }
        return apis


class Acleaner(Aserver):
    """清洁相关"""
    def get(self, cleaner):
        apis = {
            'city_list': self.cserver.get_cleanercity_list,
            'clean_list': self.cserver.get_clean_list_by_cityid,
            'clean_list_admin': self.cserver.get_clean_list,
        }
        return apis

    def post(self, cleaner):
        apis = {
            'add_cleanselector': self.cserver.add_cleanselector,
            'cancle_cleanselector': self.cserver.cancle_cleanselector,
            'add_cleanercity': self.cserver.add_cleaner_city,
            'delete_cleanercty': self.cserver.del_cleaner_city,
        }
        return apis

class AFixer(Aserver):
    def get(self, fixer):
        apis = {
            'city_list': self.cserver.get_fixercity_list, 
            'fixer_list': self.cserver.get_fixer_list_by_cityid,
        }
        return apis
