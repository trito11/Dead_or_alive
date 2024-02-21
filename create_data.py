'''
Chứa các hàm sinh data:người dùng, tác vụ

create_task(số task, thời gian 1 episode, số episode)=>Tạo một thư mục(n task) chứa các file là các tác vụ ứng với từng episode 
        Các tác vụ bao gồm: time khởi tạo; tài nguyên tính toán; dung lượng bộ nhớ tiêu thụ; kích thức dữ liệu đầu vào, ra;deadline; kinh độ,vĩ độ của tác vụ
            !!!Chú ý mỗi episode dài 30s(thay đổi sau dc), episode sau là bắt đầu từ kết thúc episode trc: episode 1:0->30, eps2:30-60,eps3:60-90


create_location_task()=> tọa độ của 1 người dùng trong hình lục giác

create_location_task_after(long,lat,time)=>new long, lat
    Tạo vị trí mới của người dùng sau x time từ vị trí ban đầu, xác định vị trí để gửi trả kết quả sau x time xử lý 
    Tọa độ dịch chuyển theo 1 vector: hướng bất kỳ, độ dài=vận tốc*time, vận tốc ngẫu nhiên(0-40km/h) 
'''