# -*- coding: utf-8 -*-
import os
APPID = os.environ.get('APPID', 'appid')
APPSECRET = os.environ.get('APPSECRET', 'appsecret')
WXTOKEN = os.environ.get('WXTOKEN', 'token')
WXSCOPE = 'snsapi_userinfo'
MCH_KEY = os.environ.get('MC_K', '')
MCH_ID = os.environ.get('MC_ID', '')