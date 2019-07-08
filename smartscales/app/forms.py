#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/2 10:33
@Author  : miaoweiwei
@File    : forms.py
@Software: PyCharm
@Desc    : 表单
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import Required


class SmFormAdmin(FlaskForm):
    status = SelectField('按类型查询', validators=[Required()],
                         choices=[('0', '全部'), ('1', '待审核'), ('2', '认证成功'), ('3', '认证失败')])
    submit = SubmitField('Submit')
