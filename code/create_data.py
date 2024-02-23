'''
Chứa các hàm sinh data:người dùng, tác vụ

create_task(số task, thời gian 1 episode, số episode)=>Tạo một thư mục (n task) chứa các file là các tác vụ ứng với từng episode 
        Các tác vụ bao gồm: \(t_i,lat_i,long_i,r_i,m_i, s_(i,out), s_(i,in), d_i)
            t_i là thời điểm khi tác vụ được tạo ra
            lat_i,long_i  là kinh độ và vĩ độ của vị trí tác vụ
            r_i là lượng tài nguyên máy tính cần thiết để sử lý tác vụ
            m_i là dung lượng bộ nhớ tiêu thụ
            s_(i,in) và s_(i,out) là kích thước dữ liệu đầu vào và đầu ra
            d_i là thời gian tác vụ cần được sử lý
            !!!Chú ý mỗi episode dài 30s(thay đổi sau dc), episode sau là bắt đầu từ kết thúc episode trc: episode 1:0->30, eps2:30-60,eps3:60-90


create_location_task()=> tọa độ của 1 người dùng trong hình lục giác

create_location_task_after(long,lat,time)=>new long, lat
    Tạo vị trí mới của người dùng sau x time từ vị trí ban đầu, xác định vị trí để gửi trả kết quả sau x time xử lý 
    Tọa độ dịch chuyển theo 1 vector: hướng bất kỳ, độ dài=vận tốc*time, vận tốc ngẫu nhiên(0-40km/h) 
'''

from config import *

def create_task(num_tasks = NUM_TASKS_PER_TIME_SLOT, time_each_episode = TIME_EACH_EPISODE, num = NUM_EPISODE):
    pass


