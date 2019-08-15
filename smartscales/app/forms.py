#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/2 10:33
@Author  : miaoweiwei
@File    : forms.py
@Software: PyCharm
@Desc    : 表单
"""
from cgitb import strong
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import Required, DataRequired
from flask_babel import _
from flask_babel import lazy_gettext as _l  # 这个新函数将文本包装在一个特殊的对象中，这个对象会在稍后的字符串使用时触发翻译。


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])  # 定义用户名字段
    password = PasswordField(_l('Password'), validators=[DataRequired()])  # 定义密码字段
    remember_me = BooleanField(_l('Remember Me'))  # 定义复选框
    # login_type = RadioField(label=_l('Login Type'), choices=(
    #     ('Administrator', _l('Administrator')),  # 第一个值也要使用字符串
    #     ('Customer', _l('Customer'))
    # ))
    submit = SubmitField(_l('Sign In'))  # 定义提交按钮
