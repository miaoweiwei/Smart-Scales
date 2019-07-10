#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/2 1:01
@Author  : miaoweiwei
@File    : fruit.py
@Software: PyCharm
@Desc    : 有关水果属性的方法
"""
from app import fruit_name_dic


class Fruit(object):
    def __init__(self, name, unitprice, netweight, describe=None):
        self.name = name
        self.unitprice = unitprice
        self.netweight = netweight
        self.describe = describe

    def get_fruit_name(self):
        return fruit_name_dic[self.name]

    def get_fruit_describe(self):
        return self.describe

    def get_fruit_unitprice(self):
        return self.unitprice

    def get_fruit_icon(self):
        return "./static/icons/" + self.name + ".png"

    def get_fruit_netweight(self):
        return self.netweight

    def get_subtotal(self):
        return round((self.get_fruit_netweight() * self.get_fruit_unitprice()), 2)
