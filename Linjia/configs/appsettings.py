# *- coding:utf8 *-
import os

SECRET_KEY = '4C2tAoH6fhI17OdNk0u93ez5DswvGVyprlFWa8PBgcEZiSLnjqQmRTxJUMKXYb'
TOKEN_EXPIRATION = 3600 * 20  # token过期时间(秒)
DEBUG = True
# test
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
MAX_CONTENT_LENGTH = 1024 * 1024 * 64
UPLOAD_FOLDER =  os.getcwd() + '/static'