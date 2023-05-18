## 진행상황.
- predict_LSTM.py = > 기 데이터의 대기시간 학습하여 향후 대기시간(5분 단위) 예측(LSTM 사용)
    - 향후 예측시간(현재 기준 5분단위 개수) 입력 시 기 학습 내용으로 향후 대기시간s 출력

- main.py = > 대기시간, 야드 내 트럭 대수를 통한 혼잡도 분석 및 Congest_level 출력
    - 입력값으로 예측 입차시기를 입력하면 예측 대기시간 및 혼잡도 출력
    - 이에 따라 1.입차시기, 2.작업 코드를 입력해야 함

- simulator 데이터 생성 및 시뮬레이션(Auto) 및 애니메이션 실행
    - simulator_make_data.py => Auto로 데이터 생성
    - simulator_sort_graph.py => simulator animation 생성
    
- randomForest.py = > 현재 대기차량, 혼잡도 입력 시 대기시간 예측(+오차 측정)
- xgboost_test2.py = > 야드 내 블록별 혼잡도를 분석하고, 혼잡도 level이 2 -> 1이 되는 데 걸리는 시간 분석(+정확도 측정)
- Arima.py = > 시간 입력 시 해당 시간의 야드 내 트럭 대수 분석

## Todo
- 

## 세부내용
- main.py 실행 : 'http://10.125.121.220:5001/api/congest2'
    - 입력예제 : {"입차시간": ["2021-02-07 22:30:37"],"작업코드": ["적하"]}
- 