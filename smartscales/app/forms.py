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
from wtforms import SelectField, SubmitField
from wtforms.validators import Required, DataRequired


class ErrorCorrectionForm(FlaskForm):
    tag = SelectField(
        label='类别',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, '情感'), (2, '星座'), (3, '爱情')],
        defalut=3,
        coerce=int
    )
