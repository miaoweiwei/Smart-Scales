#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/6/22 12:44
@Author  : miaoweiwei
@File    : forms.py
@Software: PyCharm
@Desc    : 为了再次践行我的松耦合原则，我会将表单类单独存储到名为app/forms.py的模块中。
就让我们来定义用户登录表单来做一个开始吧，它会要求用户输入username和password，
并提供一个“remember me”的复选框和提交按钮：
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
    login_type = RadioField(  # 定义登录类型
        label=_l('Login Type'),
        choices=(
            ('Administrator', _l('Administrator')),  # 第一个值也要使用字符串
            ('Customer', _l('Customer'))
        ))
    submit = SubmitField(_l('Sign In'))  # 定义提交按钮
