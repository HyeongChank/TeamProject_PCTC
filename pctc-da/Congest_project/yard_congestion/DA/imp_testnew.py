import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def commit_model():
    def load():
        data = pd.read_excel("D:/김형찬/Congest_project/data/congestDumfh.xlsx", sheet_name='csv')
        data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
        data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])
        data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
        data['누적 컨테이너'] = data['작업코드'].cumsum()
        print(data)
        # print(data.shape)
        # print(data.columns)
        return data


    def preprocessing(data):
        data_nasd = data
        data = {
          
            '작업 지시 시간': ['2021-02-06 14:28:45', '2021-02-06 14:34:04', '2021-02-06 14:44:12',
                            '2021-02-06 14:49:20', '2021-02-06 14:57:45', '2021-02-06 15:48:52',
                            '2021-02-06 16:28:45', '2021-02-06 16:38:04', '2021-02-06 16:44:12',
                            '2021-02-06 16:49:20', '2021-02-06 16:57:45', '2021-02-06 17:48:52'],
            '작업 완료 시간': ['2021-02-06 14:33:45', '2021-02-06 14:38:45', '2021-02-06 14:55:45',
                          '2021-02-06 14:53:45', '2021-02-06 15:02:45', '2021-02-06 16:33:45',
                            '2021-02-06 17:34:45', '2021-02-06 17:35:45', '2021-02-06 17:55:45',
                          '2021-02-06 16:59:20', '2021-02-06 16:59:45', '2021-02-06 18:48:52']

        }
        df = pd.DataFrame(data)
        df['작업 지시 시간'] = pd.to_datetime(df['작업 지시 시간'])
        df['작업 완료 시간'] = pd.to_datetime(df['작업 완료 시간'])

        df['입차시간'] = df['작업 지시 시간']
        df['출차시간'] = df['작업 완료 시간']
        df['대기시간'] = df['출차시간'] - df['입차시간']

    
        print(df[['입차시간','출차시간', '대기시간']])
        n_data = df
 
 
       # 초기화
        n_data = df.copy()
        n_data['대기차량'] = 20
        flag = 3
        # 대기차량 수 계산
        for i in range(5, len(n_data)):
            n_data.loc[i, '대기차량'] = n_data.loc[i, '대기차량'] + 1
            print(n_data.loc[i, '대기차량'])
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


        print(n_data[['입차시간','출차시간', '대기시간new','대기차량', '혼잡도']])


            # 특성(features)과 대상(target) 분리
        X = n_data[['대기차량','대기시간new', '혼잡도']]  # 입력 특성
        y = n_data['대기시간new']  # 예측할 대상

        # 데이터셋을 학습용과 테스트용으로 분할
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 랜덤 포레스트 모델 생성
        rf = RandomForestRegressor(n_estimators=100, random_state=42)

        # 모델 학습
        rf.fit(X_train, y_train)

        # 새로운 데이터
        new_data = pd.DataFrame({'대기차량': [25], '대기시간new': [10], '혼잡도':[2]})
        # 대기시간 예측
        new_pred = rf.predict(new_data)
        print("새로운 데이터 대기시간 예측:", new_pred)
        # 테스트 데이터로 예측
        y_pred = rf.predict(X_test)

        # 예측 결과 평가
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse**0.5
        print(new_pred)
        print('평균 제곱 오차(MSE):', mse)
        print('평균 제곱근 오차(RMSE):', rmse)










        # values = []
        # # 총 입차시간 중에 입력 time보다 작은 df 를 만들고 시간을 늘려가며 누적 트럭 대수를 더함
        # while time <= pd.to_datetime(n_data['입차시간'].iloc[-1]):
        #     ntrans_data = n_data[n_data['입차시간'] < time]
        #     ntrans_data = ntrans_data.reset_index(drop=True)
        #     # 예외 상황에 대한 처리
        #     last_in_entry = ntrans_data.at[ntrans_data.index[-1], '입차누적']
        #     # print(last_in_entry)
        #     mtrans_data = m_data[m_data['출차시간'] < time]
        #     mtrans_data = mtrans_data.reset_index(drop=True)
        #     last_out_entry = mtrans_data.at[mtrans_data.index[-1], '출차누적']
        #     # print(last_out_entry)
        #     interval = last_in_entry+last_out_entry
        #     # 30분마다의 '입차누적 - 출차누적' 값을 리스트에 추가
        #     values.append(interval)
        #     time += pd.Timedelta(minutes=10)
        #     # print(time)
        # # 데이터프레임 값 중 300 이상인 값을 평균 값으로 대체
        # print(len(values))
        # print(values)
        # threshold = 300
        # mean_value = np.mean(values)
        # cleaned_data = [mean_value if x >= threshold else x for x in values]

        # time_range = pd.date_range(start='2021-02-07 12:30:00', periods=len(cleaned_data), freq='10T')
        # df = pd.DataFrame({'Time': time_range, 'inner_truck': cleaned_data})
        # print(df)
    #     # Filter out the outliers based on the threshold
    #     # print(filtered_data)
    #     return df, time_range, values


    # def get_congestion(congest):
    #     if congest <= 31:
    #         return 1
    #     elif congest == 32:
    #         return 2
    #     elif congest >= 33:
    #         return 3
    #     else:
    #         return None

    # def make_df(df):

    #     # 데이터프레임 생성
    #     df['congest'] = df['inner_truck'].apply(get_congestion)

    #     print(df)
    #     return df
        

    # def make_model(df, time_range, values):
    #     pass
    #     print(df)
    #     # 데이터 전처리
    #     scaler = MinMaxScaler()
    #     scaled_data = scaler.fit_transform(df[['inner_truck']].values)
    #     print(scaled_data)
    #     # LSTM 입력 데이터 준비
    #     X = []
    #     y = []
    #     lookback = 20  # 이전 50개의 inner_truck 값을 사용하여 현재 inner_truck 값을 예측

    #     for i in range(len(scaled_data) - lookback):
    #         X.append(scaled_data[i:i+lookback])
    #         y.append(scaled_data[i+lookback])

    #     X = np.array(X)
    #     y = np.array(y)
    #     print(X)
    #     print(y)
    #     # 데이터 분할
    #     X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    #     # LSTM 모델 구축
    #     model = Sequential()
    #     model.add(LSTM(50, activation='relu', input_shape=(lookback, 1)))
    #     model.add(Dense(1))
    #     model.compile(optimizer='adam', loss='mean_squared_error')

    #     # LSTM 모델 학습
    #     model.fit(X_train, y_train, epochs=10, batch_size=1, validation_data=(X_val, y_val))
    #     predicted_values = []
    #     input_data = scaled_data[-lookback:]  # 마지막 개의 혼잡도 값을 입력으로 사용

    #     for _ in range(144):  # 1일은 144개의 10분 간격으로 구성됨
    #         # 현재 입력 데이터
    #         input_data = scaled_data[-lookback:]
    #         input_data_reshaped = input_data.reshape(1, lookback, 1)
    #         # 현재 입력 데이터로 예측
    #         predicted_value = model.predict(input_data_reshaped)
    #         # 예측값을 원래 스케일로 변환
    #         predicted_value_scaled = scaler.inverse_transform(predicted_value)
    #         # 예측값을 리스트에 추가
    #         predicted_values.append(predicted_value_scaled[0][0])
    #         # 다음 시간의 입력 데이터 업데이트
    #         input_data = np.append(input_data[1:], predicted_value_scaled)
    #         scaled_data = np.append(scaled_data, predicted_value, axis=0)

    #     # 시간대 생성
    #     start_time = df['Time'].iloc[-1] + pd.DateOffset(minutes=5)  # 데이터프레임의 마지막 시간 다음 시간부터 시작
    #     time_range = pd.date_range(start=start_time, periods=144, freq='5T')

    #     # 예측된 혼잡도 값을 데이터프레임으로 변환
    #     predicted_df = pd.DataFrame({'Time': time_range, 'Predicted_congest': predicted_values})
    #     print(predicted_df)

    #     # 원래 데이터와 예측 데이터 결합
    #     combined_df = pd.concat([df, predicted_df], axis=0)
    #     print(combined_df)

    #     # 그래프 그리기
    #     plt.plot(combined_df['Time'], combined_df['inner_truck'], label='Actual')
    #     plt.plot(combined_df['Time'], combined_df['Predicted_congest'], label='Predicted')
    #     plt.xlabel('Time')
    #     plt.ylabel('inner_truck')
    #     plt.title('Actual vs. Predicted inner_truck')
    #     plt.legend()
    #     plt.show()
    data = load()
    preprocessing(data)
    # dfe = make_df(df)
    # make_model(dfe, time_range, values)

if __name__=="__main__":
    input_new_time = '2021-02-07'
    commit_model()
    
