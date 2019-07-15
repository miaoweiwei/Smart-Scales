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


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # Post请求不能少

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/fruit_supermarket'

    # 邮件配置
    MAIL_SEND = True  # 是否发送邮件
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
