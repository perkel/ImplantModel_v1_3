# script to cycle through a set of parameters to try to optimize fit results

import common_params as cp
import FwdModel4 as fwd
import FwdModel4_2D as fwd2D
import InverseModelCombined as inv_mod
import numpy as np
import csv
import os

# params to vary
# external resistivity, stdrel, number of active neurons, minimization approach
res_ext = 500.0  # should double check that this matches the field table being used
# specify some fixed params

# start by cycling through stdrel, 3 of active neurons
stdrel_vals = [1.0, 2.0, 4.0, 8.0]
thrtarg_vals = [50, 100, 200]
# stdrel_vals = [1.0, 2.0]
# thrtarg_vals = [50, 100]

n_std = len(stdrel_vals)
n_thr = len(thrtarg_vals)
mp_err_summ = np.zeros((n_std, n_thr))
tp_err_summ = np.zeros((n_std, n_thr))
dist_err_summ = np.zeros((n_std, n_thr))
dist_corr_sum = np.zeros((n_std, n_thr))
n_corr_sig = np.zeros((n_std, n_thr))


for stdrel in stdrel_vals:
    espace = 1.1
    for thrtarg in thrtarg_vals:
        # save file with key params
        param_file = 'surv_params.txt'
        tempdata = np.zeros(4)  # 4 values
        tempdata[0] = res_ext
        tempdata[1] = stdrel
        tempdata[2] = thrtarg
        tempdata[3] = espace
        with open(param_file, mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter=',')
            for i, row in enumerate(tempdata):
                data_writer.writerow([tempdata[i]])
        data_file.close()

        # Run FwdModel
        fwd.fwd_model_4()
        # Run FwdModel2D for espace = 1.1 mm
        espace = 1.1
        # save file with key params
        param_file = 'surv_params.txt'
        tempdata = np.zeros(4)  # 4 values
        tempdata[0] = res_ext
        tempdata[1] = stdrel
        tempdata[2] = thrtarg
        tempdata[3] = espace
        with open(param_file, mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter=',')
            for i, row in enumerate(tempdata):
                data_writer.writerow([tempdata[i]])
        data_file.close()
        fwd2D.fwd_model_2D()
        # Prepare to run FwdModel2D for espace = 0.85 mm

        espace = 0.85
            # save file with key params
        param_file = 'surv_params.txt'
        tempdata = np.zeros(4)  # 3 values
        tempdata[0] = res_ext
        tempdata[1] = stdrel
        tempdata[2] = thrtarg
        tempdata[3] = espace
        with open(param_file, mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter=',')
            for i, row in enumerate(tempdata):
                data_writer.writerow([tempdata[i]])
        data_file.close()
        fwd2D.fwd_model_2D()

        # Set espace back to 1.1 in surv_params.txt
        espace = 0.85
        # save file with key params
        param_file = 'surv_params.txt'
        tempdata = np.zeros(4)  # 3 values
        tempdata[0] = res_ext
        tempdata[1] = stdrel
        tempdata[2] = thrtarg
        tempdata[3] = espace
        with open(param_file, mode='w') as data_file:
            data_writer = csv.writer(data_file, delimiter=',')
            for i, row in enumerate(tempdata):
                data_writer.writerow([tempdata[i]])
        data_file.close()

        # Run inverse model
        inv_mod.inverse_model_combined()
        print('back from inverse model')

        # Collect and collate results stats ( do this in a separate script)

## text from trial
        # TST_OUT_DIR = 'TSTOUT/'
        # if not os.path.exists(TST_OUT_DIR):
        #     os.mkdir(TST_OUT_DIR)
        # dir_base = 'TEST_DIR_NAME/'
        # orig_dir = TST_OUT_DIR + dir_base
        # # Run inverse model
        # os.mkdir(orig_dir)
        #
        # # Rename fwd and inverse output directories
        # new_dir_suffix = '_R%d' % res_ext + '_' + 'std_%.1f' % stdrel + '_thr_%d' % thrtarg
        # new_fwd_dir = orig_dir[0:-1] + new_dir_suffix
        # os.rename(orig_dir, new_fwd_dir)
###

        # Rename fwd and inverse output directories
        new_dir_suffix = '_R%d' % res_ext + '_' + 'std_%.1f' % stdrel + '_thr_%d' % thrtarg
        #offset = len(cp.FWD_OUT_PRFIX)
        new_fwd_dir = cp.FWDOUTPUTDIR[:-1] + new_dir_suffix
        os.rename(cp.FWDOUTPUTDIR, new_fwd_dir)
        #offset = len(cp.INV_OUT_PRFIX)
        new_inv_dir = cp.INVOUTPUTDIR[:-1] + new_dir_suffix
        os.rename(cp.INVOUTPUTDIR, new_inv_dir)


# Run a separate script to calculate mean & std for each subject across parameters
# Want to find out best paramwter combination, and also how robust each subject fit is
# to changes in parameter sets