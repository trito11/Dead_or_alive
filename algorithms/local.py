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
<<<<<<< HEAD:algorithms/agent.py
import sys
sys.path.append('D:\Lab\Lab_project\Dead_or_alive\system_model')
from itertools import count
import enviroment as env
=======

from ..system_model import environment as env
from ..system_model.config import NUM_EPISODE
>>>>>>> fa5428f5f037e48cfa3760e4927c3461f55db0a1:algorithms/local.py

class Agent_local:
    def __init__(self):
        self.env = env.BusEnv()

    def select_action(self):
        return 0 # 0 nghĩa là local
    
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
    agent = Agent_local()
    agent.run(num_ep=20)