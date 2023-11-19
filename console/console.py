from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Flask server!"

@app.route('/alert', methods=['GET', 'POST'])
def alert():
    if request.method == 'POST':
        # 从ESP8266接收的数据可以从request对象中提取
        temperature = request.args.get('temperature')
        print(f"Received temperature alert: {temperature}°C")
        # 你可以在这里添加代码来处理警报，例如发送通知
        # ...
        return "Alert received", 200
    else:
        return "This route is for POST requests", 200

@app.route('/buzz', methods=['GET'])
def buzz():
    print("Received buzz command from MacBook")
    # 在这里添加代码来发送指令到ESP8266，让Arduino Nano启动蜂鸣器
    # ...
    return "Buzz command sent to ESP8266", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8008)
