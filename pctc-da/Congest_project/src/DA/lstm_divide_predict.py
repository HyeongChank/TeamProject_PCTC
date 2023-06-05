import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras import backend as K

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

def load():
    # new_data 들어오면 기존 df 에 합치면 됨
    data = pd.read_excel("data/TSB_data.xlsx", sheet_name='야드크레이인_작업이력')
    scd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='반출입_예정컨테이너')
    cbd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_전')
    cad_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_후')
    quay_work_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='본선크레인_작업이력')

    # data, container_before_data, container_after_data merge
    ycb_common_values = data['컨테이너번호'].isin(cad_data['컨테이너번호']).sum() # 6103개
    #print('ycb_common_values', ycb_common_values)
    yard_con_common_df = pd.merge(data, cad_data, on='컨테이너번호')
    #print(yard_con_common_df)

    return yard_con_common_df

def preprocessing(common_df):
    # 데이터 전처리
    common_df['작업코드'] = common_df['작업코드'].replace({'VU': 1, 'VL': 2, 'GR': 3, 'GD': 4, 'TM':5,'TS':6})
    common_df['장비번호'] = common_df['장비번호'].replace({'Y02': 1})
    common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].replace({'M':1, 'F':2})
    common_df['수출/수입'] = common_df['수출/수입'].replace({'X':1,'I':2,'S':3,'M':4})
    
    # 외부트럭에 1 넣기
    common_df['야드트럭(번호)'] = common_df['야드트럭(번호)'].fillna(1)
    #print('common_df',common_df)
 
    # 시간 타입 통합
    common_df['작업생성시간'] = pd.to_datetime(common_df['작업생성시간'], format='%Y%m%d%H%M%S')
    common_df['작업완료시간'] = pd.to_datetime(common_df['작업완료시간'], format='%Y%m%d%H%M%S')
    #print('작업생성시간',common_df['작업생성시간'].dtype)
    #print('작업완료시간',common_df['작업완료시간'].dtype)
    common_df['작업+대기시간'] = common_df['작업완료시간'] -common_df['작업생성시간']
    #print(common_df['작업+대기시간'].isna().sum())
    #print('common_df',common_df.info())
    common_df = common_df[-200:]

    # 작업+대기시간을 초로 변환
    common_df['작업+대기시간'] = common_df['작업+대기시간'].dt.total_seconds() /60.0
    
    common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
    #print('common_df',common_df.info())
    common_df = common_df.dropna(subset=['작업+대기시간'])
    common_df_complete = common_df
    return common_df_complete

def make_model(common_df_complete):
    
    common_df_complete['작업+대기시간'] = common_df_complete['작업+대기시간'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    common_df_complete['작업+대기시간'] = scaler.fit_transform(common_df_complete['작업+대기시간'])


    # 시계열 데이터 준비
    window_size = 10  # 입력 시퀀스의 길이
    X = []
    y = []


    X_data = common_df_complete[['입차시간','작업+대기시간', '작업코드', '풀(F)공(M)','수출/수입','장비번호']]
    y_data = common_df_complete['작업+대기시간'].values



    for i in range(common_df_complete.shape[0] - window_size):
        X.append(X_data[i:i+window_size])
        y.append(y_data[i+window_size])
    X = np.array(X)
    y = np.array(y)

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # LSTM 모델 구성
    model = keras.Sequential()
    model.add(keras.layers.LSTM(units=64, input_shape=(window_size, 6)))
    model.add(keras.layers.Dense(units=1))
    # 모델 컴파일
    model.compile(loss='mean_squared_error', optimizer='adam')
    # # LSTM 모델 구성
    # model = Sequential()
    # model.add(LSTM(units=64, activation='relu', input_shape=(window_size, 6)))
    # model.add(Dense(units=1))
    # model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습
    model.fit(X_train, y_train, epochs=10, batch_size=32)

    # 예측 수행
    y_pred = model.predict(X_test)

    # 예측 결과 역스케일링
    y_test = scaler.inverse_transform(y_test)
    y_pred = scaler.inverse_transform(y_pred)
    # 오차 계산
    print("예측값 : ", y_pred)
    print("NaN in y_test: ", np.isnan(y_test).any())
    print("NaN in y_pred: ", np.isnan(y_pred).any())
    print("y_test dtype: ", y_test.dtype)
    print("y_pred dtype: ", y_pred.dtype)


    error = y_test - y_pred
    mae = np.mean(np.abs(error))

    print("Error: \n", error)
    print("Mean Absolute Error: ", mae)

    plt.figure(figsize=(10, 5))

    plt.scatter(range(len(y_test)), y_test, label='Actual')
    plt.scatter(range(len(y_pred)), y_pred, label='Predicted', color='red')
    plt.ylabel('작업+대기시간')
    plt.title('Time Prediction(LSTM)')
    plt.legend()
    # plt.show()
    
 
if __name__=='__main__':
    load_data = load()
    common_df_complete = preprocessing(load_data)
    make_model(common_df_complete)