import pandas as pd
import xgboost as xgb
import numpy as np
import datetime
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from scipy.interpolate import interp1d
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras import backend as K
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
# 기존 데이터
data = [26.0, 26.0, 24.0, 26.0, 16.0, 9.0, 7.0, 29.0, 25.0, 23.0, 26.0, 26.0, 24.0, 26.0, 16.0, 9.0, 7.0, 29.0, 25.0, 23.0, 26.0, 26.0, 24.0, 26.0, 16.0, 9.0, 7.0, 29.0, 25.0, 23.0, 26.0, 26.0, 24.0, 26.0, 16.0, 9.0, 7.0, 29.0, 25.0, 23.0, 26.0, 26.0, 24.0, 26.0, 16.0, 9.0, 7.0, 29.0, 25.0, 23.0, 26.0, 26.0, 24.0, 26.0, 16.0, 9.0, 7.0, 29.0, 25.0, 23.0, 26.0, 16.0, 9.0, 7.0, 29.0, 25.0, 23.0]

# data load
def load():
    data = pd.read_csv("D:/김형찬/team_project/TeamProject_PCTC/pctc-da/Congest_project/data/congestcsv.csv", encoding='cp949')
    print(data.head())
    data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
    data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])

    print(data.shape)
    print(data.columns)
    return data

# 기존 데이터와 new_data Concat 및 작업코드, 누적 컨테이너 열 정리
def add_data(data, new_data):
    new_data = pd.DataFrame(new_data, columns=['작업 지시 시간', '작업 완료 시간', '작업코드'])
    # new_data['작업코드'] = new_data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})        
    print('new_data', new_data)
    data = data[['작업 지시 시간', '작업 완료 시간', '작업코드']]
    # Combine existing data and new data
    print('기존', data)
    combined_data = pd.concat([data, new_data], ignore_index=True)
    combined_data['작업코드'] = combined_data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
    combined_data['누적 컨테이너'] = combined_data['작업코드'].cumsum()
    # # Save the combined data to a new CSV file
    # combined_data.to_csv("D:/김형찬/Congest_project/data/congestcsv.csv", index=False)
    print('combined_data', combined_data)
    return combined_data

# 실제 혼잡도 구하고, 예측에 사용할 데이터 전처리
def preprocessing(combined_data):
    # data = data

    df = pd.DataFrame(combined_data)
    df['작업 지시 시간'] = pd.to_datetime(df['작업 지시 시간'])
    df['작업 완료 시간'] = pd.to_datetime(df['작업 완료 시간'])
    df['입차시간'] = df['작업 지시 시간']
    df['출차시간'] = df['작업 완료 시간']
    df['대기시간'] = df['출차시간'] - df['입차시간']

    n_data = df.copy()
    n_data['대기차량'] = 20
    flag = 3
    # 대기차량 수 계산
    for i in range(5, len(n_data)):
        n_data.loc[i, '대기차량'] = n_data.loc[i, '대기차량'] + 1
        if n_data.loc[i, '입차시간'] >= n_data.loc[i, '출차시간']:
            n_data.loc[i, '대기차량'] = n_data.loc[i, '대기차량'] - 1
        elif n_data.loc[i, '입차시간'] < n_data.loc[i, '출차시간']:
            for j in range(i-1, flag+1, -1):
                if n_data.loc[i, '입차시간'] >= n_data.loc[j, '출차시간']:
                    n_data.loc[i, '대기차량'] = n_data.loc[i, '대기차량'] -1
                    flag = j

    n_data.loc[i, '혼잡도'] = 0                
    for i in range(0, len(n_data)):
        if n_data.loc[i, '대기차량'] > 20:
            n_data.loc[i, '혼잡도'] = 3
        elif n_data.loc[i, '대기차량'] == 20:
            n_data.loc[i, '혼잡도'] = 2
        else:
            n_data.loc[i,'혼잡도'] = 1

    # 대기시간을 숫자(분)로 변환하는 함수
    def convert_to_minutes(timedelta_obj):
        seconds = timedelta_obj.total_seconds()
        minutes = seconds // 60
        return minutes

    # 대기시간을 숫자(분)로 변환하여 새로운 열 추가
    n_data['대기시간new'] = n_data['대기시간'].apply(convert_to_minutes)
    congest_level = n_data[['혼잡도']].tail(1).values
    n_data = n_data.drop(['작업 지시 시간', '작업 완료 시간', '작업코드', '출차시간', '대기시간'], axis=1, inplace=False)
    print('new_n_data', n_data)
    column_list = n_data['대기시간new'].tolist()

    print(column_list)

    # n_data['입차시간'] = n_data['입차시간'].dt.round('5min')  # 5분 단위로 그룹화

    # n_data = n_data.groupby('입차시간').mean().reset_index()  # 나머지 열의 평균값 계산

    return column_list

new_data = {'작업 지시 시간': ['2021-02-07 13:05:37'], '작업 완료 시간': ['2021-02-07 13:28:52'], '대기차량': [25], '작업코드':['적하']}
data = load()
combined_data = add_data(data, new_data)
column_list = preprocessing(combined_data)


data = column_list



# 데이터 전처리
def preprocess_data(data, lookback):
    X, y = [], []
    for i in range(len(data) - lookback):
        X.append(data[i:i+lookback])
        y.append(data[i+lookback])
    X = np.array(X)
    y = np.array(y)
    return X, y

lookback = 30
X, y = preprocess_data(data, lookback)
previous_data = data[-30:]
# LSTM 모델 구성
model = keras.Sequential()
model.add(keras.layers.LSTM(units=64, input_shape=(lookback, 1)))
model.add(keras.layers.Dense(units=1))

# 모델 컴파일
model.compile(loss='mean_squared_error', optimizer='adam')

# 모델 학습
model.fit(X, y, epochs=10, batch_size=32)

# 이후 30개의 대기시간 예측
last_sequence = data[-lookback:]  # 최근 30개의 대기시간 데이터를 가져옵니다.
predicted_data = []
for _ in range(5):
    sequence = np.array(last_sequence)
    sequence = np.reshape(sequence, (1, lookback, 1))
    prediction = model.predict(sequence)[0][0]
    predicted_data.append(prediction)
    last_sequence.append(prediction)
    last_sequence = last_sequence[1:]

print(predicted_data)

# # 그래프로 예측 결과와 실제 데이터를 표현합니다.
# x_axis = range(len(data), len(data) + 30)
# plt.plot(x_axis, predicted_data, label='Predicted Data')
# plt.plot(x_axis, data[-30:], label='Actual Data')
# plt.xlabel('Time')
# plt.ylabel('Waiting Time')
# plt.ylim(0, 30)  # y축 범위 설정
# plt.legend()
# plt.show()

# 그래프로 예측 결과와 실제 데이터를 표현합니다.
x_axis_previous = range(len(data)-30, len(data))  # 기존 데이터 중 마지막 30개의 인덱스
x_axis_predicted = range(len(data), len(data) + 5)  # 이후 30개의 예측 데이터
# 개수 오류 계속 났었음. ( x_axis_previous = previous_data 맞춰줘야 하고, x_axis_predicted = predicted_data 맞춰줘야 함)
plt.plot(x_axis_previous, previous_data, label='Previous Data')
plt.plot(x_axis_predicted, predicted_data, label='Predicted Data')
plt.xlabel('Time')
plt.ylabel('Waiting Time')
plt.ylim(0, 30)  # y축 범위 설정
plt.legend()
plt.show()

