#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/6/22 13:53
@Author  : miaoweiwei
@File    : models.py
@Software: PyCharm
@Desc    : 数据库模型
"""
import base64
import json
import os
from functools import reduce
from datetime import datetime, timedelta
from hashlib import md5
from time import time
import jwt
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(db.Model):
    """用户表"""
    id = db.Column(db.Integer, primary_key=True)  # 字段 id ，主键
    user_name = db.Column(db.String(64), index=True, unique=True)  # unique表示唯一的
    weixin_id = db.Column(db.String(64), index=True)
    telephone_number = db.Column(db.String(11), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orders = db.relationship("Order", backref="buyer", lazy="dynamic")  # buyer 买家

    # 用db.relationship初始化。这不是实际的数据库字段，而是用户和其动态之间关系的高级视图，因此它不在数据库图表中,
    # 对于一对多关系，db.relationship字段通常在“一”的这边定义，并用作访问“多”的便捷方式。因此，如果我有一个用户实例u，
    # 表达式 u.orders 将运行一个数据库查询，返回该用户的所有订单
    # db.relationship 的第一个参数表示代表关系“多”的类。 backref参数定义了代表“多”的类的实例反向调用“一”的时候的属性名称。
    # 这将会为用户动态添加一个属性 order.buyers，调用它将返回给该用户动态的用户实例。 lazy参数定义了这种关系调用的数据库查询是如何执行的，

    def __repr__(self):
        return '<User {}>'.format(self.user_name)

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码是否正确"""
        return check_password_hash(self.password_hash, password)


# 插件期望应用配置一个用户加载函数，可以调用该函数来加载给定ID的用户
# 使用Flask-Login的@login.user_loader装饰器来为用户加载功能注册函数。
# Flask-Login将字符串类型的参数id传入用户加载函数，
# 因此使用数字ID的数据库需要如上所示地将字符串转换为整数。
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Commodity(db.Model):
    """商品表"""
    id = db.Column(db.Integer, primary_key=True)  # 商品id
    commodity_name = db.Column(db.String(64), index=True, unique=True)  # 商品名称 中文名
    unit_price = db.Column(db.Float)  # 商品单价
    pricing_method = db.Column(db.Enum('weight', 'quantity'), default='weight')  # 计价方式 weight 表示重量 quantity 表示数量
    about = db.Column(db.String(128))  # 商品描述

    def __repr__(self):
        return '<Commodity {}:{}>'.format(self.commodity_name, self.about)


class Terminal(db.Model):
    """终端机器"""
    id = db.Column(db.Integer, primary_key=True)  # 终端 id
    ip = db.Column(db.String(15), index=True, unique=True)  # 终端 ip
    mac = db.Column(db.String(15), index=True, unique=True)  # 终端 mac

    def __repr__(self):
        return '<Terminal id:{} ip:{} mac:{}>'.format(self.id, self.ip, self.mac)


class Order(db.Model):
    """订单表"""
    id = db.Column(db.Integer, primary_key=True)  # 订单id
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 订单产生时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户id
    terminal_id = db.Column(db.Integer, db.ForeignKey('terminal.id'))  # 终端机器id
    order_status = db.Column(db.Enum('unpaid', 'paid'), default='unpaid')  # unpaid 未付款，paid 已付款
    transactions = db.relationship("Transaction", backref="transaction_order", lazy="dynamic")

    def __repr__(self):
        user = User.query.filter_by(id=self.user_id).first()
        username = self.user_id if user is None else user.username
        return '<Order username:{} timestamp:{} transactions:{}>'.format(username, self.timestamp, self.mac)

    def get_total(self):
        total = reduce(lambda x, y: x.sbtotal() + y.sbtotal(), self.transactions)
        return total


class Transaction(db.Model):
    """商品交易表,记录每一种商品的交易"""
    id = db.Column(db.Integer, primary_key=True)  # 商品交易id
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))  # 商品 id
    num = db.Column(db.Float)  # 交易商品的数量或重量
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))  # 所属的订单 id

    def __repr__(self):
        commodity_name = self.get_commodity_name()
        commodity = self.commodity_id if commodity_name is None else commodity_name  # 如果商品不存在就显示商品id
        return '<Transaction order_id:{} commodity:{} num:{}>'.format(self.id, commodity, self.mac)

    def get_commodity_name(self):
        """获取交易商品的名称"""
        commodity = Commodity.query.filter_by(id=self.commodity_id).first()
        return None if commodity is None else commodity.commodity_name

    def sbtotal(self):
        """小计"""
        commodity = Commodity.query.filter_by(id=self.commodity_id).first()
        return self.num * 0 if commodity is None else commodity.unit_price  # 如果商品不存在就返回0
