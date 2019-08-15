#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/8/10 9:26
@Author  : miaoweiwei
@File    : __init__.py.py
@Software: PyCharm
@Desc    : 
"""
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l  # 这个新函数将文本包装在一个特殊的对象中，这个对象会在稍后的字符串使用时触发翻译。
# from flask_socketio import SocketIO

from config import Config

db = SQLAlchemy()  # db对象来表示数据库
migrate = Migrate()  # 数据库迁移引擎migrate
login = LoginManager()  # 登录管理初始化
login.login_view = 'auth.login'  # Flask-Login需要知道哪个视图函数用于处理登录认证
# 为了确保这个消息也能被翻译用_l()函数进行延迟处理：
login.login_message = _l('Please log in to access this page.')
mail = Mail()  # 创建邮件实例，该邮件实例用于发送更改密码验证信息
bootstrap = Bootstrap()  # CSS框架Bootstrap初始化
moment = Moment()  # 日期和时间转换成插件格式化
babel = Babel()  # Flask-Babel正是用于简化翻译工作的
# socketio = SocketIO()


# 应用程序工厂函数
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # 通知Flask读取并使用配置文件

    db.init_app(app)  # db对象来表示数据库

    migrate.init_app(app, db)  # 数据库迁移引擎migrate
    login.init_app(app)  # 登录管理初始化
    mail.init_app(app)  # 创建邮件实例，该邮件实例用于发送更改密码验证信息
    bootstrap.init_app(app)  # CSS框架Bootstrap初始化
    moment.init_app(app)  # 日期和时间转换成插件格式化
    babel.init_app(app)  # Flask-Babel正是用于简化翻译工作的

    # socketio.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)  # 向应用注册错误blueprint

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')  # url_prefix。 这完全是可选的,Flask提供了给blueprint的路由添加URL前缀的选项

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp  # 向应用注册API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

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
            file_handler = RotatingFileHandler('logs/FruitSupermarket.log', maxBytes=1024 * 1024 * 10, backupCount=10)
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Smart Fruit Supermarket Startup')  # 记录一条日志
    return app
