import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
import numpy as np

def test2(time):
    def load_data():
        data = pd.read_csv("D:/김형찬/team_project/TeamProject_PCTC/pctc-da/Congest_project/data/congestcsv.csv", encoding='cp949')
        print(data.head())

        data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
        print(data)
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
            container_count_at_time = container_count_at_block[container_count_at_block['작업 시간'] == time].reset_index(drop=True)
 
            bay = block[1]
            row = block[2]
            capacity = bay*row
  
            container_count_at_block['cong'] = 0
            container_count_at_block.loc[container_count_at_block['누적 컨테이너 개수']/capacity < 2, 'cong'] = 0
            container_count_at_block.loc[(container_count_at_block['누적 컨테이너 개수']/capacity >= 2) & (container_count_at_block['누적 컨테이너 개수']/capacity < 4), 'cong'] = 1
            container_count_at_block.loc[container_count_at_block['누적 컨테이너 개수']/capacity >= 4, 'cong'] = 2
            # 블록별 혼잡수준 딕셔너리에 넣기
            # result_dict[block[0]] = cong
            result_dict[block[0]] = container_count_at_block['cong'].values[0]
            # print('container_count_at_block',container_count_at_block)



            container_count_at_block = container_count_at_block[['블록(Block)','작업 시간', 'cong']]
            print(container_count_at_block)
            cong_df = container_count_at_block[container_count_at_block['cong']==2].copy() # 원본 데이터프레임을 유지하기 위해 .copy() 메서드 사용

            # 행 인덱스 재설정
            cong_df.reset_index(drop=True, inplace=True)

            # 작업 시간을 datetime 형식으로 변환
            cong_df['작업 시간'] = pd.to_datetime(cong_df['작업 시간'])

            # 시간 값과 인덱스 값(시간 순서)으로 새로운 데이터프레임 생성
            X = pd.DataFrame({'timestamp': cong_df.index, 'index': cong_df.index})
            print(X)
            # 종속 변수로 작업 시간 사용
            y = cong_df['작업 시간'].astype(np.int64) // 10 ** 9

            # 선형 회귀 모델 학습
            lr = LinearRegression()
            lr.fit(X, y)
            # cong 값이 0인 행들 추출
            zero_df = container_count_at_block[container_count_at_block['cong'] == 0].copy()
            if len(zero_df) > 0:
                # cong 값이 2에서 0으로 전환되는 시간 예측
                pred_timestamp = np.floor(-lr.intercept_ / lr.coef_[0])
                pred_time = pd.Timestamp(pred_timestamp, unit='s')

                # 가장 먼저 'cong' 값이 0이 되는 행의 시간 값 찾기
                zero_time = zero_df.loc[0, '작업 시간']
                for i in range(len(zero_df)):
                    if zero_df.loc[i, '작업 시간'] >= pred_time:
                        zero_time = zero_df.loc[i, '작업 시간']
                        break

                # 예측 결과 출력
                pred_time_in_minutes = (zero_time - pred_time).seconds // 60
                print('cong가 2에서 0이 되는 시간:', pred_time_in_minutes, 'minutes')
            else:
                print('cong 값이 0인 행이 없습니다.')
        return result_dict

    data = load_data()
    blocks, time = preprocessing(time)
    result_container = get_accumulated_container_count(data, blocks, time)
    return result_container


if __name__ == '__main__':
    
    time = '2021-02-07 07:20:00'
    test2(time)

