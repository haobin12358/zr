# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from flask import request, current_app

from Linjia.commons.error_response import NOT_FOUND, TOKEN_ERROR, PARAMS_ERROR
from Linjia.commons.params_validates import parameter_required
from Linjia.commons.success_response import Success
from Linjia.commons.token_handler import is_admin
from Linjia.configs.enums import FACE_CONFIG, RENT_TYPE
from Linjia.configs.timeformat import format_for_db
from Linjia.control.base_control import BaseRoomControl
from Linjia.service import SRoom, SUser, SCity, SIndex


class CRoom(BaseRoomControl):
    def __init__(self):
        self.sroom = SRoom()
        self.suser = SUser()
        self.scity = SCity()
        self.sindex = SIndex()

    def get_list(self):
        # todo 位置, 地铁, 附近
        args = request.args.to_dict()
        args_dict = {}
        if not args:
            args = {}
        args_dict['page'] = int(args.get('page', 1))  # 页码
        args_dict['count'] = int(args.get('count', 15))  # 取出条数
        # 租赁方式, 合租整租公寓民宿
        args_dict['type'] = args.get('type')
        # 装修风格 0 毛坯, 1简装, 2: 精装, 3: 豪华
        style = args.get('style').split('|') if 'style' in args else []
        # 租金
        args_dict['lowprice'] = args.get('lowprice')
        args_dict['highprice'] = args.get('highprice')
        # 朝向 face=1|2|3 ==> [1, 2, 3]
        face_args = args.get('face').split('|') if 'face' in args else []
        # 展现方式 image or video
        args_dict['show_type'] = args.get('show_type')
        # 房型 一室,二室,三室,五室以上
        args_dict['bed_count'] = args.get('bed_count').split('|') if 'bed_count' in args else None
        # 城市编号
        args_dict['city_id'] = args.get('city_id')
        # 区
        args_dict['area_id'] = args.get('area_id')
        # 地铁
        args_dict['subway'] = args.get('subway')
        # 小区
        args_dict['villege'] = args.get('villege')
        print(args_dict)
        admin = True if is_admin() else None

        args_dict = {
            k: v for k, v in args_dict.items() if v is not None
        }
        room_detail_list = self.sroom.get_room_list_filter(args_dict, admin, style=style, face_args=face_args)
        request.subway = args.get('subway')
        map(self._fill_detail_for_list, room_detail_list)
        map(self._fill_house_info, room_detail_list)  # 楼层和规格
        map(lambda x: x.fill(self.sroom.get_tags_by_roid(x.ROid), 'tags', hide=('ROid', )), room_detail_list)  # 填充tag信息
        map(lambda x: x.fill(self.sindex.is_room_showinindex_by_roid(x.ROid), 'show_index'), room_detail_list)  # 是否显示在首页
        for room in room_detail_list:
            if room.ROdistance in ['无', u'无']:
                room.fill(None, 'ROdistance')
        page_count = getattr(request, 'page_count')
        all_count = getattr(request, 'all_count')
        data = Success(u'获取房源列表成功', data=room_detail_list, page_count=page_count, all_count=all_count)
        return data

    def get_detail(self):
        """房源详细信息"""
        data = parameter_required(('roid', ))
        roid = data.get('roid')
        room = self.sroom.get_room_by_roid(roid)
        if not room:
            raise NOT_FOUND(u'房源不存在')
        self._fill_house_info(room)  # 楼层和规格
        self._fill_roomate_info(room)  # 室友信息
        room.fill(self.sroom.get_room_equirment_by_roid(room.ROid), 'equirment', hide=('IConid', 'REid', 'ROid'))
        room.fill(self.sroom.get_room_media_by_roid(room.ROid), 'media')
        room.fill(self.scity.get_city_by_city_id(room.ROcitynum), 'city')
        room.fill(self.scity.get_areainfo_by_id(room.ROareanum), 'area')
        room.ROface = FACE_CONFIG.get(room.ROface, u'未知')
        room.ROrenttype = RENT_TYPE.get(room.ROrenttype, u'未知')
        room.fill(self.sroom.get_tags_by_roid(roid), 'tags', hide=('ROid', ))   # 填充tag信息
        self._fix_villege_subway_info(room)
        room.add('ROisdelete', 'ROcreatetime', 'ROcitynum')
        return Success(u'获取房源信息成功', room)

    def get_detail_the_same_like_add(self):
        """房源信息接口2"""
        data = parameter_required(('roid', ))
        roid = data.get('roid')
        room = self.sroom.get_house_by_hoid(roid)
        if not room:
            raise NOT_FOUND(u'房源不存在')
        # room.fill(self.sroom.get_house_by_hoid(room.HOid), 'house')  # 楼层和规格
        self._fill_house_info(room)  # 楼层和规格
        self._fill_roomate_info(room)  # 室友信息
        room.fill(self.sroom.get_room_equirment_by_roid(room.ROid), 'equirment', hide=('IConid', 'REid', 'ROid'))
        room.fill(self.sroom.get_room_media_by_roid(room.ROid), 'media')
        room.fill(self.scity.get_city_by_city_id(room.ROcitynum), 'city')
        room.ROface = FACE_CONFIG.get(room.ROface, u'未知')
        room.ROrenttype = RENT_TYPE.get(room.ROrenttype, u'未知')
        room.add('ROisdelete', 'ROcreatetime', 'ROcitynum')
        return Success(u'获取房源信息成功', room)

    def get_oppener_city(self):
        """获取开放城市"""
        data = parameter_required()
        hot = data.get('hot')  # 是否热门
        citys = self.scity.get_roomoppencitylist()
        if hot == 'true':
            citys = list(filter(lambda x: x.ishot, citys))
        map(lambda x: x.fill(self.scity.get_city_by_city_id(x.city_id).name, 'name'), citys)
        return Success(u'获取城市列表成功', {
            'citys': citys
        })

    def get_area_by_citynum(self):
        args = parameter_required(('city_id', ))
        city_id = args.get('city_id')
        area_list = self.scity.get_area_list_by_cityid(city_id)
        map(lambda x: x.hide('_id'), area_list)
        return Success(u'获取城市成功', {
            'area_list': area_list
        })

    def get_subwayline_by_citynum(self):
        """获取城市内的地铁线路, 只获得线路, 暂不获得站点"""
        data = parameter_required(('city_id', ))
        city_id = data.get('city_id')
        subway_line = self.scity.get_subwayline_by_city_id(city_id)
        # map(lambda x: x.fill(
        #     self.scity.get_subwayposition_by_line_id(x.subwaylineid),
        #     'positions'
        # ), subway_line)
        return Success(u'获取地铁信息成功', subway_line)

    def get_subway_potion_by_lineid(self):
        """获取地铁线路的站点"""
        data = parameter_required(('line_id', ))
        line_id = data.get('line_id')
        line = self.scity.get_subwayline_by_lineid(line_id)
        if not line:
            raise NOT_FOUND(u'不存在的线路')
        positions = self.scity.get_subwayposition_by_line_id(line.subwaylineid)
        # 过滤空的地铁站
        positions = list(filter(lambda x: x.position, positions))
        return Success(u'获取站点信息成功', positions)

    def add_joinroom_banner(self):
        """添加友家轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('jrbimage', 'jrbsort', ), others='ignore')
        data['jrbid'] = str(uuid.uuid4())
        model_bean = self.sroom.add_model('JoinRoomBanner', data, return_fields=('JRBid', 'JRBimage', 'JRBsort'))
        for k in model_bean.keys():
            if k[0].isupper():
                # 字段转小写
                model_bean[k.lower()] = model_bean[k]
                model_bean.pop(k)
        return Success(u'添加成功', model_bean)

    def get_joinroom_banner(self):
        """获取友家轮播图"""
        join_room_banner_list = self.sroom.get_joinroom_banner_list()
        return Success(u'获取轮播图成功', join_room_banner_list)

    def delete_joinroom_banner(self):
        """删除友家轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('jrbid', ))
        jrbid = data.get('jrbid')
        joinroom = self.sroom.delete_joinroom_banner(jrbid)
        msg = u'删除成功' if joinroom else u'要删除的对象不存在'
        return Success(msg, {
            'jrbid': jrbid
        })

    def get_homestay_banner(self):
        """获取民宿页的轮播图"""
        homestay_banner_list = self.sroom.get_homestay_banner_list()
        return Success(u'获取轮播图成功', homestay_banner_list)

    def add_homestay_banner(self):
        """添加民宿页的轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('hsbimage', 'hsbsort'), others='ignore')
        data['hsbid'] = str(uuid.uuid4())
        model_bean = self.sroom.add_model('HomeStayBanner', data)
        return Success(u'添加成功', {
            'hsbid': data['hsbid']
        })

    def delete_homestay_banner(self):
        """删除民宿页的轮播图"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('hsbid',))
        hsbid = data.get('hsbid')
        homestaybanner = self.sroom.delete_homestay_banner(hsbid)
        msg = u'删除成功' if homestaybanner else u'要删除的对象不存在'
        return Success(msg, {
            'hsbid': hsbid
        })

    def add_homestay_copywriting(self):
        """添加, 这个需要问前端, 怎么获取"""
        pass

    def get_villegeinfo_by_namekeyword(self):
        """根据公寓关键字获取公寓信息, 主要是地铁距离"""
        data = parameter_required(('kw', ))
        kw = data.get('kw')
        info = self.sroom.get_villege_info_by_name(kw)
        return Success(u'获取成功', info)

    def add_room(self):
        """添加房源"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        required = ('roname', 'roimage', 'roareanum', 'roface', 'roarea', 'roshowprice', 'roshowpriceunit',
                    'rorenttype', 'rodecorationstyle', 'rocitynum', 'roareanum', 'rosubwayaround',
                     'house', 'villegeid', 'medias', 'stfid')
        data = parameter_required(required, forbidden=('roid', 'hoid', ))
        house = data.pop('house', None)
        medias = data.pop('medias', [])
        tags = data.pop('tags', [])
        roomrequirment = data.pop('roomrequirment', None)
        # 是否存在小区
        villege = self.sroom.get_villege_info_by_id(data.get('villegeid'))
        if not villege:
            raise NOT_FOUND(u'请添加小区信息')
        # 初始化添加参数
        mod = {}
        roid = str(uuid.uuid4())
        create_time = datetime.strftime(datetime.now(), format_for_db)
        house['hoid'] = data['hoid'] = data['roid'] = roid
        # 添加房源
        data['ROcreatetime'] = create_time
        data['ROdistance'] = villege.subway_primary
        data['ROaroundequirment'] = villege.around
        data['ROsubwayposionname'] = villege.position
        mod['Room'] = data
        # 添加媒体
        try:
            map(lambda x: x.setdefault('roid', roid), medias)
            map(lambda x: x.setdefault('reid', str(uuid.uuid4())), medias)
            mod['RoomMedia'] = medias
        except Exception as e:
            raise PARAMS_ERROR(u'medias参数有误')
        # 添加house
        houseinfo_required = ('hofloor', 'hototalfloor', 'hobedroomcount', 'hoparlorcount')
        parameter_required(houseinfo_required, datafrom=house)
        house['VIid'] = data.get('villegeid')
        mod['House'] = house
        # 添加tag
        try:
            map(lambda x: x.setdefault('roid', roid), tags)
            map(lambda x: x.setdefault('rtid', str(uuid.uuid4())), tags)
            mod['RoomTag'] = tags
        except Exception as e:
            raise PARAMS_ERROR(u'tags参数有误')
        # 添加设备:
        if roomrequirment:
            roomrequirment['roid'] = roid
            roomrequirment['reid'] = str(uuid.uuid4())
            mod['RoomEquirment'] = roomrequirment
        self.sroom.add_models(mod)
        return Success(u'添加成功', {
            'roid': roid
        })

    def update_room(self):
        """更新房源信息"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('roid', ))
        roid = data.get('roid')
        # 房源主体的参数
        # house信息
        # medias信息
        # tags
        # roomequi设备
        # 公寓信息
        house = data.pop('house', None)
        medias = data.pop('medias', [])
        tags = data.pop('tags', [])
        roomrequirment = data.pop('roomrequirment', None)
        room = self.sroom.get_room_by_roid(roid)
        if not room:
            raise NOT_FOUND(u'无此房源')
        room_data = {
            'ROname': data.get('roname'),
            'ROimage': data.get('roimage'),
            'ROareanum': data.get('roareanum'),
            'ROface': data.get('roface'),
            'ROarea': data.get('roarea'),
            'ROshowpriceunit': data.get('roshowpriceunit'),
            'ROrenttype': data.get('rorenttype'),
            'ROdecorationstyle': data.get('rodecorationstyle'),
            'ROshowprice': data.get('roshowprice'),
            'ROcitynum': data.get('rocitynum'),
            'ROsubwayaround': data.get('rosubwayaround'),
            'STFid': data.get('stfid')
        }
        room_data = {
            k: v for k, v in room_data.items() if v is not None
        }
        if not room_data:
            raise PARAMS_ERROR('修改room需要的参数缺失')
        room_updated = self.sroom.update_room_by_roid(roid, room_data)
        print('更新了room')
        if house:
            hoid = room.ROid
            houseinfo_required = ('hofloor', 'hototalfloor', 'hobedroomcount', 'hoparlorcount')
            parameter_required(houseinfo_required, datafrom=house)
            house_data = {
                'HOfloor': house.get('hofloor'),
                'HOtotalfloor': house.get('hototalfloor'),
                'HObedroomcount': house.get('hobedroomcount'),
                'HOparlorcount': house.get('hoparlorcount'),
            }
            house_updated = self.sroom.update_house_by_hoid(hoid, house_data)
        if medias:
            # 此处接受到的media数据是没有删除的和信添加的, 删除的将不会在传过来
            # 此处有点罗嗦, 只需删除原来的数据, 再重新添加即可
            deleted = self.sroom.delete_room_media_by_roid(roid)
            for new_media in medias:
                new_media['reid'] = str(uuid.uuid4())
                new_media['roid'] = roid
                self.sroom.add_model('RoomMedia', new_media)
                print('添加多媒体') 
        if tags:
            # 删除原来的tag
            self.sroom.delete_tag_by_roid(roid)
            print('删除了原来的tag')
            mod = {} 
            mod['RoomTag'] = []
            for tag in tags:
                tag['roid'] = roid
                tag['rtid'] = str(uuid.uuid4())
                mod['RoomTag'].append(tag)
            self.sroom.add_models(mod)
            print('添加tag')
        if roomrequirment:
            self.sroom.delete_room_equirment_by_roid(roid)
            print('删除了原来的设备')
            roomrequirment['roid'] = roid
            roomrequirment['reid'] = str(uuid.uuid4())
            self.sroom.add_model('RoomEquirment', roomrequirment)
            print('修改设备')
        if 'villegeid' in data:
            hoid = room.HOid
            # house = self.sroom.get_house_by_hoid(hoid)
            villege = self.sroom.get_villege_info_by_id(data.get('villegeid'))
            if not villege:
                raise PARAMS_ERROR(u'villege id有误')
            self.sroom.update_house_by_hoid(hoid, {
                'VIid': data.get('villegeid')
            })
        return Success(u'修改成功', {
            'roid': roid
        })

    def delete_room(self):
        """删除房源"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('roid', ))
        roid = data.get('roid')
        deleted = self.sroom.delete_room_by_roid(roid)
        # 同时取消在首页的显示
        self.sindex.delete_room_show_by_roid(roid)
        msg = u'删除成功' if deleted else u'无此记录'
        return Success(msg, {
            'roid': roid
        })

    def add_bedroom(self):
        """添加卧室, 以及卧室入住信息"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('roid', 'bbrnum'), forbidden=('bbrid', 'bbrstatus'))
        room = self.sroom.get_room_by_roid(data.get('roid'))
        mod = {}
        data['bbrid'] = str(uuid.uuid4())
        mod['BedroomBehindRoom'] = data
        if not room:
            raise NOT_FOUND(u'不存在的房源id')
        if 'bbrshowprice' in data:
            # 卧室未租出
            data['BBRstatus'] = 2
        elif 'usgender' in data:
            # 已经租出
            data['BBRstatus'] = 5
            mod['UserBedroomBehindRoom'] = {
                'UBBRid': str(uuid.uuid4()),
                'BBRid': data['bbrid'],
                'USgender': data.get('usgender')
            }
        else:
            raise PARAMS_ERROR(u'缺少必要的参数')
        self.sroom.add_models(mod)
        return Success(u'添加成功', {
            'bbrid': data['bbrid']
        })
    
    def update_bedroom(self):
        """更新卧室信息, 比如改为已租出, 或者价格之类"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('bbrid', ))
        bbrid = data.pop('bbrid')
        bedroom = self.sroom.get_bedroom_by_bbrid(bbrid)
        if not bedroom:
            raise NOT_FOUND(u'此卧室不存在')
        if 'bbrshowprice' in data:
            # 需要改为未租出的状态
            self.sroom.update_bedroom_by_bbrid(bbrid, {
                'BBRshowprice': data.get('bbrshowprice'),
                'BBRshowpriceunit': data.get('bbrshowpriceunit', 'month'),
                'BBRstatus': 2
            })
            userbedroom = self.sroom.update_roomates_info_by_bbrid(bbrid, {
                'UBBRstatus': 1
            })  # 同时需要更新卧室住户的状态
            msg = u'改为未入住成功'
        elif 'usgender' in data:
            # 需要改为入住状态
            self.sroom.update_bedroom_by_bbrid(bbrid, {
                "BBRstatus": 5
            })
            # 同时需要添加入住信息, 修改以往的入住信息为已搬(如果有)
            self.sroom.update_roomates_info_by_bbrid(bbrid, { 'UBBRstatus': 1 })
            model_dict = dict(
                UBBRid=str(uuid.uuid4()),
                BBRid=bbrid,
                USgender=data.get('usgender')
            )
            mod = dict(
                UserBedroomBehindRoom=model_dict
            )
            self.sroom.add_models(mod)
            msg = u'改为已入住成功'
        else:
            raise PARAMS_ERROR(u'缺少必要的参数')
        return Success(msg, {
            'bbrid': bbrid     
        })

    def delete_bedroom(self):
        """删除卧室"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('bbrid', ))
        deleted = self.sroom.update_bedroom_by_bbrid(data.get('bbrid'), {
            'BBRisdelete': 1
        })
        msg = u'删除成功' if deleted else u'无此记录'
        return Success(msg, {
            'bbrid': data.get('bbrid')
        })

    def add_villegetinfo(self):
        """添加小区信息"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id', 'name', ), forbidden=('id', ))
        data['id'] = str(uuid.uuid4())
        if 'subway' not in data:
            data['subway'] = data.get('subway_primary')
        added = self.sroom.add_model('VillegeInfoAndSubway', data, return_fields=(['id', 'name']))
        return added   # 返回值风格出现失误, 既然前端已经用了就不改了吧

    def update_villeginfo(self):
        """修改小区信息"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('id', ))
        updated = self.sroom.update_villege_info(data.get('id'), data)
        msg = u'更新成功' if updated else u'无此记录'
        return Success(msg, {
            'id': data.get('id')
        })

    def add_room_opencity(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id', ))
        city_id = data.get('city_id')
        room_city = self.scity.is_room_open_city(city_id)
        if room_city:
            raise PARAMS_ERROR(u'重复添加')
        data['rcid'] = str(uuid.uuid4())
        added = self.scity.add_model('RoomCity', data)
        return Success(u'添加房源开放城市成功', {'city_id': city_id})

    def del_room_opencity(self):
        """取消房源开放城市"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使管理员登录')
        data = parameter_required(('city_id', ))
        city_id = data.get('city_id')
        deleted = self.scity.delete_roomoppencity(city_id)
        msg = u'取消房源服务成功' if deleted else u'无此记录'
        return Success(msg, {'city_id': city_id})

    def add_hot_city(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id', ))
        city_id = data.get('city_id')
        updated = self.scity.update_room_open_city(city_id, {
            'ishot': True
        })
        msg = u'更新成功' if updated else u'该城市暂未开通服务'
        return Success(msg, {
            'city_id': city_id
        })

    def cancle_hot_city(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('city_id', ))
        city_id = data.get('city_id')
        updated = self.scity.update_room_open_city(city_id, {
            'ishot': False
        })
        msg = u'更新成功' if updated else u'该成功暂未开通服务'
        return Success(msg, {
            'city_id': city_id
        })
    

class CGuide(CRoom):
    """入住指南"""
    def add_customerguide(self):
        """添加入住指南"""
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('cgtitle', 'cgtext', 'cgsort'), forbidden=('cgid', ))
        data['cgid'] = str(uuid.uuid4())
        added = self.sroom.add_model('CustomerGuide', data)
        return Success(u'添加成功', {
            'cgid': data.get('cgid')
        })

    def get_list(self):
        guide_list = self.sroom.get_guide_list()
        map(lambda x: x.hide('CGisdelete'), guide_list)
        return Success(u'获取列表成功', {
            'guides': guide_list
        })

    def update_guide(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('cgid', ), forbidden=('CGisdelete', ))
        cgid = data.get('cgid')
        update_data = {
            'CGtitle': data.get('cgtitle'),
            'CGtext': data.get('cgtext'),
            'CGsort': data.get('cgsort'),
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}
        updated = self.sroom.update_guide(cgid, update_data)
        msg = u'更新成功' if updated else u'无此记录'
        return Success(msg, {
            'cgid': cgid
        })

    def delete_guide(self):
        if not is_admin():
            raise TOKEN_ERROR(u'请使用管理员登录')
        data = parameter_required(('cgid', ))
        cgid = data.get('cgid')
        deleted = self.sroom.update_guide(cgid, {
            'CGisdelete': True
        })
        msg = u'删除成功' if deleted else u'无此记录'
        return Success(msg, {
            'cgid': cgid
        })
        
    def get_guide(self):
        data = parameter_required(('cgid', ))
        cgid = data.get('cgid')
        guide = self.sroom.get_guide_by_cgid(cgid)
        if not guide:
            raise NOT_FOUND(u'不存在的指南')
        guide.hide('CGisdelete')
        return Success(u'获取指南成功', {
            'guide': guide
        })

