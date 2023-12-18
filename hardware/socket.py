import socket
import threading
import time
import struct
import requests

host_ip = "192.168.8.15"
host_port = 8080
esp8266_ip = "192.168.8.14"
esp8266_port = 8080
package_len = 1420
url = "http://localhost:8000/api/upload/temperature"


# 向所有客户端发送数据
def send_msg():
    while True:
        try:
            command = str(input("input: "))
            print("\n")
            if command == "1":
                server.sendto(command.encode(), host_esp8266)
            else:
                server.sendto("0".encode(), host_esp8266)
            time.sleep(5)
        except Exception as e:
            try:
                print("Send Error!")
            except Exception as e:
                pass


# 接收客户端的数据
def recv_data():
    while True:
        data, _ = server.recvfrom(package_len)
        # 使用 '<f' 来指定小端字节序浮点数
        temp = struct.unpack("<f", data)[0]
        payload = {
            "device": "Device A",
            "temperature": temp,
            "timestamp": int(time.time()),
        }
        response = requests.post(url, data=payload)
        print(response)
        # 检查响应
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print("Error:", response.text)


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = (host_ip, host_port)
host_esp8266 = (esp8266_ip, esp8266_port)
server.bind(host)
t0 = threading.Thread(target=recv_data)
t0.start()
t1 = threading.Thread(target=send_msg)
t1.start()
