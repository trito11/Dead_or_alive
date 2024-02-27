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
from hexagon import create_location_task_after
class BusEnv(gym.Env):
    def __init__(self, env=None):
        self.env = env
        self.alpha=0.8
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
        # Đếm số hành động                                                                             
        self.n_tasks_in_node = [0] * (NUM_ACTION)

        self.n_tasks_delay_allocation = [0] * (NUM_ACTION)

        self.n_tasks_extra_allocation = [0] * (NUM_ACTION)
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
        
        #Thời gian đầu episode
        self.time = self.queue[0][0]
        #Cập nhật khoảng cách đến từng xe 
        for i in range(NUM_VEHICLE):
            bus_lat,bus_lng=self.readcsv(f"xe_{i+1}",self.time)
            self.observation[2 *
                                 i + 4] = haversine(bus_lat,bus_lng,self.queue[1],self.queue[2])
    
        #Nếu ko phải episode đầu thì trừ hàng chờ đi độ lệch time giữa đít episode trc và đầu episode sau
        if self.index_of_episode!=0:
            for i in range(NUM_VEHICLE):
                self.observation[2 * i + 5] = max(
                    0, self.observation[2 * i + 5]-(self.time-self.time_last))
        #Thời gian cuối episode
        self.time_last = self.data[-1][0]
                
        self.observation[0] = self.queue[0][3] #REQUIRED_GPU_FLOPS
        self.observation[1] = self.queue[0][5] #s_in
        self.observation[2] = self.queue[0][6] #s_out
        self.observation[3] = self.queue[0][7] #deadline
        
        # Chỉ đến episode tiếp theo
        self.index_of_episode +=1

    def step(self, action):
    #Action là số kiểu int ko phải [] hat tensor
        time_delay = 0
        drop_out=0

        #Nếu không drop
        if action > 0:
            #khoảng cách yêu cầu
            distance_req = self.observation[(action)*2+2]
            #hàng đợi cũ
            old_waiting_queue = self.observation[3+(action)*2]
            
            Rate_trans_req_data = getRateTransData(channel_banwidth=CHANNEL_BANDWIDTH, pr=Pr, distance=distance_req,
                                                   path_loss_exponent=PATH_LOSS_EXPONENT, sigmasquare=SIGMASquare)
            #thời gian truyền đi
            

            # waiting queue                        # computation required / computation
            new_waiting_queue = self.observation[0] / PROCESSING_POWER       \
                + max(self.observation[1]/(Rate_trans_req_data), old_waiting_queue) #Độ lệch giữ hàng chờ và thời gian truyền đi
            
            #tọa độ xe sau khi xử lý task
            after_lat_bus,after_lng_bus = self.readcsv(
                f'xe_{action}', new_waiting_queue+self.time)
            
            #Tọa độ người khi đó
            task_lat,task_lng=create_location_task_after(self.queue[1],self.queue[2],new_waiting_queue)

            #Khoang cách lúc sau
            distance_response=haversine(after_lat_bus,after_lng_bus,task_lat,task_lng)

            Rate_trans_res_data = getRateTransData(channel_banwidth=CHANNEL_BANDWIDTH, pr=Pr, distance=distance_response,
                                                   path_loss_exponent=PATH_LOSS_EXPONENT, sigmasquare=SIGMASquare)
            #Tính toán thời gian trễ
            time_delay = new_waiting_queue + \
                self.observation[2]/(Rate_trans_res_data)
            #Cập nhật lại hàng chờ
            self.observation[2+(action)*2] = new_waiting_queue

        #nếu drop thì xử lý tại local
        else:
            drop_out=1 
            time_delay = self.observation[0]/MOBIE_GPU_FLOPS


        self.n_tasks_in_node[action] = self.n_tasks_in_node[action]+1 #Hàm ghi lại các hành động
        self.n_tasks_delay_allocation[action] += time_delay#Hàm ghi lại tổng delay của mỗi xe
        self.sum_delay = self.sum_delay + time_delay#tổng delay


        extra_time = self.observation[3] - time_delay#thời gian thừa

        precent_time_finish=extra_time/self.observation[2] #Tỷ lệ thời gian thừa

        #tính toán phần thưởng
        reward_drop=-drop_out/EXPECTED_DROP

        if precent_time_finish>=0:
            reward_not_drop=0
        else:
            reward_not_drop=precent_time_finish

        reward = reward_not_drop

        # reward = self.alpha*reward_not_drop+ (1-self.alpha)* reward_drop

        # caculate tolerance time
        self.sum_tolerance_time += max(0, time_delay - self.observation[3])
        
        self.n_tasks_extra_allocation[action] += extra_time


        #Xóa task đã xử lý, cập nhật thêm các tác vụ mới xuấ hiện cùng time
        if len(self.queue) != 0:
            self.queue = np.delete(self.queue, (0), axis=0)

        #hàng chờ hết còn task ngoài lấy tiếp task đưa vào hàng chờ
        if len(self.queue) == 0 and len(self.data) != 0:
            self.queue = copy.deepcopy(
                self.data[self.data[:, 0] == self.data[0][0]])
            # self.queue = self.queue[self.queue[:, 2].argsort()]
            
            # position of cars
            for i in range(NUM_VEHICLE):
                bus_lat,bus_lng=self.readcsv(f"xe_{i+1}",self.data[0][0])
                self.observation[2 *
                                    i + 4] = haversine(bus_lat,bus_lng,self.queue[1],self.queue[2])
            #Độ lệch thời gian giữa 2 tác vụ
            time = self.data[0][0] - self.time
            #Cập nhật lại các hàng chờ
            for i in range(NUM_VEHICLE):
                self.observation[2 * i +
                                 5] = max(0, self.observation[2 * i + 5]-time)
            #Lấy thời gian hiện tại
            self.time = self.data[0][0]
            #Cập nhật các tác vụ còn lại
            self.data = self.data[self.data[:, 0] != self.data[0, 0]]
        #Còn task trong hàng chờ thì lấy dữ liệu tiếp do thời gian các task trong hàng đợi như nhau lên không cần cập nhật lại hàng chờ
        if len(self.queue) != 0:
            self.observation[0] = self.queue[0][3] #REQUIRED_GPU_FLOPS
            self.observation[1] = self.queue[0][5] #s_in
            self.observation[2] = self.queue[0][6] #s_out
            self.observation[3] = self.queue[0][7] #deadline


        # check end of episode?
        done = len(self.queue) == 0 and len(self.data) == 0
        self.sum_reward += reward
        if self.observation[3] < time_delay:
            self.sum_over_time += 1

        self.nreward += 1
        self.nstep += 1
        if done:
            print(self.n_tasks_in_node)

        #Ghi kết quả  ra các file

            
            # tempstr = ','.join([str(elem) for elem in self.n_tasks_in_node])
            # self.server_allocation.write(tempstr+"\n")
            # tempstr = ','.join([str(elem/nb_step) if nb_step else '0' for elem, nb_step in zip(
            #     self.n_tasks_delay_allocation, self.n_tasks_in_node)])
            
            # self.delay_allocation.write(tempstr+"\n")

            # tempstr = ','.join([str(elem/nb_step) if nb_step else '0' for elem, nb_step in zip(
            #     self.n_tasks_extra_allocation, self.n_tasks_in_node)])
            # self.extra_allocation.write(tempstr+"\n")
            # tempstr = ','.join([str(elem) for elem in self.n_tasks_sum_extra_allocation])
            # self.sum_extra_allocation.write(tempstr+"\n")
            
            # # sum_tolerance time
            # self.tolerance_time_files.write(str(self.sum_tolerance_time)+"\n")

            # # check end of program? to close files
            # avg_reward = self.sum_reward/self.nstep
            # avg_reward_accumulate = self.sum_reward_accumulate/self.nreward
            # self.reward_files.write(
            #     str(avg_reward)+','+str(avg_reward_accumulate)+"\n")
            # self.over_time_files.write(str(self.sum_over_time/self.nstep)+"\n")
            # self.delay_files.write(
            #     str(self.sum_delay)+','+str(self.sum_delay/self.nstep)+"\n")

            self.old_avg_reward = self.sum_reward/self.nstep
            self.sum_reward = 0
            self.nstep = 0
            self.sum_over_time = 0
            self.sum_delay = 0

        return self.observation, reward, done, 
        
    
    

    

    


    


