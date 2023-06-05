import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import math
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def operate():
    def load():
        # new_data 들어오면 기존 df 에 합치면 됨
        data = pd.read_excel("data/TSB_data.xlsx", sheet_name='야드크레이인_작업이력')
        scd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='반출입_예정컨테이너')
        cbd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_전')
        cad_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_후')
        quay_work_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='본선크레인_작업이력')
        ycb_common_values = data['컨테이너번호'].isin(cad_data['컨테이너번호']).sum() # 5181개
        data_cad_data_common_df = pd.merge(data, cad_data, on='컨테이너번호')
        data_cbd_data_common_df = pd.merge(data, cbd_data, on='컨테이너번호')
        return data_cbd_data_common_df

    def preprocessing(common_df):
        # 데이터 전처리
        common_df['작업코드'] = common_df['작업코드'].replace({'VU': 1, 'VL': 2, 'GR': 3, 'GD': 4, 'TM':5,'TS':6})
        common_df['장비번호'] = common_df['장비번호'].replace({'Y02': 1})
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].replace({'M':1, 'F':2})
        common_df['수출/수입'] = common_df['수출/수입'].replace({'X':1,'I':2,'S':3,'M':4})
        common_df['야드트럭(번호)'] = common_df['야드트럭(번호)'].fillna(1)
        # 시간 타입 통합
        common_df['작업생성시간'] = pd.to_datetime(common_df['작업생성시간'], format='%Y%m%d%H%M%S')
        common_df['작업완료시간'] = pd.to_datetime(common_df['작업완료시간'], format='%Y%m%d%H%M%S')
        common_df['작업+대기시간'] = common_df['작업완료시간'] -common_df['작업생성시간']
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
        common_df = common_df.dropna(subset=['작업+대기시간'])
        ######################## x 축에 시간 넣기 위한 작업#######################
        # 작업생성시간을 Unix timestamp로 변환
        common_df['작업생성시간'] = common_df['작업생성시간'].astype('int64') // 10**9
        #########################################################################
        common_df['작업+대기시간'] = common_df['작업+대기시간'].dt.total_seconds() /60.0
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
        common_df = common_df.dropna(subset=['작업+대기시간'])
        common_df_complete = common_df
        return common_df_complete

    def make_model(common_df):
        # 데이터 준비
        X = common_df[['작업생성시간','작업코드','항차_x','야드트럭(번호)','컨테이너(사이즈 코드)','장비번호', '풀(F)공(M)', '수출/수입']]
        y = common_df['작업+대기시간']
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
        # 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y, test_size=0.2, random_state=42)

        X_train_reshaped = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
        X_test_reshaped = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))

        model = Sequential()
        model.add(Conv1D(64, 3, activation='relu', input_shape=(X_train.shape[1], 8)))
        model.add(MaxPooling1D(2))
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))
        model.add(Dense(1))
        # CNN 모델 구성 합성곱필터 64개, 각 필터의 길이는 3이며, 활성화 함수로 relu 사용
        # maxpooling1d 는 합성곱 레이어의 출력 이미지에서 주요값(최대값)만 뽑아내는 역할
        # 2 는 풀링 창의 크기를 2로 하는 maxpooling1d 레이어 생성
        # model = Sequential()
        # model.add(Conv1D(64, 3, activation='relu', input_shape=(X_train.shape[1], 8)))
        # model.add(MaxPooling1D(2))
        # model.add(Flatten())
        # model.add(Dense(64, activation='relu'))
        # model.add(Dense(1))
        # 모델 컴파일
        model.compile(loss='mean_squared_error', optimizer='adam')
        # 모델 훈련
        model.fit(X_train, y_train, epochs=10, batch_size=10, validation_data=(X_test, y_test))
        # 모델 예측
        predictions = model.predict(X_test)
        X_test_df = pd.DataFrame(X_test)
        X_test_with_predictions = X_test_df.copy()
        X_test_with_predictions['예측값'] = predictions
        # scaled된 값 복원
        X_test_inverse = scaler.inverse_transform(X_test)
        # 열 이름 원래대로
        X_test_inverse_df = pd.DataFrame(X_test_inverse, columns=X.columns)
        # print(X_test_inverse_df)
        #unix timestamp로 변환되어 있었던 작업생성시간 값 datetime으로 변환
        X_test_inverse_df['작업생성시간'] = pd.to_datetime(X_test_inverse_df['작업생성시간'], unit='s')
        # print(X_test_inverse_df['작업생성시간'])
        X_test_inverse_df['실제값'] = y_test
        X_test_inverse_df['예측값'] = predictions
        # 작업생성시간 별로 정렬
        X_test_inverse_df.sort_values('작업생성시간', inplace=True)
        X_test_inverse_df= X_test_inverse_df[['작업생성시간', '실제값', '예측값']]
        # 10분 단위 그룹화(작업생성시간 열은 인덱스가 됨)
        grouped_df = X_test_inverse_df.groupby(pd.Grouper(key='작업생성시간', freq='10min')).mean()
        grouped_df = grouped_df.fillna(grouped_df.ffill().add(grouped_df.bfill()).div(2))
        grouped_df = grouped_df.iloc[1:-1]
        time_group = grouped_df.index.tolist()
        predict_group = grouped_df['예측값'].tolist()
        actual_group = grouped_df['실제값'].tolist()
       #평가 지표 계산
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        #평가 지표 출력
        print('평균 절대 오차 (MAE):', mae)
        print('평균 제곱근 오차 (RMSE):', rmse)
        print('평균 제곱 오차 (MSE):', mse)
        print('결정 계수 (R^2):', r2)
        # 모델 저장
        with open('pctc-da/Congest_project/models/model.pkl', 'wb') as f:
            pickle.dump(model, f)

        return time_group, predict_group, actual_group

    data = load()
    common_data = preprocessing(data)
    time_group, predict_group, actual_group = make_model(common_data)
    return time_group, predict_group, actual_group

if __name__=='__main__':
    operate()