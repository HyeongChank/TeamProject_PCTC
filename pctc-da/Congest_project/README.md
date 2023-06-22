## 실행방법.
- git에서 다운로드
- 가상환경 : python -m venv venv
            .\venv\Scripts\activate
- 환경구축(requirements 다운로드) : pip install -r requirements.txt
    <!-- - pip install -U scikit-learn 추가 설치     (requirements로 다운이 안됨)
    - pip install flask 추가 설치 -->

- FLASK 실행(src 폴더의 app.py 실행) 
- 모델 예측값 출력(POST 방식)
    - 작업+대기시간 예측 : http://10.125.121.220:5001/api/cnn_time_predict
    - 작업+대기차량 수 예측 : http://10.125.121.220:5001/api/cnn_count_predict

<!-- - lstm모델 : http://10.125.121.220:5001/api/lstm_predict
- randomforest 모델 : http://10.125.121.220:5001/api/r_predict -->

## 작동
- cnn모델 요청
    - 입력값 : 없음
    - 출력값 : time(10분 단위), actual_group, predict_group 각각 리스트로 json으로 출력


pip freeze > requirements.txt
pip install -U scikit-learn

