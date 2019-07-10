#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/7 3:52
@Author  : miaoweiwei
@File    : __init__.py.py
@Software: PyCharm
@Desc    : 
"""
import logging
import os
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
from flask_socketio import SocketIO
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_cors import CORS
from flask_babel import lazy_gettext as _l  # 这个新函数将文本包装在一个特殊的对象中，这个对象会在稍后的字符串使用时触发翻译。
from app.algorithm import dataprocessing
from config import Config
from app import algorithm

# # 设置只是用CPU
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# web初始化
app = Flask(__name__)
app.config.from_object(Config)  # 通知Flask读取并使用配置文件
CORS(app, resources=r'/*')  # 解决跨域访问的问题，# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
bootstrap = Bootstrap(app)  # CSS框架Bootstrap初始化
moment = Moment(app)  # 日期和时间转换成插件格式化
babel = Babel(app)  # Flask-Babel正是用于简化翻译工作的
socketio = SocketIO(app)
fruit_name_dic = {"apple": "苹果", "banana": "香蕉", "cucumber": "黄瓜", "eggplant": "茄子", "kiwifruit": "奇异果",
                  "maize": "玉米", "mushroom": "蘑菇", "orange": "橙子", "pineapple": "菠萝", "pitaya": "火龙果",
                  "unknown": "未知的水果"}

# 算法初始化
dataprocessing.init_repository()  # 初始化数据库
al = algorithm
yolo, graph = al.algorithm_init()  # 在web项目中使用algorithm时能使用这个，不然会加载多次模型

# 日志初始化
if not app.debug and app.config['MAIL_SEND']:  # 调试的时候不记录日志
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()

        mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        fromaddr = app.config['MAIL_USERNAME']
        toaddrs = app.config['ADMINS']
        subject = "Fruit Supermarket Failure"
        credentials = auth
        mail_handler = SMTPHandler(mailhost, fromaddr, toaddrs, subject,
                                   credentials=credentials,
                                   secure=secure,
                                   timeout=10)
        # 设置要发送邮件日志的格式
        mail_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
        mail_handler.setLevel(logging.ERROR)  # 设置级别
        mail_handler.set_name("failure email")  # 设置该条日志配置的名称
        app.logger.addHandler(mail_handler)

        # 记录日志
        if not os.path.exists('logs'):
            os.mkdir('logs')
        # 设置每个日志文件10M，总共备份10个日志文件
        file_handler = RotatingFileHandler('logs/smartscales.log', maxBytes=1024 * 1024 * 10, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Smart scales startup')  # 记录一条日志


# localeselector 装饰器。为每个请求调用装饰器函数以选择用于该请求的语言
@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES']) # 会根据浏览器的设置显示语言
    return 'zh'  # 这样会使所有的浏览器都显示为中文


# 最下面的导入是解决循环导入的问题
from app import routes, errors
