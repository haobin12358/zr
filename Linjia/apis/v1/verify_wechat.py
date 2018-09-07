# *- coding:utf8 *-
# -*- coding: utf-8 -*-
import hashlib

from flask import Flask, request, abort, redirect, jsonify, Blueprint

from Linjia.commons.base_error import BaseError
from Linjia.configs.wxconfig import WXTOKEN
app = Flask(__name__)
wechat = Blueprint(__name__, 'wechat')



@wechat.before_request
def prepare():
    """验证消息"""
    args = request.args.to_dict()
    if not args:
        return 'args is missed '
    my_signature = args.get('signature')  # 获取携带的signature参数
    my_timestamp = args.get('timestamp')  # 获取携带的timestamp参数
    my_nonce = args.get('nonce')
    my_echostr = args.get('echostr')  # 获取携带的echostr参数
    token = WXTOKEN
    # 进行字典排序
    data = [token, my_timestamp, my_nonce]
    data.sort()
    # 拼接成字符串
    temp = ''.join(data)
    # 进行sha1加密
    mysignature = hashlib.sha1(temp).hexdigest()
    # 加密后的字符串可与signature对比，标识该请求来源于微信
    print('正在验证消息')
    if my_signature != mysignature:
        raise BaseError('签名有误')


@wechat.route('/wechat', methods=['GET', 'POST'])
def verfiry_domain_setting():
    """公众号回复测试"""
    if request.method == 'GET':
        my_echostr = request.args.get('echostr')  # 获取携带的echostr参数
        return my_echostr


def register_blueprint(app):
    app.register_blueprint(wechat)
