import math
import random
import numpy as np

def legallxAndly():
    lx_up = 4
    lx_dn = 2
    lx_lim = (lx_up - (lx_dn))

    ly_up = 2
    ly_dn = -1
    ly_lim = (ly_up - (ly_dn))

    limit = 2
    randomlx = np.round(np.random.uniform(lx_dn, lx_up), 9)  # 創建一個落在lx範圍內的浮點數，取小數點後第九位
    randomly = np.round(np.random.uniform(ly_dn, ly_up), 9)
    if ((randomlx+randomly) < 2):
        legallxAndly()
    return randomlx,randomly

randomlx01,randomly01 = legallxAndly()
randomlx02,randomly02 = legallxAndly()
randomlx03,randomly03 = legallxAndly()
randomlx04,randomly04 = legallxAndly()



print(f"randomlx= {randomlx01}, randomly= {randomly01}")
print(f"randomlx= {randomlx02}, randomly= {randomly02}")
print(f"randomlx= {randomlx03}, randomly= {randomly03}")
print(f"randomlx= {randomlx04}, randomly= {randomly04}")
