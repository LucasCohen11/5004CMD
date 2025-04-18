from q1a import *
from q1b import *
from q1c import *
from q1d import *
from q1e import *
from tester import compareImplementations as compare
import pandas as pd
import matplotlib.pyplot as plt

sequential_implementations =(q1a_sequential,q1b_sequential,q1c_sequential,q1d_sequential,q1e_sequential)
Dask_implementations =(q1a_Dask,q1b_Dask,q1c_Dask,q1d_Dask,q1e_Dask)


rows = []
for index,(seq,dask) in enumerate(zip(sequential_implementations,Dask_implementations)):
    timings = compare(seq,dask)
    new_row = {
            'Task':chr(65+index),
            'Sequential Runtime':timings[0],
            'Dask Runtime':timings[1]
        }
    rows.append(new_row)

results = pd.DataFrame(rows)


print(results)


ax = results.plot(kind='bar', x='Task')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

