import simpy 
import random
import csv
import numpy as np
import matplotlib.dates as mdates
import csv
from datetime import datetime, timedelta
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# ## 데이터 정렬해서 다시 저장
# file_path = './truck_simulation_results.csv'
# with open(file_path, 'r') as file:
#     reader = csv.reader(file)
#     data = list(reader)

# header = data[0]
# data_rows = data[1:]
# sorted_data = sorted(data_rows, key =lambda row: int(row[0]))
# sorted_data.insert(0,header)
# # 정렬된 데이터를 CSV 파일로 저장
# sorted_file_path = './sorted_truck_simulation_results.csv'
# with open(sorted_file_path, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(sorted_data)

# print("데이터를 첫 번째 트럭 열을 기준으로 오름차순으로 정렬하여 저장했습니다.")


## 애니메이션 구현 부분
file_path = './sorted_truck_simulation_results.csv'
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
header = data[0]
data_rows = data[1:]
in_time_out = []
waiting_time = []

start_time = '2021-02-01 12:00:00'
new_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
print(new_start_time)

## str을 datetime 형식으로 바꾸기 위해 int -> timedelta 로 변경
min_before = '30'
min_int = int(min_before)
min_new = timedelta(minutes = min_int)

print(new_start_time + min_new)

for row in data_rows:
    min_before = row[2]
    min_int = int(min_before)
    min_tr= timedelta(minutes=min_int)
    
    new_time = new_start_time + min_tr
    print(new_time)
    in_time_out.append(new_time)
    waiting_time.append(int(row[4]))

## 리스트 안의 datetime 값 모두 str로 변경하기
str_list = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in in_time_out]
print(str_list)

max_time = str_list[-1]
print(max_time)
x_min = start_time
x_max = max_time 

## 리스트 안의 datetime 값 모두 int로 변경하기
print(in_time_out)
x = mdates.date2num(in_time_out)
x_int_list = [int(num) for num in x]
print(x_int_list)

x_min = x_int_list[0]
x_max = x_int_list[-1]


sinegraph = plt.figure()
sine = plt.axes()
sine.set_xlim(x_min, x_max)
sine.set_ylim(0, max(waiting_time))

x = np.array(x_int_list)
y = np.array(waiting_time)

line, = sine.plot([],[])

def update(num, x, y, line):
    line.set_data(x[:num], y[:num])
    return line,
sineani = animation.FuncAnimation(sinegraph, update, frames = len(x) +1, fargs=(x,y, line),
                                  interval = 100, repeat = False)
animation_filename = "test2_animation.gif"
sineani.save(animation_filename, writer="pillow")
print(f"애니메이션을 '{animation_filename}' 파일로 저장했습니다.")
plt.show()