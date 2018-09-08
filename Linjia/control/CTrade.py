# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from flask import request

from Linjia.commons.error_response import TOKEN_ERROR
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_tourist
from Linjia.configs.timeformat import format_for_db
from Linjia.service import STrade


class CTrade(object):
    def __init__(self):
        self.strade = STrade()

    def add_providehouse_apply(self):
        data = parameter_required('phacity', 'phavillege', 'phaphone', 'phaname')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后申请')
        data['usid'] = request.user.id
        data['PHAcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
        data['PHAid'] = str(uuid.uuid4())
        self.strade.add_model('ProvideHouseApply', **data)
        return Success(u'申请成功, 等待管家回电', {
            'data': data['PHAid']
        })

