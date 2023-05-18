import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import matplotlib.pyplot as plt

def load():
    # data = pd.read_excel("D:/김형찬/ai-algorism/data/conjestDum.xlsx", sheet_name='csv')
    data = pd.read_excel("D:/김형찬/Congest_project/data/congestDumfh.xlsx", sheet_name='csv')
    # data['작업코드'] = data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
    # print(data)
    data['작업 지시 시간'] = pd.to_datetime(data['작업 지시 시간'])
    data['작업 완료 시간'] = pd.to_datetime(data['작업 완료 시간'])
    print(data.head())

    print(data.shape)
    print(data.columns)
    return data


def preprocessing(data):
    data['입차시간'] = data['작업 지시 시간'] + timedelta(minutes=10)
    data['출차시간'] = data['작업 완료 시간'] + timedelta(minutes=10)
    data['소요시간'] = data['출차시간'] - data['입차시간']    

    n_data = data
    m_data = data
    n_data['수량'] = 1
    m_data['마수량'] = -1

    n_data['입차누적'] = n_data['수량'].cumsum()
    n_data['출차누적'] = n_data['마수량'].cumsum()

    time = pd.to_datetime('2021-02-06 15:29:06')
    # # 입력받은 time 이후의 데이터만 선택하여 새로운 데이터프레임 생성
    # n_data = n_data[n_data['입차시간'] < time]
    # n_data = n_data.reset_index(drop=True)
    # print(n_data[['입차시간', '입차누적']])
    # last_in_entry = n_data.at[n_data.index[-1], '입차누적']
    # print(last_in_entry)


    # m_data = m_data[m_data['출차시간'] < time]
    # m_data = m_data.reset_index(drop=True)
    # print(m_data[['입차시간', '출차누적']])
    # last_out_entry = m_data.at[m_data.index[-1], '입차누적']
    # print(last_out_entry)

    # print(last_in_entry-last_out_entry)
    values = []
    while time <= pd.to_datetime(n_data['입차시간'].iloc[-1]):
        print(time)
        n_data = n_data[n_data['입차시간'] < time]
        n_data = n_data.reset_index(drop=True)
        print(n_data[['입차시간', '입차누적']])
        last_in_entry = n_data.at[n_data.index[-1], '입차누적']
        print(last_in_entry)


        # m_data = m_data[m_data['출차시간'] < time]
        # m_data = m_data.reset_index(drop=True)
        # print(m_data[['입차시간', '출차누적']])
        # last_out_entry = m_data.at[m_data.index[-1], '출차누적']
        # print(last_out_entry)

        # interval = last_in_entry-last_out_entry

        # # 30분마다의 '입차누적 - 출차누적' 값을 리스트에 추가
        # values.append(interval)

        # time을 30분씩 증가
        time += pd.Timedelta(minutes=30)

    # 그래프로 표현
    # time_range = pd.date_range(start='2021-02-06 15:30:00', end=pd.to_datetime(n_data['입차시간'].iloc[-1]), freq='30T')
    # plt.plot(time_range, values)
    # plt.xlabel('Time')
    # plt.ylabel('Difference (입차누적 - 출차누적)')
    # plt.title('Difference between 입차누적 and 출차누적')
    # plt.show()
    # 새로운 열 추가
    # n_data['코드'] = n_data['작업코드'].apply(lambda x: 1 if x.startswith('반입') else (-1 if x.startswith('반출') else (-1 if x.startswith('적하') else (1 if x.startswith('양하') else 0))))


    # data.loc[data['작업코드'].str.startswith('반입'), '코드'] = 1
    # data.loc[data['작업코드'].str.startswith('반출'), '코드'] = 2
    # data.loc[data['작업코드'].str.startswith('적하'), '코드'] = 3
    # data.loc[data['작업코드'].str.startswith('양하'), '코드'] = 4

    # 행 선택 나누기
    # mask = data['코드'] ==1
    # data = data[mask]
    # data = data[mask].reset_index(drop=True)



    # n_data['연월일'] = n_data['입차시간'] = n_data['입차시간'].dt.strftime('%Y-%m-%d')
    # print(n_data[['수량','입차시간','출차시간', '입차누적']])
    # print(n_data.shape)
    # return n_data

# def divide(time, data):
#         cong_diffs = []
#         for idx, row in data.iterrows():
#             if row['cong'] == 2:
#                 cong2_time = row['작업 시간']
#                 cong2_index = idx
                
#                 for cong2_index, row in df.loc[idx:].iterrows():
#                     if row['cong'] ==1:
#                         cong1_time = row['작업 시간']
#                         print(cong1_time, cong2_time)
#                         cong_diff = (cong1_time - cong2_time).total_seconds() // 60
#                         cong_diffs.append(cong_diff)
#                         print('cong1', cong2_index)
#                         print(cong_diffs)
#                         break
#                     else:
#                         pass

#         data = cong_diffs    
#     new_data = data
#     print('divide', time)
#     for i in time:
#         mask = new_data['연월일'] == i
#         new_data = new_data[mask]
#         new_data = new_data[mask].reset_index(drop=True)
#         new_data.plot(x='입차시간', y='누적 트럭 대수', kind='line')

        # mask2 = data['연월일'] =='2022-02-07'
        # data3 = data[mask]
        # data3 = data[mask].reset_index(drop=True)
        # print(data3[['코드','입차시간','소요시간','누적 트럭 대수', '연월일']])
        # plt.show()
    

# fig, (ax1, ax2) = plt.subplots(2,1)
#     fig.subplots_adjust(hspace=1.5)
#     # Plot 1
#     ax1.plot(stock_rd.index, stock_rd['Adj Close'], label='stock')

#     s_date = datetime.datetime.strptime(s_date, '%Y-%m-%d')
#     e_date = datetime.datetime.strptime(e_date, '%Y-%m-%d')
#     ax1.set_title('Stock Prices ({0} - {1})'.format(s_date, e_date))

#     ax1.set_ylabel('Price')
#     ax1.tick_params(axis='x', labelsize=6)   
#     ax1.legend()
#     # Plot 2
#     ax2.plot(train_predict_df, label='train predict')
#     ax2.plot(train_Y_df, label='train actual')
#     ax2.set_title('Predict Prices')
#     ax2.set_ylabel('Price')
#     ax2.legend()


if __name__=="__main__":
    time = ['2021-02-06','2021-02-07']
    data = load()
    data = preprocessing(data)
 


