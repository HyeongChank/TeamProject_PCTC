import simpy 
import random
import csv
import numpy as np
import csv
from datetime import datetime, timedelta
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

## 데이터 정렬해서 다시 저장
file_path = './truck_simulation_results.csv'
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

header = data[0]
data_rows = data[1:]
sorted_data = sorted(data_rows, key =lambda row: int(row[0]))
sorted_data.insert(0,header)
# 정렬된 데이터를 CSV 파일로 저장
sorted_file_path = './sorted_truck_simulation_results.csv'
with open(sorted_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(sorted_data)

print("데이터를 첫 번째 트럭 열을 기준으로 오름차순으로 정렬하여 저장했습니다.")


## 애니메이션 구현 부분
file_path = './sorted_truck_simulation_results.csv'
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
header = data[0]
data_rows = data[1:]
in_time_out = []
waiting_time = []

for row in data_rows:
 
    in_time_out.append(int(row[2]))
    waiting_time.append(int(row[4]))

sinegraph = plt.figure()
sine = plt.axes()
sine.set_xlim(0, max(in_time_out))
sine.set_ylim(0, 50)

x = np.array(in_time_out)
y = np.array(waiting_time)

line, = sine.plot([],[])

def update(num, x, y, line):
    line.set_data(x[:num], y[:num])
    return line,
sineani = animation.FuncAnimation(sinegraph, update, frames = len(x) +1, fargs=(x,y, line),
                                  interval = 100, repeat = False)
animation_filename = "test_animation.gif"
sineani.save(animation_filename, writer="pillow")
print(f"애니메이션을 '{animation_filename}' 파일로 저장했습니다.")
plt.show()