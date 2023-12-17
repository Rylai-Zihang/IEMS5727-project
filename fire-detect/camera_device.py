import cv2
import torch
from torchvision import transforms
from PIL import Image
import shutil
import requests
import time
import os
import sys
import threading



if len(sys.argv) < 2:
    print("Usage: python camera_device.py device_name")
    sys.exit(1)

# 置信度阈值
kConfThreshold = 0.2
# 发送的最小间隔
kMinAlarmEventIntervalInS = 10
# 服务端接口
kUploadServerApi = "http://127.0.0.1:8000/api/upload/fire"
kkeepAliveServerApi = "http://127.0.0.1:8000/api/keepalive"


# 每隔5S发一次心跳保活包
def keepalive():
    while True:
        try:
            response = requests.post(
                kkeepAliveServerApi,
                data={'device': sys.argv[1], "type": 'camera', "timestamp": int(time.time())},
            )
            if response.status_code == 200:
                print(response)
        except Exception as e:
            print("keepalive failed", e)
        threading.Event().wait(5)


# 启动keepalive线程
threading.Thread(target=keepalive, daemon=True).start()


# 记录上一次调用的时间
last_call_time = None


# 发送火情到服务器，有最小发送间隔限制
def asyncSendFireAlarm(image_file, conf):
    print(image_file, conf)
    global last_call_time
    # 获取当前时间
    current_time = time.time()
    # 如果是第一次调用函数或距离上次调用超过最小限制，则执行发送
    if (
        last_call_time is None
        or current_time - last_call_time >= kMinAlarmEventIntervalInS
    ):
        try:
            response = requests.post(
                kUploadServerApi,
                files={"image": open(image_file, "rb")},
                data={'device': sys.argv[1], "conf": conf, "timestamp": int(current_time)},
            )
            if response.status_code == 200:
                print("上传成功")
            else:
                print("上传失败")
        except Exception as e:
            print("上传异常", e)
        # 更新上次调用的时间
        last_call_time = current_time
    else:
        print("处于冷静期，忽略发送本次火情")


model = torch.hub.load(
    "ultralytics/yolov5", "custom", "best.pt"
)  # force_reload=True to update

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    # 读取摄像头图像
    ret, frame = cap.read()

    # 将图像转为Tensor并进行预处理
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 使用模型进行推理
    results = model(img)

    # 实时预览
    results.render()
    cvimg = cv2.cvtColor(results.ims[0], cv2.COLOR_RGB2BGR)
    cv2.imshow("YOLOv5", cvimg)

    # 读取置信度，该yolo模型的Detections对象中没有直接的conf可以读取，需要先crop后，在crop的结果中读取
    boxs = results.crop()

    if len(boxs) > 0:
        conf = boxs[0]["conf"].numpy().item()
        print("fire conf=", conf)
        if conf > kConfThreshold:
            # 保存 Image 对象为临时文件
            temp_file = ".temp.jpg"
            temp_img = Image.fromarray(results.ims[0])
            temp_img.save(temp_file)
            print(os.path.getsize(temp_file))
            asyncSendFireAlarm(temp_file, conf)

    # crop后会创建临时文件，需要及时删除，否则会不断占用存储空间
    shutil.rmtree("runs/detect")

    # 等待并监听键盘事件
    key = cv2.waitKey(1) & 0xFF

    # 如果按下 'q' 键，退出循环并关闭窗口
    if key == ord("q"):
        break

# 释放摄像头和关闭窗口
cap.release()
cv2.destroyAllWindows()
