# -*- coding: utf-8 -*-
from flask import request, jsonify
from werkzeug.security import generate_password_hash

from Linjia.commons.base_resource import Resource
from Linjia.commons.error_response import TOKEN_ERROR
from Linjia.commons.params_validates import parameter_required
from Linjia.commons.token_handler import is_admin
from Linjia.service import SUser


class MUserManage(Resource):
    def __init__(self):
        self.suser = SUser()

    def post(self):
        if not is_admin():
            raise TOKEN_ERROR('请使用管理员登录')
        data = parameter_required(('password', ))
        hash_pass = generate_password_hash(data.get('password'))
        admin = self.suser.update_admin_by_adid(request.user.id, {
            'ADpassword':hash_pass
        })
        return jsonify({
            'message': '修改成功',
            'status': 200
        })

