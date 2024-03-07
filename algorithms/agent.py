'''
File chạy thuật toán

Tạo class thuật toán

Tạo class memory: lưu trữ các state cũ  
    Có các hàm: 
        init: Tạo queue chứa
        push(state): Thêm state hiện tại vào hàng chờ
        sample(batch_size): lấy mẫu ngẫu nhiên n=batch_size mẫu từ hàng chờ để train

Tạo class Agent: đưa ra quyết định chọn hành động nào
    init(): Khai báo các trọng số sử dụng, batch_size, learning rate, khởi tạo các mạng, tạo hàm tối ưu, tạo hàng chờ
    select_action(state)=>đưa ra hành động: Chọn hành động
    optimal_model(các tham số để tối ưu): Tính toán loss, cập nhật lại các mạng để tối ưu hơn.
    train(số iter, số episode, số duration, tham số tối ưu,số episode):Huấn luyện thuật toán
    test(): 
    runAC():
'''
import sys
import os
from pathlib import Path
link=Path(os.path.abspath(__file__))
link=link.parent.parent
link=os.path.join(link, "system_model")
sys.path.append(link)
import numpy as np
import torch
import gym
from matplotlib import pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import copy
import environment as env

from config import *
import copy
from MyGlobal import MyGlobals
from itertools import count
from torch.distributions import Categorical
import random
import math
from collections import namedtuple, deque
import pickle

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
result_train2=list()
result_test2=list()
Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

state_size = NUM_STATE
action_size = NUM_ACTION
lr = 0.001
eps_start=0.9
eps_end=0.05
eps_decay=1000


class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
        self.Transition = namedtuple('Transition',('state', 'action', 'next_state', 'reward'))
    def push(self, *args):
        self.memory.append(self.Transition(*args))
    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    def __len__(self):
        return len(self.memory)
replay = ReplayMemory(10000)
class DQNnet(nn.Module):
    def __init__(self,n_observations,n_actions):
        super(DQNnet,self).__init__()
        self.layer1=nn.Linear(n_observations,128)
        self.layer2=nn.Linear(128,128)
        self.layer3=nn.Linear(128,n_actions)
    def forward(self,x):
        x=F.relu(self.layer1(x))
        x=F.relu(self.layer2(x))
        return self.layer3(x)

