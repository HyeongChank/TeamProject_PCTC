import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras import backend as K
import tensorflow as tf
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def load():
    # data = pd.read_excel("D:/김형찬/ai-algorism/data/conjestDum.xlsx", sheet_name='csv')
    data = pd.read_excel("D:/김형찬/Congest_project/data/congestdum3.xlsx", sheet_name='csv')
    # data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
    # print(data)
    data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
    data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])
    data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
    data['누적 컨테이너'] = data['작업코드'].cumsum()
    print(data.shape)
    # print(data.shape)
    # print(data.columns)
    return data


def preprocessing(data):
    data['입차시간'] = data['작업 지시 시간'] + timedelta(minutes=10)
    data['출차시간'] = data['작업 완료 시간'] + timedelta(minutes=10)
    data['소요시간'] = data['출차시간'] - data['입차시간']    
    print(data[['입차시간', '출차시간']])
    n_data = data
    m_data = data
    n_data['수량'] = 1
    m_data['마수량'] = -1

    n_data['입차누적'] = n_data['수량'].cumsum()+2
    n_data['출차누적'] = n_data['마수량'].cumsum()

    # time = pd.to_datetime('2021-02-06 15:30:00')
    time = pd.to_datetime('2021-02-06 15:30:00')
    print(n_data[['입차시간','입차누적','누적 컨테이너']])
    # print(n_data['입차시간'].iloc[-1])

    values = []
    # 총 입차시간 중에 입력 time보다 작은 df 를 만들고 시간을 늘려가며 누적 트럭 대수를 더함
    while time <= pd.to_datetime(n_data['입차시간'].iloc[-1]):
        ntrans_data = n_data[n_data['입차시간'] < time]
        ntrans_data = ntrans_data.reset_index(drop=True)
 
        # 예외 상황에 대한 처리
        last_in_entry = ntrans_data.at[ntrans_data.index[-1], '입차누적']
 

        mtrans_data = m_data[m_data['출차시간'] < time]
        mtrans_data = mtrans_data.reset_index(drop=True)
 
        last_out_entry = mtrans_data.at[mtrans_data.index[-1], '출차누적']
 

        interval = last_in_entry+last_out_entry

        # 30분마다의 '입차누적 - 출차누적' 값을 리스트에 추가
        values.append(interval)

        time += pd.Timedelta(minutes=5)
        # print(time)
    # print(values)
    # 이상값 평균값으로 변화

    # 데이터프레임 값 중 300 이상인 값을 평균 값으로 대체
    threshold = 300
    mean_value = np.mean(values)
    cleaned_data = [mean_value if x >= threshold else x for x in values]


    # time_range = pd.date_range(start='2021-02-06 10:30:00', end=pd.to_datetime(n_data['입차시간'].iloc[-1]), freq='3T')
    time_range = pd.date_range(start='2021-02-06 15:30:00', periods=len(cleaned_data), freq='5T')
    df = pd.DataFrame({'Time': time_range, 'inner_truck': cleaned_data})
    # print(df)
    # Filter out the outliers based on the threshold
    # print(filtered_data)
    print(df)
    return df, time_range, values


def get_congestion(congest):
    if congest <= 31:
        return '원활'
    elif congest == 32:
        return '보통'
    elif congest >= 33:
        return '혼잡'
    else:
        return None

def make_df(df):

    # # 데이터프레임 생성
    # df['congest'] = df['inner_truck'].apply(get_congestion)
    # print(df)
    return df
    

def make_model(df, time_range, values):
    print('df',df)
    # 그래프 초기 설정
    plt.figure(figsize=(10, 6))

    # 마지막 10개 행의 데이터 추출
    last_10_data = df.tail(10)
    print(last_10_data.head)
    # 그래프로 데이터 그리기
    plt.plot(last_10_data['Time'], last_10_data['inner_truck'], 'o-', color='blue', label='inner_truck')

    # 그래프 출력 설정
    plt.xlabel('Time')
    plt.ylabel('inner_truck')
    plt.title('Last 10 Data')
    # plt.show()



    # 데이터프레임에서 시계열 데이터 추출
    time_series = pd.Series(df['inner_truck'].values, index=pd.to_datetime(df['Time']))
 
    # ARIMA 모델 학습
    model = ARIMA(time_series, order=(1, 0, 0))
    model_fit = model.fit()

    # 그래프 초기 설정
    plt.figure(figsize=(10, 6))
    # plt.plot(time_series.index, time_series.values, color='blue', label='forcast Data')
    print("yes")

    # 다음 시간 데이터 예측
    next_time = pd.to_datetime('2021-02-07 14:35:00')
    next_prediction = model_fit.forecast(steps=1)[0]

    next_times = []
    next_predictions = []
    # 예측 결과를 기존 데이터에 추가하여 다음 시간 데이터 예측 반복
    while next_time <= pd.to_datetime('2021-02-07 15:00:00'):
        print(f'{next_time}: {next_prediction}')
        next_times.append(next_time)
        next_predictions.append(next_prediction)
        # 예측 결과를 기존 데이터에 추가
        time_series[next_time] = next_prediction

        # ARIMA 모델 재학습
        model_fit = ARIMA(time_series, order=(1, 0, 0)).fit()

        # 다음 시간 데이터 예측
        next_time += pd.Timedelta(minutes=5)
        next_prediction = model_fit.forecast(steps=1)[0]
        # 예측 결과를 포함하여 그래프에 추가

    # 리스트들을 딕셔너리로 변환
    data = {'next_times': next_times, 'next_predictions': next_predictions}

    # 딕셔너리를 데이터프레임으로 변환

    plt.plot(data['next_times'], data['next_predictions'], label='Forecasted Data')


    # 그래프 출력 설정
    plt.xlabel('Time')
    plt.ylabel('inner_truck')
    plt.title('ARIMA Forecast')
    plt.legend()
    plt.show()
 

if __name__=="__main__":
    time = ['2021-02-06','2021-02-07']
    data = load()
    df, time_range, values = preprocessing(data)
    dfe = make_df(df)
    make_model(dfe, time_range, values)
