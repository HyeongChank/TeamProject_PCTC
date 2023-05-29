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

def operate():
    def load():
        # new_data 들어오면 기존 df 에 합치면 됨
        data = pd.read_excel("data/TSB_data.xlsx", sheet_name='야드크레이인_작업이력')
        scd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='반출입_예정컨테이너')
        cbd_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_전')
        cad_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='장치장_후')
        quay_work_data = pd.read_excel("data/TSB_data.xlsx", sheet_name='본선크레인_작업이력')
        # data, container_before_data, container_after_data merge
        ycb_common_values = data['컨테이너번호'].isin(cad_data['컨테이너번호']).sum() # 5181개
        print('ycb_common_values', ycb_common_values)
        data_cad_data_common_df = pd.merge(data, cad_data, on='컨테이너번호')
        data_cbd_data_common_df = pd.merge(data, cbd_data, on='컨테이너번호')
        print(data_cbd_data_common_df)

        return data_cbd_data_common_df

    def preprocessing(common_df):
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
        print(common_df['작업생성시간'])
        print('작업완료시간',common_df['작업완료시간'].dtype)
        common_df['작업+대기시간'] = common_df['작업완료시간'] -common_df['작업생성시간']
        print(common_df['작업+대기시간'].isna().sum())
        print('common_df',common_df.info())
        # common_df = common_df[-300:]
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
        common_df = common_df.dropna(subset=['작업+대기시간'])

        ######################## x 축에 시간 넣기 위한 작업#######################
        # 작업생성시간을 Unix timestamp로 변환
        common_df['작업생성시간'] = common_df['작업생성시간'].astype('int64') // 10**9
        #########################################################################
        common_df['작업+대기시간'] = common_df['작업+대기시간'].dt.total_seconds() /60.0
        
        common_df['풀(F)공(M)'] = common_df['풀(F)공(M)'].astype('int64')
        print('common_df',common_df.info())
        common_df = common_df.dropna(subset=['작업+대기시간'])
        common_df_complete = common_df
        return common_df_complete

    def make_model(common_df):
        # 특성과 목표 변수 설정
        X = common_df[['작업생성시간','작업코드','항차_x','야드트럭(번호)','컨테이너(사이즈 코드)','장비번호', '풀(F)공(M)', '수출/수입']]
        y = common_df['작업+대기시간']
        # 데이터를 훈련 세트와 테스트 세트로 분리
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 랜덤 포레스트 모델 객체 생성 100개 예측
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        # 모델 훈련
        model.fit(X_train, y_train)

        # 모델 예측
        predictions = model.predict(X_test)


    ###########################################################################
        # x 축에 시간 넣기 위한 작업
        # 예측값을 X_test에 추가
        X_test_with_predictions = X_test.copy()
        X_test_with_predictions['예측값'] = predictions

        X_test_with_predictions['작업생성시간'] = pd.to_datetime(X_test_with_predictions['작업생성시간'], unit='s')
        
        # 작업생성시간 별로 정렬
        X_test_with_predictions.sort_values('작업생성시간', inplace=True)
        X_test_with_predictions= X_test_with_predictions[['작업생성시간', '예측값']]
        # 결과 출력
        print(X_test_with_predictions)
        # Unix timestamp를 datetime으로 변환
        grouped_df = X_test_with_predictions.groupby(pd.Grouper(key='작업생성시간', freq='10min')).max()
        print(grouped_df)

        plt.figure(figsize=(10, 5))
        plt.plot(X_test_with_predictions['작업생성시간'], X_test_with_predictions['예측값'])
        plt.xlabel('작업생성시간')
        plt.ylabel('예측값')
        plt.title('예측값 시간별 추이')
        # plt.show()
        return grouped_df

#############################################################################

    ## 상관관계 히트맵 그리기
    # correlation_matrix = common_df[['작업코드','항차_x','야드트럭(번호)','컨테이너(사이즈 코드)','장비번호', '작업생성시간','작업완료시간', '풀(F)공(M)', '수출/수입','작업+대기시간']].corr()

    # sns.heatmap(correlation_matrix, annot=True)
    # plt.show()
    common_df = load()
    common_df_complete = preprocessing(common_df)
    grouped_df = make_model(common_df_complete)
    print(grouped_df.index.dtype)
    # 인덱스를 컬럼으로 변환
    grouped_df.reset_index(inplace=True)
    print(grouped_df)

    predict_dic = {}
    entry_time = grouped_df['작업생성시간'].tolist()
    print(entry_time)
    # grouped_df['작업생성시간'] = pd.to_datetime(grouped_df['작업생성시간'], unit='ms')
    # grouped_df_json = grouped_df.to_json(orient='records')
    return grouped_df

if __name__=='__main__':
    operate()