import psycopg2

table_name = "fire"


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

    def insert_image_data(self, image_file, conv, detected_at):
        if not self.conn:
            print("Not connected to the database")
            return

        try:
            cursor = self.conn.cursor()
            sql = (
                "INSERT INTO "
                + table_name
                + " (image_file, conv, detected_at) VALUES (%s, %s, %s)"
            )
            cursor.execute(
                sql,
                (
                    image_file,
                    conv,
                    detected_at,
                ),
            )
            self.conn.commit()
            print("Image data inserted into the database")
        except psycopg2.Error as e:
            print("Error inserting image data into the database:", e)
