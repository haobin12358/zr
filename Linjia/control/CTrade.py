# -*- coding: utf-8 -*-
import uuid
import math
from datetime import datetime

from flask import request

from Linjia.commons.baidu_map import BdMap
from Linjia.commons.error_response import TOKEN_ERROR, PARAMS_ERROR, NOT_FOUND
from Linjia.commons.params_validates import parameter_required, validate_phone
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_admin, is_tourist
from Linjia.configs.enums import SERVER_STATUS, COMPLAIN_STATUS, PROVIDE_HOUSE_STATUS
from Linjia.configs.server_config import MOVER_APPOINT_MAX_TIME_ON_ROAD, MOVER_APPOINT_MIN_TIME_ON_ROAD
from Linjia.configs.timeformat import format_for_db
from Linjia.service import STrade, SServer, SCity, SUser


class CTrade(object):
    def __init__(self):
        self.strade = STrade()
        self.sserver = SServer()
        self.scity = SCity()
        self.suser = SUser()

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
        if already_apply:
            last_applytime = datetime.strptime(already_apply.PHAcreatetime, format_for_db)
            seconds = (datetime.now() - last_applytime).total_seconds()
            if seconds < 600:
                # 短时间内重复提交不记录
                return Success(u'申请成功, 等待管家回电')
        data['usid'] = usid
        data['PHAcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
        data['PHAid'] = str(uuid.uuid4())
        self.strade.add_model('ProvideHouseApply', data)
        return Success(u'申请成功, 等待管家回电')

    def mover_appointment(self):
        """搬家预约"""
        if is_admin():
            return TOKEN_ERROR(u'普通用户才可以预约')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后预约')
        required = ('smsid', 'umtstarttime', 'umtmoveoutaddr', 'umtmoveinaddr',
                    'umtmoveoutlocation', 'umtmoveinlocation', 'umtphone', 'umtspecialwish', 'umtpreviewprice')
        data = parameter_required(required, others='ignore')
        # 是否存在这个服务
        mover_exsits = self.sserver.get_mover_by_smsid(data.get('smsid'))
        if not mover_exsits:
            raise NOT_FOUND(u'不存在服务{}'.format(data.get('smsid')))
        validate_phone(data.get('umtphone'))
        self._allow_starttime(data.get('umtstarttime'))
        data['UMTid'] = str(uuid.uuid4())
        data['usid'] = request.user.id
        data['UMTcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
        model_bean_dict = self.strade.add_model('UserMoveTrade', data, ['UMTstarttime', 'UMTid'])
        model_bean_dict['name'] = mover_exsits.SMStitle
        return Success(u'预约成功', model_bean_dict)

    def cleaner_appiontment(self):
        """清洁服务预约"""
        if is_admin():
            return TOKEN_ERROR(u'普通用户才可以预约')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后预约')
        required = ('sceid', 'uctpreviewstarttime', 'uctaddr', 'uctpreviewlastingtime', 'uctphone', 'uctprice', 'uctspecialwish', 'uctlocation')
        data = parameter_required(required, others='ignore')
        cleaner_exists = self.sserver.get_cleanerserver_by_sceid(data.get('sceid'))
        if not cleaner_exists:
            raise NOT_FOUND(u'不存在的清洁服务')
        validate_phone(data.get('uctphone'))
        self._allow_starttime(data.get('uctpreviewstarttime'))
        data['uctid'] = str(uuid.uuid4())
        data['usid'] = request.user.id
        data['UCTcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
        modelbean_dict = self.sserver.add_model('UserCleanTrade', data, ['UCTpreviewstarttime', 'UCTid'])
        modelbean_dict['name'] = cleaner_exists.SCMtitle
        return Success(u'预约成功', modelbean_dict)

    def fixer_appiontment(self):
        """维修预约"""
        if is_admin():
            return TOKEN_ERROR(u'只有普通用户才可以预约')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后预约')
        required = ('uftaddr' , 'uftstarttime', 'uftphone', 'uftlocation')
        forbidden = ('usid', 'uftstatus')
        data = parameter_required(required, forbidden=forbidden)
        validate_phone(data.get('uftphone'))
        self._allow_starttime(data.get('uftstarttime'))
        data['UFTid'] = str(uuid.uuid4())
        data['usid'] = request.user.id
        data['UFTcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
        model_bean_dict = self.sserver.add_model('UserFixerTrade', data, ['UFTid', 'UFTstarttime'])
        model_bean_dict['name'] = u'维修预约'
        return Success(u'预约成功', model_bean_dict)

    def get_my_oppintment(self):
        """获得我的预约搬家, 维修, 清洁 type=mover, fixer, cleaner"""
        if is_admin():
            return TOKEN_ERROR(u'普通用户查看')
        if is_tourist():
            return TOKEN_ERROR(u'请登录后查看')
        data = parameter_required()
        data['page_num'] = int(data.get('page', 1))
        data['page_size'] = int(data.get('count', 15))
        usid = request.user.id
        server_type = data.get('type')
        if server_type == 'mover':
            order_list = self.strade.get_mover_serverlist_by_usid(usid, data)
            map(lambda x: x.clean.add('UMTid', 'SMSid', 'UMTstarttime', 'UMTmoveoutaddr',
                                      'UMTmoveinaddr', 'UMTphone', 'UMTspecialwish',
                                      'UMTpreviewprice', 'UMTmoveinlocation', 'UMTmoveoutlocation', 'USid', 'UMTcreatetime'), order_list)
            map(lambda x: x.fill(SERVER_STATUS.get(x.UMTstatus), 'umtstatus'), order_list)
            map(lambda x: x.fill(self.sserver.get_mover_by_smsid(x.SMSid).SMStitle, 'name'), order_list)
            map(lambda x: x.fill('mover', 'type'), order_list)
        elif server_type == 'fixer':
            order_list = self.strade.get_fixer_serverlist_by_usid(usid, data)
            map(lambda x: setattr(x, 'UFTstatus', SERVER_STATUS.get(x.UFTstatus)), order_list)
            map(lambda x: x.fill(u'fixer', 'type'), order_list)
        elif server_type == 'cleaner':
            order_list = self.strade.get_clean_serverlist_by_usid(usid, data)
            map(lambda x: setattr(x, 'UCTstatus', SERVER_STATUS.get(x.UCTstatus)), order_list)
            map(lambda x: x.fill(self.sserver.get_cleanerserver_by_sceid(x.SCEid).SCMtitle, 'name'), order_list)
            map(lambda x: x.fill('cleaner', 'type'), order_list)
        else:
            mover_order_list = self.strade.get_mover_serverlist_by_usid(usid)
            fixer_order_list = self.strade.get_fixer_serverlist_by_usid(usid)
            cleaner_list = self.strade.get_clean_serverlist_by_usid(usid)
            order_list = mover_order_list + fixer_order_list + cleaner_list
            len_order_list = len(order_list)
            page_size = data['page_size']
            start = (data['page_num'] - 1) * data['page_size']
            end = start + page_size
            if end > len_order_list:
                end = len_order_list
            if start > end:
                start = end
            order_list = order_list[start: end]
            # 搬家

            map(lambda x: x.clean.add('UMTid', 'SMSid', 'UMTstarttime', 'UMTmoveoutaddr',
                                      'UMTmoveinaddr', 'UMTphone', 'UMTspecialwish',
                                      'UMTpreviewprice', 'UMTmoveinlocation', 'UMTmoveoutlocation', 'USid', 'UMTcreatetime'), mover_order_list)
            map(lambda x: x.fill(getattr(self.sserver.get_mover_by_smsid(x.SMSid), 'SMStitle', u'未知'), 'name'),
                mover_order_list)
            map(lambda x: x.fill('mover', 'type'), mover_order_list)
            map(lambda x: x.fill(SERVER_STATUS.get(x.UMTstatus), 'umtstatus'), mover_order_list)
            map(lambda x: setattr(x, 'createtime', x.UMTcreatetime), mover_order_list)
            # 清洁
            map(lambda x: x.fill(getattr(self.sserver.get_cleanerserver_by_sceid(x.SCEid), 'SCMtitle', u'未知'), 'name'), cleaner_list)
            map(lambda x: setattr(x, 'UCTstatus', SERVER_STATUS.get(x.UCTstatus)), cleaner_list)
            map(lambda x: setattr(x, 'createtime', x.UCTcreatetime), cleaner_list)
            map(lambda x: x.fill('cleaner', 'type'), cleaner_list)
            # 维修
            map(lambda x: setattr(x, 'createtime', x.UFTcreatetime), fixer_order_list)
            map(lambda x: x.fill(u'邻家维修', 'name'), fixer_order_list)
            map(lambda x: setattr(x, 'UFTstatus', SERVER_STATUS.get(x.UFTstatus)), fixer_order_list)
            map(lambda x: x.fill(u'fixer', 'type'), fixer_order_list)
            order_list = sorted(order_list, key=lambda x: x.createtime)
            request.page_count = math.ceil(float(len_order_list) / page_size)
            request.all_count = len_order_list
        return Success(u'获取列表成功', order_list)

    def add_complaint(self):
        if is_admin():
            raise TOKEN_ERROR(u'只有普通用户才可是投诉')
        if is_tourist():
            raise TOKEN_ERROR(u'请登录后投诉')
        data = parameter_required(('usercomplainttext', 'usercomplaintaddress', 'usercomplaintphone'), others='ignore')
        validate_phone(data.get('usercomplaintphone'))
        data['usid'] = request.user.id
        data['UserComplaintid'] = str(uuid.uuid4())
        data['UserComplaintcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
        self.strade.add_model('UserComplaint', data)
        return Success(u'投诉成功')

    def get_complaint_list(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        args = request.args.to_dict()
        page = int(args.get('page', 1))
        count = int(args.get('count', 15))
        status = args.get('status')
        complain_list = self.strade.get_complaint_list(page, count, status)
        map(lambda x: setattr(x, 'UserComplaintstatus', COMPLAIN_STATUS[x.UserComplaintstatus]), complain_list)
        return Success(u'获取投诉列表成功', complain_list)

    def update_complaint(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('usercomplaintid', 'status'))
        status = data.get('status')
        if str(status) not in ['1', '0']:
            raise PARAMS_ERROR(u'status参数不合法')
        comlain = self.strade.update_somplaint_by_complaintid(data.get('usercomplaintid'), {
            'UserComplaintstatus': status
        })
        if not comlain:
            raise NOT_FOUND(u'修改失败')
        return Success(u'修改成功', {
            'status': COMPLAIN_STATUS[status]
        })

    def get_provide_house_list(self):
        """获取业主提交的申请列表"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        args = request.args.to_dict()
        page = int(args.get('page', 1))
        count = int(args.get('count', 15))
        status = args.get('status')
        provice_house_list = self.strade.get_provideapply_list(page, count, status)
        map(lambda x: setattr(x, 'PAHstatus', PROVIDE_HOUSE_STATUS.get(x.PAHstatus, u'未知')), provice_house_list)
        map(lambda x: setattr(x, 'PHAcity', getattr(self.scity.get_city_by_city_id(x.PHAcity), 'name', u'未知')), provice_house_list)
        return Success(u'获取申请列表成功', {
            'provide': provice_house_list
        })

    def get_appointment_list(self):
        """后台获取预约列表"""
        # 此处将改用for循环 todo
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required()
        data['page_num'] = int(data.get('page', 1))
        data['page_size'] = int(data.get('count', 15))
        usid = data.get('usid')
        server_type = data.get('type')
        if server_type == 'mover':
            order_list = self.strade.get_mover_serverlist_by_usid(usid, data)
            for mover_order in order_list:
                mover_order.clean.add('UMTid', 'SMSid', 'UMTstarttime', 'UMTmoveoutaddr',
                                      'UMTmoveinaddr', 'UMTphone', 'UMTspecialwish',
                                      'UMTpreviewprice', 'UMTmoveinlocation', 'UMTmoveoutlocation', 'USid', 'UMTcreatetime')
                mover_order.fill(getattr(self.sserver.get_mover_by_smsid(mover_order.SMSid), 'SMStitle', u'未知'), 'name'),
                mover_order.fill('mover', 'type')
                mover_order.fill(SERVER_STATUS.get(mover_order.UMTstatus, u'其它'), 'umtstatus')
                setattr(mover_order, 'createtime', mover_order.UMTcreatetime)
        elif server_type == 'fixer':
            order_list = self.strade.get_fixer_serverlist_by_usid(usid, data)
            for fixer_order in order_list:
                setattr(fixer_order, 'createtime', fixer_order.UFTcreatetime)
                fixer_order.fill(u'邻家维修', 'name')
                setattr(fixer_order, 'UFTstatus', SERVER_STATUS.get(fixer_order.UFTstatus, u'其它'))
                fixer_order.fill(u'fixer', 'type')
        elif server_type == 'cleaner':
            order_list = self.strade.get_clean_serverlist_by_usid(usid, data)
            for clean_order in order_list:
                clean_order.fill(getattr(self.sserver.get_cleanerserver_by_sceid(clean_order.SCEid), 'SCMtitle', u'未知'),
                                 'name')
                setattr(clean_order, 'UCTstatus', SERVER_STATUS.get(clean_order.UCTstatus))
                setattr(clean_order, 'createtime', clean_order.UCTcreatetime)
                clean_order.fill('cleaner', 'type')
        else:
            mover_order_list = self.strade.get_mover_serverlist_by_usid(usid)
            fixer_order_list = self.strade.get_fixer_serverlist_by_usid(usid)
            cleaner_list = self.strade.get_clean_serverlist_by_usid(usid)
            order_list = mover_order_list + fixer_order_list + cleaner_list
            len_order_list = len(order_list)
            page_size = data['page_size']
            start = (data['page_num'] - 1) * data['page_size']
            end = start + page_size
            if end > len_order_list:
                end = len_order_list
            if start > end:
                start = end
            order_list = order_list[start: end]
           # 搬家
            for mover_order in mover_order_list:
                mover_order.clean.add('UMTid', 'SMSid', 'UMTstarttime', 'UMTmoveoutaddr',
                                      'UMTmoveinaddr', 'UMTphone', 'UMTspecialwish',
                                      'UMTpreviewprice', 'UMTmoveinlocation', 'UMTmoveoutlocation', 'USid', 'UMTcreatetime')
                mover_order.fill(getattr(self.sserver.get_mover_by_smsid(mover_order.SMSid), 'SMStitle', u'未知'), 'name'),
                mover_order.fill('mover', 'type')
                mover_order.fill(SERVER_STATUS.get(mover_order.UMTstatus), 'umtstatus')
                setattr(mover_order, 'createtime', mover_order.UMTcreatetime)
            for clean_order in cleaner_list:
                clean_order.fill(getattr(self.sserver.get_cleanerserver_by_sceid(clean_order.SCEid), 'SCMtitle', u'未知'), 'name')
                setattr(clean_order, 'UCTstatus', SERVER_STATUS.get(clean_order.UCTstatus))
                setattr(clean_order, 'createtime', clean_order.UCTcreatetime)
                clean_order.fill('cleaner', 'type')
            # 维修
            for fixer_order in fixer_order_list:
                setattr(fixer_order, 'createtime', fixer_order.UFTcreatetime)
                fixer_order.fill(u'邻家维修', 'name')
                setattr(fixer_order, 'UFTstatus', SERVER_STATUS.get(fixer_order.UFTstatus))
                fixer_order.fill(u'fixer', 'type')
            # 员工id 姓名.
            # map(lambda x: setattr( x, 'staff', self.suser.get_staff_by_stfid(x.STFid)) if not x.STFid order_list)
        for order in order_list:
            stfid = order.STFid
            staff = {}
            if stfid:
                staff = self.suser.get_staff_by_stfid(stfid).clean.add('STFid', 'STFname')
            setattr(order, 'staff', staff)
            order.add('staff')
        order_list = sorted(order_list, key=lambda x: x.createtime)
        # request.page_count = math.ceil(float(len_order_list) / page_size)
        # request.all_count = len_order_list
        return Success(u'获取列表成功', order_list)

    def update_fixerorder_status(self):
        """更新维修订单状态, 订单状态先使用随意改变的"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('uftid', 'status'))
        uftid = data.get('uftid')
        fix_order = self.strade.get_fixer_order_by_uftid(uftid)
        if not fix_order:
            raise NOT_FOUND()
        status = data.get('status')
        self._allow_order_status(fix_order.UFTstatus, int(status))
        updated = self.strade.update_fixertrade_status_by_utfid(uftid, status)
        msg = u'修改成功'
        return Success(msg, {
            'uftid': uftid
        })

    def update_fixorder_price(self):
        """修改维修价格"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('uftid', 'price'), others='ignore')
        uftid = data.get('uftid')
        fix_order = self.strade.get_fixer_order_by_uftid(uftid)
        if not fix_order:
            raise NOT_FOUND()
        if fix_order.UFTstatus != 0:
            raise PARAMS_ERROR(u'当前订单状态为{}, 只可以修改未付款的订单'.format(SERVER_STATUS.get(fix_order.UFTstatus)))
        updated = self.strade.update_fixerorder_detail_by_uftid(uftid, {
            'UFTprice': data.get('price')
        })
        return Success(u'修改成功', {
            'uftid': uftid
        })

    def update_cleanorder_status(self):
        """"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('uctid', 'status'))
        status = data.get('status')
        uctid = data.get('uctid')
        cleaner_order = self.strade.get_clean_order_by_uctid(uctid)
        if not cleaner_order:
            raise NOT_FOUND()
        self._allow_order_status(cleaner_order.UCTstatus, int(status))
        msg = u'修改成功'
        return Success(msg, {
            'uctid': uctid
        })

    def update_cleanerorder_price(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('uctid', 'price'))
        price = data.get('price')
        uctid = data.get('uctid')
        cleaner_order = self.strade.get_clean_order_by_uctid(uctid)
        if not cleaner_order:
            raise NOT_FOUND()
        if cleaner_order.UCTstatus != 0:
            raise PARAMS_ERROR(u'当前订单状态为{}, 只可以修改未付款的订单'.format(SERVER_STATUS.get(cleaner_order.UCTstatus)))
        updated = self.strade.update_cleanorder_detail_by_uctid(uctid, {
            "UCTprice": price
        })
        return Success(u'修改成功', {
            'uctid': uctid
        })

    def update_moverorder_status(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('umtid', 'status'))
        status = data.get('status')
        umtid = data.get('umtid')
        mover_order = self.strade.get_mover_order_by_umtid(umtid)
        if not mover_order:
            raise NOT_FOUND()
        self._allow_order_status(mover_order.UMTstatus, int(status))
        updated = self.strade.update_movertrade_status_by_umtid(umtid, status)
        msg = u'修改成功' if updated else u'无此记录'
        return Success(msg, {
            'umtid': umtid
        })

    def update_moverorder_price(self):
        """更新订单价格"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('umtid', 'price'))
        price = data.get('price')
        umtid = data.get('umtid')
        mover_order = self.strade.get_mover_order_by_umtid(umtid)
        if not mover_order:
            raise NOT_FOUND()
        if mover_order.UMTstatus != 0:
            raise PARAMS_ERROR(u'当前订单状态为{}, 只可以修改未付款的订单'.format(SERVER_STATUS.get(mover_order.UMTstatus)))
        updated = self.strade.update_movertrade_detail_by_umtid(umtid, {
            'UMTpreviewprice': price
        })
        return Success(u'修改成功', {
            'umtid': umtid
        })


    @staticmethod
    def _allow_starttime(str_time):
        try:
            startime = datetime.strptime(str_time, format_for_db)
        except Exception as e:
            raise PARAMS_ERROR(str(str_time) + u'时间格式不正确')
        time_on_road_seconds = (startime - datetime.now()).total_seconds()
        if MOVER_APPOINT_MIN_TIME_ON_ROAD < time_on_road_seconds < MOVER_APPOINT_MAX_TIME_ON_ROAD:
            return str_time
        raise PARAMS_ERROR(u'时间不合理')

    @staticmethod
    def _allow_order_status(old, new):
        if old == 0:
            # 0: 待支付, 1: 等待服务, 2: 服务完成, 3: 取消'
            forbidden = [2]
        elif old == 1:
            forbidden = [0]
        elif old == 2:
            forbidden = [0, 1]
        else:
            forbidden = [0, 1, 2, 3]
        if new in forbidden:
            raise PARAMS_ERROR(u'状态不合理, 当前状态为: {} '
                               u''.format(SERVER_STATUS.get(old)))

    @staticmethod
    def refund():
        # todo 退款状态
        pass
