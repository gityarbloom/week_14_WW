import pymysql

class MySQLConnection:
    def __init__(self, host, root, password):
        self.host = os.getenv("HOST", "localhost")
        self.root = root
        self.password = password
        self.conn = None
        self.db = None
        self.table = None


    def mysqlconnect(self):
        if self.conn is None:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.root,
                password=self.password
            )

    def create_db(self, db_name):
        self.mysqlconnect()
        cur = self.conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.conn.select_db(db_name)
        self.conn.commit()
        self.db = db_name

    def create_table(self, table_name):
        self.mysqlconnect()
        cur = self.conn.cursor()
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT PRIMARY KEY AUTO_INCREMENT,
            weapon_id VARCHAR(50),
            weapon_name VARCHAR(50),
            weapon_type VARCHAR(50),
            range_km INT,
            weight_kg FLOAT,
            manufacturer VARCHAR(50),
            origin_country VARCHAR(50),
            storage_location VARCHAR(50),
            year_estimated INT,
            risk_level VARCHAR(50) NOT NULL
        )
        """)
        self.conn.commit()
        self.table = table_name

    def insert_into(self, weapon_id, weapon_name, weapon_type, range_km, weight_kg, manufacturer, origin_country, storage_location, year_estimated, risk_level):
        self.mysqlconnect()
        cur = self.conn.cursor()
        sql_query = f"""
        INSERT INTO {self.table} (weapon_id, weapon_name, weapon_type, range_km, weight_kg, manufacturer, origin_country, storage_location, year_estimated, risk_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (weapon_id, weapon_name, weapon_type, range_km, weight_kg, manufacturer, origin_country, storage_location, year_estimated, risk_level)
        cur.execute(sql_query, values)
        self.conn.commit()
        return "The insert to the table was done successfuly"

    def close_connection(self):
        self.conn.close()
        self.conn = None