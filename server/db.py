import psycopg2
import base64
import random
from collections import defaultdict
import json





table_name_fire = "fire"
table_name_temperature = "temperature"


class Database:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            print("Connected to the database")
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from the database")

    def insert_fire_data(self, device, image_file, conv, detected_at):
        if not self.conn:
            print("Not connected to the database")
            return

        try:
            cursor = self.conn.cursor()
            sql = (
                "INSERT INTO "
                + table_name_fire
                + " (device, image_file, conv, detected_at) VALUES (%s, %s, %s, to_timestamp(%s))"
            )
            cursor.execute(
                sql,
                (
                    device,
                    image_file,
                    conv,
                    detected_at,
                ),
            )
            self.conn.commit()
            print("Fire data inserted into the database")
        except psycopg2.Error as e:
            print("Error inserting fire data into the database:", e)

    def insert_temperature_data(self, device, temperature, detected_at):
        if not self.conn:
            print("Not connected to the database")
            return

        try:
            cursor = self.conn.cursor()
            sql = (
                "INSERT INTO "
                + table_name_temperature
                + " (device, temperature, detected_at) VALUES (%s, %s, to_timestamp(%s))"
            )
            cursor.execute(
                sql,
                (
                    device,
                    temperature,
                    detected_at,
                ),
            )
            self.conn.commit()
            print("Temperature data inserted into the database")
        except psycopg2.Error as e:
            print("Error inserting temperature data into the database:", e)


    def get_recent_fires_by_device(self, num):
        if not self.conn:
            print("Not connected to the database")
            return

        query = f"WITH RankedFire AS (   SELECT     id,     device,     image_file,     conv,     detected_at,     ROW_NUMBER() OVER (PARTITION BY device ORDER BY detected_at DESC) AS rn   FROM     fire ) SELECT   id,   device,   image_file,   conv,   detected_at FROM   RankedFire WHERE   rn <= %s;"

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (num,))
            records = cursor.fetchall()
            self.conn.commit()
            fires = []
            for record in records:
                fire = {
                    'device': record[1],
                    'conv':  float(record[3]), 
                }
                fires.append(fire)
            return fires
        except psycopg2.Error as e:
            print("Database error:", e)
            return []

    def get_recent_fires_with_images(self, num):
        if not self.conn:
            print("Not connected to the database")
            return

        query = f"SELECT * FROM {table_name_fire} ORDER BY detected_at DESC LIMIT %s;"

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (num,))
            records = cursor.fetchall()
            self.conn.commit()
            fires = []
            for record in records:
                if random.randint(1, 2) % 2 == 0:
                    dealt_value = "true"
                else:
                    dealt_value = "false"
                fire = {
                    'device': record[1],
                    'shortcut': "data:image/jpg;base64,"+base64.b64encode(record[2].tobytes()).decode('utf-8'),
                    'level':  "Low" if float(record[3]) < 0.4 else ("Medium" if float(record[3]) < 0.6 else "High"), 
                    'dealt' : dealt_value,
                    'time': record[4].isoformat(),
                }
                fires.append(fire)
            return fires
        except psycopg2.Error as e:
            print("Database error:", e)
            return []

    def get_device_warning_data(self):
        if not self.conn:
            print("Not connected to the database")
            return

        query = f"SELECT device, COUNT(CASE WHEN conv BETWEEN 0.2 AND 0.4 THEN 1 END) AS count_02_to_04, COUNT(CASE WHEN conv BETWEEN 0.4 AND 0.6 THEN 1 END) AS count_04_to_06, COUNT(CASE WHEN conv BETWEEN 0.6 AND 0.8 THEN 1 END) AS count_06_to_08 FROM {table_name_fire} GROUP BY device ORDER BY device;"

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            records = cursor.fetchall()
            deviceWarningData = []
            for record in records:
                data = {
                    'device': record[0],
                    'warningLevels' :[
                        {
                        'name':"Low",
                        'value':record[1],
                        },
                        {
                        'name':"Medium",
                        'value':record[2],
                        },
                        {
                        'name':"High",
                        'value':record[3],
                        }
                    ]
                }
                deviceWarningData.append(data)
            return deviceWarningData
        except psycopg2.Error as e:
            print("Database error:", e)
            return []


    def get_recent_device_tempeature_data(self, num):
        if not self.conn:
            print("Not connected to the database")
            return

        query = f"WITH RankedTemperatures AS (  SELECT device, temperature, to_char(detected_at, 'YYYY-MM-DD\"T\"HH24:MI:SS.MS') as time, ROW_NUMBER() OVER (PARTITION BY device ORDER BY detected_at DESC) as rn  FROM temperature) SELECT  device,  temperature,  time FROM  RankedTemperatures WHERE  rn <= %s ORDER BY device,  time;"

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (num,))
            self.conn.commit()
            devices_data = defaultdict(list)
            for record in cursor.fetchall():
                device, temperature, time = record
                devices_data[device].append({
                    'device': device,
                    'temperature': temperature,
                    'time': time
                })
            devices_data = dict(devices_data)
            return list(devices_data.values())
        except psycopg2.Error as e:
            print("Database error:", e)
            return []


    def get_total_fires_count(self):
        if not self.conn:
            print("Not connected to the database")
            return

        query = f"SELECT COUNT(*) FROM {table_name_fire};"

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            records = cursor.fetchall()
            return records[0][0]
        except psycopg2.Error as e:
            print("Database error:", e)
            return 0

    def get_risk_data(self):
        if not self.conn:
            print("Not connected to the database")
            return

        query = f"SELECT COUNT(*) FROM {table_name_fire};"

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            records = cursor.fetchall()
            return records[0][0]
        except psycopg2.Error as e:
            print("Database error:", e)
            return 0

