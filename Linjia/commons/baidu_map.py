# -*- coding: utf-8 -*-
import requests

from Linjia.commons.error_response import SYSTEM_ERROR
from Linjia.configs.baidumap import BD_AK

class BdMap(object):
    def __init__(self, origins, destinations, perprice=None):
        self.perprice = perprice
        self.api = u'http://api.map.baidu.com/routematrix/v2/driving?' \
                   u'ak={}&origins={}&destinations={}'.format(BD_AK, origins.replace(' ', ''), destinations.replace(' ', ''))
        self.data = self.http()

    def http(self):
        data = requests.get(self.api).json()
        if data.get('status') == 0:
            return data.get('result')[0]
        raise SYSTEM_ERROR(u'baidu api error{}: '.format(data.get('message')))

    @property
    def distance(self):
        return self.data.get('distance').get('value')  # 米

    @property
    def duration(self):
        return self.data.get('duration').get('text')  # 驾车时间估算

    @property
    def price(self):
        return '%2f' % (self.perprice * float(self.distance) / 1000)  # 价格


if __name__ == '__main__':
    bd = BdMap('40.056878,116.30815', '44.056878,116.3081')
    print(bd.price)