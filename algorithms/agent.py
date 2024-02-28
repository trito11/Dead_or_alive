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
from itertools import count
import enviroment as env

class Agent_local:
    def __init__(self):
        self.env = env.BusEnv()

    def select_action(self):
        return 0 # 0 nghĩa là local
    
    def run(self):
        self.env.replay()
        
        self.state = self.env.reset()

        done = False
        step = 0
        while (not done) and  step in count() :
                self.action = self.select_action()
                self.state, reward, done = self.env.step(self.action)
                print(f'Step {step}: {reward}')

if __name__ == '__main__':
    agent = Agent_local()
    agent.run()