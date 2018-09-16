# -*- coding: utf-8 -*-
from Linjia.commons.base_resource import Resource
from Linjia.control import CServer, CMover, CLeaner, CFixer


class Aserver(Resource):
    def __init__(self):
        self.cserver = CServer()
        self.cmover = CMover()
        self.cleaner = CLeaner()
        self.cfixer = CFixer()


class AMover(Aserver):
    """搬家相关"""
    def get(self, mover):
        apis = {
            'city_list': self.cmover.get_moveercity_list,
            'move_list': self.cmover.get_mover_list_by_city,
            'get_detail': self.cmover.get_mover_detail,
            'mover_list_admin': self.cmover.get_moverlist,
        }
        return apis

    def post(self, mover):
        apis = {
            'add_moverselector': self.cmover.add_moverselector,
            'cancle_moverselector': self.cmover.cancle_moverselector,
            'add_mover_city': self.cmover.add_mover_oppencity,
            'delete_mover_city': self.cmover.del_mover_oppencity,
            'update_mover_selector': self.cmover.update_mover_selector,  # 修改搬家详情
        }
        return apis


class Acleaner(Aserver):
    """清洁相关"""
    def get(self, cleaner):
        apis = {
            'city_list': self.cleaner.get_cleanercity_list,
            'clean_list': self.cleaner.get_clean_list_by_cityid,
            'clean_list_admin': self.cleaner.get_clean_list,
            'get_detail': self.cleaner.get_cleaner_detail,
        }
        return apis

    def post(self, cleaner):
        apis = {
            'add_cleanselector': self.cleaner.add_cleanselector,
            'cancle_cleanselector': self.cleaner.cancle_cleanselector,
            'add_cleanercity': self.cleaner.add_cleaner_city,
            'delete_cleanercty': self.cleaner.del_cleaner_city,
        }
        return apis


class AFixer(Aserver):
    def get(self, fixer):
        apis = {
            'city_list': self.cfixer.get_fixercity_list,
            'fixer_list': self.cfixer.get_fixer_list_by_cityid,
        }
        return apis

    def post(self, fixer):
        apis = {
            'add_fixercity': self.cfixer.add_fixer_city,
            'delete_fixercity': self.cfixer.del_fixer_city,
        }
        return apis
