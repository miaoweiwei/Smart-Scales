import requests
import os
import time
import datetime


def upload_image():
    url = "http://127.0.0.1:5000"
    # filepath='H:/pythonworkspace/fruitnew/validation/Banana/1_100.jpg'
    # filepath = 'H:/pythonworkspace/Serverstore/new/image_20190702_210230AA_006.jpg'
    # filepath = 'H:/pythonworkspace/Serverstore/test1/20190702210230AB/image_20190702_210230AA_002.jpg'
    filepath = 'D:/Myproject/Python/Flask/smartscales/app/algorithm/data/test1/20190702210230AB/image_20190702_210230AA_002.jpg'
    split_path = filepath.split('/')
    filename = split_path[-1]
    print(filename)
    weight = {"weight": 1.5}
    info = {"info": "background"}
    info = {"info": "fruit"}
    file = open(filepath, 'rb')
    files = {'file': (filename, file, 'image/jpg')}

    r = requests.post(url, data=weight, files=files)
    result = r.text
    print(result)


def upload_image_with_args(filepath, w):
    url = "http://127.0.0.1:5000/upload"

    # filepath='H:/pythonworkspace/fruitnew/validation/Banana/1_100.jpg'
    # filepath = 'H:/pythonworkspace/Serverstore/new/image_20190702_210230AA_006.jpg'
    # filepath = 'H:/pythonworkspace/Serverstore/test1/20190702210230AB/image_20190702_210230AA_002.jpg'
    split_path = filepath.split('/')
    filename = split_path[-1]
    print(filename)
    weight = {"weight": w}
    info = {"info": "background"}
    info = {"info": "fruit"}
    file = open(filepath, 'rb')
    files = {'file': (filename, file, 'image/jpg')}

    r = requests.post(url, data=weight, files=files)
    result = r.text
    print(result)


def upload_background():
    url = "http://127.0.0.1:5000/getbackground"
    filepath = 'D:/Myproject/Python/Flask/smartscales/app/algorithm/data/test1/20190702210230AB/background_20190702_210230AA_000.jpg'
    # filename = 'background_image.jpg'
    # filename = os.path.split(filepath)
    split_path = filepath.split('/')
    filename = split_path[-1]
    file = open(filepath, 'rb')
    files = {'file': (filename, file, 'image/jpg')}
    r = requests.post(url, files=files)
    result = r.text
    print(result)


def claer_shoplist():
    url = 'http://127.0.0.1:5000/clear'
    r = requests.post(url)
    print(r.text)


def test():
    path = 'D:/Myproject/Python/Flask/Smart-Scales/smartscales/app/algorithm/data/test1/20190708110708AA/image_20190708_110708AA_'
    weight = [1.5, 1.5, 1.5, 1.5, -1.5, -3, -1.5]
    for i in range(7):
        time_1 = datetime.datetime.now()
        upload_image_with_args(path + '%s' % str(i + 1).zfill(3) + '.jpg', weight[i])
        time_2 = datetime.datetime.now()
        print(time_2 - time_1)
        time.sleep(5)


def test2():
    path = 'D:/Myproject/Python/Flask/smartscales/app/algorithm/data/test1/20190702210230AA/image_20190702_210230AA_'
    weight = [1.5, 1.5, 1.5, -1.5]
    for i in range(1):
        time_1 = datetime.datetime.now()
        upload_image_with_args(path + '%s' % str(i + 1).zfill(3) + '.jpg', weight[i])
        time_2 = datetime.datetime.now()
        print(time_2 - time_1)
        time.sleep(5)
    # upload_image_with_args('H:/pythonworkspace/Serverstore/test1/20190702210230AA/image_20190702_210230AA_005.jpg',
    #                        -1.5)


# upload_background()
# upload_image()
claer_shoplist()
test()
# claer_shoplist()
