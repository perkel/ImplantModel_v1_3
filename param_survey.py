# script to cycle through a set of parameters to try to optimize fit results

import common_params as cp
import FwdModel4 as fwd
import FwdModel4_2D as fwd2D
import InverseModelCombined as inv_mod
import numpy as np
from shutil import move, copymode
import os


# params to vary
# external resistivity, stdrel, number of active neurons, minimization approach
res_ext = 250.0  # should double check that this matches the field table being used
# specify some fixed params

# start by cycling through stdrel, 3 of active neurons
# stdrel_vals = [1.0, 2.0, 4.0, 8.0]
# thrtarg_vals = [50, 100, 200]
stdrel_vals = [1.0, 2.0]
thrtarg_vals = [50, 100]

n_std = len(stdrel_vals)
n_thr = len(thrtarg_vals)
mp_err_summ = np.zeros((n_std, n_thr))
tp_err_summ = np.zeros((n_std, n_thr))
dist_err_summ = np.zeros((n_std, n_thr))
dist_corr_sum = np.zeros((n_std, n_thr))
n_corr_sig = np.zeros((n_std, n_thr))


for stdrel in stdrel_vals:
    for thrtarg in thrtarg_vals:
        # Do something. Make a new common params file
        # Read common_params.py
        fd = os.open('common_params2.py', os.O_RDWR | os.O_CREAT)
        with os.fdopen(fd, 'w') as new_file:
            with open('common_params.py') as old_file:
                for line in old_file:
                    if line.startswith('ACT_STDREL'):
                        valtext = '%.1f' % stdrel
                        new_file.write('ACT_STDREL = ' + valtext + '\n')
                    elif line.startswith('THRTARG'):
                        valtext = '%.1f' % thrtarg
                        new_file.write('THRTARG = ' + valtext + '\n')
                    else:
                        new_file.write(line)
        # Copy the file permissions from the old file to the new file
        copymode('common_params.py', 'common_params2.py')
        # Remove original file
        os.remove('common_params.py')
        # Move new file
        move('common_params2.py', 'common_params.py')

        # Run FwdModel
        fwd.fwd_model_4()
        # Run FwdModel2D for espace = 1.1 mm
        fwd2D.fwd_model_2D()
        # Prepare to run FwdModel2D for espace = 0.85 mm
        # Read common_params.py
        fd = os.open('common_params2.py', os.O_RDWR | os.O_CREAT)
        with os.fdopen(fd, 'w') as new_file:
            with open('common_params.py') as old_file:
                for line in old_file:
                    if line.startswith('espace'):
                        new_file.write('espace = 0.85\n')
                    else:
                        new_file.write(line)
        # Copy the file permissions from the old file to the new file
        copymode('common_params.py', 'common_params2.py')
        # Remove original file
        os.remove('common_params.py')
        # Move new file
        move('common_params2.py', 'common_params.py')

        # common_params should now have espace = 0.85
        fwd2D.fwd_model_2D()

        # Set espace back to 1.1 in common_params
        # Read common_params.py
        fd = os.open('common_params2.py', os.O_RDWR | os.O_CREAT)
        with os.fdopen(fd, 'w') as new_file:
            with open('common_params.py') as old_file:
                for line in old_file:
                    if line.startswith('espace'):
                        new_file.write('espace = 1.1\n')
                    else:
                        new_file.write(line)
        # Copy the file permissions from the old file to the new file
        copymode('common_params.py', 'common_params2.py')
        # Remove original file
        os.remove('common_params.py')
        # Move new file
        move('common_params2.py', 'common_params.py')

        # Run inverse model
        inv_mod.inverse_model_combined()

        # Collect and collate results stats ( do this in a separate script)


        # Rename fwd and inverse output directories
        new_dir_suffix = '_R%d' % res_ext + '_' + 'std_%.1f' % stdrel + '_thr_%d' % thrtarg
        new_fwd_dir = cp.FWDOUTPUTDIR[0:-1] + new_dir_suffix
        os.rename(cp.FWDOUTPUTDIR, new_fwd_dir)
        new_inv_dir = cp.INVOUTPUTDIR[0:-1] + new_dir_suffix
        os.rename(cp.INVOUTPUTDIR, new_inv_dir)


# Run a separate script to calculate mean & std for each subject across parameters
# Want to find out best paramwter combination, and also how robust each subject fit is
# to changes in parameter sets