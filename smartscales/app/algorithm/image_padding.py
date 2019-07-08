import cv2
import numpy as np


def fill_image_from_path(background_path, image_path):
    image_background = cv2.imread(background_path)
    (h_b, w_b, c_b) = image_background.shape
    image = cv2.imread(image_path)
    (h, w, c) = image.shape
    print(w)
    filled_image = image_background
    if h % 2 == 1:
        h -= 1
    if w % 2 == 1:
        w -= 1
    print(w)
    # print((h_b - h)/2,(h_b + h) / 2, (w_b - w) / 2, (w_b + h) / 2)
    filled_image[int((h_b - h) / 2): int((h_b + h) / 2), int((w_b - w) / 2): int((w_b + w) / 2)] = image[0:h, 0:w]
    return filled_image


def fill_image(background, image):
    (h_b, w_b, c_b) = background.shape
    (h, w, c) = image.shape
    filled_image = background
    print(h_b, w_b, c_b, h, w, c)
    if h % 2 == 1:
        h -= 1
    if w % 2 == 1:
        w -= 1
    filled_image[int((h_b - h) / 2): int((h_b + h) / 2), int((w_b - w) / 2): int((w_b + w) / 2)] = image[0:h, 0:w]
    return filled_image


if __name__ == '__main__':
    background_path = 'H:/pythonworkspace/Serverstore/new/background_20190702_210230AA_000.jpg'
    image_path = 'H:/pythonworkspace/Serverstore/cropped/image_20190702_210230AA_003_new.jpg'
    background = cv2.imread(background_path)
    image = cv2.imread(image_path)
    new_image = fill_image(background, image)
    cv2.imshow("new:", new_image)
    # jie_image(src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print(src.shape)
    # (h, w, c) = src.shape
    # print(h, w, c)
