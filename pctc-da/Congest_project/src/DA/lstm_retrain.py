import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.metrics import r2_score
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
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# data load
def operate(predict_c):
    count = 1
    p_count = predict_c
    prediction_list = []
    def load():
        # new_data 들어오면 기존 df 에 합치면 됨
        data = pd.read_excel("data/TSB_data.xlsx", sheet_name='야드크레이인_작업이력')
        scd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='반출입_예정컨테이너')
        cbd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_전')
        cad_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_후')
        quay_work_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='본선크레인_작업이력')

        # data, container_before_data, container_after_data merge
        ycb_common_values = data['컨테이너번호'].isin(cad_data['컨테이너번호']).sum() # 6103개
        yard_con_common_df = pd.merge(data, cad_data, on='컨테이너번호')


        return yard_con_common_df

    def preprocessing(common_df):
        # 데이터 전처리
        common_df['작업코드'] = common_df['작업코드'].replace({'VU': 1, 'VL': 2, 'GR': 3, 'GD': 4, 'TM':5,'TS':6})
        common_df['장비번호'] = common_df['장비번호'].replace({'Y02': 1})
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].replace({'M':1, 'F':2})
        common_df['수출/수입'] = common_df['수출/수입'].replace({'X':1,'I':2,'S':3,'M':4})
        
        # 외부트럭에 1 넣기
        common_df['야드트럭(번호)'] = common_df['야드트럭(번호)'].fillna(1)
    
        # 시간 타입 통합
        common_df['작업생성시간'] = pd.to_datetime(common_df['작업생성시간'], format='%Y%m%d%H%M%S')
        common_df['작업완료시간'] = pd.to_datetime(common_df['작업완료시간'], format='%Y%m%d%H%M%S')
        #print('작업생성시간',common_df['작업생성시간'].dtype)
        #print('작업완료시간',common_df['작업완료시간'].dtype)
        common_df['작업+대기시간'] = common_df['작업완료시간'] -common_df['작업생성시간']
        # common_df = common_df[-200:]

        # 작업+대기시간을 초로 변환
        common_df['작업+대기시간'] = common_df['작업+대기시간'].dt.total_seconds() /60.0
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
        common_df = common_df.dropna(subset=['작업+대기시간'])
        common_df_complete = common_df
        common_df_complete.sort_values('작업생성시간', inplace=True)
        #print(common_df_complete[['작업생성시간','작업+대기시간']])


        common_df_complete = common_df_complete[['작업생성시간','작업+대기시간', '작업코드', '장비번호', '풀(F)공(M)', '수출/수입']]
        common_df_complete['입차시간'] = common_df_complete['작업생성시간']
        #print(common_df_complete['작업+대기시간'])
        grouped_df = common_df_complete.groupby(pd.Grouper(key='작업생성시간', freq='5min')).mean()
        #print('grouped_df',grouped_df['작업+대기시간'])
        grouped_df['입차시간'] = grouped_df['입차시간'].astype('int64') // 10**9
        return grouped_df


    # 데이터 전처리
    def make_model(grouped_df):
        nonlocal prediction_list
        nonlocal count
        nonlocal p_count
        lookback = 30
        X, y = [], []
        X_data = grouped_df[['입차시간','작업+대기시간', '작업코드', '풀(F)공(M)','수출/수입','장비번호']]
        y_data = grouped_df['작업+대기시간'].values
        print('y_data', y_data)
        for i in range(grouped_df.shape[0] - lookback):
            X.append(X_data[i:i+lookback])
            y.append(y_data[i+lookback])
        X = np.array(X)
        y = np.array(y)
##############
        # # 데이터 분할
        # scaler = MinMaxScaler()
        # X_reshaped = X.reshape(-1, X.shape[-1])
        # X_scaled = scaler.fit_transform(X_reshaped)
        # #X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
        # X_scaled_reshaped = X_scaled.reshape(X.shape)
        # X_train, X_test, y_train, y_test = train_test_split(X_scaled_reshaped, y, test_size=0.2, random_state=42)
