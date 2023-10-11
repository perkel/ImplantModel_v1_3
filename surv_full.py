# A commonly called function to get full grid of survival values from
# vector of nElec survival values
import numpy as np


def surv_full(e_pos, surv_vec, grid_pos):
    """

    :rtype: object
    """
    # e_pos is an array of electrode positions, in mm
    # surv_vec is an array of neuron survival values at those electrode
    # positions
    # grid_pos is the entire array of grid positions, typically 0:0.1:32.9

    # This function returns values interpolated within the range of the
    # electrode positions and extrapolated beyond the first and last positions
    # in a horizontal manner.

    # Special condition for ForwardModel4_2D
    if not isinstance(e_pos, list):
        elec_basalpos = 30
        espace = 1.1  # in mm; 'ELECTRODE' parameters must be vectors
        e_pos = elec_basalpos - np.arange(16 - 1, -1, -1) * espace

        # also process survival value
        surv_scalar = surv_vec
        tempsurv_vec = np.ones(16) * surv_scalar
        surv_vec = tempsurv_vec

    nz = len(grid_pos)

    idxa = np.argmin(np.abs(grid_pos - e_pos[0]))
    idxb = np.argmin(np.abs(grid_pos - e_pos[-1]))

    surv_vals = np.empty(nz)
    surv_vals[:] = np.nan
    nsurvtemp = np.interp(grid_pos[idxa:idxb], e_pos, surv_vec)
    surv_vals[0:idxa] = nsurvtemp[0]
    surv_vals[idxa:idxb] = nsurvtemp
    surv_vals[idxb:] = nsurvtemp[-1]

    return surv_vals
