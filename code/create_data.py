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

create_location_task_after(lat,lng,time)=>new lat, lng
    Tạo vị trí mới của người dùng sau x time từ vị trí ban đầu, xác định vị trí để gửi trả kết quả sau x time xử lý 
    Tọa độ dịch chuyển theo 1 vector: hướng bất kỳ, độ dài=vận tốc*time, vận tốc ngẫu nhiên(0-40km/h) 
'''

from config import *
import random
import pandas as pd
import math
import random
import h3
import numpy as np
import os
from pathlib import Path

path = os.path.abspath(__file__)
path = Path(path).parent.parent

def create_task(num_tasks = NUM_TASKS_PER_TIME_SLOT, time_each_episode = TIME_EACH_EPISODE, num = NUM_EPISODE, hexagon = None):
    try:
        os.makedirs(DATA_LOCATION) 
    except OSError as e:
        print(e)

    for i in range(NUM_EPISODE):
        with open("{}/{}/datatask{}.csv".format(str(path), DATA_LOCATION, i), "w") as output:
            columns = ['time', 'lat', 'long', 'require', 'dung_luong_bo_nho_yeu_cau', 'kich_thuoc_du_lieu_vao', 'kich_thuoc_du_lieu_ra', 'deadline']
            lat=[]
            lng=[]
            #30s mình sinh ra ngẫu nhiên x khe thời gian đang sinh theo phân phối uniform
            num_time=int(random.uniform(MIN_NUM_TIME,MAX_NUM_TIME))
            #Sinh thời gian ứng với x khe thời gian
            t = np.sort(np.random.randint(i*100*time_each_episode,(i+1)*100*time_each_episode,num_time)/100) #Thời gian các task xuất hiện
            #Sinh số lượng task theo phân phối poisson trong từng khe thời gian
            tasks_per_interval = np.random.poisson(num_tasks / num_time, num_time)

            total_generated_tasks = np.sum(tasks_per_interval)

            # Tính số lượng tác vụ thừa
            excess_tasks = total_generated_tasks - num_tasks

            # Phân bổ số lượng tác vụ thừa vào các khoảng thời gian trước đó
            if excess_tasks > 0:
                for i in range(num_time):
                    if excess_tasks == 0:
                        break
                    tasks_per_interval[i] -= 1
                    excess_tasks -= 1
            #Poisson process point
            # tạo tọa độ
            #Lặp cho từng khe thời gian thì lấy ngẫu nhiên 1 ô H3
            for time in range(num_time):
                num_task=tasks_per_interval[time]
                random_index=random.choice(NEIGHBOR_HEX)
                hex_boundary = h3.h3_to_geo_boundary(random_index) # array of arrays of [lat, lng]
                #Sinh tọa độ ngẫu nhiên trong ô h3 với từng task 
                for j in range(num_task):
                    point=create_point(hex_boundary)
                    lat.append(point.lat)
                    lng.append(point.lng)
            
            # lượng tài nguyên cần thiết - cấu hình trong trong file config
            r = random.uniform(REQUIRED_GPU_FLOPS[0], REQUIRED_GPU_FLOPS[1],NUM_TASKS_PER_TIME_SLOT)

            # 
            m =random.uniform() # bộ nhớ tiêu thụ - cấu hình trong file config

            #
            s_in = random.uniform(MIN_S_IN, MAX_S_IN,NUM_TASKS_PER_TIME_SLOT)
            s_out = random.uniform(MIN_S_OUT, MAX_S_OUT)

            # deadline
            d = random.uniform(DEADLINE[0], DEADLINE[1],NUM_TASKS_PER_TIME_SLOT)

            # Thêm một hàng vào DataFrame
            df.loc[len(df)] = [time, lat, long, r, m, s_in, s_out, d]


            # lưu dữ liệu theo file 
            csv_file_path = DATA_LOCATION + "file" + i
            df.to_csv(csv_file_path, index=False)


# Hàm dịch chuyển điểm theo một hướng ngẫu nhiên
def move_random(latitude, longitude, distance_meters):
    # Chọn một hướng ngẫu nhiên (0 - 359 độ)
    direction = random.uniform(0, 360)
    
    # Chuyển đổi khoảng cách từ mét sang độ
    # 1 độ kinh độ tại xích đạo tương ứng với khoảng cách khoảng 111,111 mét
    # Tại các vùng cực, giá trị này sẽ thay đổi
    distance_degrees = distance_meters / 111111
    
    # Tính toán dịch chuyển
    # Dịch chuyển theo hướng ngẫu nhiên
    new_latitude = latitude + (distance_degrees * math.cos(math.radians(direction)))
    new_longitude = longitude + (distance_degrees * math.sin(math.radians(direction)))
    
    return new_latitude, new_longitude


def create_location_task_after(lat,lng,time):
    speed = random.uniform(0,3)
    index=h3.geo_to_h3(lat,lng,HEX_LEVEL)
    while True:
        new_lat,new_lng=move_random(lat,lng,speed*time)
        new_index=h3.geo_to_h3(new_lat,new_lng,HEX_LEVEL)
        if new_index==index:
            return new_lat,new_lng

if __name__ == '__main__':
    