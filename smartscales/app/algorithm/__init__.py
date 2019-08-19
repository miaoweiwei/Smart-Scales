#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/6 23:24
@Author  : miaoweiwei
@File    : __init__.py.py
@Software: PyCharm
@Desc    : YOLO算法的初始化
"""
import datetime
from os.path import join, dirname, realpath
from PIL import Image
from app.algorithm.yolo import YOLO
from app.algorithm import dataprocessing
import tensorflow as tf

ALGORITHM_PATH = dirname(realpath(__file__))  # 算法文件夹的路径
DATA_PATH = join(ALGORITHM_PATH, 'data')

FONT_PATH = join(ALGORITHM_PATH, 'font')

MODEL_WEIGHT_PATH = join(ALGORITHM_PATH, 'model_weight')  # 模型权重的文件夹路径
MODEL_DATA_PATH = join(ALGORITHM_PATH, 'model_data')  # 模型数据路径

TEST_PATH = join(DATA_PATH, 'test1')
IMAGES_PATH = join(DATA_PATH, 'images')
CROPPED_PATH = join(DATA_PATH, 'cropped')
RESULT_PATH = join(DATA_PATH, 'result')
# BACK_GROUND = join(DATA_PATH, 'background/background1.jpg')
BACK_GROUND = join(DATA_PATH, 'background/background1.jpg')
'''背景'''


def algorithm_init():
    yolo_test_args = {
        "model_path": join(MODEL_WEIGHT_PATH, 'trained_weights_final.h5'),
        "anchors_path": join(MODEL_DATA_PATH, 'yolo_anchors.txt'),
        "classes_path": join(MODEL_DATA_PATH, 'fruit_classes.txt'),
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 0,
    }
    new_yolo_test_args = {
        "model_path": join(MODEL_WEIGHT_PATH, 'new_trained_weights_final.h5'),
        "anchors_path": join(MODEL_DATA_PATH, 'yolo_anchors.txt'),
        "classes_path": join(MODEL_DATA_PATH, 'new_fruit_classes.txt'),
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 0,
    }
    tiny_yolo_test_args = {
        "model_path": join(MODEL_WEIGHT_PATH, 'fruit_yolo_ckpt_tiny.h5'),
        "anchors_path": join(MODEL_DATA_PATH, 'tiny_yolo_anchors.txt'),
        "classes_path": join(MODEL_DATA_PATH, 'new_fruit_classes.txt'),
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 0,
    }
    final_yolo_test_args = {
        "model_path": join(MODEL_WEIGHT_PATH, 'fruit_yolo_ckpt.h5'),
        "anchors_path": join(MODEL_DATA_PATH, 'yolo_anchors.txt'),
        "classes_path": join(MODEL_DATA_PATH, 'final_fruit_classes.txt'),
        "score": 0.3,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 0,
    }

    graph = tf.get_default_graph()  # 功能：获取当前默认计算图。
    yolo = YOLO(**final_yolo_test_args)  # 初始化算法
    return yolo, graph
    return yolo, graph


if __name__ == '__main__':
    yolo = algorithm_init()
    time_1 = datetime.datetime.now()
    image = Image.open(join(DATA_PATH, 'images/banana_7.jpg'))
    time_2 = datetime.datetime.now()
    r_image, result = yolo.detect_image(image)
    time_3 = datetime.datetime.now()
    print(time_3 - time_2, time_2 - time_1)

    # r_image.show()
    time_1 = datetime.datetime.now()
    image = Image.open(join(DATA_PATH, 'images/apple_62.jpg'))
    time_2 = datetime.datetime.now()
    r_image, result = yolo.detect_image(image)
    time_3 = datetime.datetime.now()
    print(time_3 - time_2, time_2 - time_1)

    time_1 = datetime.datetime.now()
    image = Image.open(join(DATA_PATH, 'images/apple_68.jpg'))
    time_2 = datetime.datetime.now()
    r_image, result = yolo.detect_image(image)
    time_3 = datetime.datetime.now()
    print(time_3 - time_2, time_2 - time_1)
