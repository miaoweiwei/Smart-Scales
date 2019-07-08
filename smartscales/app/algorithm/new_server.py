import os
import tensorflow as tf
import keras
import sys
import argparse
from flask import request, Flask, jsonify

from app.algorithm import dataprocessing
from app.algorithm.yolo import YOLO, detect_video
from PIL import Image
import app.algorithm.dataprocessing
from app.algorithm.image_detect_func import get_difference
from collections import Counter
from flask_cors import CORS

fruit_dict = {"apple": "苹果", "banana": "香蕉", "orange": "橙子"}
# 定义仓库
# dataprocessing.repository = dict()
# dataprocessing.name_id = dict()
# dataprocessing.shop_list = []
graph = tf.get_default_graph()  # 功能：获取当前默认计算图。
yolo_test_args = {
    "model_path": 'D:/Myproject/Python/Flask/smartscales/app/algorithm/model_weight/trained_weights_final.h5',
    "anchors_path": 'D:/Myproject/Python/Flask/smartscales/app/algorithm/model_data/yolo_anchors.txt',
    "classes_path": 'D:/Myproject/Python/Flask/smartscales/app/algorithm/model_data/fruit_classes.txt',
    "score": 0.3,
    "iou": 0.45,
    "model_image_size": (416, 416),
    "gpu_num": 0,
}

new_yolo_test_args = {
    "model_path": './model_weight/new_trained_weights_final.h5',
    "anchors_path": './model_data/yolo_anchors.txt',
    "classes_path": './model_data/new_fruit_classes.txt',
    "score": 0.3,
    "iou": 0.45,
    "model_image_size": (416, 416),
    "gpu_num": 0,
}

tiny_yolo_test_args = {
    "model_path": './model_weight/fruit_yolo_ckpt_tiny.h5',
    "anchors_path": './model_data/tiny_yolo_anchors.txt',
    "classes_path": './model_data/new_fruit_classes.txt',
    "score": 0.3,
    "iou": 0.45,
    "model_image_size": (416, 416),
    "gpu_num": 0,
}

yolo_test = YOLO(**new_yolo_test_args)
# app = Flask(__name__)
# CORS(app, resources=r'/*')
# dataprocessing.init_repository()
# # dataprocessing.show_goods()
#
# # mydir = 'H:/pythonworkspace/Serverstore/test1/'
# mydir = 'D:/Myproject/Python/Flask/smartscales/app/algorithm/data/test1/'  # 放图片的主目录
# # cropped_image_path = "H:/pythonworkspace/Serverstore/cropped/"
# # 放处理过后准备识别的图片
# cropped_image_path = "D:/Myproject/Python/Flask/smartscales/app/algorithm/data/cropped/"
#
#
# @app.route("/getbackground", methods=['POST'])
# def get_background():
#     upload_file = request.files['file']
#     background_file_name = upload_file.filename
#     dirname = background_file_name.split('_')[1] + background_file_name.split('_')[2]
#     dirpath = os.path.join(mydir + dirname)
#     folder = os.path.exists(dirpath)
#     if not folder:
#         os.makedirs(dirpath)
#     file_path = os.path.join(mydir + dirname + '/' + background_file_name)
#     if upload_file:
#         upload_file.save(file_path)
#         print("upload background successfully ")
#         return 'success'
#     else:
#         return 'failed'
#
#
# # 上传图片进行识别
# @app.route("/", methods=['POST'])
# def get_frame():
#     upload_file = request.files['file']
#     weight = request.form.get('weight')
#     old_file_name = upload_file.filename
#     image_count = old_file_name.split('_')[-1].split('.')[0]
#     dirname = old_file_name.split('_')[1] + old_file_name.split('_')[2]
#     dirpath = os.path.join(mydir + dirname)
#     folder = os.path.exists(dirpath)
#     if not folder:
#         os.makedirs(dirpath)
#     file_path = os.path.join(mydir + dirname + '/' + old_file_name)
#     print('weight:', weight)
#     print(image_count)
#
#     if upload_file:
#         upload_file.save(file_path)
#         print("upload successfully ")
#         print(file_path)
#         if int(image_count) == 1:
#             image_A_path = 'D:/Myproject/Python/Flask/smartscales/app/algorithm/data/test1/20190702210230AA/background_20190702_210230AA_000.jpg'
#             image_B_path = file_path
#         else:
#             image_A_name = 'image_' + old_file_name.split('_')[1] + '_' + old_file_name.split('_')[2] + '_' \
#                            + str(int(image_count) - 1).zfill(3) + '.jpg'
#             image_A_path = os.path.join(mydir + dirname + '/' + image_A_name)
#             image_B_path = file_path
#         cropped_B_path, cropped_A_path = get_difference(image_A_path, image_B_path, cropped_image_path)
#         image_B = Image.open(cropped_B_path)
#         image_A = Image.open(cropped_A_path)
#         weight = float(weight)
#         print('A_path:', cropped_A_path)
#         print('B_path:', cropped_B_path)
#
#         with graph.as_default():
#             if weight > 0.05:
#                 r_image, result = yolo_test.detect_image(image_B)
#                 if len(result) == 0:
#                     return "can not recognize"
#                 name = result[0]
#                 namelist = result
#                 id = dataprocessing.name_id[name]
#                 idlist = [dataprocessing.name_id[i] for i in namelist]
#                 print('adding:', id, name)
#                 dataprocessing.add_fruit(id, weight)
#                 print('add successfully')
#
#             elif weight < -0.05:
#                 r_image, result = yolo_test.detect_image(image_A)
#                 if len(result) == 0:
#                     return "can not recognize"
#                 name = result[0]
#                 namelist = result
#                 id = dataprocessing.name_id[name]
#                 idlist = [dataprocessing.name_id[i] for i in namelist]
#                 print('removing:', id, name)
#                 dataprocessing.remove_fruit(id, weight)
#                 print('remove successfully')
#             dataprocessing.show_list()
#             print(dataprocessing.getshoplist())
#             print('current_list:', dataprocessing.current_list)
#         return 'success'
#     else:
#         return 'failed'
#
#
# @app.route("/get_new")
# def get_new_kind():
#     print(dataprocessing.current_list)
#     new_list = dataprocessing.make_web_new()
#     print(new_list)
#
#
# @app.route("/clear_fruits", methods=["GET", "POST"])
# def clear_chose_fruits():
#     print('under clear function')
#     dataprocessing.clear_shoplist()
#     print(dataprocessing.shop_list)
#     dataprocessing.show_list()
#     return 'success'
#
#
# @app.route("/reset", methods=["GET", "POST"])
# def reset():
#     paid = False
#     if paid == True:
#         return 'success'
#     else:
#         return 'computing'
#
#
# @app.route("/edit_kind")
# def edit_fruit_kind():
#     initial_id = request.form.get('initial_id')
#     weight = float(request.form.get('weight'))
#     target_id = request.form.get('targetid')
#     dataprocessing.edit_kind(initial_id, weight, target_id)
#     dataprocessing.show_list()
#     print(dataprocessing.getshoplist())
#
#
# if __name__ == "__main__":
#     # image = Image.open(r'H:/pythonworkspace/Serverstore/apple_3.jpg')
#     # r_image, result = yolo_test.detect_image(image)
#     # print("result:", result)
#     # r_image.show()
#     app.run('0.0.0.0')
