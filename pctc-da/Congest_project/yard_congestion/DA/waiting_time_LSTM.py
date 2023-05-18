import pandas as pd
import datetime
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras import backend as K
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def load():
    data = pd.read_csv("D:/김형찬/team_project/TeamProject_PCTC/pctc-da/Congest_project/data/congestcsv.csv", encoding='cp949')
    print(data.head())
    data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
    data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])
    data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
    data['누적 컨테이너'] = data['작업코드'].cumsum()
    print(data)
    return data

def preprocessing(data):
    data['입차시간'] = data['작업 지시 시간']
    data['출차시간'] = data['작업 완료 시간']
    data['대기시간'] = (data['출차시간'] - data['입차시간']).dt.total_seconds()//60
    print(data[['입차시간', '대기시간']])
    return data

def make_model(data):
    df = data
    # 데이터 전처리
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[['대기시간']].values)
    # 입력 (X)와 출력 (y) 데이터 설정하기
    X = df['입차시간'].tolist()
    y = df['대기시간'].tolist()
    X_timestamps = pd.to_datetime(X).astype('int64') // 10**9  # POSIX 시간 변환
    # 입력 시퀀스 생성
    
    sequence_length = 30  # 입력으로 사용할 이전 시간 데이터의 개수
    X_sequence = []
    y_sequence = []
    for i in range(sequence_length, len(X_timestamps)):
        X_sequence.append(X_timestamps[i-sequence_length:i])
        y_sequence.append(y[i])

    # 배열 형태로 변환
    X_sequence = np.array(X_sequence)
    y_sequence = np.array(y_sequence)
    
    # LSTM 모델 구축
    model = Sequential()
    model.add(LSTM(units=64, input_shape=(sequence_length, 1)))
    model.add(Dense(units=1))
    # 모델 컴파일
    model.compile(loss='mean_squared_error', optimizer='adam')
    # 모델 학습
    model.fit(X_sequence, y_sequence, epochs=10, batch_size=32)
    # 향후 대기시간 예측
    future_X_sequence = X_sequence[-1].reshape(1, sequence_length, 1)
    future_predicted_wait_time = model.predict(future_X_sequence)
    print(len(future_X_sequence))
    print(f"향후 예측된 대기시간: {future_predicted_wait_time}")

    predicted_values = []
    input_data = scaled_data[-sequence_length:]  # 마지막 4개의 혼잡도 값을 입력으로 사용    
    for _ in range(12):  # 1일은 144개의 10분 간격으로 구성됨
            # 현재 입력 데이터
            input_data = scaled_data[-sequence_length:]
            input_data_reshaped = input_data.reshape(1, sequence_length, 1)
            # 현재 입력 데이터로 예측
            predicted_value = model.predict(input_data_reshaped)
            # 예측값을 원래 스케일로 변환
            predicted_value_scaled = scaler.inverse_transform(predicted_value)
            # 예측값을 리스트에 추가
            predicted_values.append(predicted_value_scaled[0][0])
            # 다음 시간의 입력 데이터 업데이트
            input_data = np.append(input_data[1:], predicted_value_scaled)
            scaled_data = np.append(scaled_data, predicted_value, axis=0)            

    # 시간대 생성
    start_time = df['입차시간'].iloc[-1] + pd.DateOffset(minutes=10)  # 데이터프레임의 마지막 시간 다음 시간부터 시작
    time_range = pd.date_range(start=start_time, periods=12, freq='10T')
    # 예측된 혼잡도 값을 데이터프레임으로 변환
    predicted_df = pd.DataFrame({'입차시간': time_range, 'Predicted_congest': predicted_values})
    # 원래 데이터와 예측 데이터 결합
    combined_df = pd.concat([df, predicted_df], axis=0)
    print(combined_df)            
    # 그래프 그리기
    plt.plot(combined_df['입차시간'], combined_df['대기시간'], label='Actual')
    plt.plot(combined_df['입차시간'], combined_df['Predicted_congest'], label='Predicted')
    plt.xlabel('입차시간')
    plt.ylabel('대기시간')
    plt.title('Actual vs. Predicted 대기시간')
    plt.legend()
    plt.show()


if __name__=='__main__':
    data = load()
    data = preprocessing(data)
    make_model(data)