# *- coding:utf8 *-
from Linjia.commons.base_resource import Resource
from Linjia.control import CUser


class AUser(Resource):
    def __init__(self):
        self.cuser = CUser()

    def get(self, user):
        print(user)
        apis = {
            # 'wechat_login': self.cuser.wechat_login,
            # 'weixin_callback': self.cuser.weixin_callback,
            'staff_list': self.cuser.get_staff_list,  # 员工
            'get_staff': self.cuser.get_staff_by_id,
            'get_admin_list': self.cuser.get_admin_list,
            'get_user_list': self.cuser.get_user_list,
            'get_one_housekeeper': self.cuser.get_one_housekeeper,
        }
        return apis

    def post(self, user):
        apis = {
            'admin_login': self.cuser.admin_login,
            'get_code': self.cuser.get_code,
            'login': self.cuser.login,
            'get_wechat_config': self.cuser.get_wx_config,
            'update_staff': self.cuser.update_staff,
            'add_staff': self.cuser.add_staff,
            'delete_staff': self.cuser.delete_staff,
            'add_admin': self.cuser.add_admin,
            'freeze_admin': self.cuser.freeze_admin,
            'unfreeze_admin': self.cuser.unfreeze_admin,
        }
        return apis
