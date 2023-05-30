from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
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
    print('ycb_common_values', ycb_common_values)
    yard_con_common_df = pd.merge(data, cad_data, on='컨테이너번호')
    print(yard_con_common_df)

    return yard_con_common_df

def make_df(common_df):
    # 데이터 전처리
    common_df['작업코드'] = common_df['작업코드'].replace({'VU': 1, 'VL': 2, 'GR': 3, 'GD': 4, 'TM':5,'TS':6})
    common_df['장비번호'] = common_df['장비번호'].replace({'Y02': 1})
    common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].replace({'M':1, 'F':2})
    common_df['수출/수입'] = common_df['수출/수입'].replace({'X':1,'I':2,'S':3,'M':4})
    
    # 외부트럭에 1 넣기
    common_df['야드트럭(번호)'] = common_df['야드트럭(번호)'].fillna(1)
    print('common_df',common_df)
 
    # 시간 타입 통합
    common_df['작업생성시간'] = pd.to_datetime(common_df['작업생성시간'], format='%Y%m%d%H%M%S')
    common_df['작업완료시간'] = pd.to_datetime(common_df['작업완료시간'], format='%Y%m%d%H%M%S')
    print('작업생성시간',common_df['작업생성시간'].dtype)
    print('작업완료시간',common_df['작업완료시간'].dtype)
    common_df['작업+대기시간'] = common_df['작업완료시간'] -common_df['작업생성시간']
    print(common_df['작업+대기시간'].isna().sum())
    print('common_df',common_df.info())
    common_df = common_df[-500:]


    # 작업+대기시간을 초로 변환
    common_df['작업+대기시간'] = common_df['작업+대기시간'].dt.total_seconds() /60.0
    
    common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
    print('common_df',common_df.info())
    common_df = common_df.dropna(subset=['작업+대기시간'])

    # 특성과 목표 변수 설정
    X = common_df[['작업코드','항차_x','야드트럭(번호)','컨테이너(사이즈 코드)','장비번호', '풀(F)공(M)', '수출/수입']]
    y = common_df['작업+대기시간']
    # 데이터를 훈련 세트와 테스트 세트로 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # 랜덤 포레스트 모델 객체 생성 100개 예측
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    # 모델 훈련
    model.fit(X_train, y_train)



    # 모델 예측
    predictions = model.predict(X_test)
    print(predictions)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    plt.figure(figsize=(10, 5))
    ## 선그래프로 바꾸려면 range(len()) 을 지우고, scatter을 plot 으로 바꾸면 됨
    plt.scatter(range(len(y_test.values)), y_test.values, label='Actual')
    plt.scatter(range(len(predictions)), predictions, label='Predicted')
    plt.ylabel('작업완료-입차시간(min)')
    plt.title('Time Prediction(RandomForest)')
    plt.legend()
    # plt.show()

    # model_file = "D:/김형찬/Congest_project/model/randomForest_model.pkl"
    # # commit_model 함수를 pickle로 저장
    # with open(model_file, 'wb') as f:
    #     pickle.dump(commit_model, f)


    # 상관관계 히트맵 그리기
    correlation_matrix = common_df[['작업코드','항차_x','야드트럭(번호)','컨테이너(사이즈 코드)','장비번호', '작업생성시간','작업완료시간', '풀(F)공(M)', '수출/수입','작업+대기시간']].corr()

    sns.heatmap(correlation_matrix, annot=True)
    plt.show()
    

if __name__=='__main__':
    common_df = load()
    make_df(common_df)