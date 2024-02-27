'''
Các hàm tính toán 

khoảng các giữa 2 tọa độ(long1,lat1,long2,lat2)=>distance

Tốc độ truyền(channel_banwidth, pr, distance, path_loss_exponent, sigmasquare)=>time
'''

from math import radians, cos, sin, asin, sqrt
import numpy as np
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

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