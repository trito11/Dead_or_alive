'''
Vai trò môi trg

Tạo môi trường
init():
    liệt kê các thứ cần khởi tạo
    các biến: seed, trọng số giữa thời gian trễ và drop
    dữ liệu của các xe bus
    observation():list có độ dài phụ thuộc vào số xe, mỗi observation tương ứng với 1 state ứng với mỗi khi một tác vụ được tạo ra
    time tác vụ được tạo, lượng tài nguyên máy tính cần thiết, dung lượng bộ nhớ tiêu thụ,deadline tác vụ, khoảng cách task đến xe 1, hàng chờ trên xe 1,...khoảng cách task đến xe n, hàng chờ trên xe n

    task_list(): Một queue để chứa các task, lấy dữ liệu từ file create data, đưa dữ liệu vào queue, mỗi lẫn lấy ra 1 task để cho mô hình xử lý, khi queue trống tức các task đã dc xử lý thì done=True

    tạo file chứa:tổng reward, số tác vụ drop, thời gian trễ,  


reset()=>state đầu tiên ứng với tác vụ đầu của episode
    !!!Chú ý: các hàng chờ vẫn tiếp tục từ cái cũ tại thời gian bọn nó liên tiếp nhau 
replay(): 
    Reset lại môi trg, đưa lại về episode 0
    !!!Chú ý các hàng chờ phải làm mới

step(action)=>next_state, reward, done:
    nhận một hành động, tính toán ứng với hành động ấy thì tác vụ xử lý trong bao lâu 
    lấy task tiếp theo từ task_list đưa vào next_state, cập nhật lại state mới, kiểm tra done
    Đưa ra thời gian trễ, reward, next_state, done
    !!! Chú ý cập nhật tất cả các hàng chờ, trừ đi khoảng thời giữa 2 state
task_distance(xe_thu_i,tac_vu_j,thoi_gian_k)=>Khoang cách của task j đến xe i tại thời gian k
    Tính khoảng cách theo tọa độ, tọa độ xe xác định tại thời gian gần với k nhất 
  
'''


