# -*- coding: utf-8 -*-
from weixin.mp import WeixinMP

mp = WeixinMP('wxa7109d8534a2d837', 'd9c41da55f5d2710a220f1d')
print(mp.access_token)
print(mp.jsapi_sign(url='http://www.baidu.com'))
