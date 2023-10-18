# set_scenario returns a vector of survival values and a vector of radial positions
import numpy as np


def set_scenario(this_scen, n_elec):
    surv_vals = np.zeros(n_elec)
    rpos_vals = np.zeros(n_elec)
    # If uniform, then calculate values, otherwise use switch and specify manually
    if this_scen[0:7] == 'Uniform':
        # parse scenario name
        surv_vals = np.ones(n_elec) * int(this_scen[7:9]) * 0.01
        # Find 'R'
        the_idx = this_scen.find('R')
        rpos_vals = np.zeros(n_elec) + int(this_scen[the_idx + 1:]) * 0.01
    else:
        if this_scen == 'Gradual80R00':
            surv_vals = [0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'Gradual2_80R00':
            surv_vals = [0.8, 0.8, 0.8, 0.8, 0.7, 0.6, 0.5, 0.4, 0.4, 0.5, 0.6, 0.7, 0.8, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'Gradual80R75':
            surv_vals = [0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec) + 0.75
        elif this_scen == 'Gradual80R-50':
            surv_vals = [0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec) - 0.5
        elif this_scen == 'Gradual50R00':
            surv_vals = [0.5, 0.5, 0.35, 0.2, 0.2, 0.35, 0.5, 0.5, 0.5, 0.35, 0.2, 0.2, 0.35, 0.5, 0.5, 0.5]
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'Sudden80R-05':
            surv_vals = [0.8, 0.8, 0.8, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec) - 0.5
        elif this_scen == 'Sudden80R00':
            surv_vals = [0.8, 0.8, 0.8, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'Sudden80R05':
            surv_vals = [0.8, 0.8, 0.8, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8, 0.8, 0.4, 0.4, 0.8, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec) + 0.5
        elif this_scen == 'Uniform80R05':
            surv_vals = 0.8 * np.ones(n_elec)
            rpos_vals = np.zeros(1, n_elec) + 0.5
        elif this_scen == 'Uniform40R00':
            surv_vals = 0.4 * np.ones(n_elec)
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'Step40_80R00':
            surv_vals = 0.4 * np.ones(n_elec)
            surv_vals[7:] = 0.8
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'RampRposRampSurv':
            surv_vals = np.arange(0.25, 0.73, 0.03)
            rpos_vals = np.arange(-0.8, 0.75, 0.1)
        elif this_scen == 'Ramp80Rvariable1':
            surv_vals = 0.8 * np.ones(n_elec)
            rpos_vals = np.arange(-0.8, 0.75, 0.1)
        elif this_scen == 'Ramp80Rvariable2':
            surv_vals = 0.8 * np.ones(n_elec)
            rpos_vals = np.arange(-0.6, 0.95, 0.1)
        elif this_scen == 'RampSurvR00':
            surv_vals = np.arange(0.1, 0.86, 0.05)
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'RampSurvR03':
            surv_vals = np.arange(0.2, 0.65, 0.03)
            rpos_vals = np.zeros(n_elec) + 0.3
        elif this_scen == 'RampSurvR07':
            surv_vals = np.arange(0.1, 0.86, 0.05)
            rpos_vals = np.zeros(n_elec) + 0.7
        elif this_scen == 'RampRposS20':
            surv_vals = 0.2 * np.ones(n_elec)
            rpos_vals = np.arange(0.8, -0.8, -0.1)
        elif this_scen == 'RampRposS80':
            surv_vals = 0.8 * np.ones(n_elec)
            rpos_vals = np.arange(0.8, -0.8, -0.1)
        elif this_scen == 'RampRposS50':
            surv_vals = 0.5 * np.ones(n_elec)
            rpos_vals = np.arange(0.8, -0.8, -0.1)
        elif this_scen == 'RampRposS70':
            surv_vals = 0.7 * np.ones(n_elec)
            rpos_vals = np.arange(0.8, -0.8, -0.1)
        elif this_scen == 'RampRposS75':
            surv_vals = 0.75 * np.ones(n_elec)
            rpos_vals = np.arange(0.8, -0.8, -0.1)
        elif this_scen == 'RampRposS100':
            surv_vals = np.ones(n_elec)
            rpos_vals = np.arange(0.8, -0.8, -0.1)
        elif this_scen == 'RampRposSGradual80':
            rpos_vals = np.arange(0.8, -0.8, -0.1)
            surv_vals = [0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8]
        elif this_scen == 'RampRpos2SGradual80':
            rpos_vals = np.arange(0.6, -0.65, -0.08)
            surv_vals = [0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8]
        elif this_scen == 'RampRposSOneHoleGradual80':
            surv_vals = [0.8, 0.8, 0.8, 0.7, 0.6, 0.5, 0.4, 0.4, 0.4, 0.5, 0.6, 0.7, 0.8, 0.8, 0.8, 0.8]
            rpos_vals = np.arange(0.8, -0.8, -0.1)
        elif this_scen == 'RampRpos_revSGradual80':
            surv_vals = [0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8]
            rpos_vals = np.arange(-0.8, 0.8, 0.1)
        elif this_scen == 'Rpos-03S0_4':
            surv_vals = np.zeros(n_elec) + 0.4
            rpos_vals = np.zeros(n_elec) - 0.3
        elif this_scen == 'ExtremeHole':
            surv_vals = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.8, 0.8, 0.8, 0.6, 0.4, 0.4, 0.6, 0.8, 0.8, 0.8]
            rpos_vals = np.zeros(n_elec)
        elif this_scen == 'Checking_REXT_2500':
            surv_vals = [0.10000000000091800, 0.2795777575802930, 0.10000000000548900, 0.10000000000030100,
                         0.10000000000001700, 0.10000000001060400, 0.100000000094481, 0.1000000002795140,
                         0.10000000001596000, 0.10000000000249200, 0.1000000000001920, 0.10000000000004600,
                         0.10000000000005000, 0.10000000000008700, 0.10000000000013000, 0.10000000000000200]
            rpos_vals = [0.8500000000000000, 0.8500000000000000, 0.8294766964064310, 0.7554343854939560,
                         0.6869450353778850, 0.6603663682745040, 0.6334152983712870, 0.5703408020246940,
                         0.4826291910479900, -0.5584458399599040, -0.8499998101274480, -0.849999948485318,
                         -0.8499998907133960, -0.8499996105750090, -0.8499995809009720, -0.8499999066711080]
        elif this_scen == 'S43':
            surv_vals = np.zeros(n_elec) + 0.6
            rpos_vals = np.array([0.089, 0.485, 0.354, 0.205, -0.071, -0.193, -0.238, -0.315, -0.234, -0.111, 0.044,
                                  0.350, 0.633, 0.694, 0.606, 0.362])
        elif this_scen == 'CustomForECAPFigure':
            # surv_vals = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])
            # rpos_vals = np.array([-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5,
            #                       0.5, 0.5, 0.5, 0.5])
            surv_vals = np.ones(n_elec) * 1.0
            rpos_vals = np.zeros(n_elec) - 0.5
        elif this_scen == 'TestLookingForAnomalies':
            surv_vals = [0.35, 0.35, 0.35, 0.36, 0.36, 0.36, 0.375, 0.375, 0.375, 0.38, 0.38, 0.38, 0.39, 0.39, 0.4,
                         0.41]
            rpos_vals = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125,
                         0.125, 0.125, 0.125]

    return [surv_vals, rpos_vals]
