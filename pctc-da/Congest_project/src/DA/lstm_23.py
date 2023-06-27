import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from tensorflow import keras
from scipy.interpolate import interp1d
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras import backend as K
import pickle
from sklearn.model_selection import train_test_split
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# data load
def operate():
    count = 1
 
    prediction_list = []
    def load():
        # new_data 들어오면 기존 df 에 합치면 됨
        data = pd.read_excel("data/TSB_data.xlsx", sheet_name='야드크레이인_작업이력')
        # scd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='반출입_예정컨테이너')
        # cbd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_전')
        # cad_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_후')
        # # quay_work_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='본선크레인_작업이력')

        # # data, container_before_data, container_after_data merge
        # ycb_common_values = data['컨테이너번호'].isin(cad_data['컨테이너번호']).sum() # 6103개
        # yard_con_common_df = pd.merge(data, cad_data, on='컨테이너번호')
        # # yard_con_common_df = yard_con_common_df[:-300]

        return data

    def preprocessing(common_df):
        # 데이터 전처리
        common_df['작업코드'] = common_df['작업코드'].replace({'VU': 1, 'VL': 2, 'GR': 3, 'GD': 4, 'TM':5,'TS':6})
        common_df['장비번호'] = common_df['장비번호'].replace({'Y02': 1})
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].replace({'M':1, 'F':2})
        #common_df['수출/수입'] = common_df['수출/수입'].replace({'X':1,'I':2,'S':3,'M':4})
        
        # 외부트럭에 1 넣기
        common_df['야드트럭(번호)'] = common_df['야드트럭(번호)'].fillna(1)
    

        # 시간 타입 통합
        common_df['작업생성시간'] = pd.to_datetime(common_df['작업생성시간'], format='%Y%m%d%H%M%S')
        common_df['작업완료시간'] = pd.to_datetime(common_df['작업완료시간'], format='%Y%m%d%H%M%S')
        #print('작업생성시간',common_df['작업생성시간'].dtype)
        #print('작업완료시간',common_df['작업완료시간'].dtype)
        common_df['작업+대기시간'] = common_df['작업완료시간'] -common_df['작업생성시간']
        print(common_df['작업+대기시간'])
  

        # 작업+대기시간을 초로 변환
        common_df['작업+대기시간'] = common_df['작업+대기시간'].dt.total_seconds() /60.0

        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
        common_df = common_df.dropna(subset=['작업+대기시간'])
        common_df_complete = common_df
        common_df_complete.sort_values('작업생성시간', inplace=True)
        print(common_df_complete[['작업생성시간','작업+대기시간']])
        time_list = common_df_complete['작업생성시간'][:-30]
        print('len(time_list)', len(time_list))
        print(common_df_complete.shape)
     

        common_df_complete = common_df_complete[['작업+대기시간','작업코드', '장비번호', '풀(F)공(M)','컨테이너(사이즈 코드)']]
        #common_df_complete['입차시간'] = common_df_complete['작업생성시간']
        
        print(common_df_complete.isna().sum())
        print(common_df_complete.dtypes)
        # grouped_df = common_df_complete.groupby(pd.Grouper(key='작업생성시간', freq='10min')).mean()

        

        # # 인덱스를 다시 열로 변경
        # grouped_df.reset_index(inplace=True)

        # # 작업생성시간 열을 입차시간 열로 복사
        # grouped_df['입차시간'] = grouped_df['작업생성시간']

        # # 작업생성시간 열을 다시 인덱스로 설정
        # grouped_df.set_index('작업생성시간', inplace=True)

        # print(grouped_df.dtypes)

        # print(grouped_df.isna().sum())
        return common_df_complete, time_list


    # 데이터 전처리
    def make_model(grouped_df, time_list):
        lookback = 50
        # grouped_df = grouped_df[0:300]
        # 데이터 전처리
        X_data = grouped_df[['작업코드', '풀(F)공(M)','장비번호', '컨테이너(사이즈 코드)']]
        y_data = grouped_df['작업+대기시간'].values

        X, y = [], []
        for i in range(grouped_df.shape[0] - lookback):
            X.append(X_data[i:i+lookback].values)
            y.append(y_data[i+lookback])
        X = np.array(X)
        y = np.array(y)
 
        # 시계열이라 데이터를 랜덤하게 분할하지 않고 시간대에 따라 분할
        train_size = int(len(X) * 0.8)

        # 시간 순서를 유지하면서 데이터 분할
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        print('y_train', y_train)
        print('y_test', y_test)
        
        print(X_train.shape)
        # 데이터 정규화
        scaler = MinMaxScaler()
        X_train_scaled = np.zeros_like(X_train)
        X_test_scaled = np.zeros_like(X_test)

        for i in range(X_train.shape[2]):
            X_train_scaled[:, :, i] = scaler.fit_transform(X_train[:, :, i])
            X_test_scaled[:, :, i] = scaler.transform(X_test[:, :, i])

        # y_train, y_test 스케일링
        scaler_y = MinMaxScaler()
        y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1))
        y_test_scaled = scaler_y.transform(y_test.reshape(-1, 1))
        print('y_train_scaled', y_train_scaled)
        num_nans = np.isnan(y_train_scaled).sum()
        print(num_nans)
        # LSTM 모델 구성
        model = keras.Sequential()
        model.add(keras.layers.LSTM(units=64, input_shape=(lookback, X_train.shape[-1])))
        model.add(keras.layers.Dense(units=64, activation='relu'))
        model.add(keras.layers.Dense(units=32, activation='relu'))
        model.add(keras.layers.Dense(units=1))

        # 모델 컴파일
        model.compile(loss='mean_squared_error', optimizer='adam')
        # 모델 학습
        model.fit(X_train_scaled, y_train_scaled, epochs=100, batch_size=32)
        # 모델 예측
        y_train_pred_scaled = model.predict(X_train_scaled)
        y_test_pred_scaled = model.predict(X_test_scaled)
        # 예측값을 원래의 스케일로 되돌리기
        y_train_pred = scaler_y.inverse_transform(y_train_pred_scaled)
        y_test_pred = scaler_y.inverse_transform(y_test_pred_scaled)
        # 원래의 스케일로 되돌린 실제값
        y_train_real = scaler_y.inverse_transform(y_train_scaled)
        y_test_real = scaler_y.inverse_transform(y_test_scaled)

        # # '입차시간' 데이터 추출
        # X_train_time = X_train[:, -1:, time_index].reshape(-1)
        # X_test_time = X_test[:, -1:, time_index].reshape(-1)
        # # '입차시간' 데이터 원래대로 되돌리기
        # X_train_time_original = pd.to_datetime(X_train_time * 10**9)
        # X_test_time_original = pd.to_datetime(X_test_time * 10**9)
        # combined_time = np.concatenate((X_test_time_original, X_train_time_original), axis=0)
        # print(combined_time)
        # print(len(combined_time))
        print(len(time_list))
        combined_pred = np.concatenate((y_test_pred, y_train_pred), axis=0)
        print(len(combined_pred))
        combined_real = np.concatenate((y_test_real, y_train_real), axis=0)
        # print(combined_real)
        print(len(combined_real))
        # datetime 형식을 리스트로 바꾸면 유닉스타임 스탬프로 변경돼서 다른 방법 써야 함
        
        # datetime_list = pd.to_datetime(combined_time.tolist(), unit='ns')
        actual_values = np.ravel(combined_real).tolist()
        predict_values = np.ravel(combined_pred).tolist()
        listlen = len(actual_values)
        # print('time', datetime_list)


        time_list = time_list[:listlen]



        # print('actual_values',actual_values)
        print(len(actual_values))
        # print('predict_values',predict_values)
        df = pd.DataFrame({
            'Time': time_list,
            'Prediction':predict_values,
            'Actual': actual_values
        })
        print(df.dtypes)
        print('df', df)
        df = df.groupby(pd.Grouper(key='Time', freq='10min')).mean()
        # 인덱스를 다시 열로 변경
        df.reset_index(inplace=True)
        df['Time'] = df['Time'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        print('df', df)

        time_group = df['Time'].tolist()
        predict_time = df['Prediction'].tolist()
        actual_time = df['Actual'].tolist()


        # Mean Absolute Error (MAE)
        mae_train = mean_absolute_error(y_train_real, y_train_pred)
        mae_test = mean_absolute_error(y_test_real, y_test_pred)

        print(f'Train MAE: {mae_train}, Test MAE: {mae_test}')

        # Mean Squared Error (MSE)
        mse_train = mean_squared_error(y_train_real, y_train_pred)
        mse_test = mean_squared_error(y_test_real, y_test_pred)

        print(f'Train MSE: {mse_train}, Test MSE: {mse_test}')

        # Root Mean Squared Error (RMSE)
        rmse_train = np.sqrt(mse_train)
        rmse_test = np.sqrt(mse_test)

        print(f'Train RMSE: {rmse_train}, Test RMSE: {rmse_test}')

        # R^2 Score
        r2_train = r2_score(y_train_real, y_train_pred)
        r2_test = r2_score(y_test_real, y_test_pred)

        print(f'Train R^2: {r2_train}, Test R^2: {r2_test}')

        # 그래프의 크기 설정
        plt.figure(figsize=(14, 7))
        plt.scatter(time_list, actual_values, color='blue', label='Actual values')
        plt.scatter(time_list, predict_values, color='red', label='Predicted values')
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.title('Scatter plot of actual and predicted values over time')
        plt.legend()
        graph_image_filename = "lstm_graph_notime_days2.png"
        plt.savefig(graph_image_filename)
        print(f"그래프를 '{graph_image_filename}' 파일로 저장했습니다.")
        # plt.show()
  
        # 모델 저장
        with open('pctc-da/Congest_project/models/lstm_model_notime_days222.pkl', 'wb') as f:
            pickle.dump(model, f)
        return time_group, predict_time, actual_time
        
       
    
    data = load()
    grouped_df, time_list = preprocessing(data)
    time, predict_values, actual_values = make_model(grouped_df, time_list)    


    return time, predict_values, actual_values

if __name__=='__main__':

    time, predict_values, actual_values = operate()
