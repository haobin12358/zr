# -*- coding: utf-8 -*-
import uuid

from Linjia.commons.error_response import NOT_FOUND
from Linjia.commons.success_response import Success
from Linjia.service import SServer, SCity
from Linjia.commons.params_validates import parameter_required
from Linjia.commons.error_response import TOKEN_ERROR, PARAMS_ERROR
from Linjia.commons.token_handler import is_admin


class CMover(object):
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
        data = parameter_required(('city_id',), others='ignore')
        city_id = data.get('city_id')
        is_in_oppner = self.scity.is_move_oppener(city_id)
        if not is_in_oppner:
            raise NOT_FOUND(u'该城市暂未开通搬家服务')
        move_list = self.sserver.get_mover_serverlist()
        for move in move_list:
            smsid = move.SMSid
            price = self.sserver.get_mover_price_by_smsid(smsid)
            if price is None:
                continue
            move.fill(price, 'pricedetail')
            move.SMSshowprice = price.SMSPstartprice
        return Success(u'获取列表成功', {
            'movers': move_list
        })

    def cancle_moverselector(self):
        """取消搬家服务"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('smsid',))
        smsid = data.get('smsid')
        cancled = self.sserver.update_mover_server(smsid, {
            'SMStatus': 1
        })
        msg = u'取消成功' if cancled else u'无此记录'
        return Success(msg, {
            'smsid': smsid
        })

    def get_moverlist(self):
        """获取所有的搬家服务, 管理员使用"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        move_list = self.sserver.get_mover_serverlist()
        for move in move_list:
            smsid = move.SMSid
            price = self.sserver.get_mover_price_by_smsid(smsid)
            if price is None:
                continue
            move.fill(price, 'pricedetail')
            move.SMSshowprice = price.SMSPstartprice
        map(lambda x: x.hide('SMStatus'), move_list)
        return Success(u'获取列表成功', {
            'movers': move_list
        })

    def add_mover_oppencity(self):
        """添加搬家服务开通城市"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id',))
        city_id = data.get('city_id')
        # 先判断是否是已经开通的
        mover_oppen = self.scity.is_move_oppener(city_id)
        if mover_oppen:
            raise PARAMS_ERROR(u'重复开通')
        data['mcid'] = str(uuid.uuid4())
        self.scity.add_model('MoverCity', data)
        return Success('添加搬家服务开放城市成功', {
            'city_id': data.get('city_id')
        })

    def del_mover_oppencity(self):
        """取消城市的搬家服务开放"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id',))
        city_id = data.get('city_id')
        deleted = self.scity.delete_moveroppen(city_id)
        msg = u'取消成功' if deleted else u'无此记录'
        return Success(msg, {
            'city_id': city_id
        })

    def add_moverselector(self):
        """添加搬家服务选项, 同时添加价格详情"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('smstitle', 'smstitlepic', 'smssubtitle', 'smsshowprice', 'pricedetail'),
                                  forbidden=('smsid',))
        mod = {}
        data['smsid'] = str(uuid.uuid4())
        mod['ServersMoveSelector'] = data
        pricedetail = data.pop('pricedetail')
        price_data = parameter_required(('smspstartprice', 'smsppricestartdeadline', 'smsppricesoverstartperkg'),
                                        datafrom=pricedetail)
        price_data['smsid'] = data['smsid']
        price_data['smspid'] = str(uuid.uuid4())
        mod['ServersMoveSelectorPrice'] = price_data
        self.sserver.add_models(mod)
        return Success(u'添加成功', {
            'smsid': data['smsid']
        })

    def update_mover_selector(self):
        """修改搬家服务选项, 同时更新服务价格详情"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('smsid', ))
        smsid = data.get('smsid')
        update_data = {
            'SMStitlepic': data.get('smstilepic'),
            'SMStitle': data.get('smstitle'),
            'SMSsubtitle': data.get('smssubtitle'),
            'SMSshowprice': data.get('smsshowprice'),
        }
        update_data = {
            k: v for k, v in update_data.items() if v is not None
        }
        updated = self.sserver.update_mover_server(smsid, update_data)
        pricedetail = data.pop('pricedetail', None)
        if pricedetail:  # 因不确定数据库中是否存在价格详情, 应尝试更新, 而后在决定是否添加
            pricedetail_data = {
                'SMSPstartprice': pricedetail.get('smspstartprice'),
                'SMSPpricestartdeadline': pricedetail.get('smsppricestartdeadline'),
                'SMSPpricesoverstartperkg': pricedetail.get('smsppricesoverstartperkg'),
            }
            price_updated = self.sserver.update_mover_server_price(smsid, pricedetail_data)
            if not price_updated:
                print('不存在价格详情, 添加')
                pricedetail_data['smsid'] = smsid
                pricedetail_data['smspid'] = str(uuid.uuid4())
                self.sserver.add_model('ServersMoveSelectorPrice', pricedetail_data)
        msg = u'更新成功' if updated else u'无此记录'
        return Success(msg, {
            'smsid': smsid
        })

    def get_mover_detail(self):
        """获取单个搬家服务的详细信息"""
        data = parameter_required(('smsid',), others='ignore')
        smsid = data.get('smsid')
        move = self.sserver.get_mover_by_smsid(smsid)
        if not move:
            raise NOT_FOUND(u'没有这项服务')
        price = self.sserver.get_mover_price_by_smsid(smsid)
        if price is not None:
            move.fill(price, 'pricedetail')
            move.SMSshowprice = price.SMSPstartprice
        return Success(u'获取服务详情成功', {
            'detail': move
        })


