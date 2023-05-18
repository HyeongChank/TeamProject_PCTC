import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
def test2(time):
    result_model_at_block = []
    block_list = []
    def load_data():
        # data = pd.read_excel("D:/김형찬/ai-algorism/data/conjestDum.xlsx", sheet_name='csv')
        data = pd.read_excel("D:/김형찬/Congest_project/data/congestDumfh.xlsx", sheet_name='csv')
        data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
        # print(data)
        data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
        data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])
        print(data.head())
        return data

    def preprocessing(time):
        # [블록명, bay, row]
        blocks = [['Q111', 8, 10], ['Q112', 9, 10]]
        time_pre = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        # 분과 초를 0으로 설정
        time_pre = time_pre.replace(minute=0, second=0, microsecond=0)
        # 시간 단위로 변환된 값을 출력
        time = time_pre.strftime('%Y-%m-%d %H:%M:%S')
        return blocks, time
    
    def get_accumulated_container_count(data, blocks, time):
    
        result_dict={}
        for block in blocks:
            # 블록(Block), 작업 시간 별 누적 컨테이너 개수 계산
            container_counts = data.groupby(['블록(Block)', pd.Grouper(key='작업 지시 시간', freq='30min')])['작업코드'].apply(lambda x: x.apply(lambda y: 1 if y == 1 else -1 if y == -1 else -1).cumsum())
            container_counts = container_counts.reset_index(level=[0, 1])
            container_counts['누적 컨테이너 개수'] = container_counts.groupby(['블록(Block)', pd.Grouper(key='작업 지시 시간', freq='30min')])['작업코드'].cumsum()

            # 블록(Block), 작업 시간 별 누적 컨테이너 개수 최종값 계산
            final_container_counts = container_counts.groupby(['블록(Block)', pd.Grouper(key='작업 지시 시간', freq='30min')])['누적 컨테이너 개수'].last().reset_index()
            final_container_counts = final_container_counts.rename(columns={'작업 지시 시간': '작업 시간'})
            container_count_at_block = final_container_counts[final_container_counts['블록(Block)'] == block[0]].reset_index(drop=True)

            # # 입력받은 time 이후의 데이터만 선택하여 새로운 데이터프레임 생성
            # container_count_at_block = container_count_at_block[container_count_at_block['작업 시간'] >= time]
            # container_count_at_block = container_count_at_block.reset_index(drop=True)

             # 블록별 capacity
            bay = block[1]
            row = block[2]
            capacity = bay*row
            # print(capacity)

            # 혼잡도 구분
            container_count_at_block['cong'] = 0
            container_count_at_block.loc[container_count_at_block['누적 컨테이너 개수']/capacity < 2, 'cong'] = 0
            container_count_at_block.loc[(container_count_at_block['누적 컨테이너 개수']/capacity >= 2) & (container_count_at_block['누적 컨테이너 개수']/capacity < 4), 'cong'] = 1
            container_count_at_block.loc[container_count_at_block['누적 컨테이너 개수']/capacity >= 4, 'cong'] = 2

            # 혼잡도 df에 넣고 모델 실행
            result_dict[block[0]] = container_count_at_block['cong'].values[0]
            print('container_count_at_block',container_count_at_block)
            result = make_LinearRegression_model(container_count_at_block)
            result_model_at_block.append(result)
            block_list.append(block[0])
        print(result_model_at_block)
        print(block_list)        
        return result_model_at_block, block_list
        
    def make_LinearRegression_model(container_count_at_block):
        df = container_count_at_block
        # 2->1로 혼잡도 변하는 것 구하기 위해 0은 일단 제외
        mask = df['cong'] !=0
        df = df[mask]
        df = df[mask].reset_index(drop=True)

        # 혼잡도 변하는데 소요되는 시간 별도 리스트 저장(모델 돌리기 위해서)
        # for 문 2번 돌지 않는 코드로 수정하기!!!~~~~~~
        cong_diffs = []
        for idx, row in df.iterrows():
            if row['cong'] == 2:
                cong2_time = row['작업 시간']
                cong2_index = idx
                
                for cong2_index, row in df.loc[idx:].iterrows():
                    if row['cong'] ==1:
                        cong1_time = row['작업 시간']
                        print(cong1_time, cong2_time)
                        cong_diff = (cong1_time - cong2_time).total_seconds() // 60
                        cong_diffs.append(cong_diff)
                        print('cong1', cong2_index)
                        print(cong_diffs)
                        break
                    else:
                        pass

        data = cong_diffs
        # 독립변수와 종속변수로 데이터 분리
        X = np.arange(len(data)).reshape(-1, 1)
        # print(X)
        y = np.array(data)

        # 훈련셋과 테스트셋 분리
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 선형회귀 모델 훈련
        reg = LinearRegression()
        reg.fit(X_train, y_train)
        # 테스트셋을 이용하여 모델 예측
        y_pred = reg.predict(X_test)
        # 모델 평가
        score = reg.score(X_test, y_test)
        print(f'R-squared: {score:.4f}')

        # 다음 cong2에서 cong1로 변하는 시간 예측
        next_cong2 = np.array([[len(data)]])
        next_cong1 = reg.predict(next_cong2)
        print(f'Next cong2-cong1 time: {next_cong1[0]:.1f}')
        print('next_cong1[0]', round(next_cong1[0]))
        return round(next_cong1[0])

    data = load_data()
    blocks, time = preprocessing(time)
    result_model_at_block = get_accumulated_container_count(data, blocks, time)
    return result_model_at_block

if __name__ == '__main__':
    time = '2021-02-08 13:30:00'
    test2(time)

