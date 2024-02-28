'''
Các hàm tính toán 

khoảng các giữa 2 tọa độ(long1,lat1,long2,lat2) => distance

Tốc độ truyền(channel_banwidth, pr, distance, path_loss_exponent, sigmasquare) => time
'''

from math import radians, cos, sin, asin, sqrt
import numpy as np
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula 
    dlat = lat2 - lat1
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    # Convert kilometers to meters
    m = km * 1000
    return m

'''
Toc do truyen ko day
'''
def getRateTransData(channel_banwidth, pr, distance, path_loss_exponent, sigmasquare):
    return (channel_banwidth * np.log2(
            1 + pr / np.power(distance,path_loss_exponent) / sigmasquare
        )
    ) 

# Hàm chuyển đổi thời gian dạng chuỗi thành giây
def time_to_seconds(time_str):
    parts = time_str.split(':')
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

def calculate_intermediate_coordinate(lat1, lng1, lat2, lng2, n):
    # Tính tọa độ của xe tại thời điểm x theo tỷ lệ n
    lat = lat1 + n * (lat2 - lat1)
    lng = lng1 + n * (lng2 - lng1)
    return lat, lng

