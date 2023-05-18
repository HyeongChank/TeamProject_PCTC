import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 데이터프레임 생성
df = pd.DataFrame({
    'Block': ['Q111'] * 32,
    '작업 시간': pd.date_range('2021-02-06 14:30:00', periods=32, freq='30T'),
    '누적 컨테이너 개수': [3, 1, 3, 1, 6, 1, 6, 435, 435, 378, 406, 253, 406, 190, 253, 561, 528, 171, 105, 153, 190, 171, 276, 120, 325, 210, 153, 406, 300, 666, 153, 300],
    'cong': [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 0, 0, 1, 1, 1, 0, 2, 1, 0, 2, 1, 2, 0, 1]
})
mask = df['cong'] !=0
df = df[mask]
df = df[mask].reset_index(drop=True)
print(df)
# print(df)
# print(df.index)
indexes = []
cong_diffs = []
for idx, row in df.iterrows():
    if row['cong'] == 2:
        cong2_time = row['작업 시간']
        cong2_index = idx
        print('cong2', idx)
        
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
#독립변수와 종속변수로 데이터 분리
X = np.arange(len(data)).reshape(-1, 1)
y = np.array(data)

#훈련셋과 테스트셋 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#선형회귀 모델 훈련
reg = LinearRegression()
reg.fit(X_train, y_train)

#테스트셋을 이용하여 모델 예측
y_pred = reg.predict(X_test)

#모델 평가
score = reg.score(X_test, y_test)
print(f'R-squared: {score:.4f}')

#다음 cong2에서 cong1로 변하는 시간 예측
next_cong2 = np.array([[len(data)]])
next_cong1 = reg.predict(next_cong2)
print(f'Next cong2-cong1 time: {next_cong1[0]:.1f}')



    # if i
    #     print(row.index)
    #     cong2_time = df.loc[i, '작업 시간']
    #     print(cong2_time)

# 'cong' 열 값이 2인 첫 번째 행과 이후 가장 빠른 'cong' 열 값이 1인 행의 인덱스 찾기


# mask2 = (df['cong'] == 1)
# indices = []
# for i in df[mask1].index:
#     try:
#         idx = min(df[mask2 & (df.index > i)].index)
#         print(idx)
#         indices.append((i, idx))
#     except ValueError:
#         pass

# # 인덱스 간 차이 계산하여 소요 시간 구하기
# durations = [(df.loc[idx2, '작업 시간'] - df.loc[idx1, '작업 시간']).total_seconds() / 60 for idx1, idx2 in indices]

# print(durations)