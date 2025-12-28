#FROM python:3.9 : Python 3.9 기반의 도커 이미지 사용
#WORKDIR /app: 컨테이너 내의 작업 디렉토리를 /app으로 설정
#COPY . /app: 현재 디렉토리와 모든 파일을 /app으로 복사
#RUN pip install --upgrade pip: pip 업그레이드
#RUN pip install -r requirements.txt: 모든 의존성 패키지 설치
#CMD []: 컨테이너 시작할 때 실행할 기본 명령어

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

COPY . /app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "-k", "eventlet", "-w", "4", "-b", "0.0.0.0:5001", "app.main:app"]

