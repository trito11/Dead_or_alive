import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pathlib import Path
from itertools import count
import sys
import os
from pathlib import Path
link=Path(os.path.abspath(__file__))
link=link.parent.parent
links=os.path.join(link, "system_model")
sys.path.append(links)



# D:\Lab\Lab_project\Dead_or_alive\result\test\loss_files.csv
with open(f"{link}/result/test/loss_files.csv", "r") as file:
    result = pd.read_csv(file)
minrange = 0
maxrange = -1
result_info = result[minrange:maxrange]
plt.plot(result_info, label = f"loss")


        # plt.ylim(-0.05, -0)
plt.title( f'Biểu đồ loss  ')
plt.legend(loc='upper right',bbox_to_anchor=(1.7, 1), ncol=1, fancybox=True)
# plt.savefig(f"{LINK_PROJECT}/fig/{which_algorithm}/env_2_4/5vehicle/{NUMS_TASK}task/num_iters{iters}/eps{eps}/Biểu đồ TOLERANCE_TIME với giá trị trung bình trong pha Test-{which_algorithm}-reward_drop:{reward_drop}.png")
plt.show()