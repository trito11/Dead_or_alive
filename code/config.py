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
NUM_VEHICLE=
NUM_ACTION = 
NUM_STATE=
NUM_TASKS_PER_TIME_SLOT = 

# Đường dẫn lưu trữ file
LINK_PROJECT = Path(os.path.abspath(__file__))
LINK_PROJECT = LINK_PROJECT.parent.parent
DATA_LOCATION = "data_task/data" + str(NUM_TASKS_PER_TIME_SLOT) + "/"
DATA_DIR = os.path.join(LINK_PROJECT, "data")
RESULT_DIR = os.path.join(LINK_PROJECT, "result/")
DATA_TASK = os.path.join(LINK_PROJECT, DATA_LOCATION)

# Tốc độ xử lý và yêu cầu tài nguyên của các loại task
COMPUTATIONAL_CAPACITY=
Required_Computing_Resources=



