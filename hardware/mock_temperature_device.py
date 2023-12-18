from torchvision import transforms
from PIL import Image
import requests
import time
import os
import sys
import threading
import random


if len(sys.argv) < 2:
    print("Usage: python mock_temperature_device.py device_name")
    sys.exit(1)

# 服务端接口
kUploadServerApi = "http://127.0.0.1:8000/api/upload/temperature"
kkeepAliveServerApi = "http://127.0.0.1:8000/api/keepalive"


# 每隔5S发一次心跳保活包
def keepalive():
    while True:
        try:
            response_sensor = requests.post(
                kkeepAliveServerApi,
                data={
                    "device": sys.argv[1],
                    "type": "sensor",
                    "timestamp": int(time.time()),
                },
            )
            if response_sensor.status_code == 200:
                print(response)
        except Exception as e:
            print("keepalive failed", e)
        threading.Event().wait(5)


# 启动keepalive线程
threading.Thread(target=keepalive, daemon=True).start()


def sendTemperature(conf):
    try:
        response = requests.post(
            kUploadServerApi,
            data={"device": sys.argv[1], "temperature": conf, "timestamp": int(time.time())},
        )
        if response.status_code == 200:
            print("上传成功")
        else:
            print("上传失败")
    except Exception as e:
        print("上传异常", e)


# 每隔10秒随机上报一次事件
while True:
    random_temp = random.uniform(22.5, 25.8)
    sendTemperature(random_temp)
    threading.Event().wait(10)
