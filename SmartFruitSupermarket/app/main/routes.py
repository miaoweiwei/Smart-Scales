#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/19 9:48
@Author  : miaoweiwei
@File    : routes.py
@Software: PyCharm
@Desc    : 
"""
from flask import render_template

from app.main import bp


# @bp.before_request注册在视图函数之前执行的函数因为现在我可以在一处地方编写代码，
# 并让它在任何视图函数之前被执行
@bp.route("/", methods=['GET', 'POST'])
@bp.route("/index", methods=['GET', 'POST'])
def index():
    """ 首页"""
    return render_template("index.html")


@bp.route("/cart", methods=['GET', 'POST'])
def cart():
    """购物车"""
    return ""