class CLeaner(object):
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
        clean_list = self.sserver.get_clearerserver_list()
        return Success(u'获取清洁列表成功', {
            'cleans': clean_list
        })

    def get_clean_list(self):
        """获取保洁服务列表, 管理员使用"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        clean_list = self.sserver.get_clearerserver_list()
        map(lambda x: x.hide('SCMstatus'), clean_list)
        return Success(u'获取清洁列表成功', {
            'cleans': clean_list
        })

    def add_cleanselector(self):
        """添加保洁服务"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('scmtitle', 'scmtitlepic', 'scmsubtitle', 'scprice'), forbidden=('scmid'))
        data['sceid'] = str(uuid.uuid4())
        added = self.sserver.add_model('ServerCleanSelector', data)
        return Success(u'添加成功', {
            'sceid': data['sceid']
        })

    def cancle_cleanselector(self):
        """取消保洁服务"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('sceid',))
        updated = self.sserver.update_cleanserver(data.get('sceid'), {
            'SCMstatus': 1
        })
        msg = u'取消成功' if updated else u'无此记录'
        return Success(msg, {
            'sceid': data.get('sceid')
        })

    def add_cleaner_city(self):
        """添加保洁开放城市"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id',))
        city_id = data.get('city_id')
        cleaner_city = self.scity.is_clean_oppener(city_id)
        if cleaner_city:
            raise PARAMS_ERROR(u'重复添加')
        data['ccid'] = str(uuid.uuid4())
        added = self.sserver.add_model('CleanerCity', data)
        return Success(u'添加保洁开放城市成功', {
            'city_id': city_id
        })

    def del_cleaner_city(self):
        """取消保洁开放城市"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id',))
        city_id = data.get('city_id')
        deleted = self.scity.delete_cleanoppen(city_id)
        msg = u'取消成功' if deleted else u'无此记录'
        return Success(msg, {
            'city_id': city_id
        })

    def get_cleaner_detail(self):
        """获取单条服务的详情"""
        data = parameter_required(('sceid', ))
        sceid = data.get('sceid')
        clean = self.sserver.get_cleanerserver_by_sceid(sceid)
        if not clean:
            raise NOT_FOUND(u'该服务不存在')
        return Success(u'获取保洁服务成功', {
            'clean': clean
        })


class CFixer(object):
    def get_fixercity_list(self):
        """获取开通维修服务的城市"""
        city_list = self.scity.get_fixeroppencitylist()
        map(lambda x: x.fill(getattr(self.scity.get_city_by_city_id(x.city_id), 'name', u'未知'),  # 仅额外填充城市的名字
                             'name'), city_list)
        return Success(u'获取城市列表成功', {
            'citys': city_list
        })

    def get_fixer_list_by_cityid(self):
        """获取该城市下的所有维修服务"""
        data = parameter_required(('city_id',), others='ignore')
        city_id = data.get('city_id')
        is_in_oppner = self.scity.is_fixer_oppener(city_id)
        if not is_in_oppner:
            raise NOT_FOUND(u'该城市暂未开通维修服务')
        fixer_list = []
        return Success(u'获取维修列表成功', {
            'fixers': fixer_list
        })

    def add_fixer_city(self):
        """添加维修开通城市"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id',))
        city_id = data.get('city_id')
        fixer_city = self.scity.is_fixer_oppener(city_id)
        if fixer_city:
            raise PARAMS_ERROR(u'重复添加')
        data['fcid'] = str(uuid.uuid4())
        added = self.scity.add_model('FixerCity', data)
        return Success(u'添加维修服务开通城市成功', {'city_id': city_id})

    def del_fixer_city(self):
        """取消维修服务开通城市"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id',))
        city_id = data.get('city_id')
        deleted = self.scity.delete_fixeroppencity(city_id)
        msg = u'取消成功' if deleted else u'无此记录'
        return Success(msg, {'city_id': city_id})

    def add_city(self):
        """添加开通城市, 租房以及服务"""
        data = parameter_required(('city_id',), others='ignore')
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        mod = dict()
        data['rcid'] = data['mcid'] = data['ccid'] = data['fcid'] = str(uuid.uuid4())
        mod['RoomCity'] = mod['MoverCity'] = mod['CleanerCity'] = mod['FixerCity'] = data
        self.scity.add_models(mod)
        return Success(u'添加开通服务成功', {
            'city_id': data.get('city_id')
        })


class CServer(CMover, CLeaner, CFixer):
    def __init__(self):
        self.sserver = SServer()
        self.scity = SCity()

