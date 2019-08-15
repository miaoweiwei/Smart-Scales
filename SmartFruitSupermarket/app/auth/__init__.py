#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/8/10 9:40
@Author  : miaoweiwei
@File    : __init__.py.py
@Software: PyCharm
@Desc    : 这里是写登录，登出等需要验证的页面
"""
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes
