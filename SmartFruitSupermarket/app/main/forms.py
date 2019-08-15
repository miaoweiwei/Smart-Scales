#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/19 9:48
@Author  : miaoweiwei
@File    : forms.py
@Software: PyCharm
@Desc    : 
"""
from flask import request
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length

from app.models import User


