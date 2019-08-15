#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/1 23:30
@Author  : miaoweiwei
@File    : config.py
@Software: PyCharm
@Desc    : 配置文件
"""
import os
import uuid
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))  # 该应用程序的根目录
# 创建一个 .env 文件并在其中写入应用所需的所有环境变量了
# 不要将 .env 文件加入到源代码版本控制中，这非常重要。否则，一旦你的密码和其他重要信息上传到远程代码库中后，你就会后悔莫及.
# .env文件可以用于所有配置变量，但是不能用于Flask命令行的FLASK_APP和FLASK_DEBUG环境变量，
# 因为它们在应用启动的早期（应用实例和配置对象存在之前）就被使用了。
load_dotenv(os.path.join(basedir, '.env'))  # 不能存放对Flask设置的配置


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # Post请求不能少

    # 数据库配置
    # Flask-SQLAlchemy插件从SQLALCHEMY_DATABASE_URI配置变量中获取应用的数据库的位置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://microblog:123456@127.0.0.1:3306/fruit_supermarket"

    # SQLALCHEMY_TRACK_MODIFICATIONS配置项用于设置数据发生变更之后是否发送信号给应用，我不需要这项功能，因此将其设置为False。
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮件配置
    MAIL_SEND = False  # 是否发送邮件
    MAIL_SERVER = 'smtp.qq.com'  # 服务器
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True  # TLS 发送日志使用这种方式使用Message发送邮件也可以使用这种方式
    MAIL_PORT = 587
    MAIL_USERNAME = '1353263604@qq.com'
    MAIL_PASSWORD = 'uhuobgoaynquhdeb'  # 该密码要到qq邮箱的设置中开启 POP3/SMTP 和 IMAP/SMTP
    FLASK_MAIL_SENDER = '1353263604@qq.com'
    ADMINS = ['1353263604@qq.com', '1000460675 @ smail.shnu.edu.cn']  # ADMINS配置变量是将收到错误报告的电子邮件地址列表

    # 跟踪支持的语言列表
    LANGUAGES = ['zh', 'en']  # 中文，英文

    # 识别图片的保存路径
    PHOTO_PATH = "photos"
