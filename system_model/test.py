import numpy as np
import pandas as pd
import gym
from gym import spaces
from gym.utils import seeding
import copy
import os
from metric import *
from config import *
from create_data import create_location_task_after



def load_bus_data( num_files=60):
        data_list = {}
        for i in range(1, num_files + 1):
            filename = f"xe_{i}"
            data_list[filename]=preprocessBusLocation(filename)
        return data_list

def preprocessBusLocation( excel_file):
    #địa chỉ bus
    a = pd.read_csv(os.path.join(DATA_BUS, excel_file))
    a['hex'] = a.apply(lambda x: h3.geo_to_h3(x.latitude,x.longitude,7),1)
    a = a.iloc[:500, [1, 4, 5]]
    a['time'] = a['time'].apply(time_to_seconds)
    min_time=a['time'].min()
    a['time']-=min_time
    return a.to_numpy()

def readcsv( number_bus, time):
    #đọc excel tính lat,lng của xe bus tại t=time
    data_bus=load_bus_data()
    data = data_bus[number_bus]

    after_time = data[data[:, 0] >= time]
    pre_time = data[data[:, 0] <= time]
    if len(after_time) == 0:
        return 1.8,1.8
    las = after_time[0]
    first = pre_time[-1]
    diff1=las[0]-first[0]
    diff2=time-first[0]
    # weighted average of the distance
    lat,lng=calculate_intermediate_coordinate(first[1],first[2],las[1],las[2],diff2/diff1)
    return lat, lng

# data_bus=preprocessBusLocation('xe_1')
a = pd.read_csv(os.path.join(DATA_BUS, 'xe_1'))
a['hex'] = a.apply(lambda x: h3.geo_to_h3(x.latitude,x.longitude,7),1)
a = a[a['hex'].isin(NEIGHBOR_HEX)]
print(a)