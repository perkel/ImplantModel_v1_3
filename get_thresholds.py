# get_thresholds.py version of 25 October 2023
# Original code by Steven Bierer
# Translated to python by David J. Perkel

import numpy as np
import thr_function as thr_f
import cylinder3d_makeprofile as c3dm


# The function that is used by the optimization algorithm
def objectivefunc(x, e_field, sim_params):
    target = sim_params['neurons']['thrtarg']  # threshold # neurons
    tv1 = thr_f.thr_function(x, e_field, sim_params)[0]  # returns nCount, NeuralProfile, ActiveProfile
    retval = (tv1 - target) ** 2
    # print('stim (dB): ', 20*np.log10(x), ' ; # neurons activated: ', tv1)
    return retval


# Constants
fit_precision = 0.01


def get_thresholds(field_table, field_params, sim_params):
    # function that is called by both forward and inverse models
    # Preallocate the arrays needed
    nz = len(sim_params['grid']['z'])
    if isinstance(sim_params['electrodes']['rpos'], list):
        nelec = len(sim_params['electrodes']['rpos'])
    elif not isinstance(sim_params['electrodes']['rpos'], np.ndarray):  # special case for 2D version of fwd model
        nelec = 1
    else:  # regular situation when called from forward or inverse model
        nelec = len(sim_params['electrodes']['rpos'])
    thresholds = np.empty(nelec)  # Array to hold threshold data for different stim electrodes and varied sigma values
    thresholds[:] = np.nan
    e_field = np.empty(nz)
    e_field[:] = np.nan

    if nelec == 1:
        elec_vals = range(7, 8)  # use electrode 7 to be in middle of cochlear length
        # set the position manually in the center of the array
        espace = sim_params['electrodes']['zpos'][elec_vals[0]] - sim_params['electrodes']['zpos'][elec_vals[0] - 1]
        neuron_midpoint = np.max(sim_params['grid']['z'])/2.0
        sim_params['electrodes']['zpos'][elec_vals[0]] = neuron_midpoint
        sim_params['electrodes']['zpos'][elec_vals[0]-1] = neuron_midpoint - espace
        sim_params['electrodes']['zpos'][elec_vals[0]+1] = neuron_midpoint + espace
    else:
        if sim_params['channel']['sigma'] == 0.0:  # monopolar
            elec_vals = range(0, nelec)
        else:
            elec_vals = range(1, nelec - 1)  # Can't do tripolar stimulation at end electrodes

    nvalarray = []
    nvals = 0

    for j in elec_vals:  # Loop on stimulating electrodes
        sim_params['channel']['number'] = j
        aprofile = c3dm.cylinder3d_makeprofile(field_table, field_params, sim_params)
        # This is the biophysically correct behavior, to include sidelobes
        e_field = abs(aprofile)  # uV^2/mm^2

        # We can remove sidelobes by setting negative values to zero
        # for kk in range(len(aprofile):
        #     if aprofile[kk] < 0.0:
        #         efield[kk] = 0.0
        #     else:
        #         efield[kk] = aprofile[kk]
        # e_field = aprofile
        # e_field[np.where(aprofile < 0.0)] = 0.0

        # for kk in range(len(e_field)):
        #     if aprofile[kk] < 0.0:
        #         e_field[kk] = 0.0
        #     else:
        #         e_field[kk] = aprofile[kk]

        # Use our own solving algorithm; this is clumsy but I couldn't find a solver in scipy.optimize that took
        # advantage of the known monotonicity of the function
        error = 20  # Ensure that the system starts with a large "error"
        target = sim_params['neurons']['thrtarg']
        nextstim = sim_params['channel']['current']
        lastpos = nextstim
        lastneg = 0.0
        while np.abs(error) > fit_precision:
            [n_neur, nvals, _aa] = thr_f.thr_function(nextstim, e_field, sim_params)
            # returns nCount, NeuralProfile, ActiveProfile
            error = n_neur - target
            if error < -fit_precision:  # want to increase stim
                if nextstim == sim_params['channel']['current']:
                    break
                lastneg = nextstim
                nextstim = nextstim + ((lastpos - nextstim)/2.0)
            elif error > fit_precision:  # decrease stimulus
                lastpos = nextstim
                nextstim = nextstim - ((nextstim - lastneg)/2.0)
        if nelec == 1:
            thresholds[0] = nextstim
        else:
            thresholds[j] = nextstim

        # Here call thrFunction to get the neural profile at threshold
        if len(thresholds) > 1:
            profileval = thr_f.thr_function(thresholds[j], e_field, sim_params)[1]
            nvalarray.append(profileval)

    thresholds = 20 * np.log10(thresholds)  # return thresholds in dB
    ncount = np.sum(np.asarray(nvals))
    if np.abs(ncount - sim_params['neurons']['thrtarg']) > 10:
        print("getThresholds returning ncount: ", ncount)
    if len(thresholds) == 1:
        return [thresholds, np.asarray(nvals)]
    else:
        return [thresholds, np.asarray(nvalarray)]
