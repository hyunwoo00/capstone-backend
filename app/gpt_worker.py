import json
from flask_socketio import SocketIO
from app.openai_api import call_openAi
import numpy as np
from redis import Redis

# Redis 연결
r = Redis(host='redis', port='6379', db=0)

# 여기도 똑같은 Redis를 바라보게 설정
# write_only=True는 수신은 안 하고 발신만 하겠다는 최적화 옵션.
external_socketio = SocketIO(message_queue='redis://redis:6379/0', write_only=True)

def gpt_worker():
    while True:
        _, json_data = r.blpop("gpt_queue")
        data = json.loads(json_data)
        
        sid = data["sid"]
        img_data = data["img_data"]
        label = data["label"] 

        result = call_openAi(img_data, label)

        external_socketio.emit('gpt_response', {"suggestion":result, "label": label}, room = sid)
        

if __name__ == "__main__":
    gpt_worker()
