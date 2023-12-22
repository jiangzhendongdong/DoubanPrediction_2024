"""
配置信息：'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
"""
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

DIALECT='mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'douban'
SQLALCHEMY_DATABASE_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = True







