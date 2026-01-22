from fastapi import HTTPException
from models import *
import os

host = os.getenv("HOST", "localhost")
root = os.getenv("ROOT", "")
password = os.getenv("PASSWORD", "password")
db_name = os.getenv("DB_NAME", "weapons_db")

def connect_and_create():
    connection = MySQLConnection(host, root, password)
    try:
        connection.mysqlconnect()
        connection.create_db(db_name)
        connection.create_table("weapons_table")
        return connection    
    except Exception as e:
        raise HTTPException(status_code=503, detail=e)