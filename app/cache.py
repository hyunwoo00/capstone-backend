import redis
from dotenv import load_dotenv
from app.db import get_connection
import os
import json

load_dotenv()

host = os.getenv('REDIS_HOST', 'redis')
port = os.getenv('REDIS_PORT', 6379)

# 로컬 Redis 연결
# host = 'redis' 도커 환경 내에서 host는 docker-compose.yml 내에서 정의한 redis의 이름.
# db = 0, 0번 db 사용.
# decode_responses=True // redis에서 가져온 데이터를 문자열로 자동 디코딩
r = redis.Redis(host=host, port=port, db=0, decode_responses=True)

def fetch_label(display_name):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SET NAMES utf8mb4;")
            cursor.execute("SELECT * FROM yamnet_labels WHERE display_name = %s;", (display_name, ))
        return cursor.fetchone()
    finally:
        #db 연결해제.
        conn.close()

#DB값을 REDIS로 쓰기
def cache_label_info(row):
    key = f"display_name:{row['display_name']}"
    value = {
            'display_name_kor': row['display_name_kor'],
            'label_category': row['label_category']
            }
    print(row['display_name_kor'])
    #redis 저장. 만료시간을 설정해 사용자의 위치를 고려한 캐싱.
    r.set(key, json.dumps(value, ensure_ascii=False), ex=3600)
    print(f"[CACHE] {key} → {value}")

    return value


#Hit -> Redis / Miss-> DB -> Redis
def get_label_infos(display_name):

    key = f"display_name:{display_name}"
    chaced_value = r.get(key)

    if chaced_value is not None:
        # JSON 문자열을 파이썬 딕셔너리로 변환
        return json.loads(chaced_value)      # str → dict
    
    row = fetch_label(display_name)
    if row is None:
        return None
    
    return cache_label_info(row)



    
    

