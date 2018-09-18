# -*- coding: utf-8 -*-
from Linjia.commons.base_resource import Resource
from Linjia.control import CTrade


class ATrade(Resource):
    def __init__(self):
        self.ctrade = CTrade()

    def post(self, trade):
        apis = {
            'add_providehouse_apply': self.ctrade.add_providehouse_apply,
            'mover_appointment': self.ctrade.mover_appointment,
            'cleaner_apponintment': self.ctrade.cleaner_appiontment,
            'fixer_appointment': self.ctrade.fixer_appiontment,
            'add_complaint': self.ctrade.add_complaint,
            'update_complaint': self.ctrade.update_complaint,
            # 改状态
            'update_fixerorder_status': self.ctrade.update_fixerorder_status,
            'update_cleanorder_status': self.ctrade.update_cleanorder_status,
            'update_moverorder_status': self.ctrade.update_moverorder_status,
            # 改价
            'update_fixorder_price': self.ctrade.update_fixorder_price,
            'update_cleanerorder_price': self.ctrade.update_cleanerorder_price,
            'update_moverorder_price': self.ctrade.update_moverorder_price,
            # 修改申请房源的状态
            'update_provide_house': self.ctrade.update_provide_house_status,
            # 给订单制定工作人员
            'point_staff': self.ctrade.point_staff,
            # 用户取消订单
            'user_cancle_moverorder': self.ctrade.user_cancle_moverorder,
            'user_cancle_fixerordder': self.ctrade.user_cancle_fixer_order,
            'user_cancle_cleanerorder': self.ctrade.user_cancle_cleaner_order,
            # 同意用户取消订单
            'agree_cancle_mover_order': self.ctrade.agree_cancle_mover_order,
            'agree_cancel_clean_order': self.ctrade.agree_cancle_cleaner_order,
            'agree_cancel_fixer_order': self.ctrade.agree_cancle_fixer_order,
        }
        return apis

    def get(self, trade):
        apis = {
            'get_my_appiontlist': self.ctrade.get_my_oppintment,
            'get_complaint_list': self.ctrade.get_complaint_list,
            'get_provide_house_list': self.ctrade.get_provide_house_list,
            'get_appointment_list': self.ctrade.get_appointment_list,
            'get_appointment_one': self.ctrade.get_appointment_one,
        }
        return apis
