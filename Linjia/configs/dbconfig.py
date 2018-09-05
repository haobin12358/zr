# -*- coding: utf-8 -*-
import os
database = os.environ.get('DB_NAME', "ziru")
host = os.environ.get('DB_HOST', "127.0.0.1")
port = "3306"
username = os.environ.get('DB_USER', 'username')
password = os.environ.get('DB_PWD', 'password')
charset = "utf8"
sqlenginename = 'mysql+pymysql'