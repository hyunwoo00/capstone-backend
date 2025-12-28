import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv
from collections import deque
from app.cache import get_label_infos

buffer = deque()
buffer_size = 5  # sec
buffer_count = 0

def class_names_from_csv(class_map_csv_text):
  """Returns list of class names corresponding to score vector."""
  class_names = []
  with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      class_names.append(row['display_name'])

  return class_names

model = hub.load('https://tfhub.dev/google/yamnet/1')
class_map_path = model.class_map_path().numpy()
class_names = class_names_from_csv(class_map_path)

def get_predicted_label(wav_data):
  waveform = tf.convert_to_tensor(wav_data, dtype=tf.float32)
  scores, embeddings, spectrogram = model(waveform)
  infered_class = class_names[scores.numpy().mean(axis=0).argmax()]
  return infered_class

def model_output(wav_data):
  global buffer, buffer_count
  buffer.append(wav_data)

  label = get_predicted_label(wav_data)

  label_infos = get_label_infos(label)

   # 캐싱 실패 시 기본값 처리
  if label_infos is None:
    display_name_kor = "알 수 없음"
    label_category = 0
    print(f"[WARNING] 캐시에서 '{label}' 라벨을 찾을 수 없습니다.")

  else:
    display_name_kor = label_infos["display_name_kor"]
    label_category = label_infos["label_category"]

  #speech_check_data = None

  if len(buffer) > buffer_size:
    buffer.popleft()
  buffer_count += 1
  if buffer_count >= buffer_size:
    buffer_count = 0
    #speech_check_data = np.concatenate(list(buffer))

  return display_name_kor, label_category