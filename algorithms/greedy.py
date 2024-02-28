from ..system_model import environment as env
from ..system_model.config import NUM_EPISODE
import numpy as np

class Agent_greedy_nearest:
    def __init__(self):
        self.env = env.BusEnv()

    # chon xe gan nhat
    def select_action(self):
        distances_to_bus = self.env.observation[4::2]
        print(distances_to_bus)
        print(min(distances_to_bus))
        print(np.argmin(distances_to_bus) + 1)
        return int(np.argmin(distances_to_bus)) + 1
    
    def run(self, num_ep = NUM_EPISODE):
        self.env.replay()
        
        for ep in range(num_ep):
            self.state = self.env.reset()

            done = False
            step = 0
            while (not done) and  (step := step + 1) :
                self.action = self.select_action()
                self.state, reward, done = self.env.step(self.action)

            print(f'Episode {ep}, avarage_reward: {self.env.old_avg_reward}\n')

if __name__ == '__main__':
    agent = Agent_greedy_nearest()
    agent.run(num_ep=2)