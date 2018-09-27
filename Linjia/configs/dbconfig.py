# -*- coding: utf-8 -*-
import os
database = os.environ.get('LJ_DB_NAME', "ziru")
host = os.environ.get('1LJ_DB_HOST', "127.0.0.1")
port = "3306"
username = os.environ.get('LJ_DB_USER', 'root')
password = os.environ.get('LJ_DB_PWD', 'root')
charset = "utf8"
sqlenginename = 'mysql+pymysql'

print(host)
