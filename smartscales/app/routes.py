#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/1 23:21
@Author  : miaoweiwei
@File    : routes.py
@Software: PyCharm
@Desc    : 路由视图
"""
import os
from PIL import Image
from flask import render_template, request
from flask_babel import _
from app import al, yolo
from app.algorithm import graph, dataprocessing
from app.algorithm.image_detect_func import get_difference
from app.fruit import Fruit
from app import app, socketioutils, fruit_name_dic

mydir = al.TEST_PATH


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    """ 首页"""
    return render_template("index.html")


@app.route("/cart", methods=['GET', 'POST'])
def cart():
    """购物车"""
    cart_list, total = dataprocessing.make_web_list()
    new_cart_list = dataprocessing.make_web_new()
    fruit_list = []
    if len(cart_list) > 0:
        for i in range(len(cart_list)):
            fruit = Fruit(cart_list[i][0], cart_list[i][1], cart_list[i][2])
            fruit_list.append(fruit)

    new_fruit_list = []
    if new_cart_list is not None and len(new_cart_list) > 0:
        fruit = Fruit(new_cart_list[0], new_cart_list[1], new_cart_list[2])
        new_fruit_list.append(fruit)

    return render_template("cart.html", title=_('Shopping Cart'),
                           fruit_list=fruit_list,  # 水果列表
                           newfruits=new_fruit_list,  # 新增水果的列表
                           total=total,  # 总价计算
                           fruitnames=fruit_name_dic.values(), )


@app.route("/pay", methods=['GET', 'POST'])
def pay():
    """未付款订单"""
    cart_list, total = dataprocessing.make_web_list()
    fruit_list = []
    if len(cart_list) > 0:
        for i in range(len(cart_list)):
            fruit = Fruit(cart_list[i][0], cart_list[i][1], cart_list[i][2])
            fruit_list.append(fruit)
    return render_template('pay.html', title=_('Payment'), fruit_list=fruit_list, total=total)


@app.route("/paidorder", methods=["GET", "POST"])
def paidorder():
    """已付款订单页面"""
    cart_list, total = dataprocessing.make_web_list()
    fruit_list = []
    if len(cart_list) > 0:
        for i in range(len(cart_list)):
            fruit = Fruit(cart_list[i][0], cart_list[i][1], cart_list[i][2])
            fruit_list.append(fruit)
    return render_template('paidorder.html', title=_('The fruit I bought'), fruit_list=fruit_list, total=total)


@app.route("/settlement", methods=["GET", "POST"])
def settlement():
    """结算"""
    return "settlement"


# 上传图片进行识别
@app.route("/upload", methods=['POST'])
def get_frame():
    upload_file = request.files['file']
    weight = request.form.get('weight')
    old_file_name = upload_file.filename
    image_count = old_file_name.split('_')[-1].split('.')[0]  # 获取图像的编号
    dirname = old_file_name.split('_')[1] + old_file_name.split('_')[2]  # 取文件的时间当做文件夹的名字
    dirpath = os.path.join(mydir, dirname)
    folder = os.path.exists(dirpath)
    if not folder:
        os.makedirs(dirpath)
    file_path = os.path.join(mydir, dirname, old_file_name)
    print('weight:', weight)
    print(image_count)

    if upload_file:
        upload_file.save(file_path)
        print("upload successfully ")
        print(file_path)
        if int(image_count) == 1:
            image_A_path = al.BACK_GROUND
            image_B_path = file_path
        else:
            image_A_name = 'image_' + old_file_name.split('_')[1] + '_' + old_file_name.split('_')[2] + '_' \
                           + str(int(image_count) - 1).zfill(3) + '.jpg'
            image_A_path = os.path.join(mydir, dirname, image_A_name)
            image_B_path = file_path
        cropped_B_path, cropped_A_path = get_difference(image_A_path, image_B_path, al.CROPPED_PATH)
        image_B = Image.open(cropped_B_path)
        image_A = Image.open(cropped_A_path)
        weight = float(weight)
        print('A_path:', cropped_A_path)
        print('B_path:', cropped_B_path)

        with graph.as_default():
            if weight > 0.05:
                r_image, result = yolo.detect_image(image_B)
                if len(result) == 0:
                    return "can not recognize"
                name = result[0]
                namelist = result
                id = dataprocessing.name_id[name]
                idlist = [dataprocessing.name_id[i] for i in namelist]
                print('adding:', id, name)
                dataprocessing.add_fruit(id, weight)
                print('add successfully')

            elif weight < -0.05:
                r_image, result = yolo.detect_image(image_A)
                if len(result) == 0:
                    return "can not recognize"
                name = result[0]
                namelist = result
                id = dataprocessing.name_id[name]
                idlist = [dataprocessing.name_id[i] for i in namelist]
                print('removing:', id, name)
                dataprocessing.remove_fruit(id, weight)
                print('remove successfully')
            dataprocessing.show_list()
            print(dataprocessing.getshoplist())
            print('current_list:', dataprocessing.current_list)
        print('make_web_list', dataprocessing.make_web_list())
        print('make_web_new', dataprocessing.make_web_new())
        socketioutils.report(1)
        return 'success'
    else:
        return 'failed'
