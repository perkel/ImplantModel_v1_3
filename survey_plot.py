## survey plot
import os
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from common_params import *
# For each directory in the INV_OUTPUT directory, read the summary fit stats
fname = 'summary_inverse_fit_results.csv'
i_o = 'INV_OUTPUT/'

std_vals = np.array([0.5, 0.2, 0.1], dtype=float)
targ_vals = np.array([1, 2, 5, 10, 25, 50, 100, 200, 500, 1000], dtype=float)

# set up main arrays
errs = np.zeros((3, 10))

#  loop on directories
for entry in os.scandir(i_o):
    if not entry.name.startswith('.') and entry.is_dir():
        # print('Entry name is: ',  entry.name)

        # parse params from dirname
        this_r = entry.name.split('_')[4]
        this_r_val = int(this_r[1:])
        this_std_val = float(entry.name.split('_')[6])
        this_targ_val = float(entry.name.split('_')[8])
        print('val is: ', this_r_val, ' std: ', this_std_val, ' and targ: ', this_targ_val)

        # set up local arrays
        subj = []
        mp_thr_err = []
        tp_thr_err = []
        pos_err = []

        with open(i_o + entry.name + '/' + fname, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for idx, row in enumerate(spamreader):
                if idx > 3:
                    subj.append(row[0])
                    mp_thr_err.append(float(row[1]))
                    tp_thr_err.append(float(row[2]))
                    pos_err.append(float(row[3]))

        # convert list to nparray
        temp1 = np.array(mp_thr_err)
        temp2 = np.array(tp_thr_err)
        avg_thr_err = np.add(temp1, temp2)/2.0
        print('done with gathering data')

        std_idx = np.argwhere(std_vals == this_std_val)
        targ_idx = np.argwhere(targ_vals == this_targ_val)
        errs[std_idx, targ_idx] = np.mean(avg_thr_err)

# Finished looping
print(errs)


ax = sns.heatmap(errs, linewidth=0.5, cmap='plasma')

# plt.imshow(errs)
plt.show()



