'''
Vai trò môi trg

Tạo môi trường
init():
    liệt kê các thứ cần khởi tạo
    các biến: seed, trọng số giữa thời gian trễ và drop
    dữ liệu của các xe bus
    observation():list có độ dài phụ thuộc vào số xe, mỗi observation tương ứng với 1 state ứng với mỗi khi một tác vụ được tạo ra
    time tác vụ được tạo, lượng tài nguyên máy tính cần thiết, dung lượng bộ nhớ tiêu thụ,deadline tác vụ, khoảng cách task đến xe 1, hàng chờ trên xe 1,...khoảng cách task đến xe n, hàng chờ trên xe n

    task_list(): Một queue để chứa các task, lấy dữ liệu từ file create data, đưa dữ liệu vào queue, mỗi lẫn lấy ra 1 task để cho mô hình xử lý, khi queue trống tức các task đã dc xử lý thì done=True

    tạo file chứa:tổng reward, số tác vụ drop, thời gian trễ,  


reset()=>state đầu tiên ứng với tác vụ đầu của episode
    !!!Chú ý: các hàng chờ vẫn tiếp tục từ cái cũ tại thời gian bọn nó liên tiếp nhau 
replay(): 
    Reset lại môi trg, đưa lại về episode 0
    !!!Chú ý các hàng chờ phải làm mới

step(action)=>next_state, reward, done:
    nhận một hành động, tính toán ứng với hành động ấy thì tác vụ xử lý trong bao lâu 
    lấy task tiếp theo từ task_list đưa vào next_state, cập nhật lại state mới, kiểm tra done
    Đưa ra thời gian trễ, reward, next_state, done
    !!! Chú ý cập nhật tất cả các hàng chờ, trừ đi khoảng thời giữa 2 state
task_distance(xe_thu_i,tac_vu_j,thoi_gian_k)=>Khoang cách của task j đến xe i tại thời gian k
    Tính khoảng cách theo tọa độ, tọa độ xe xác định tại thời gian gần với k nhất 
  
'''
import numpy as np
import pandas as pd
import gym
from gym import spaces
from gym.utils import seeding
import copy
import os
from metric import *
from config import *

class BusEnv(gym.Env):
    def __init__(self, env=None):
        self.env = env
        # episode đầu
        self.index_of_episode = 0
        # Tổng phần thưởng
        self.sum_reward = 0
        # Số phần thưởng đã nhận
        self.nreward = 0
        # Không gian hành động
        self.n_actions=NUM_ACTION
        # Không gian state
        self.n_observations=NUM_STATE  
        
    #Lấy dữ liệu của xe bus, xử lý rồi đưa nó vào 1 list
    def load_bus_data(self, num_files=60):
        data_list = {}
        for i in range(1, num_files + 1):
            filename = f"xe_{i}"
            data_list[filename]=self.preprocessBusLoction(filename)
        return data_list

    #Lấy dữ liệu xe bus từ file csv trừ đi thời gian min để tất cả bắt đầu từ 0, đưa thời gian về s
    def preprocessBusLoction(self, excel_file):
        #địa chỉ bus
        a = pd.read_csv(os.path.join(DATA_BUS, excel_file))
        a = a.iloc[:500, [1, 4, 5]]
        a['time'] = a['time'].apply(time_to_seconds)
        min_time=a['time'].min()
        a['time']-=min_time
        return a.to_numpy()
    

    def readcsv(self, number_bus, time):
        #đọc excel tính lat,lng của xe tại t=time
        data = self.data_bus[str(number_bus)]

        after_time = data[data[:, 1] >= time]
        pre_time = data[data[:, 1] <= time]
        if len(after_time) == 0:
            return 1.8
        las = after_time[0]
        first = pre_time[-1]
        diff1=las[0]-first[0]
        diff2=time-first[0]
        # weighted average of the distance
        lat,lng=calculate_intermediate_coordinate(first[1],first[2],las[1],lng[2],diff2/diff1)
        return lat,lng


    def seed(self, seed=SEED):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def replay(self):
        # Khởi đâù của iter đặt lại episode về 0
        self.index_of_episode = 0
        self.data_bus=self.load_bus_data()


    def reset(self):
        # Khởi tạo state ban đầu 
        self.observation=np.zero(NUM_STATE)
        self.sum_tolerance_time = 0
        #Đọc dữ liệu từ file task ứng với số rpisode
        self.data = pd.read_csv(os.path.join(DATA_TASK, "datatask{}.csv".format(
                self.index_of_episode)), header=None).to_numpy()
        #Tạo 1 queue lấy các task có cùng time với task ban đầu
        self.queue = copy.deepcopy(
                self.data[self.data[:, 0] == self.data[0][0]])
        # self.queue = self.queue[self.queue[:, 2].argsort()]
        self.data = self.data[self.data[:, 0] != self.data[0][0]]
        self.result = []
        
        self.time = self.queue[0][0]

        for i in range(NUM_VEHICLE):
            bus_lat,bus_lng=self.readcsv(f"xe_{i+1}")

            self.observation[2 *
                                 i + 4] = haversine(bus_lat,bus_lng,self.queue[1],self.queue[2])
        #Nếu ko phải episode đầu thì trừ hàng chờ đi độ lệch time giữa đít episode trc và đầu episode sau
        if self.index_of_episode!=0:
            for i in range(NUM_VEHICLE):
                self.observation[2 * i + 5] = max(
                    0, self.observation[2 * i + 5]-(self.time-self.time_last))
                
        self.time_last = self.data[-1][0]
                
        self.observation[0] = self.queue[0][3] #REQUIRED_GPU_FLOPS
        self.observation[1] = self.queue[0][5] #s_in
        self.observation[2] = self.queue[0][6] #s_out
        self.observation[3] = self.queue[0][7] #deadline
        
        # Chỉ đến episode tiếp theo
        self.index_of_episode +=1

    def step(self, action):
        time_delay = 0
        drop_out=0



        return self.observation, reward, done
        
    
    
        
        return self.observation
    
    def task_distance(self, bus_number,long_task,lat_task,time):
        pass
        return distance

    

    


    


