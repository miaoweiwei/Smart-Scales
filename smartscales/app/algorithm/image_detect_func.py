from skimage.measure import compare_ssim
# ~ import skimage  as ssim
import argparse
import imutils
import cv2
import numpy as np
import os
import app.algorithm.image_padding

# img_A_path = "H:/pythonworkspace/Serverstore/new/image4.jpg"
# img_B_path = "H:/pythonworkspace/Serverstore/new/image5.jpg"
from app.algorithm import image_padding


def get_difference(img_A_path, img_B_path, cropped_image_path):
    imageA = cv2.imread(img_A_path)
    imageB = cv2.imread(img_B_path)
    (A_path, temp_A_name) = os.path.split(img_A_path)
    (B_path, temp_B_name) = os.path.split(img_B_path)
    (image_A_name, extension_A) = os.path.splitext(temp_A_name)
    (image_B_name, extension_B) = os.path.splitext(temp_B_name)
    print(image_A_name, image_B_name)
    full_A_name = image_A_name + "_pre" + extension_A
    full_B_name = image_B_name + "_new" + extension_B
    print(full_A_name, full_B_name)

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, win_size=3, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    # cv2.imshow("Diff", diff)

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 5), np.uint8)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    max_size = 0
    max_list = [0, 0, 0, 0]
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w < 50 or h < 50:
            continue
        rect_size = w * h
        if rect_size > max_size:
            max_size = rect_size
            max_list = [x, y, w, h]
        else:
            x_pre = max_list[0]
            y_pre = max_list[1]
            w_pre = max_list[2]
            h_pre = max_list[3]
            x_max, y_max, w_max, h_max = max_list[0], max_list[1], max_list[2], max_list[3]
            if x_pre < x < x_pre + w_pre and y_pre < y < y_pre + h_pre:
                if x + w > x_pre + w_pre:
                    w_max = x - x_pre + w
                if y + h > y_pre + h_pre:
                    h_max = y - y_pre + h
            elif x_pre < x + w < x_pre + w_pre and y_pre < y < y_pre + h_pre:
                if x < x_pre:
                    x_max = x
                    w_max = x_pre - x + w_pre
                if y + h > y_pre + h_pre:
                    h_max = y - y_pre + h
            elif x_pre < x < x_pre + w_pre and y_pre < y + h < y_pre + h_pre:
                if x + w > x_pre + w_pre:
                    w_max = x - x_pre + w
                if y < y_pre:
                    y_max = y
                    h_max = y_pre - y + h_pre
            elif x_pre < x + w < x_pre + w_pre and y_pre < y + h < y_pre + h_pre:
                if x < x_pre:
                    x_max = x
                    w_max = x_pre - x + w_pre
                if y < y_pre:
                    y_max = y
                    h_max = y_pre - y + h_pre
            max_list = [x_max, y_max, w_max, h_max]

    [x, y, w, h] = max_list
    if x > 10:
        x = x - 10
    elif x > 5:
        x = x - 5
    if y > 10:
        y = y - 10
    elif y > 5:
        y = y - 5
    if y + h < 470:
        h += 10
    elif y + h < 475:
        h += 5
    if x + w < 630:
        w += 10
    elif x + w < 635:
        w += 5

    cropped_new = imageB[y:y + h, x:x + w]
    cropped_old = imageA[y:y + h, x:x + w]

    cropped_new_path = os.path.join(cropped_image_path, full_B_name)
    cropped_old_path = os.path.join(cropped_image_path, full_A_name)
    background_path = app.algorithm.BACK_GROUND
    background = cv2.imread(background_path)
    cropped_new = image_padding.fill_image(background, cropped_new)
    cv2.imwrite(cropped_new_path, cropped_new)
    cropped_old = image_padding.fill_image(background, cropped_old)
    cv2.imwrite(cropped_old_path, cropped_old)
    return cropped_new_path, cropped_old_path

# get_difference(img_A_path, img_B_path)
