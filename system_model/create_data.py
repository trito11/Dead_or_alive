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
from hexagon import create_point

path = os.path.abspath(__file__)
path = Path(path).parent.parent

def get_random(arr, so_lan_lay):
    # Tạo một mảng chứa chỉ số của các phần tử trong mảng arr
    indices = list(range(len(arr)))
    # Mảng kết quả
    result = []
    
    for _ in range(so_lan_lay):
        # Chọn ngẫu nhiên một chỉ số từ mảng indices
        index = random.choice(indices)
        # Lấy phần tử tương ứng và thêm vào mảng kết quả
        result.append(arr[index])
        # Xóa chỉ số đã chọn khỏi mảng indices để tránh lấy lại
        del indices[index]
    
    return result

def create_task(num_tasks = NUM_TASKS_PER_TIME_SLOT, time_each_episode = TIME_EACH_EPISODE, num = NUM_EPISODE):
    data_location = "{}/{}".format(str(path), DATA_LOCATION)
    if not os.path.exists(data_location):
        os.makedirs(data_location)

    for i in range(NUM_EPISODE):
        with open("{}/{}/datatask{}.csv".format(str(path), DATA_LOCATION, i), "w") as output:
            columns = ['time', 'lat', 'long', 'require', 'dung_luong_bo_nho_yeu_cau', 'kich_thuoc_du_lieu_vao', 'kich_thuoc_du_lieu_ra', 'deadline']
            latitude=[]
            longtitude=[]
            lat=[]
            lng=[]
            #30s mình sinh ra ngẫu nhiên x khe thời gian đang sinh theo phân phối uniform
            num_time=int(random.uniform(MIN_NUM_TIME,MAX_NUM_TIME))
            #Sinh thời gian ứng với x khe thời gian
            t = np.sort(np.random.randint(i*100*time_each_episode,(i+1)*100*time_each_episode,num_time)/100) #Thời gian các task xuất hiện
            time=[]
            #Sinh số lượng task theo phân phối poisson trong từng ô h3
            location_per_interval = np.random.poisson(LAMDA, 10)
            tasks_per_interval = np.random.poisson(num_tasks/num_time, num_time)

            total_generated_tasks = np.sum(tasks_per_interval)

            # Tính số lượng tác vụ thừa
            excess_tasks = total_generated_tasks - NUM_TASKS_PER_TIME_SLOT

            # Phân bổ số lượng tác vụ thừa vào các khoảng thời gian trước đó
            if excess_tasks > 0:
                for i in range(num_time):
                    if excess_tasks == 0:
                        break
                    tasks_per_interval[i] -= 1
                    excess_tasks -= 1
            if excess_tasks < 0:
                for i in range(num_time):
                    if excess_tasks == 0:
                        break
                    tasks_per_interval[i] += 1
                    excess_tasks += 1
            #Poisson process point
            # tạo tọa độ
            k=0
            for index in NEIGHBOR_HEX:
                num_location=location_per_interval[k]
                hex_boundary = h3.h3_to_geo_boundary(index) # array of arrays of [lat, lng]
                #Sinh tọa độ ngẫu nhiên trong ô h3 với từng task 
                for j in range(num_location):
                    point=create_point(hex_boundary)
                    latitude.append(point.lat)
                    longtitude.append(point.lng)
                k+=1
            a=len(latitude)
            for i in range(num_time):
                num_task=tasks_per_interval[i]
                for j in range (num_task):
                    time.append(t[i])
                    b=random.randint(0,a-1)
                    lat.append(latitude[b])
                    lng.append(longtitude[b])


            # print(len(lat))
            print(sum(tasks_per_interval))
            print(len(time))
            # lượng tài nguyên cần thiết - cấu hình trong trong file config
            r = np.random.randint(REQUIRED_GPU_FLOPS[0], REQUIRED_GPU_FLOPS[1],NUM_TASKS_PER_TIME_SLOT)
            # 
            m =REQUIRED_GPU_RAM # bộ nhớ tiêu thụ - cấu hình trong file config

            #
            s_in = np.random.randint(MIN_S_IN, MAX_S_IN,NUM_TASKS_PER_TIME_SLOT)/1000 # p in Mb
            s_out = np.random.randint(MIN_S_OUT*10, MAX_S_OUT*10,NUM_TASKS_PER_TIME_SLOT)/10000 # p out Mb

            # deadline
            d = np.random.randint(DEADLINE[0]*100, DEADLINE[1]*100,NUM_TASKS_PER_TIME_SLOT)/100
            for j in range(num_tasks):
                output.write("{},{},{},{},{},{},{},{}\n".format(
                    time[j], lat[j], lng[j], r[j], m, s_in[j],s_out[j],d[j]))
                
        

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
    speed = random.uniform(0,2)
    index=h3.geo_to_h3(lat,lng,HEX_LEVEL)
    while True:
        new_lat,new_lng=move_random(lat,lng,speed*time)
        new_index=h3.geo_to_h3(new_lat,new_lng,HEX_LEVEL)
        if new_index==index:
            return new_lat,new_lng

if __name__ == '__main__':
    np.random.seed(SEED)
    random.seed(SEED)
    create_task()