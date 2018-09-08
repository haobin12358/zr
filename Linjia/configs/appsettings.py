# *- coding:utf8 *-
import os
SECRET_KEY = '4C2tAoH6fhI17OdNk0u93ez5DswvGVyprlFWa8PBgcEZiSLnjqQmRTxJUMKXYb'
TOKEN_EXPIRATION = 3600 * 20  # token过期时间(秒)
DEBUG = True
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

if __name__ == '__main__':
    print(UPLOAD_FOLDER)