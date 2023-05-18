# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# import datetime
# # 데이터 불러오기

# data = pd.read_csv("D:/김형찬/team_project/TeamProject_PCTC/pctc-da/Congest_project/data/congestcsv.csv", encoding='cp949')
# print(data.head())

# data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])
# data['작업코드'] = data['작업코드'].replace({'양하': 0, '적하': 0, '반입': 1, '반출': 0})
# data['반입차량대수'] = data['작업코드']


# data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
# data = data[['작업 지시 시간', '반입차량대수']]
# # 데이터 전처리

# data.set_index('작업 지시 시간', inplace=True)

# # 데이터 스케일링
# scaler = MinMaxScaler()
# scaled_data = scaler.fit_transform(data)

# # 학습 데이터와 테스트 데이터로 분할
# train_size = int(len(data) * 0.8)
# train_data = scaled_data[:train_size]
# test_data = scaled_data[train_size:]

# # LSTM 입력 데이터 생성
# def create_lstm_dataset(dataset, look_back):
#     X, y = [], []
#     for i in range(len(dataset) - look_back):
#         X.append(dataset[i:i+look_back])
#         y.append(dataset[i+look_back])
#     return np.array(X), np.array(y)

# look_back = 24  # 24시간 이전 데이터를 사용하여 예측
# train_X, train_y = create_lstm_dataset(train_data, look_back)
# test_X, test_y = create_lstm_dataset(test_data, look_back)

# # LSTM 모델 구성
# model = Sequential()
# model.add(LSTM(64, input_shape=(look_back, 1)))
# model.add(Dense(1))
# model.compile(loss='mean_squared_error', optimizer='adam')

# # 모델 학습
# model.fit(train_X, train_y, epochs=10, batch_size=32, verbose=1)

# # # 테스트 데이터에 대한 예측
# # predicted = model.predict(test_X)
# # predicted = scaler.inverse_transform(predicted)

# # # 예측 결과 시각화
# # import matplotlib.pyplot as plt

# # plt.scatter(data.index[train_size+look_back:], data['반입차량대수'][train_size+look_back:], label='Actual')
# # plt.scatter(data.index[train_size+look_back:], predicted, label='Predicted')
# # plt.xlabel('Time')
# # plt.ylabel('Vehicle Count')
# # plt.ylim(0, 2)  # y축 범위 설정
# # plt.legend()
# # plt.show()

# # 향후 추세 예측
# future_data = test_X[-1].reshape(1, look_back, 1)
# future_predictions = []
# for i in range(len(test_data)):
#     predicted = model.predict(future_data)
#     future_predictions.append(predicted)
#     future_data = np.concatenate((future_data[:, 1:, :], predicted.reshape(1, 1, 1)), axis=1)

# future_predictions = np.array(future_predictions).reshape(-1, 1)
# future_predictions = scaler.inverse_transform(future_predictions)
# print('future_predictions', len(future_predictions))
# print('size', data['반입차량대수'][train_size+look_back:].size)

# # 예측 결과 시각화
# import matplotlib.pyplot as plt

# plt.plot(data.index[train_size+look_back:], data['반입차량대수'][train_size+look_back:], label='Actual')
# plt.plot(data.index[train_size+look_back:], future_predictions, label='Predicted')
# plt.xlabel('Time')
# plt.ylabel('Vehicle Count')
# plt.legend()
# plt.show()