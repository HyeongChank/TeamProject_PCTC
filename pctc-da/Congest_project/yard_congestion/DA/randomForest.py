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


def commit_model(new_data):
    def load():
        # data = pd.read_excel("D:/김형찬/Congest_project/data/congestDumfh.xlsx", sheet_name='csv')
        data = pd.read_csv("D:/김형찬/Congest_project/data/congestcsv.csv", encoding='cp949')
        print(data.head())
        data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
        data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])
        data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
        data['누적 컨테이너'] = data['작업코드'].cumsum()

        print(data['누적 컨테이너'])
        # print(data.shape)
        # print(data.columns)
        return data


    def preprocessing(data):
        # data = data
        df = pd.DataFrame(data)
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
        print(n_data[['입차시간','출차시간', '대기시간new','대기차량', '혼잡도']])
        return n_data
    
    def make_model(n_data, new_data):
        # 특성(features)과 대상(target) 분리
        X = n_data[['대기차량', '혼잡도']]  # 입력 특성
        y = n_data['대기시간new']  # 예측할 대상
        # 데이터셋을 학습용과 테스트용으로 분할
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 랜덤 포레스트 모델 생성
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        # 모델 학습
        rf.fit(X_train, y_train)

        # 새로운 데이터
        new_data = pd.DataFrame(new_data)
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
        
    data = load()
    data = preprocessing(data)
    make_model(data, new_data)


if __name__=="__main__":
    new_data = {'대기차량': [25], '혼잡도':[2]}
    commit_model(new_data)
    
