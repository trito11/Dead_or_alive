'''
Chứa các hàm sinh data:người dùng, tác vụ

create_task(số task, thời gian 1 episode, số episode, hexagon đã chọn) => Tạo một thư mục (n task) chứa các file là các tác vụ ứng với từng episode 
        Các tác vụ bao gồm: (t_i,lat_i,long_i,r_i,m_i, s_(i,out), s_(i,in), d_i)
            t_i là thời điểm khi tác vụ được tạo ra
            lat_i,long_i  là kinh độ và vĩ độ của vị trí tác vụ
            r_i là lượng tài nguyên máy tính cần thiết để sử lý tác vụ
            m_i là dung lượng bộ nhớ tiêu thụ
            s_(i,in) và s_(i,out) là kích thước dữ liệu đầu vào và đầu ra
            d_i là thời gian tác vụ cần được sử lý
            !!!Chú ý mỗi episode dài 30s(thay đổi sau dc), episode sau là bắt đầu từ kết thúc episode trc: episode 1:0->30, eps2:30-60,eps3:60-90

create_location_task_after(long,lat,time)=>new long, lat
    Tạo vị trí mới của người dùng sau x time từ vị trí ban đầu, xác định vị trí để gửi trả kết quả sau x time xử lý 
    Tọa độ dịch chuyển theo 1 vector: hướng bất kỳ, độ dài=vận tốc*time, vận tốc ngẫu nhiên(0-40km/h) 
'''

from config import *
import random
import pandas as pd

def create_task(num_tasks = NUM_TASKS_PER_TIME_SLOT, time_each_episode = TIME_EACH_EPISODE, num = NUM_EPISODE, hexagon = None):
    for i in range(NUM_EPISODE):
        columns = ['time', 'lat', 'long', 'require', 'dung_luong_bo_nho_yeu_cau', 'kich_thuoc_du_lieu_vao', 'kich_thuoc_du_lieu_ra', 'deadline']
        df = pd.DataFrame(columns=columns)

        for j in range(NUM_TASKS_PER_TIME_SLOT):
            # tạo dữ liệu 
            time = random.uniform(0, time_each_episode)

            # tạo tọa độ


            # lượng tài nguyên cần thiết - cấu hình trong trong file config
            r = random.choice(Required_Computing_Resources)

            # 
            m = # bộ nhớ tiêu thụ - cấu hình trong file config

            #
            s_in = random.uniform(MIN_S_IN, MAX_S_IN)
            s_out = random.uniform(MIN_S_OUT, MAX_S_OUT)

            # deadline
            d = 

            # Thêm một hàng vào DataFrame
            df.loc[len(df)] = [time, lat, long, r, m, s_in, s_out, d]


        # lưu dữ liệu theo file 
        csv_file_path = DATA_LOCATION + "file" + i
        df.to_csv(csv_file_path, index=False)


