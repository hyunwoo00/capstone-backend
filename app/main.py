from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from app.openai_api import call_openAi
from app.yamnet import model_output
from app.routes import main as main_blueprint
import numpy as np
import json
from redis import Redis


app = Flask(__name__)
socket = SocketIO(app,
                  async_mode='eventlet', 
                  ping_timeout=120, 
                  message_queue='redis://redis:6379/0', 
                  cors_allowed_origins="*"
                  )

r = Redis(host= "redis", port="6379", db=0, decode_responses=True)

#blueprint 등록(다른 파일에 http routes 정리)
app.register_blueprint(main_blueprint)

@socket.on("connect")
def on_connect():
    sid = request.sid
    r.setex(f"client:{sid}", 60, "alive")


@socket.on('audio')
def handle_audio(audio_data):

    data = {
        "sid": request.sid, #클라이언트 세션 id
        "audio_data": audio_data
    }

    r.rpush("audio_queue", json.dumps(data))

@socket.on('screenshot')
def handle_openAi(request_data):
    if isinstance(request_data, str):  # 문자열이면 JSON 파싱
        loaded_data = json.loads(request_data)

    img_data = loaded_data["image"]
    label = loaded_data["label"]

    data = {
        "sid": request.sid, #클라이언트 세션 id
        "img_data": img_data,
        "label": label
    }

    r.rpush("gpt_queue", json.dumps(data))

@socket.on("disconnect")
def on_disconnect():
    sid = request.sid
    r.delete(f"client:{sid}")
