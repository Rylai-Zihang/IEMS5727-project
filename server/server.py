from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from db import Database
import os

# 创建自定义的请求处理程序
class MyRequestHandler(BaseHTTPRequestHandler):
    # 类变量，所有实例共享同一个数据库连接
    db = None

    @classmethod
    def setup_database(cls):
        username = os.getenv('USER') or "defaultuser"  # 如果 USER 环境变量不存在，则使用默认用户名
        # 初始化数据库连接
        cls.db = Database("localhost", "5432", "iot", username, "")
        cls.db.connect()

    @classmethod
    def teardown_database(cls):
        # 关闭数据库连接
        if cls.db:
            cls.db.disconnect()
            cls.db = None

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
                conf_value = form_data.getvalue("conf", "")
                # 获取 'timestamp' 字段的值
                detected_at = form_data.getvalue("timestamp", "")
                print(conf_value)
                print(detected_at)
                # 插入图像数据到数据库
                MyRequestHandler.db.insert_image_data(image_file, conf_value, int(detected_at))
                # 返回响应
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("Image received and processed", "utf-8"))
            else:
                self.send_error(400, "Invalid request")
        else:
            self.send_error(404, "Not found")

# 创建服务器实例并启动
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    handler_class.setup_database()  # 设置数据库连接
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    try:
        print(f"Starting server on port {port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        handler_class.teardown_database()  # 清理数据库连接
        httpd.server_close()
        print("Stopping server.")

# 运行服务器
if __name__ == "__main__":
    run()
