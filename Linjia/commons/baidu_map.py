# -*- coding: utf-8 -*-
import requests

from Linjia.commons.error_response import SYSTEM_ERROR
from Linjia.configs.baidumap import BD_AK


class BdMap(object):
    def __init__(self, location):
        location_list = location.split(',')
        location_list = sorted(location_list, reverse=True)
        location = ','.join(location_list)
        self.api = u'http://api.map.baidu.com/geocoder/v2/?ak={}&location={}&output=json'.format(BD_AK, location)
        self.data = self.http()

    def http(self):
        data = requests.get(self.api).json()
        if data.get('status') == 0:
            return data.get('result').get('addressComponent')
        raise SYSTEM_ERROR(u'baidu api error{}: '.format(data.get('message')))
    
    @property
    def area_code(self):
        return self.data.get('adcode')
    
    @property
    def city_id(self):
        return self.area_code[:-2] + '00'

if __name__ == '__main__':

    bd = BdMap('30.231565,120.256622')
    print(bd.city_id)
    print(bd.area_code)
