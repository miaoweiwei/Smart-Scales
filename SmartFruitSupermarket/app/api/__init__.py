#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/8/10 9:45
@Author  : miaoweiwei
@File    : __init__.py.py
@Software: PyCharm
@Desc    : 
"""
from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import errors
# 需要将导入移动到底部以避免循环依赖错误
