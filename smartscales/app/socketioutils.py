#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/2 15:55
@Author  : miaoweiwei
@File    : socketioutils.py
@Software: PyCharm
@Desc    : 用于服务器和前端进行通信，双向全双工，websocket
"""
from app import socketio, app, fruit_name_dic
from app.algorithm import dataprocessing
from flask_socketio import emit


@socketio.on('update_cart')  # 使用socketio.on装饰器注册socket
def update_cart(content):
    print(content)
    new_dict = {v: k for k, v in fruit_name_dic.items()}
    id0 = "1000"
    if content["name"] != "1000":
        id0 = dataprocessing.name_id[content["name"]]
    id1 = dataprocessing.name_id[new_dict[content["changeName"]]]
    dataprocessing.edit_kind(id0, id1)
    # 发送消息到前端 参数一表示这个通道的名字，参数二是发送的内容，参数broadcast表示是否广播是所有的前端都能收到信息
    # emit('new_message', {'message_html': render_template('message.html', message=message)}, broadcast=True)
    # emit('update_cart', content, broadcast=True)
    emit('update_cart', "1", broadcast=False)


@socketio.on("settlement")
def settlement(content):
    print(content)
    if content == "1":  # 收到1就去通知 pay页面跳转到settlement页面
        emit('settlement', "2", broadcast=True)


# 用于服务端主动向前端发送信息
def report(content):
    # while True:
    with app.app_context():
        # text = input("要发送的信息：")
        # socketio.emit('response')
        socketio.emit('update_cart', content, broadcast=True)


def update_cart():
    """刷新购物车页面"""
    report("1")
