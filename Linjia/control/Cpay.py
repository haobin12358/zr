# -*- coding: utf-8 -*-
from flask import request, jsonify

from Linjia.commons.error_response import PARAMS_ERROR, TOKEN_ERROR, AUTHORITY_ERROR, SYSTEM_ERROR
from Linjia.commons.error_response import NOT_FOUND
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
            out_trade_no = umtid.replace('-', '')
            body = u'邻家搬家'
            attach = u'mover'
        elif 'uctid' in data:
            uctid = data.get('uctid')
            user_clean_order = self.strade.get_clean_order_by_uctid(uctid)
            if not user_clean_order or user_clean_order.UCTstatus != 0:
                raise NOT_FOUND()
            total_fee = user_clean_order.UCTprice
            out_trade_no = uctid.replace('-', '')
            body = u'邻家清洁'
            attach = u'cleaner'
        elif 'uftid' in data:
            uftid = data.get('uftid')
            user_fixer_order = self.strade.get_fixer_order_by_uftid(uftid)
            if not user_fixer_order or user_fixer_order.UFTstatus != 0:
                raise NOT_FOUND()
            total_fee = user_fixer_order.UFTprice
            out_trade_no = uftid.replace('-', '')
            body = u'邻家维修'
            attach = u'fixer'
        else:
            raise PARAMS_ERROR()
        try:
            raw = self.pay.unified_order(trade_type="JSAPI", openid=openid, body=body,
                                         out_trade_no=out_trade_no,
                                         total_fee=1, attach=attach)
            raw = dict(raw)
            res = {
                "appId": raw['appid'],
                "nonceStr": raw['nonce_str'],
                "package": "prepay_id=" + raw['prepay_id'],
                "signType": "MD5",
                "paySign": raw['sign']
            }
        except WeixinPayError, e:
            return SYSTEM_ERROR(e.message)
        return Success(res)

    def pay_notify(self):
        data = self.pay.to_dict(request.data)
        import ipdb
        ipdb.set_trace()
        if not self.pay.check(data):
            return self.pay.reply(u"签名验证失败", False)
        attach = data.get('attach')
        if attach == u'mover':
            out_trade_no = data.get('out_trade_no')
            self.strade.get_mover_order_by_sn(out_trade_no)
        elif attach == u'cleaner':
            pass
        elif attach == u'fixer':
            pass

        return self.pay.reply("OK", True)
