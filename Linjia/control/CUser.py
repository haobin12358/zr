# -*- coding: utf-8 -*-
import random
import traceback
import uuid
from datetime import datetime
from threading import Thread

from flask import request
from raven.transport import requests
from weixin import WeixinLogin
from werkzeug.security import generate_password_hash

from Linjia.commons.error_response import NOT_FOUND, SYSTEM_ERROR, TOKEN_ERROR, PARAMS_ERROR, AUTHORITY_ERROR
from Linjia.commons.params_validates import parameter_required, validate_phone, validate_arg
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import usid_to_token, is_admin, is_hign_level_admin
from Linjia.configs.enums import STAFF_TYPE, GENDER_CONFIG
from Linjia.configs.phone_code import auth_key, code_url
from Linjia.configs.timeformat import format_for_db
from Linjia.configs.url_config import HTTP_HOST
from Linjia.configs.wxconfig import APPID, APPSECRET, WXSCOPE
from Linjia.service import SUser, SUserCode


class CUser():
    def __init__(self):
        self.suser = SUser()
        self.susercode = SUserCode()
        self.wxlogin = WeixinLogin(APPID, APPSECRET)

    def admin_login(self):
        """管理员登录"""
        data = parameter_required(('username', 'password'))
        username = data.get('username')
        password = data.get('password')
        admin = self.suser.verify_admin_login(username, password)
        if not admin:
            raise NOT_FOUND(u'用户名或者密码错误')
        level = admin.ADlevel  # 管理员等级
        token = usid_to_token(admin.ADid, 'Admin', level=level)
        return Success(u'获取token成功', {
            'token': token,
            'level': level
        })

    def login(self):
        """登录, 没有用户则自动创建"""
        data = parameter_required(('phone', 'code'), others='ignore')
        phone = str(data.get('phone'))
        code = int(data.get('code'))
        usercode = self.susercode.get_active_usercode_by_phone_code(phone, code)
        if not usercode:
            return NOT_FOUND(u'验证码已过期或不正确')
        user = self.suser.get_user_by_phone(phone)
        if not user:
            user_dict = {
                'usid': str(uuid.uuid4()),
                'USphone': str(phone),
            }
            self.suser.add_model('User', user_dict)
            token = usid_to_token(user_dict['usid'])
        else:
            token = usid_to_token(user.USid)
        return Success(u'获取token成功', {
            'token': token
        })

    def get_code(self):
        """发送验证码"""
        data = parameter_required(('phone', ))
        phone = validate_phone(data.get('phone'))
        send = Thread(target=self._async_send_code, args=(phone, ))
        send.start()
        message = u'获取成功'
        return Success(message)

    def wechat_login(self):
        """获取微信跳转链接"""
        url = self.wxlogin.authorize(HTTP_HOST + "/user/weixin_callback/", WXSCOPE)
        return Success(u'获取跳转链接成功',  {'url': url}, status=302)

    def weixin_callback(self):
        """通过code, 获取用户信息"""
        args = parameter_required(('code', ))
        code = args.get('code')
        data = self.wxlogin.access_token(code)
        data = self.wxlogin.user_info(data.access_token, data.openid)
        return data

    def get_wx_config(self):
        data = request.json
        if not data:
            data = {}
        current_url = data.get('url', request.url)
        from weixin.mp import WeixinMP
        mp = WeixinMP(APPID, APPSECRET)
        print(current_url)
        data = {
            'config': mp.jsapi_sign(url=current_url),
            'url': current_url
        }
        response = Success(u'返回签名成功', data)
        return response

    def get_staff_list(self):
        """获取工作人员"""
        data = request.args.to_dict()
        level = data.get('level')
        page = int(data.get('page', 1))
        count = int(data.get('count', 15))
        gender = int(data.get('gender')) if 'gender' in data else None
        kw = data.get('kw')  # 员工姓名模糊搜索
        staff_list = self.suser.get_staff_list(level, page, count, gender, kw)
        for staff in staff_list:
            setattr(staff,  'STFlevel', STAFF_TYPE.get(staff.STFlevel, u'其他'))
            setattr(staff, 'STFgender', GENDER_CONFIG.get(staff.STFgender, u'未知'))
        return Success(u'获取工作人员成功', {
            'staff': staff_list
        })

    def add_staff(self):
        """添加工作人员"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('stfname', 'stfmobiel', 'stfaddress', 'stfgender', 'stflevel'), others='allow', forbidden=('STFid', ))
        validate_phone(data.get('stfmobiel'))
        if 'stfphone' in data:
            validate_phone(data.get('stfphone'))
        data['stfid'] = str(uuid.uuid4())
        data['STFcreatetime'] = datetime.strftime(datetime.now(), format_for_db)
        self.suser.add_model('Staff', data)
        return Success(u'添加成功', {
            'stfid': data.get('stfid')
        })

    def update_staff(self):
        """修改工作人员信息"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        json_data = parameter_required(('stfid', ), others='allow')
        stfid = json_data.get('stfid')
        data = {
            'STFname': json_data.get('stfname'),
            'STFmobiel': json_data.get('stfmobiel'),
            'STFphone': json_data.get('stfphone'),
            'STFaddress': json_data.get('stfaddress'),
            'STFgender': json_data.get('stfgender'),
            'STFlevel': json_data.get('stflevel'),
            'ADaddressnum': json_data.get('adaddressnum'),
            'APid': json_data.get('apid'),
            'ADdesc': json_data.get('addesc'),
            'STFisblocked': json_data.get('stfisblocked'),
        }
        data = {
            k: v for k, v in data.items() if v is not None
        }
        staff = self.suser.update_staff_info(stfid, data)
        if not staff:
            return Success(u'无此记录', {
                'stfid': stfid
            })
        else:
            return Success(u'修改成功', {
                'stfid': stfid
            })

    def get_staff_by_id(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('stfid', ))
        staff = self.suser.get_staff_by_stfid(data.get('stfid'))
        if not staff:
            raise NOT_FOUND(u'无记录')
        staff.all.hide('STFisdelete')
        setattr(staff,  'STFlevel', STAFF_TYPE.get(staff.STFlevel, u'其他'))
        setattr(staff, 'STFgender', GENDER_CONFIG.get(staff.STFgender, u'未知'))
        return Success(u'获取成功', {
            'staff': staff
        })

    def delete_staff(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('stfid',))
        stfid = data.get('stfid')
        staff = self.suser.delete_staff_by_stfid(stfid)
        if not staff:
            return Success(u'无此记录', {
                'stfid': stfid
            })
        return Success(u'删除成功', {
            'stfid': stfid
        })

    def add_admin(self):
        # 添加管理员, 默认添加0级别管理员
        if not is_hign_level_admin():
            raise TOKEN_ERROR(u'需要高级管理权限')
        required = ['adname', 'adusername', 'adpassword', 'admobiel', 'ademail']
        data = parameter_required(required)
        if self.suser.get_admin_by_adusername(data.get('adusername')):
            raise PARAMS_ERROR(u'用户名重复')

        validate_phone(data.get('admobiel'))
        validate_phone(data.get('adphone'))
        validate_arg('\w+@\w+\.\w+', data.get('ademail'), u'电子邮箱格式不正确')
        data['adlevel'] = 0 or data.get('adlevel')
        if data['adlevel'] >= request.user.level:
            raise AUTHORITY_ERROR()
        data['adid'] = str(uuid.uuid4())
        data['adpassword'] = generate_password_hash(data.get('adpassword'))
        self.suser.add_model('Admin', data)
        return Success(u'添加管理员成功', {
            'adid': data.get('adid')
        })

    def freeze_admin(self):
        """冻结管理员"""
        if not is_hign_level_admin():
            raise TOKEN_ERROR(u'需要高级管理权限')
        data = parameter_required(('adid', ))
        adid = data.get('adid')
        admin = self.suser.get_admin_by_adid(adid)
        if admin and admin.ADlevel >= request.user.level:
            raise AUTHORITY_ERROR()
        freezed = self.suser.freeze_adiin_by_adid(adid)
        msg = u'操作成功' if freezed else u'无此记录'
        return Success(msg, {
            'adid': adid
        })

    def get_admin_list(self):
        """查看管理员列表"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = request.args.to_dict()
        page = data.get('page', 1)
        count = data.get('count', 15)
        freeze_args = data.get('freeze')
        freeze = None
        if freeze_args is not None:
            freeze = False if str(freeze_args) == '0' else True
        print('>>>>>>>>>>>', freeze)
        admin_list = self.suser.get_admin_list(data.get('level'), freeze, page, count)
        map(lambda x: x.hide('ADpassword'), admin_list)
        return Success(u'ok', {
            'admins': admin_list
        })


    def _async_send_code(self, phone):
        headers = {
            'Authorization': auth_key
        }
        code = str(random.randint(1111, 9999))
        url = code_url.format(code, phone)
        content_json = requests.post(url, headers=headers).json()
        if content_json.get('return_code') == '00000':
            print(0000)
            data = {
                'UCid': str(uuid.uuid4()),
                'Codenum': int(code),
                'Phone': phone,
                'Createtime': datetime.strftime(datetime.now(), format_for_db)
            }
            self.suser.add_model('UserCode', data)
        else:
            raise SYSTEM_ERROR(traceback.format_exc().decode('unicode-escape'))