class DQNAgent:
    def __init__(self) :
        self.env=env.BusEnv()
        self.optimize=0
        self.env.seed(123)
        self.batch_size=256
        self.eps_start=0.5
        self.eps_end=0.05
        self.eps_decay=1000
        self.tau_decay=1000
        self.tau=0.01
        self.lr=1e-4
        self.n_actions=NUM_ACTION
        self.n_observations=NUM_STATE
        self.policy_net=DQNnet(self.n_observations,self.n_actions-1).to(device)
        self.target_net=DQNnet(self.n_observations,self.n_actions-1).to(device)
        
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer=optim.AdamW(self.policy_net.parameters(),lr=self.lr,amsgrad=True)
        self.memory=ReplayMemory(10000)
        self.stepdone=0
        self.stepdone1=0
    def normalize(self, state):
        array = torch.zeros(1,24)
        array[0][0] = (state[0][0] - REQUIRED_GPU_FLOPS[0]) / (REQUIRED_GPU_FLOPS[1] - REQUIRED_GPU_FLOPS[0])
        array[0][1] = (state[0][1] - MIN_S_IN) / (MAX_S_IN - MIN_S_IN)
        array[0][2] = (state[0][2] - MIN_S_OUT) / (MAX_S_OUT - MIN_S_OUT)
        array[0][3] = (state[0][3] - DEADLINE[0]) / (DEADLINE[1] - DEADLINE[0])
        for i in range(NUM_VEHICLE):
            array[0][i * 2 + 4] = state[0][i * 2 + 4] / 8
            array[0][i * 2 + 5] = state[0][i * 2 + 5] / 300
        return array

        
        
    def select_action(self,state):
            sample=random.random()
            eps_threshold=self.eps_end+(self.eps_start-self.eps_end)*math.exp(-1.*self.stepdone/self.eps_decay)
            self.stepdone+=0.005
            if sample > eps_threshold:
                with torch.no_grad():
                    return self.policy_net(state).max(-1)[1].view(1, 1)
            else:
                return torch.tensor([[random.randint(0,NUM_ACTION-2)]], device=device, dtype=torch.long)    
    
    def optimize_model(self,gamma):
            # self.start_time=time.time()
            if len(self.memory) < self.batch_size:
                return
            transitions = self.memory.sample(self.batch_size)
            batch = Transition(*zip(*transitions))

            
            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                                batch.next_state)), device=device, dtype=torch.bool)
            non_final_next_states = torch.cat([s for s in batch.next_state
                                                        if s is not None])
            batch_state=[]
            for i in batch.state :
                batch_state.append(i.view(1,24))
            state_batch = torch.cat(batch_state)
            action_batch = torch.cat(batch.action)

           
            reward_batch = torch.cat(batch.reward)

            
            state_action_values = self.policy_net(state_batch).gather(1, action_batch)

            next_state_values = torch.zeros(self.batch_size, device=device)
            with torch.no_grad():
                #  next_state_values[non_final_mask] =self.target_net(non_final_next_states).max(1)[0]
                next_state_values[non_final_mask] =self.policy_net(non_final_next_states).gather(1,self.target_net(non_final_next_states).max(1)[1].unsqueeze(0))
                
            # Compute the expected Q values
            expected_state_action_values = (next_state_values * gamma) + reward_batch
            

            # Compute Huber loss
            criterion = nn.SmoothL1Loss()
            loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

            # Optimize the model
            self.optimizer.zero_grad()
            loss.backward()
            # In-place gradient clipping
            torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
            self.optimizer.step()
            self.optimize+=1
            # self.end_time=time.time()
            # print(f"optimze_time:{self.end_time-self.start_time},times{self.optimize}")
    def train(self,num_iters,num_episodes,gamma):
    
            for iter in range(num_iters):
                self.env.replay()
                for episode in range(num_episodes):
                    state = self.env.reset()
                    state=torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
                    done = False
                    while not done:
                        for i in count():
                            state=self.normalize(state)
                            
                            action = self.select_action(state)
                            action1=action.item()
                            next_state, reward, done= self.env.step(np.array(action1+1))
                            # print(next_state)
                            reward = torch.tensor([reward], device=device)
                            if done:
                                if (self.env.old_avg_reward < -1000):
                                    return
                                next_state = None
                                print('Episode: {}, Score: {}'.format(
                                    episode, self.env.old_avg_reward))
                                break 
                            next_state = torch.tensor(next_state, dtype=torch.float32, device=device).unsqueeze(0)
                            
                            next_state=self.normalize(next_state)
                            self.memory.push(state, action, next_state, reward)
                            state = next_state

                            self.optimize_model(gamma)
                            
                            target_net_state_dict = self.target_net.state_dict()
                            policy_net_state_dict = self.policy_net.state_dict()
                            for key in policy_net_state_dict:
                                target_net_state_dict[key] = policy_net_state_dict[key]*self.tau + target_net_state_dict[key]*(1-self.tau)
                                
                            self.target_net.load_state_dict(target_net_state_dict)

    def test(self,num_episodes):
            
            if (self.env.old_avg_reward < -150000):
                return
            for episode in range(num_episodes):
                state = self.env.reset()
                done = False

                while not done:
                    state = torch.FloatTensor(state).to(device)
                    action= self.select_action(state)
                    action1=action.item()
                    next_state, reward, done,= self.env.step(np.array(action1))

                    state = next_state

                print('Test Episode: {}, Score: {}'.format(episode, self.env.old_avg_reward))
    def runAC(self,gamma):
        MyGlobals.folder_name = "RL/"
        self.train(num_iters=1, num_episodes=90,
            gamma=gamma )
        self.test( num_episodes=10, )

Agent=DQNAgent()
Agent.runAC(0.99)