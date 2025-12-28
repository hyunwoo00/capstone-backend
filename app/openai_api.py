from dotenv import load_dotenv
import os
from openai import OpenAI

# .env 파일에서 OPENAI_API_KEY를 불러옴
load_dotenv()

client = OpenAI()  # 키는 환경 변수에서 자동 로드됨

# system prompt
system_prompt = (
        "너는 청각장애인을 위한 MR 보조 시스템에서 작동하는 안전 행동 추천 AI다."
        "사용자는 청각장애로 인해 소리를 직접 들을 수 없다. 현재 시스템은 마이크로 수집한 소리를 분석하여 라벨링하고, 카메라 화면을 캡처해 함께 제공한다."
        "너는 입력된 **소리 라벨 정보**와 **이미지의 시각 정보**를 함께 분석해, 사용자가 위험한 상황에 처했는지를 판단하고, 그에 맞는 **구체적이고 즉각 실행 가능한 행동**을 한 문장으로 제안해야 한다."
        "입력 정보: - 소리 라벨: 사용자의 주변에서 감지된 소리들의 라벨 목록 (예: 차량 경적, 사이렌, 말소리 등)- 이미지: 사용자의 현재 시야를 보여주는 장면 (예: 도로, 차량, 사람, 교통 상황 등이 포함될 수 있음)"
        "출력 형식: - 권장 행동: [한 문장으로 명확하게 사용자에게 지시]"
        "지시 사항:- 행동은 짧고, 명령형 문장으로 말해줄 것 (예: ""도로 가장자리로 이동하세요."")- 현재 위험이 크지 않더라도, 소리를 기반으로 할 수 있는 조심성 있는 행동을 제안할 것- 소리와 이미지가 모순될 경우, **이미지 정보**를 더 신뢰할 것- 추상적 조언 대신, 물리적인 행동 지시를 줄 것"
        "예시:- 소리 라벨: ""차량 경적""- 이미지: 도로 앞에서 차량이 빠르게 접근 중인 이미지→ 권장 행동: ""횡단을 멈추고 차량이 지나간 후 다시 움직이세요."""
)

# 이미지 + 텍스트를 기반으로 OpenAI Vision API 호출
def call_openAi(image_data, audio_label):
    messages = []
    messages.append({
        "role": "system",
        "content": system_prompt
    })
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": audio_label  # 예: "'Vehicle'이라는 소리가 감지된 상황에서 찍힌 이미지입니다..."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}"
                    }
                }
            ]
        }
    )

    # GPT-4o 모델 호출 (Vision 지원)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    # 텍스트 응답 추출
    return response.choices[0].message.content