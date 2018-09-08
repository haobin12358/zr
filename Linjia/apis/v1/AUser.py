# *- coding:utf8 *-
from flask import jsonify

from Linjia.commons.base_resource import Resource
from Linjia.control import CUser


class AUser(Resource):
    def __init__(self):
        self.cuser = CUser()

    def get(self, user):
        print(user)
        apis = {
            'wechat_login': self.cuser.wechat_login,
            'wexin_callback': self.cuser.wexin_callback,
            'get_wechat_config': self.cuser.get_wx_config
        }
        res = apis[user]()
        return jsonify(res)

    def post(self, user):
        apis ={
            'admin_login': self.cuser.admin_login
        }
        res = apis[user]()
        return jsonify(res)