# -*- coding: utf-8 -*-
from Linjia.commons.error_response import NOT_FOUND
from Linjia.commons.success_response import Success
from Linjia.service import SServer, SCity
from Linjia.commons.params_validates import parameter_required


class CServer(object):
    def __init__(self):
        self.sserver = SServer()
        self.scity = SCity()

    # 弃用
    def get_move_list(self):
        """获取所有的服务"""
        move_list = self.sserver.get_mover_serverlist()
        return Success(u'获取列表成功', {
            'servers': move_list
        })

    # 搬家
    def get_moveercity_list(self):
        """获取开通搬家服务的城市"""
        city_list = self.scity.get_moveroppencitylist()
        # 将名字赋值到列表中的每一个, 等同于for循环 + city.fill(name, 'name')
        map(lambda x: x.fill(getattr(self.scity.get_city_by_city_id(x.city_id), 'name', u'未知'),  # 仅提取城市的名字
            'name'), city_list)

        return Success(u'获取列表成功', {
            'citys': city_list
        })

    def get_mover_list_by_city(self):
        """获取搬家的服务列表"""
        data = parameter_required(('city_id', ), others='ignore')
        city_id = data.get('city_id')
        is_in_oppner = self.scity.is_move_oppener(city_id)
        if not is_in_oppner:
            raise NOT_FOUND(u'该城市暂未开通搬家服务')
        move_list = self.sserver.get_mover_serverlist()
        return Success(u'获取列表成功', {
            'movers': move_list
        })

    def get_mover_detail(self):
        """获取该服务的详细信息"""
        data = parameter_required(('smsid', ), others='ignore')
        smsid = data.get('smsid')
        is_exists = self.sserver.get_mover_by_smsid(smsid)
        if not is_exists:
            raise NOT_FOUND(u'没有这项服务')
        detail = self.sserver.get_mover_price_by_smsid(smsid)
        return Success(u'获取服务详情成功', {
            'detail': detail
        })

    # 保洁
    def get_cleanercity_list(self):
        """获取开通清洁的城市"""
        city_list = self.scity.get_cleaneroppencitylist()
        map(lambda x: x.fill(getattr(self.scity.get_city_by_city_id(x.city_id), 'name', u'未知'),  # 仅额外填充城市的名字
                             'name'), city_list)
        return Success(u'获取城市列表成功', {
            'citys': city_list
        })

    def get_clean_list_by_cityid(self):
        """获取城市下的所有清洁服务"""
        data = parameter_required(('city_id',), others='ignore')
        city_id = data.get('city_id')
        is_in_oppner = self.scity.is_clean_oppener(city_id)
        if not is_in_oppner:
            raise NOT_FOUND(u'该城市暂未开通清洁服务')
        move_list = self.sserver.get_clearerserver_list()
        return Success(u'获取清洁列表成功', {
            'movers': move_list
        })