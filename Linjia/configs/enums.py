# -*- coding: utf-8 -*-

__all__ = ['FACE_CONFIG', 'ROSTATUS', 'GENDER_CONFIG', 'RENT_TYPE', 'DECORATOR_STYLE',
           'SERVER_STATUS', 'COMPLAIN_STATUS', 'PROVIDE_HOUSE_STATUS']

FACE_CONFIG = {
    1: '东', 2: '东南', 3: '南', 4: '西南', 5: '西', 6: '西北', 7: '北', 8: '东北', 0: '未知'
}

ROSTATUS = {
    0: '待审核', 1: '配置中(可预订)', 2: '可入住', 3: '转租', 4: '实习', 5: '已入住'
}

GENDER_CONFIG = {
    0: '男', 1: '女'
}

RENT_TYPE = {
    0: '合租', 1: '整租', 2: '公寓', 3: '民宿'
}

DECORATOR_STYLE = {
    0: '毛坯', 1: '简装', 2: '精装', 3: '豪华'
}

SERVER_STATUS = {  # 搬家订单状态
    0: '待支付', 1: '等待服务', 2: '服务完成', 3: '取消'
}

COMPLAIN_STATUS = {  # 用户投诉状态
    0: '未处理', 1: '已处理'
}

PROVIDE_HOUSE_STATUS = {
    0: '未查看', 1: '已查看', 2: '待处理', 3: '已处理'
}
