# -*- coding: utf-8 -*-
import os
import uuid
from datetime import datetime

from flask import request

from Linjia.commons.error_response import AUTHORITY_ERROR, NOT_FOUND, SYSTEM_ERROR
from Linjia.commons.params_validates import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_admin
from Linjia.configs.appsettings import BASEDIR
from Linjia.configs.enums import RENT_TYPE
from Linjia.configs.url_config import API_HOST
from Linjia.control.base_control import BaseRoomControl, BaseIndexControl
from Linjia.service import SIndex, SRoom, SCity


class CIndex(BaseRoomControl, BaseIndexControl):
    def __init__(self):
        self.sindex = SIndex()
        self.sroom = SRoom()
        self.scity = SCity()

    def get_banner(self):
        banner_list = self.sindex.get_banner_list()
        return Success('获取成功', banner_list)

    def get_index_room_list(self):
        index_shows = self.sindex.get_rooms_index_show()
        map(self._fill_index_room_detail, index_shows)
        # 分类
        data = dict(
            join_rent=filter(lambda x: x.ROrenttype == RENT_TYPE[0], index_shows),
            whole_rent=filter(lambda x: x.ROrenttype == RENT_TYPE[1], index_shows),
            apartment=filter(lambda x: x.ROrenttype == RENT_TYPE[2], index_shows),
            homestay=filter(lambda x: x.ROrenttype == RENT_TYPE[3], index_shows),
        )
        return Success(u'获取首页信息成功', data)

    def get_index_server(self):
        """获取首页显示的服务"""
        server_index_show = self.sindex.get_index_server()
        return Success(u'获取首页服务成功', server_index_show)

    def add_banner(self):
        """新建轮播图, 必要的参数: 图片地址, 顺序标志, 链接"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required(('ibimage', 'iblink', 'ibsort'), others='ignore')
        data['IBid'] = str(uuid.uuid4())
        self.sindex.add_model('IndexBanner', data)
        return Success(u'添加成功', {
            'ibid': data['IBid']
        })

    def add_room_show(self):
        """新建首页显示的合租整租公寓民宿, 必要的参数 房源id, type, 和顺序: """
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required(('roid', 'rotype', 'rosort'), others='ignore')
        data['RISid'] = str(uuid.uuid4())
        self.sindex.add_model('RoomIndexShow', data)
        return Success(u'添加成功', {
            'risid': data['RISid']
        })

    def add_server_index(self):
        """新建首页显示的服务项目"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required(('sisimage', 'sislink', 'sissort'), others='ignore')
        data['SISid'] = str(uuid.uuid4())
        self.sindex.add_model('ServerIndexShow', data)
        return Success(u'添加成功', {
            'sisid': data['SISid']
        })

    def delete_banner_show(self):
        """删除轮播"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required(('ibid', ))
        banner = self.sindex.delete_banner_show_by_ibid(data.get('ibid'))
        message = u'删除成功' if banner else u'要删除的元素不存在'
        return Success(message, {
            'ibid': data.get('ibid')     
        })

    def delete_room_show(self):
        """删除首页显示的整租或合租房源"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required(('risid', ))
        room_index_show = self.sindex.delete_room_show_by_risid(data.get('risid'))
        message = u'删除成功' if room_index_show else u'要删除的对象不存在'
        return Success(message, {
            'risid': data.get('risid')
        })

    def delete_room_show_by_roid(self):
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required(('roid', ))
        room_index_show = self.sindex.delete_room_show_by_roid(data.get('roid'))
        message = u'取消成功' if room_index_show else u'要取消的房源不在首页'
        return Success(message, {
            'roid': data.get('roid')
        })

    def delete_server_index_show(self):
        """删除首页显示的服务"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required(('sisid', ))
        server_index_show = self.sindex.delete_server_index_show(data.get('sisid'))
        message = u'删除成功' if server_index_show else u'要删除的对象不存在'
        return Success(message, {
            'sisid': data.get('sisid')
        })

    def upload_img(self):
        file = request.files.get('file')
        if not file:
            raise SYSTEM_ERROR(u'上传有误')
        filename = file.filename

        shuffix = os.path.splitext(filename)[-1]
        if self.allowed_file(shuffix):
            newName = self.new_name(shuffix)
            img_name = newName

            time_now = datetime.now()
            year = str(time_now.year)
            month = str(time_now.month)
            day = str(time_now.day)
            newPath = os.path.join(BASEDIR, 'img', year, month, day)
            if not os.path.isdir(newPath):
                os.makedirs(newPath)

            newPath = os.path.join(newPath, newName)
            file.save(newPath)  # 保存图片

            data = '{}/img/{}/{}/{}/{}'.format(API_HOST, year, month, day, img_name)
            return Success(u'上传成功', data)
        else:
            return SYSTEM_ERROR(u'上传有误')

    @staticmethod
    def new_name(shuffix, length=32):
        import string, random
        myStr = string.ascii_letters + '0123456789'
        newName = ''.join(random.choice(myStr) for i in range(length))
        return newName + shuffix

    @staticmethod
    def allowed_file(shuffix):
        return shuffix in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', ]




