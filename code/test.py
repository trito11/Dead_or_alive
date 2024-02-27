import numpy as np
import pandas as pd
import gym
from gym import spaces
from gym.utils import seeding
import copy
import os
from metric import *
from config import *

def preprocessBusLoction(excel_file):
    #địa chỉ bus
    a = pd.read_csv(os.path.join(DATA_BUS, excel_file))
    a = a.iloc[:500, [1, 4, 5]]
    a['time'] = a['time'].apply(time_to_seconds)
    min_time=a['time'].min()
    a['time']-=min_time
    return a.to_numpy()
file_path = 'd:\\Lab\\Lab_project\\Dead_or_alive\\data\\Bus_data\\xe_1.csv'
# D:\Lab\Lab_project\Dead_or_alive\data\Bus_data\xe_1
exists = os.path.exists('d:\\Lab\\Lab_project\\Dead_or_alive\\data/Bus_data\\xe_1')
print("File exists:", exists)
df=preprocessBusLoction('xe_1')
print(df[0:10])