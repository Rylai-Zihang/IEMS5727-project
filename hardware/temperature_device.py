import socket
import threading
import time
import struct
import requests
import sys


if len(sys.argv) < 2:
    print("Usage: python temperature_device.py device_name")
    sys.exit(1)


host_ip = "192.168.8.15"
host_port = 8080
esp8266_ip = "192.168.8.14"
esp8266_port = 8080
package_len = 1420
global former_time
former_time = time.time()
global sensor_online
sensor_online = 0
kUploadSeverApi = "http://localhost:8000/api/upload/temperature"
kkeepAliveServerApi = "http://127.0.0.1:8000/api/keepalive"


# 向所有客户端发送数据
def send_msg():
    global sensor_online
    while True:
        try:
            if sensor_online == 0:
                sensor_online = 1
            command = str(input("input: "))
            print("\n")
            if command == "1":
                server.sendto(command.encode(), host_esp8266)
            else:
                server.sendto("0".encode(), host_esp8266)
            time.sleep(5)
        except Exception as e:
            print("Send Error: ", e)
            sensor_online = 0


# 接收客户端的数据
def recv_data():
    global sensor_online
    while True:
        if sensor_online == 0:
            sensor_online = 1
        data, _ = server.recvfrom(package_len)
        # 使用 '<f' 来指定小端字节序浮点数
        temp = struct.unpack("<f", data)[0]
        payload = {
            "device": sys.argv[1],
            "temperature": temp,
            "timestamp": int(time.time()),
        }
        try:
            # 间隔小于5s不上报
            global former_time
            if (time.time() - former_time) >= 5:
                former_time = time.time()
                response = requests.post(kUploadSeverApi, data=payload)
                # 检查响应
                if response.status_code == 200:
                    print("Success:", response.json())
                else:
                    print("Error:", response.text)
                pass
        except Exception as e:
            print("Receive Error: ", e)
            sensor_online = 0
            pass


def keepalive():
    global sensor_online
    while True:
        if sensor_online == 1:
            try:
                response = requests.post(
                    kkeepAliveServerApi,
                    data={
                        "device": sys.argv[1],
                        "type": "sensor",
                        "timestamp": int(time.time()),
                    },
                )
                if response.status_code == 200:
                    print(response)
            except Exception as e:
                print("keepalive failed", e)
        threading.Event().wait(5)


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = (host_ip, host_port)
host_esp8266 = (esp8266_ip, esp8266_port)
server.bind(host)
t0 = threading.Thread(target=recv_data)
t0.start()
t1 = threading.Thread(target=send_msg)
t1.start()
# 启动keepalive线程
t2 = threading.Thread(target=keepalive, daemon=True)
t2.start()
