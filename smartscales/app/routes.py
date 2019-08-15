#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/1 23:21
@Author  : miaoweiwei
@File    : routes.py
@Software: PyCharm
@Desc    : 路由视图
"""
import datetime
import os
from PIL import Image
from flask import render_template, request, flash, url_for, redirect
from flask_babel import _
from flask_babel import lazy_gettext as _l  # 这个新函数将文本包装在一个特殊的对象中，这个对象会在稍后的字符串使用时触发翻译。
from app import al, yolo, graph
from app.algorithm import dataprocessing
from app.algorithm.image_detect_func import get_difference
from app.forms import LoginForm
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
    # cart_list = [["apple", 23.12, 12]]
    # total = 23.12 * 12
    # new_cart_list = [["apple", 23.12, 12]]
    fruit_list = []
    if len(cart_list) > 0:
        for i in range(len(cart_list)):
            fruit = Fruit(cart_list[i][0], cart_list[i][1], cart_list[i][2])
            fruit_list.append(fruit)

    new_fruit_list = []
    if new_cart_list is not None and len(new_cart_list) > 0:
        for i in range(len(new_cart_list)):
            fruit = Fruit(new_cart_list[i][0], new_cart_list[i][1], new_cart_list[i][2])
            new_fruit_list.append(fruit)
    if len(new_cart_list) >= 2:
        if new_cart_list[0][2] > 0:
            flash(_(
                "You may have placed a variety of items at once. Sorry, you can't carefully identify the weight of each item. Please take out the various items you just placed and put them in order. If you confirm that only one item is placed, please Make corrections."))
        else:
            flash(_(
                "You may have taken a variety of items at once, and I am sorry that you cannot carefully identify the weight of each item. If you confirm that only one item has been removed, please correct it."))
    elif len(new_cart_list) == 1:
        if new_cart_list[0][2] > 0 and new_cart_list[0][0] != '1000':
            fruit_name = new_cart_list[0][0]
            flash(_l("You added new %(fruit_name)s", fruit_name=fruit_name_dic[fruit_name]))
        if new_cart_list[0][2] < 0 and new_cart_list[0][0] != '1000':
            fruit_name = new_cart_list[0][0]
            flash(_l("You took the %(fruit_name)s away", fruit_name=fruit_name_dic[fruit_name]))
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
    cart_list, total = dataprocessing.make_web_list()
    fruit_list = []
    if len(cart_list) > 0:
        for i in range(len(cart_list)):
            fruit = Fruit(cart_list[i][0], cart_list[i][1], cart_list[i][2])
            fruit_list.append(fruit)
    return render_template('settlement.html', title=_("Settlement"), fruit_list=fruit_list, total=total)


# 上传图片进行识别
@app.route("/upload", methods=['POST'])
def get_frame():
    starttime = datetime.datetime.now()
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
        image_C = Image.open(file_path)
        weight = float(weight)
        print('A_path:', cropped_A_path)
        print('B_path:', cropped_B_path)

        with graph.as_default():
            if weight > 0.05:
                if image_count == "001":
                    r_image, result = yolo.detect_image(image_C)
                    print("detect 001")
                else:
                    r_image, result = yolo.detect_image(image_B)
                if len(result) == 0:
                    dataprocessing.add_empty(weight)
                    socketioutils.report(1)
                    print("upload耗时：" + str(datetime.datetime.now() - starttime))
                    return "can not recognize"
                name = result[0]
                namelist = result
                id = dataprocessing.name_id[name]
                idlist = [dataprocessing.name_id[i] for i in namelist]
                idlist = list(set(idlist))
                print('idlist:', idlist)
                print('adding:', id, name)
                dataprocessing.add_list(idlist, weight)
                # dataprocessing.add_fruit(id, weight)
                print('add successfully')

            elif weight < -0.05:
                r_image, result = yolo.detect_image(image_A)
                if len(result) == 0:
                    dataprocessing.remove_empty(weight)
                    socketioutils.report(1)
                    print("upload耗时：" + str(datetime.datetime.now() - starttime))
                    return "can not recognize"
                name = result[0]
                namelist = result
                id = dataprocessing.name_id[name]
                idlist = [dataprocessing.name_id[i] for i in namelist]
                idlist = list(set(idlist))
                print('removing:', id, name)
                dataprocessing.remove_list(idlist, weight)
                # dataprocessing.remove_fruit(id, weight)
                print('remove successfully')
            dataprocessing.show_list()
            print(dataprocessing.getshoplist())
            print('current_list:', dataprocessing.current_list)
        result_image, result_res = yolo.detect_image(image_C)
        print('make_web_list', dataprocessing.make_web_list())
        print('make_web_new', dataprocessing.make_web_new())
        socketioutils.report(1)
        print("upload耗时：" + str(datetime.datetime.now() - starttime))
        return 'success'
    else:
        print("upload耗时：" + str(datetime.datetime.now() - starttime))
        return 'failed'


@app.route("/change", methods=["POST"])
def change_fruit():
    target_fruit_name = "orange"
    target_fruit_id = dataprocessing.name_id[target_fruit_name]
    weight = 1.5
    current_fruit = dataprocessing.current_list
    if len(current_fruit) == 0:
        return 'no new fruits'
    else:
        id = current_fruit[0][0]
        name = dataprocessing.repository[id][1]
    dataprocessing.edit_kind(id, weight, target_fruit_id)
    return 'success'


@app.route("/clear", methods=["POST"])
def clear_fruits():
    dataprocessing.clear_shoplist()
    socketioutils.report(1)
    return 'clear success'


# 涉及到 表单 的视图都要使用 POST方式
@app.route('/login', methods=['GET', 'POST'])
def login():  # 用户登录
    form = LoginForm(login_type='Customer')
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # login_type = form.login_type.data
        print(username)
        print(password)
        # print(login_type)
        if username != 'root' or password != '123456':
            flash(_('Invalid username or password'))  # 会闪现一条消息到登录界面
            return redirect(url_for('login'))
        return redirect(url_for('manage'))
    return render_template('login.html', title=_('Backstage Management Sign In'), form=form)  # 此处不能使用 url_for()函数


@app.route('/manage', methods=['GET', 'POST'])
def manage():
    """后台登录的首页"""

    # error_num 表示错误的数量
    return render_template('manage.html', title=_('manage'), error_num=0)


@app.route('/bills', methods=['GET', 'POST'])
def bills():
    """账单"""

    # error_num 表示错误的数量
    return render_template('bills.html', title=_('manage'), error_num=0)


@app.route('/modify', methods=['GET', 'POST'])
def modify():
    """后台纠错"""
    cart_list, total = dataprocessing.make_web_list()
    new_cart_list = dataprocessing.make_web_new()

    fruit_list = []
    if len(cart_list) > 0:
        for i in range(len(cart_list)):
            fruit = Fruit(cart_list[i][0], cart_list[i][1], cart_list[i][2])
            fruit_list.append(fruit)
    new_fruit_list = []
    if new_cart_list is not None and len(new_cart_list) > 0:
        for i in range(len(new_cart_list)):
            fruit = Fruit(new_cart_list[i][0], new_cart_list[i][1], new_cart_list[i][2])
            new_fruit_list.append(fruit)
    if len(new_cart_list) >= 2:
        if new_cart_list[0][2] > 0:
            flash(_(
                "You may have placed a variety of items at once. Sorry, you can't carefully identify the weight of each item. Please take out the various items you just placed and put them in order. If you confirm that only one item is placed, please Make corrections."))
        else:
            flash(_(
                "You may have taken a variety of items at once, and I am sorry that you cannot carefully identify the weight of each item. If you confirm that only one item has been removed, please correct it."))
    elif len(new_cart_list) == 1:
        if new_cart_list[0][2] > 0 and new_cart_list[0][0] != '1000':
            fruit_name = new_cart_list[0][0]
            flash(_l("You added new %(fruit_name)s", fruit_name=fruit_name_dic[fruit_name]))
        if new_cart_list[0][2] < 0 and new_cart_list[0][0] != '1000':
            fruit_name = new_cart_list[0][0]
            flash(_l("You took the %(fruit_name)s away", fruit_name=fruit_name_dic[fruit_name]))
    return render_template('modify.html', title=_('manage'),
                           error_num=0,
                           fruit_list=fruit_list,  # 水果列表
                           newfruits=new_fruit_list,  # 新增水果的列表
                           fruitnames=fruit_name_dic.values(), )
