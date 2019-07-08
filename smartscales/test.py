#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/7/7 3:45
@Author  : miaoweiwei
@File    : test.py
@Software: PyCharm
@Desc    : 
"""

import tensorflow as tf

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

if __name__ == '__main__':
    print(tf.__version__)
