# -*- coding: utf-8 -*-

__all__ = ['FACE_CONFIG', 'PAY_PERIOD', 'HYTING_TYPE', 'ROstatus', 'GENDER_CONFIG', 'RENT_TYPE']

FACE_CONFIG = {
    1: '东',
    2: '东南',
    3: '南',
    4: '西南',
    5: '西',
    6: '西北',
    7: '北',
    8: '东北',
    0: '未知'
}

PAY_PERIOD = {
    0: '月付',
    1: '季付',
    2: '半年付',
    3: '一年付',
    4: '自如客分期',
    5: '其它'
}

HYTING_TYPE = {
    0: '不供暖',
    1: '集体供暖',
    2: '独立供暖',
    3: '中央供暖'
}

ROstatus = {
    0: '待审核',
    1: '配置中(可预订)',
    2: '可入住',
    3: '转租',
    4: '实习',
    5: ''
}

GENDER_CONFIG = {
    0: '男',
    1: '女'
}

RENT_TYPE = {
    0: '合租',
    1: '整租',
    2: '精选',
    3: '豪宅'
}
