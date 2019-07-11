from skimage.measure import compare_ssim
#~ import skimage  as ssim
import argparse
import imutils
import cv2
import datetime
import numpy as np
from PIL import Image
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
#     help="first input image")
# ap.add_argument("-s", "--second", required=True,
#     help="second")
# args = vars(ap.parse_args())
# load the two input images
# imageA = cv2.imread(args["first"])
# imageB = cv2.imread(args["second"])

# imageA = cv2.imread("img/image02-0.png")
# imageB = cv2.imread("img/image02-1.png")

# imageA = cv2.imread("img/image0.jpg")
# imageB = cv2.imread("img/image1.jpg")

imageA = cv2.imread("H:/pythonworkspace/Serverstore/6.jpg")
imageB = cv2.imread("H:/pythonworkspace/Serverstore/7.jpg")
# imageB2crop = Image.open("H:/pythonworkspace/Serverstore/new/image4.jpg")
# print(type(imageA), type(imageB2crop))

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
# structural similarity index measurement (SSIM) system
# 一种衡量两幅图像结构相似度的新指标，其值越大越好，最大为1。
#
# def whiteBalance(img):
#     rows = img.shape[0]
#     cols = img.shape[1]
#     final = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
#     avg_a = np.average(final[:, :, 1])
#     avg_b = np.average(final[:, :, 2])
#
#     for x in range(final.shape[0]):
#         for y in range(final.shape[1]):
#             l, a, b = final[x, y, :]
#             l *= 100 / 255.0
#             final[x, y, 1] = a - ((avg_a - 128) * (1 / 100.0) * 1.1)
#             final[x, y, 2] = b - ((avg_b - 128) * (1 / 100.0) * 1.1)
#     final = cv2.cvtColor(final, cv2.COLOR_LAB2BGR)
#     return final

time_1 = datetime.datetime.now()
(score, diff) = compare_ssim(imageA, imageB, win_size=3, full=True, multichannel=True)
# print(diff, len(diff))
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))
cv2.imshow("Diff", diff)
time_2 = datetime.datetime.now()

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
grayA = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
# thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
thresh = cv2.threshold(diff, 188, 255, cv2.THRESH_BINARY)[1]

grayB = cv2.threshold(grayA, 128, 255, cv2.THRESH_BINARY)[1]
# grayC = cv2.threshold(thresh, 128, 255, cv2.THRESH_BINARY)[1]
grayC = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)

kernel = np.ones((3, 3), np.uint8)
img2 = cv2.dilate(grayC, kernel)
img3 = cv2.erode(img2, kernel)
# img3 = cv2.erode(img2, kernel)

# kernel = np.ones((5, 5), np.uint8)
# img4 = cv2.erode(img3, kernel)
img4 = cv2.dilate(img3, kernel)
img5 = cv2.dilate(img4, kernel)
# kernel = np.ones((7, 7), np.uint8)
img6 = cv2.erode(img5, kernel)

thresh_new = cv2.threshold(img4, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh_new.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

time_3 = datetime.datetime.now()

max_size = 0
max_list = [0, 0, 0, 0]


my_array = np.zeros((480, 640), dtype=np.uint8)
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if w < 50 or h < 50:
        continue
    my_array[y:y + h, x:x + w] = 1

new_cnts = cv2.findContours(my_array.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
new_cnts = new_cnts[0] if imutils.is_cv2() else new_cnts[1]


my_array = np.zeros((480, 640), dtype=np.uint8)
for c in new_cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if w < 50 or h < 50:
        continue
    my_array[y:y + h, x:x + w] = 1
new_cnts = cv2.findContours(my_array.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
new_cnts = new_cnts[0] if imutils.is_cv2() else new_cnts[1]

my_array = np.zeros((480, 640), dtype=np.uint8)
for c in new_cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if w < 50 or h < 50:
        continue
    my_array[y:y + h, x:x + w] = 1
new_cnts = cv2.findContours(my_array.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
new_cnts = new_cnts[0] if imutils.is_cv2() else new_cnts[1]

for c in new_cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    print(x, y, w, h)
    rect_size = w * h
    if rect_size > max_size:
        max_size = rect_size
        max_list = [x, y, w, h]
    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

# for i in range(10):
#     cv2.rectangle(imageA, (64 * i, 0), (64 * (i + 1), 48), (0, 0, 255), 2)


[x, y, w, h] = max_list
# print(x, y, w, h)
cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
# cropped = imageB2crop.crop((x, y, x + w, y + h))
cropped_new = imageB[y:y + h, x:x + w]
cropped_old = imageA[y:y + h, x:x + w]
time_4 = datetime.datetime.now()
# show the output images
cv2.imshow("Original", imageA)
cv2.imshow("Modified", imageB)
cv2.imshow("Diff", diff)

# cv2.imshow("cropped", cropped_new)
# cv2.imshow('thresh2', thresh2)
# cv2.imshow('thresh3', thresh3)
# cv2.imshow('thresh4', thresh4)
# cv2.imshow('thresh5', thresh5)
cv2.imshow("Thresh", thresh)
cv2.imshow("grayA", grayA)
cv2.imshow('grayB', grayB)
cv2.imshow('grayC', grayC)
cv2.imshow('fushi', img2)
cv2.imshow('pengzhang', img3)
cv2.imshow('fpf', img4)
# cv2.imshow('fpfp', img5)
cv2.imshow('thresh_new', thresh_new)
# cv2.imshow('fpfpf', img6)
# cv2.imwrite("H:/pythonworkspace/Serverstore/cropped_1.jpg", cropped_new)
# cv2.imwrite("H:/pythonworkspace/Serverstore/cropped_2.jpg", cropped_old)
# cv2.imwrite("H:/pythonworkspace/Serverstore/cropped_3.jpg", diff)

cv2.waitKey(0)

# time_4 = datetime.datetime.now()

print(time_2 - time_1, time_3 - time_2, time_4 - time_3)

