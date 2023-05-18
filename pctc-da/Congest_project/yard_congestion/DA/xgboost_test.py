import pandas as pd
import xgboost as xgb
import numpy as np
import datetime
from scipy.interpolate import interp1d
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


def commit_model(new_data):
    # data load
    def load():
        data = pd.read_csv("D:/김형찬/Congest_project/data/congestcsv.csv", encoding='cp949')
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
        print(n_data)
        # 대기시간을 숫자(분)로 변환하는 함수
        def convert_to_minutes(timedelta_obj):
            seconds = timedelta_obj.total_seconds()
            minutes = seconds // 60
            return minutes

        # 대기시간을 숫자(분)로 변환하여 새로운 열 추가
        n_data['대기시간new'] = n_data['대기시간'].apply(convert_to_minutes)
        n_data['대기시간old'] = n_data['대기시간'].apply(convert_to_minutes)
        congest_level = n_data[['혼잡도']].tail(1).values
        n_data = n_data.drop(['작업 지시 시간', '작업 완료 시간', '작업코드', '출차시간', '대기시간'], axis=1, inplace=False)
        print('new_n_data', n_data)


        n_data['입차시간'] = n_data['입차시간'].dt.round('10min')  # 10분 단위로 그룹화

        n_data = n_data.groupby('입차시간').mean().reset_index()  # 나머지 열의 평균값 계산

        print(n_data)
    
    # XGBoost 를 이용한 대기시간 예측 및 평가
    def make_model(n_data):
        X = n_data[['누적 컨테이너', '대기차량', '혼잡도','대기시간old']]  # 입력 특성에 '누적 컨테이너' 열 추가
        y = n_data['대기시간new']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = xgb.XGBRegressor()
        # flask 로 호출 시 fit 에서 The feature names should match those that were passed during fit.
		# Feature names unseen at fit time:
		# - 작업 완료 시간
		# - 작업 지시 시간
		# - 작업코드
		# Feature names seen at fit time, yet now missing:
		# - 혼잡도  오류가 남
        model.fit(X_train, y_train)
        # new_data = pd.DataFrame(new_data)
        new2 = pd.DataFrame({
            
            '누적 컨테이너': [n_data['누적 컨테이너'].iloc[-1]],
            '대기차량': [n_data['대기차량'].iloc[-1]],
            '혼잡도': [n_data['혼잡도'].iloc[-1]],
            '대기시간old': [n_data['대기시간old'].iloc[-1]]
        })
        new_pred = model.predict(new2)
        print("새로운 데이터 대기시간 예측:", new_pred)

        y_pred = model.predict(X_test)
        print("대기시간 예측:", y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        print('평균 제곱 오차(MSE):', mse)
        print('평균 제곱근 오차(RMSE):', rmse)
        x = np.arange(len(y_pred))

        # 예측값 보간
        f = interp1d(x, y_pred, kind='cubic')
        x_interp = np.linspace(0, len(y_pred)-1, 30)
        y_interp_pred = f(x_interp)
        # 실제값 보간
        f_actual = interp1d(x, y_test, kind='cubic')
        y_interp_actual = f_actual(x_interp)

        # 예측값과 실제값 그래프 그리기
        plt.plot(x_interp, y_interp_pred, label='Predicted')
        plt.plot(x_interp, y_interp_actual, label='Actual')
        plt.xlabel('Sample')
        plt.ylabel('Waiting Time')
        plt.title('Waiting Time Prediction')
        plt.legend()
        plt.grid(True)
        plt.show()
        return new_pred
            
    data = load()
    combined_data = add_data(data, new_data)
    n_data, congest_level = preprocessing(combined_data)
    # new_pred = make_model(n_data)
    # print(new_pred)
    # print(congest_level)
    # return new_pred, congest_level


# model_file = "D:/김형찬/Congest_project/model/xgboost_model.pkl"
# # commit_model 함수를 pickle로 저장
# with open(model_file, 'wb') as f:
#     pickle.dump(commit_model, f)

if __name__=="__main__":
    new_data = {'작업 지시 시간': ['2021-02-07 13:05:37'], '작업 완료 시간': ['2021-02-07 13:28:52'], '대기차량': [25], '작업코드':['적하']}
    commit_model(new_data)
    
