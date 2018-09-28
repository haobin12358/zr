# -*- coding: utf-8 -*-
import time

from flask import request, jsonify

from Linjia.commons.error_response import PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, SYSTEM_ERROR
from Linjia.commons.error_response import NOT_FOUND
from Linjia.commons.logger_handler import generic_log
from Linjia.commons.params_validates import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_tourist, is_admin
from Linjia.configs.url_config import notify_url
from Linjia.configs.wxconfig import APPID, MCH_KEY, MCH_ID
from Linjia.libs.weixin import WeixinPay
from Linjia.libs.weixin.pay import WeixinPayError
from Linjia.service import SServer, STrade, SUser


class CPay(object):
    def __init__(self):
        self.sserver = SServer()
        self.strade = STrade()
        self.suser = SUser()
        self.pay = WeixinPay(APPID, MCH_ID, MCH_KEY, notify_url, '/home/admin/tool/apiclient_key.pem',
                             '/home/admin/tool/apiclient_cert.pem')  # 后两个参数可选

    def pay_for_service(self):
        data = parameter_required()
        if is_tourist():
            raise TOKEN_ERROR()
        if is_admin():
            raise AUTHORITY_ERROR(u'请使用普通用户登陆')
        usid = request.user.id
        user = self.suser.get_user_by_usid(usid)
        openid = user.WXopenid
        if 'umtid' in data:
            umtid = data.get('umtid')
            usermoverorder = self.strade.get_mover_order_by_umtid(umtid)
            if not usermoverorder or usermoverorder.UMTstatus != 0:
                raise NOT_FOUND()
            total_fee = usermoverorder.UMTpreviewprice
            out_trade_no = self.pay.nonce_str
            self.strade.update_movertrade_detail_by_umtid(umtid, {
                'sn': out_trade_no
            })
            body = u'邻家搬家'
            attach = u'mover'
        elif 'uctid' in data:
            uctid = data.get('uctid')
            user_clean_order = self.strade.get_clean_order_by_uctid(uctid)
            if not user_clean_order or user_clean_order.UCTstatus != 0:
                raise NOT_FOUND()
            total_fee = user_clean_order.UCTprice
            out_trade_no = self.pay.nonce_str
            self.strade.update_cleanorder_detail_by_uctid(uctid, {
                'sn': out_trade_no
            })
            body = u'cleaner'
            attach = u'cleaner'
            
        elif 'uftid' in data:
            uftid = data.get('uftid')
            user_fixer_order = self.strade.get_fixer_order_by_uftid(uftid)
            if not user_fixer_order or user_fixer_order.UFTstatus != 0:
                raise NOT_FOUND()
            total_fee = user_fixer_order.UFTprice
            out_trade_no = self.pay.nonce_str
            self.strade.update_fixerorder_detail_by_uftid(uftid, {
                'sn': out_trade_no
            })
            body = u'fixer'
            attach = u'fixer'
        else:
            raise PARAMS_ERROR()
        try:
            total_fee *= 100
            raw = self.pay.jsapi(trade_type="JSAPI", openid=openid, body=body,
                                         out_trade_no=out_trade_no,
                                         total_fee=int(total_fee), attach=attach, spbill_create_ip=request.remote_addr)
            res = dict(raw)
            res['paySign'] = res.get('sign')
        except WeixinPayError as e:
            return SYSTEM_ERROR(e.message)
        return Success(res)

    def pay_notify(self):
        data = self.pay.to_dict(request.data)
        generic_log(data)
        if not self.pay.check(data):
            return self.pay.reply(u"签名验证失败", False)
        sn = data.get('out_trade_no')
        paytime = data.get('time_end')
        attach = data.get('attach')
        if attach == u'mover':
            updated = self.strade.update_movertrade_detail_by_sn(sn, {
                'UMTstatus': 1,
                'paytime': paytime
            })
        elif attach == u'cleaner':
            updated = self.strade.update_cleanerorder_detail_by_sn(sn, {
                'UCTstatus': 1,
                'paytime': paytime
            })
            pass
        elif attach == u'fixer':
            updated = self.strade.udpate_fixerorder_detail_by_sn(sn, {
                'UFTstatus': 1,
                'paytime': paytime
            })
        return self.pay.reply("OK", True)

    def check_refund(self):
        """查询是否退款"""
        # if not is_admin():
        #     raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required()
        if 'umtid' in data:
            umtid = data.get('umtid')
            order = self.strade.get_mover_order_by_umtid(umtid)
            if not order or order.UMTstatus != 0:
                raise NOT_FOUND()
            pass
        elif 'uctid' in data:
            uctid = data.get('uctid')
            order = self.strade.get_clean_order_by_uctid(uctid)
            if not order or order.UCTstatus != 0:
                raise NOT_FOUND()
        elif 'uftid' in data:
            uftid = data.get('uftid')
            order = self.strade.get_fixer_order_by_uftid(uftid)
            if not order or order.UFTstatus != 0:
                raise NOT_FOUND()
        else:
            raise PARAMS_ERROR()
        sn = order.sn
        try:
            res = self.pay.refund_query(out_trade_no=sn)
        except WeixinPayError as e:
            raise SYSTEM_ERROR(e.message)
        return Success(data=res)


