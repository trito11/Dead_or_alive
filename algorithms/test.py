import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import count
import sys
import os
from pathlib import Path
link=Path(os.path.abspath(__file__))
link=link.parent.parent
link=os.path.join(link, "system_model")
sys.path.append(link)
import environment as env
from config import *
import torch
import random
from metric import *

def load_bus_data( num_files=14):
        data_list = {}
        for i in range(1, num_files + 1):
            filename = f"xe_{i}"
            data_list[filename]=preprocessBusLocation(filename)
        return data_list

    #Lấy dữ liệu xe bus từ file csv trừ đi thời gian min để tất cả bắt đầu từ 0, đưa thời gian về s
def preprocessBusLocation( excel_file):
        #địa chỉ bus
        a = pd.read_csv(os.path.join(DATA_BUS, excel_file))
        value=a.iloc[0,0]
        a=a[a.iloc[:, 0] == value].copy()
        a['hex'] = a.apply(lambda x: h3.geo_to_h3(x.latitude,x.longitude,7),1)
        a = a[a['hex'].isin(NEIGHBOR_HEX)]
        a = a.iloc[30:500, [1, 4, 5]]
        a=a.reset_index(drop=True)
        a['time'] = a['time'].apply(time_to_seconds)
        min_time=a['time'][0]
        a['time']-=min_time
        return a.to_numpy()
x=preprocessBusLocation("xe_22")
print(x)