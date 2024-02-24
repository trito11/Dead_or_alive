'''
Các thông số cài đặt của hệ thống

Số hành động

Số chiều của state

Số task sẽ dùng

tốc độ xử lý

channel_banwidth, pr, distance, path_loss_exponent, sigmasquare
'''
import os
from pathlib import Path

# Tham số truyền thông
Pr = 46
P = 39.810  # mW
SIGMASquare = 100 
CHANNEL_BANDWIDTH = 20
PATH_LOSS_EXPONENT = 4 

# Tham số về mô hình
NUM_VEHICLE = 10
NUM_ACTION = NUM_VEHICLE + 1 # thêm 1 trường hợp bị là loại bỏ
NUM_STATE = NUM_VEHICLE # [[cac khoang cach toi xe 1, do dai hang cho xe 1], [tuong tu voi xe 2], ...]
NUM_TASKS_PER_TIME_SLOT = 100 # moi time slot la 30s
TIME_EACH_EPISODE = 30 # giay
NUM_EPISODE = 100

# Đường dẫn lưu trữ file
LINK_PROJECT = Path(os.path.abspath(__file__))
LINK_PROJECT = LINK_PROJECT.parent.parent
DATA_LOCATION = "data_task/data" + str(NUM_TASKS_PER_TIME_SLOT) + "_per_" + str(TIME_EACH_EPISODE) + "/"
DATA_DIR = os.path.join(LINK_PROJECT, "data")
RESULT_DIR = os.path.join(LINK_PROJECT, "result/")
DATA_TASK = os.path.join(LINK_PROJECT, DATA_LOCATION)

# Tốc độ xử lý và yêu cầu tài nguyên của các loại task
# https://doi.org/10.1109/TMC.2020.2994232
# https://doi.org/10.1109/ACCESS.2023.3252575

REQUIRED_CPU_CYCLE = 400  
REQUIRED_GPU_FLOPS = [1000, 1500] # đơn vị là GFLOPS

#
MIN_S_IN = 400 # KB
MAX_S_IN = 500
MIN_S_OUT = 1.5 # KB
MAX_S_OUT = 2

#
DEADLINE = [1.5, 2]


