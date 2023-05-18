import pandas as pd
import xgboost as xgb
import numpy as np
import datetime
from scipy.interpolate import interp1d
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras import backend as K
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def commit_model(new_data):
    # data load
    def load():
        # data = pd.read_csv("D:/김형찬/team_project/TeamProject_PCTC/pctc-da/Congest_project/data/congestcsv.csv", encoding='cp949')
        data = pd.read_csv("./data/congestcsv.csv", encoding='cp949')
        print(data.head())
        data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
        data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])

        print(data.shape)
        print(data.columns)
        return data
    
    # 기존 데이터와 new_data Concat 및 작업코드, 누적 컨테이너 열 정리
    def add_data(data, new_data):
        new_data = pd.DataFrame(new_data)
        new_data['작업 지시 시간'] = new_data['입차시간']
        new_data['작업 완료 시간'] = new_data['작업 지시 시간']
        print(new_data['작업 완료 시간'])
        # new_data = pd.DataFrame(new_data)
        new_data = new_data[['작업 지시 시간', '작업 완료 시간', '작업코드']]
        # new_data['작업코드'] = new_data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})        
        print('new_data', new_data)
        data = data[['작업 지시 시간', '작업 완료 시간', '작업코드']]
        # Combine existing data and new data
        print('기존', data)
        combined_data = pd.concat([data, new_data], ignore_index=True)
        combined_data['작업코드'] = combined_data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
        combined_data['누적 컨테이너'] = combined_data['작업코드'].cumsum()
        # # Save the combined data to a new CSV file

    ###### 기존 데이터를 포함한 데이터프레임을 CSV 파일로 저장
        # existing_csv_path = "./data/congestcsv.csv"
        # new_data.to_csv(existing_csv_path, index=False, mode='a', header=not os.path.exists(existing_csv_path))
        # print(f"데이터를 '{existing_csv_path}' 파일에 업데이트하여 저장했습니다.")

        print('combined_data', combined_data)
        return combined_data

    # 실제 혼잡도 구하고, 예측에 사용할 데이터 전처리
    def preprocessing(combined_data):

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


        n_data['입차시간'] = n_data['입차시간'].dt.round('5min')  # 5분 단위로 그룹화
        n_data = n_data.groupby('입차시간').mean().reset_index()  # 나머지 열의 평균값 계산
        return n_data, congest_level
    
    def make_model(data):
        # 데이터 전처리
        data = n_data[['입차시간', '대기시간new']].copy()
        data.set_index('입차시간', inplace=True)
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)

        # 시계열 데이터 준비
        window_size = 10  # 입력 시퀀스의 길이
        X = []
        y = []
        for i in range(len(scaled_data) - window_size):
            X.append(scaled_data[i:i+window_size])
            y.append(scaled_data[i+window_size])
        X = np.array(X)
        y = np.array(y)

        # 데이터셋 분할
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # LSTM 모델 구성
        model = Sequential()
        model.add(LSTM(units=64, activation='relu', input_shape=(window_size, 1)))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # 모델 학습
        model.fit(X_train, y_train, epochs=10, batch_size=32)

        # 예측 수행
        y_pred = model.predict(X_test)

        # 예측 결과 역전처리
        y_pred = scaler.inverse_transform(y_pred)
        # 예측 결과 출력
        predictions = pd.DataFrame({'입차시간': data.index[train_size+window_size:], '예측 대기시간new': y_pred.flatten()})
        print('predictions',predictions)
        predict_time = predictions['예측 대기시간new'].iloc[-1]
        # 입력한 시간의 예측 대기시간###################################
        print(predict_time)
        # 시간 복원
        test_dates = data.index[train_size+window_size:]
        test_dates = pd.to_datetime(test_dates)

    ########## 새로운 입력 데이터에 대한 예측 수행######################################
        # new_data.rename(columns={'입차시간': '입차시간'}, inplace=True)  # Match the column name
        # new_scaled_data = scaler.transform(new_data)
        # new_X = []
        # for i in range(len(new_scaled_data) - window_size + 1):
        #     new_X.append(new_scaled_data[i:i+window_size])
        # new_X = np.array(new_X)

        # new_y_pred = model.predict(new_X)
        # new_y_pred = scaler.inverse_transform(new_y_pred)

        # # 시간 복원
        # new_dates = new_data.index[window_size-1:]
        # new_dates = pd.to_datetime(new_dates)

        # # 예측 결과 출력
        # new_predictions = pd.DataFrame({'입차시간': new_dates, '예측 대기시간new': new_y_pred.flatten()})
        # print('new_predictions', new_predictions)
        
        # 예측 결과 그래프로 출력
        plt.figure(figsize=(12, 6))

        plt.scatter(test_dates, y_pred, label='Predicted', color='blue')
        plt.scatter(test_dates, data['대기시간new'].values[train_size+window_size:], label='Actual', color='red')
        # plt.scatter(new_dates, new_y_pred, label='New Prediction', color='green')  # 새로운 데이터 예측 추가
        plt.xlabel('입차시간')
        plt.ylabel('대기시간(min)')
        plt.title('Waiting Time Prediction')
        plt.ylim(0, 30)  # y축 범위 설정
        plt.legend()
        plt.grid(True)
        plt.show()
        return predict_time

    # 새로운 데이터 포인트 생성

    data = load()
    combined_data = add_data(data, new_data)
    n_data, congest_level = preprocessing(combined_data)
    predict_time = make_model(n_data)
    return predict_time, congest_level

    # new_pred = make_model(n_data)
    # print(new_pred)
    # print(congest_level)
    # return new_pred, congest_level


# model_file = "D:/김형찬/Congest_project/model/xgboost_model.pkl"
# # commit_model 함수를 pickle로 저장
# with open(model_file, 'wb') as f:
#     pickle.dump(commit_model, f)

if __name__=="__main__":
    new_data = {
    "입차시간": ["2021-02-07 23:10:37"],
    "작업코드": ["적하"]
}
    commit_model(new_data)
    
