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
DATA_LOCATION = "data_task/data" + str(NUM_TASKS_PER_TIME_SLOT) + "/"
DATA_DIR = os.path.join(LINK_PROJECT, "data")
RESULT_DIR = os.path.join(LINK_PROJECT, "result/")
DATA_TASK = os.path.join(LINK_PROJECT, DATA_LOCATION)

# Tốc độ xử lý và yêu cầu tài nguyên của các loại task
COMPUTATIONAL_CAPACITY = 1
Required_Computing_Resources = 1



