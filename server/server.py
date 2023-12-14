from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from db import Database


# 创建自定义的请求处理程序
class MyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = Database("localhost", "5432", "fire-db", "hezihang", "")
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/upload":
            # 解析请求的内容
            content_type, _ = cgi.parse_header(self.headers["Content-Type"])
            if content_type == "multipart/form-data":
                form_data = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={"REQUEST_METHOD": "POST"},
                )

                # 获取上传的图像数据
                image_file = form_data["image"].file.read()
                # 获取 'conf' 字段的值
                conf_value = form_data.getfirst("conf", "")
                # 获取 'timestamp' 字段的值
                detected_at = form_data.getfirst("timestamp", "")
                print(conf_value)
                print(detected_at)

                # 连接到数据库并插入图像数据
                self.db.connect()
                self.db.insert_image_data(image_file, conf_value, detected_at)
                self.db.disconnect()

                # 处理图像数据，可以在这里进行任何图像处理操作

                # 返回响应
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Image received and processed", "utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Invalid request", "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Not found", "utf-8"))


# 创建服务器实例并启动
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print("Starting server on port", port)
    httpd.serve_forever()


# 运行服务器
if __name__ == "__main__":
    run()
