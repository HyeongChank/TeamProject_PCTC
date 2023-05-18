import simpy 
import random
import csv
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

class Truck:
    def __init__(self, env, name, arrival_time, in_trucks_completed, out_trucks_completed, in_out_trucks_completed, waiting_time, result_waiting):
        self.env = env
        self.name = name
        self.in_trucks_completed = in_trucks_completed
        self.out_trucks_completed = out_trucks_completed
        self.arrival_time = arrival_time
        self.in_out_trucks_completed = in_out_trucks_completed
        self.waiting_time = waiting_time
        self.result_waiting = result_waiting

        #분포에 따라 customer 도착
        self.action = env.process(self.truck_generate())

    def truck_generate(self):
        yield env.timeout(self.arrival_time)
   
        print(f"트럭 {self.name}이(가) 입차했습니다. 시간: {env.now}")
        
        in_yard_time = env.now
        waiting_times[self.name] = in_yard_time
        self.env.process(self.in_out_work(waiting_times))


    def in_out_work(self, waiting_times):
        select_num = random.randint(1,10)
        if select_num <= 4:
            # 작업 시간
            in_work_time = random.randint(5,20)
            yield env.timeout(in_work_time)
   
            print(f"트럭 {self.name}이(가) 반입을 완료했습니다. 시간: {env.now}")
            
            print(f"트럭 {self.name}이(가) 출차했습니다. 시간: {env.now}")
            out_yard_time = env.now

            in_yard_time = waiting_times[self.name]
            print('key', in_yard_time)
            waiting_time = out_yard_time- in_yard_time
            result_waiting.append(waiting_time)
            print(f"트럭 {self.name}의 반입만 대기시간: {waiting_time}")
            new_data = [self.name, "in", in_yard_time, out_yard_time, waiting_time]
            in_trucks_completed.append(new_data)

        elif select_num <= 8:
            # 작업 시간
            in_work_time = random.randint(5,10)
            yield env.timeout(in_work_time)
    
            print(f"트럭 {self.name}이(가) 반입을 완료했습니다. 시간: {env.now}")
            
            out_work_time = random.randint(5,10)
            yield env.timeout(out_work_time)
       
            print(f"트럭 {self.name}이(가) 반출 작업을 완료했습니다. 시간: {env.now}")
            print(f"트럭 {self.name}이(가) 출차했습니다. 시간: {env.now}")
            out_yard_time = env.now
            print(out_yard_time)

            in_yard_time = waiting_times[self.name]
            print('key', in_yard_time)
            waiting_time = out_yard_time- in_yard_time
            result_waiting.append(waiting_time)
            print(f"트럭 {self.name}의 반입, 출차 대기시간: {waiting_time}")
            new_data = [self.name, "in_out", in_yard_time, out_yard_time, waiting_time]
            in_out_trucks_completed.append(new_data)

        else:
            out_work_time = random.randint(5,20)
            yield env.timeout(out_work_time)
      
            print(f"트럭 {self.name}이(가) 반출 작업을 완료했습니다. 시간: {env.now}")
            print(f"트럭 {self.name}이(가) 출차했습니다. 시간: {env.now}")
            out_yard_time = env.now

            in_yard_time = waiting_times[self.name]
            print('key', in_yard_time)
            waiting_time = out_yard_time- in_yard_time
            result_waiting.append(waiting_time)
            
            print(f"트럭 {self.name}의 반출만 대기시간: {waiting_time}")
            new_data = [self.name, "out", in_yard_time, out_yard_time, waiting_time]
            out_trucks_completed.append(new_data)

env = simpy.Environment()
arrival_interval = random.randint(3,18)  # 트럭 도착 주기 (분 단위)
in_trucks_completed = []
out_trucks_completed = []
waiting_times = {}
result_waiting = []
in_out_trucks_completed = []
waiting_time = 1

# 트럭 대수
for i in range(30):
    Truck(env, i+1, i*arrival_interval, in_trucks_completed, out_trucks_completed, in_out_trucks_completed, waiting_time,result_waiting)

#env.run(until=240)  # 시뮬레이션 시간 (분 단위)

fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], 'bo')

def init():
    ax.set_xlim(0, 100)  # 시뮬레이션 시간에 맞게 x축 범위 설정
    ax.set_ylim(0, 30)  # 트럭 대수에 맞게 y축 범위 설정
    return line,

def update(frame):
    time_interval = arrival_interval  # 트럭 도착 주기
    env.run(until=(frame+1) * time_interval)  # 프레임에 해당하는 시간까지 시뮬레이션 실행
    print(result_waiting)
    
    # 시뮬레이션 결과를 이용한 데이터 업데이트
    x_data.append(frame)
    y_data.append(result_waiting[frame])
    line.set_data(x_data, y_data)
    return line,

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=range(100), init_func=init, blit=True)
print(result_waiting)
# 애니메이션 저장
animation_filename = "truck_simulation_animation.gif"
ani.save(animation_filename, writer="pillow")

print(f"애니메이션을 '{animation_filename}' 파일로 저장했습니다.")