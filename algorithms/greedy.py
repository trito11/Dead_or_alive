from itertools import count
import sys
sys.path.append('D:\Lab\Lab_project\Dead_or_alive\system_model')
import environment as env
from config import *
import torch
class DQNAgent:
    def __init__(self) :
        self.env=env.BusEnv()
        self.optimize=0
        self.env.seed(123)
        self.batch_size=2
        self.n_actions=NUM_ACTION
        self.n_observations=NUM_STATE

    def select_action(self,state,greedy):
        if greedy=='queue':
            action=1
            queue=state[5]
            for i in range(1,NUM_VEHICLE):
                if state[i*2+5]<=queue:
                    action=i+1
                    queue=state[i*2+5]
            return action
        if greedy=='distance':
            action=1
            distance=state[4]
            for i in range(1,NUM_VEHICLE):
                if state[i*2+4]<distance:
                    action=i+1
                    distance=state[i*2+4]
            return action
 
    def run(self,greedy):
        self.env.replay()
        for episode in range(10):
            state = self.env.reset()
            done = False
            while not done:
                for i in count():
                    action = self.select_action(state,greedy)
                    next_state, reward, done= self.env.step(action)
                    if done:
                        next_state = None
                        print('Episode: {}, Score: {}'.format(
                            episode, self.env.old_avg_reward))
                        break
                    state = next_state
if __name__ == '__main__':
    Agent=DQNAgent()
    Agent.run('distance')