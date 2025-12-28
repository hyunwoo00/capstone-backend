import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "myuser"),
        password=os.getenv("MYSQL_PASSWORD", 1111),
        db=os.getenv("MYSQL_DATABASE", "mydb"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor #튜플이 아닌 딕셔너리로 반환.
    )