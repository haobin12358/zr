# -*- coding: utf-8 -*-
import os
import uuid

from flask import request

from Linjia.commons.error_response import AUTHORITY_ERROR, NOT_FOUND, SYSTEM_ERROR
from Linjia.commons.params_required import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_admin
from Linjia.configs.appsettings import UPLOAD_FOLDER
from Linjia.configs.enums import RENT_TYPE
from Linjia.configs.url_config import HTTP_HOST
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
        data = parameter_required('ibimage', 'iblink', 'ibsort')
        data['IBid'] = str(uuid.uuid4())
        self.sindex.add_model('IndexBanner', **data)
        return Success(u'添加成功', {
            'ibid': data['IBid']
        })

    def add_room_show(self):
        """新建首页显示的合租整租公寓民宿, 必要的参数 房源id, type, 和顺序: """
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('roid', 'rotype', 'rosort')
        data['RISid'] = str(uuid.uuid4())
        self.sindex.add_model('RoomIndexShow', **data)
        return Success(u'添加成功', {
            'risid': data['RISid']
        })

    def add_index_index(self):
        """新建首页显示的服务项目"""


    def delete_banner_show(self):
        """删除轮播"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('ibid')
        banner = self.sindex.delete_banner_show_by_ibid(data.get('ibid'))
        message = u'删除成功' if banner else u'要删除的元素不存在'
        return Success(message, {
            'ibid': data.get('ibid')     
        })

    def delete_room_show(self):
        """删除首页显示的整租或合租房源"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('risid')
        room_index_show = self.sindex.delete_room_show_by_risid(data.get('risid'))
        message = u'删除成功' if room_index_show else u'要删除的对象不存在'
        return Success(message, {
            'risid': data.get('risid')
        })

    def delete_server_index_show(self):
        """删除首页显示的服务"""
        if not is_admin():
            raise AUTHORITY_ERROR('请使用管理员登录')
        data = parameter_required('sisid')
        server_index_show = self.sindex.delete_server_index_show(data.get('sisid'))
        message = u'删除成功' if server_index_show else u'要删除的对象不存在'
        return Success(message, {
            'sisid': data.get('sisid')
        })

    def upload_img(self):
        img_name = None
        # print(request.files)
        file = request.files.get('file')  # 拿到文件对象
        if not file:
            raise SYSTEM_ERROR(u'上传有误')
        filename = file.filename  # 获取上传的图片名称
        shuffix = os.path.splitext(filename)[-1]
        # 获取到名称的后缀
        if self.allowed_file(shuffix):
            # 调用生成随机图片名称的函数
            newName = self.new_name(shuffix)
            img_name = newName
            # 拼凑完整的图片上传路径
            newPath = os.path.join(UPLOAD_FOLDER, 'img', 'banner', newName)
            file.save(newPath)  # 保存图片
            data = HTTP_HOST + '/img/banner/' + img_name
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
        return shuffix in ['.jpg','.jpeg','.png','.gif']

    @staticmethod
    def new_name(shuffix):
        import string, random  # import random
        myStr = string.ascii_letters + '12345678'
        return ''.join(random.choice(myStr) for i in range(20)) + shuffix




