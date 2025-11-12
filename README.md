# WebReqTest
서버 api 통신 테스트

servers/
├─ server1/
│  ├─ main.py
│  └─ static/
│     └─ index.html
├─ server2/
│  ├─ main.py
│  └─ data.json
└─ requirements.txt

python -m venv server1
python -m venv server2
### 각 서버에서
pip install -r ../requirements.txt

### 서버 1
uvicorn server1.main:app --reload --port 8001
### 서버 2
uvicorn server2.main:app --reload --port 8002
