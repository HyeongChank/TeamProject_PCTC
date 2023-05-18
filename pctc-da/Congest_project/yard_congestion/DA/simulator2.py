import simpy 
import random
import csv

class Truck:
    def __init__(self, env, name, arrival_time, in_trucks_completed, out_trucks_completed, in_out_trucks_completed):
        self.env = env
        self.name = name
        self.in_trucks_completed = in_trucks_completed
        self.out_trucks_completed = out_trucks_completed
        self.arrival_time = arrival_time
        self.in_out_trucks_completed = in_out_trucks_completed

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

# 트럭 대수
for i in range(100):
    Truck(env, i+1, i*arrival_interval, in_trucks_completed, out_trucks_completed, in_out_trucks_completed)

env.run(until=240)  # 시뮬레이션 시간 (분 단위)

print(f"반입 작업을 완료한 트럭 수: {len(in_trucks_completed)}")
print(f"반출 작업을 완료한 트럭 수: {len(out_trucks_completed)}")

# 결과를 저장할 CSV 파일 이름
csv_filename = "truck_simulation_results.csv"

    # CSV 파일에 결과를 기록하는 함수
def save_results_to_csv(filename, in_trucks_completed, out_trucks_completed, in_out_trucks_completed):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Truck", "Operation", "in_Time", "out_Time", "waiting_Time"])  # 헤더 라인 작성

        # 반입 작업 완료 트럭 기록
        for truck in in_trucks_completed:
            
            writer.writerow([truck[0], truck[1], truck[2], truck[3], truck[4]])

        # 반출 작업 완료 트럭 기록
        for truck in out_trucks_completed:
        
            writer.writerow([truck[0], truck[1], truck[2], truck[3], truck[4]])

        for truck in in_out_trucks_completed:
        
            writer.writerow([truck[0], truck[1], truck[2], truck[3], truck[4]])

        env.run(until=300)  # 시뮬레이션 시간 (분 단위)

        print(f"반입 작업을 완료한 트럭 수: {len(in_trucks_completed)}")
        print(f"반출 작업을 완료한 트럭 수: {len(out_trucks_completed)}")
        print(f"반출 작업을 완료한 트럭 수: {len(in_out_trucks_completed)}")

# 결과를 CSV 파일로 저장
save_results_to_csv(csv_filename, in_trucks_completed, out_trucks_completed, in_out_trucks_completed)

print(f"결과를 '{csv_filename}' 파일로 저장했습니다.")