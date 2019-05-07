# *- coding:utf8 *-
import os
SECRET_KEY = '4xxxxxxC2tAoH6fhI17OdNk0u93ez5DswvGVyprlFWa8PBgcEZiSLnjqQmRTxJUMKXYb'
TOKEN_EXPIRATION = 3600 * 222  # token过期时间(秒)
DEBUG = True
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CACHE_TYPE = 'redis'
CACHE_KEY_PREFIX = 'linjia_server'
CACHE_DEFAULT_TIMEOUT = 3600
if __name__ == '__main__':
    print(BASEDIR)
