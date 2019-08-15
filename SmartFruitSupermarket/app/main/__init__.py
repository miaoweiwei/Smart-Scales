#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/8/10 9:41
@Author  : miaoweiwei
@File    : __init__.py.py
@Software: PyCharm
@Desc    : 这里主要是主页等一些公共的页面
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
