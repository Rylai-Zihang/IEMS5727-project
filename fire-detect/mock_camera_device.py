from torchvision import transforms
from PIL import Image
import requests
import time
import os
import sys
import threading
import random


if len(sys.argv) < 2:
    print("Usage: python mock_camera_device.py device_name ")
    sys.exit(1)

# 服务端接口
kUploadServerApi = "http://127.0.0.1:8000/api/upload/fire"
kkeepAliveServerApi = "http://127.0.0.1:8000/api/keepalive"


# 每隔5S发一次心跳保活包
def keepalive():
    while True:
        try:
            response = requests.post(
                kkeepAliveServerApi,
                data={
                    "device": sys.argv[1],
                    "type": "camera",
                    "timestamp": int(time.time()),
                },
            )
            if response.status_code == 200:
                print(response)
            if response_sensor.status_code == 200:
                print(response)
        except Exception as e:
            print("keepalive failed", e)
        threading.Event().wait(5)


# 启动keepalive线程
threading.Thread(target=keepalive, daemon=True).start()


def asyncSendFireAlarm(conf):
    try:
        response = requests.post(
            kUploadServerApi,
            files={"image": open(sys.argv[1] + ".jpg", "rb")},
            data={"device": sys.argv[1], "conf": conf, "timestamp": int(time.time())},
        )
        if response.status_code == 200:
            print("上传成功")
        else:
            print("上传失败")
    except Exception as e:
        print("上传异常", e)


# 每隔30秒随机上报一次事件
while True:
    random_conv = random.uniform(0.2, 0.9)
    asyncSendFireAlarm(random_conv)
    threading.Event().wait(30)
