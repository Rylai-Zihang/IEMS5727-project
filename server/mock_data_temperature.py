import psycopg2
from psycopg2.extras import execute_values
import random
from datetime import datetime, timedelta
import os

# 数据库连接参数
conn_params = {
    "dbname": "iot",
    "user": os.getenv("USER"),
    "password": "",
    "host": "localhost",
}

# 建立数据库连接
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

# 生成伪造数据
num_records = 100  # 要生成的记录数
devices = ["DeviceB", "DeviceC", "DeviceD", "DeviceE"]
data = []

for _ in range(num_records):
    device = random.choice(devices)
    temp = random.randint(20, 100)  # 假设温度范围在20到100之间
    # 随机生成过去10分钟内的时间
    random_seconds = random.randint(0, 10 * 60)
    detected_at = datetime.now() - timedelta(seconds=random_seconds)

    data.append((device, temp, detected_at))

# 插入数据
insert_query = "INSERT INTO temperature (device, temperature, detected_at) VALUES %s"
execute_values(cur, insert_query, data)

# 提交事务
conn.commit()

# 关闭游标和连接
cur.close()
conn.close()
