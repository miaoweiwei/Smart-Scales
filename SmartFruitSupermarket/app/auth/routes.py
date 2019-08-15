#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/6/22 11:39
@Author  : miaoweiwei
@File    : routes.py
@Software: PyCharm
@Desc    : 
"""

from flask import render_template, flash, redirect, url_for, request
from flask_babel import _
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm
from app.models import User


@bp.route('/login', method=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # 用户已经登录
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        loing_type = form.login_type.data

