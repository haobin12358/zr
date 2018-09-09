# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from flask import request

from Linjia.commons.error_response import TOKEN_ERROR, PARAMS_ERROR
from Linjia.commons.params_validates import parameter_required, validate_phone
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_admin, is_tourist
from Linjia.configs.server_config import MOVER_APPOINT_ON_ROAD
from Linjia.configs.timeformat import format_for_db
from Linjia.service import STrade


class CTrade(object):
    def __init__(self):
        self.strade = STrade()

    def add_providehouse_apply(self):
        """申请房源"""
        if is_admin():
            return TOKEN_ERROR(u'普通用户才可以申请')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后申请')
        data = parameter_required(('phacity', 'phavillege', 'phaphone', 'phaname'), others='ignore')
        validate_phone(data.get('phaphone'))
        usid = request.user.id
        already_apply = self.strade.get_provide_appy_by_usid_village(usid, data.get('phavillege'))
        if not already_apply:
            data['usid'] = usid
            data['PHAcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
            data['PHAid'] = str(uuid.uuid4())
            self.strade.add_model('ProvideHouseApply', **data)
        return Success(u'申请成功, 等待管家回电')

    def subscribe_clean(self):
        """预约清洁"""
        if is_admin():
            return TOKEN_ERROR(u'普通用户才可以申请')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后申请')
        usid = request.user.id

    def mover_appointment(self):
        """搬家预约"""
        if is_admin():
            return TOKEN_ERROR(u'普通用户才可以申请')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后申请')
        data = parameter_required(('smsid', 'umtstarttime', 'umtmoveoutaddr', 'umtphone', 'umtspecialwish'), others='ignore')
        # todo是否存在这个服务
        # 暂时只简单判断预约时间
        validate_phone(data.get('umtphone'))
        self._allow_starttime(data.get('umtstarttime'))
        data['UMTid'] = str(uuid.uuid4())
        model_bean_dict = self.strade.add_model('UserMoveTrade', **data)
        return Success(u'预约成功', {
            'data': model_bean_dict
        })

    @staticmethod
    def _allow_starttime(str_time):
        try:
            startime = datetime.strptime(str_time, format_for_db)
        except Exception as e:
            raise PARAMS_ERROR(str(str_time) + u'时间格式不正确')
        time_at_road = (startime - datetime.now()).total_seconds()
        if time_at_road < MOVER_APPOINT_ON_ROAD:
            raise PARAMS_ERROR(u'时间不合理')
        return str_time