#############

        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        previous_data = data[-30:]
        # LSTM 모델 구성
        model = keras.Sequential()
        model.add(keras.layers.LSTM(units=64, input_shape=(lookback, 6)))
        model.add(keras.layers.Dense(units=1))
        # 모델 컴파일
        model.compile(loss='mean_squared_error', optimizer='adam')
        # 모델 학습
        model.fit(X_train, y_train, epochs=30, batch_size=32)
        
        # 모델 예측
        y_pred = model.predict(X_test)
        print('y_pred',y_pred)
        # 결정계수 계산
        r2 = r2_score(y_test, y_pred)
        print('R-squared: ', r2)

        last_sequence = X_data[-lookback:]  # 최근 30개의 대기시간 데이터를 가져옵니다.
        predicted_data = []
        for _ in range(10):
            sequence = np.array(last_sequence)
            sequence = np.reshape(sequence, (1, lookback, 6))
            prediction = model.predict(sequence)[0][0]
            predicted_data.append(prediction)
            new_row = np.array([prediction]*6).reshape(1, -1)
            last_sequence = np.concatenate((last_sequence[1:], new_row), axis=0)
        
        print(predicted_data)



       # scaled된 값 복원
        X_test_inverse = scaler.inverse_transform(X_test)
        X_test_inverse_df = pd.DataFrame(X_test_inverse, columns=X.columns)
        print(X_test_inverse_df)



        #unix timestamp로 변환되어 있었던 작업생성시간 값 datetime으로 변환
        X_test_inverse_df['입차시간'] = pd.to_datetime(X_test_inverse_df['입차시간'], unit='s')
        print(X_test_inverse_df['입차시간'])
        X_test_inverse_df['실제값'] = y_test
        X_test_inverse_df['예측값'] = y_pred
        # 작업생성시간 별로 정렬
        X_test_inverse_df.sort_values('입차시간', inplace=True)
        X_test_inverse_df= X_test_inverse_df[['입차시간', '실제값', '예측값']]

        r2 = r2_score(y_test, y_pred)

        print('결정 계수 (R^2):', r2)
        # 모델 저장
        with open('pctc-da/Congest_project/models/lstm_model.pkl', 'wb') as f:
            pickle.dump(model, f)



        # # 그래프로 예측 결과와 실제 데이터를 표현합니다.
        # x_axis_previous = range(grouped_df.shape[0]-30, grouped_df.shape[0])  # 기존 데이터 중 마지막 30개의 인덱스
        # x_axis_predicted = range(grouped_df.shape[0], grouped_df.shape[0] + 1)  # 이후 1개의 예측 데이터
        # # 개수 오류 계속 났었음. ( x_axis_previous = previous_data 맞춰줘야 하고, x_axis_predicted = predicted_data 맞춰줘야 함)
        # plt.plot(x_axis_previous, previous_data, label='Previous Data')
        # plt.scatter(x_axis_predicted, predicted_data, label='Predicted Data', color='red')
        # plt.xlabel('Time')
        # plt.ylabel('Waiting Time')
        # plt.ylim(0, 100)  # y축 범위 설정
        # plt.legend()
        # graph_image_filename = "test_graph.png"
        # plt.savefig(graph_image_filename)
        # print(f"그래프를 '{graph_image_filename}' 파일로 저장했습니다.")
        # # plt.show()

        # # 예측값을 data에 추가
        # for predict_value in predicted_data:
        #     new_row = pd.DataFrame([[predict_value]*6], columns=X_data.columns)
        #     X_data = X_data.append(new_row, ignore_index=True)
        # print('count', count)
        
        # # 입력 횟수만큼 예측값 학습한 값 출력(새로운 값 추가하여 재학습)
        # if count < p_count:
        #     count+=1
        #     make_model(X_data)
        
        return predicted_data
    
    data = load()
    grouped_df = preprocessing(data)
    predicted_data = make_model(grouped_df)    


    return predicted_data

if __name__=='__main__':
    predict_c= 3
    predicted_data = operate(predict_c)
