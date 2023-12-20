# Common parameters for the implant model

import numpy as np

# Basic parameters
NELEC = 16
ELEC_BASALPOS = 30  # in mm
espace = 1.1

# Neural activation parameters
THRTARG = 100.0
TARG_TEXT = '_TARG' + str(round(THRTARG)) + '/'
ACTR = 100.0
ACTR_TEXT = 'ACTR' + str(round(ACTR)) + '_'
ACT_STDREL = 2.0
STD_TEXT = 'STDR' + str(ACT_STDREL)
STD_TEXT = STD_TEXT.replace('.', '_')

# File locations
sigmaVals = [0, 0.9]  # Always explore monopolar stimulation and one value of sigma for triploar
# can be overridden for individual subjects

COCHLEA = {'source': 'manual', 'timestamp': [], 'radius': []}
electrodes = {'source': 'manual', 'timestamp': [], 'zpos': ELEC_BASALPOS - np.arange(NELEC - 1, -1, -1) * espace,
              'rpos': []}
NEURONS = {'act_ctr': ACTR, 'act_stdrel': ACT_STDREL, 'nsurvival': [], 'sidelobe': 1.0, 'neur_per_clust': 10,
           'rlvl': [], 'rule': 'proportional', 'coef': 0.0, 'power': 1.0, 'thrTarg': THRTARG}
# For COEF convex: <0 | 0.4, 0.9  linear: 0 | 1; concave: >0 | 1.0, 1.8
CHANNEL = {'source': 'manual', 'number': range(0, NELEC), 'config': 'pTP', 'sigma': 0.9, 'alpha': 0.5,
           'current': 10000000000.0}
GRID = {'r': 0.1, 'th': 0.0, 'z': np.arange(0, 33, 0.01)}  # mm
RUN_INFO = {'scenario': 'scenario', 'run_time': [], 'run_duration': 0.0}
simParams = {'cochlea': COCHLEA, 'electrodes': electrodes, 'channel': CHANNEL, 'grid': GRID, 'neurons': NEURONS,
             'run_info': RUN_INFO}

nZ = len(GRID['z'])
NSURVINIT = 1.0

ct_uncertainty = 0.1  # uncertainty for CT values in case one wants to display it on graphs

# Set specific scenarios to run with forward model.

## NOTE!!
# scenario names beginning with 'A' or 'S' and followed by 2 numerals are considered subjects
# other scenario names are considered to be associated with the forward model

# Not used by the 2D exploration tool. These are left in for convenience
# scenarios = ['Gradual80R75']
# scenarios = ['Uniform80R05']
# scenarios = ['Uniform100R05', 'Uniform100R10', 'Uniform100R15']
# scenarios = ['Uniform80R05', 'Uniform80R10', 'Uniform80R15']  # Used for Fig 3
# scenarios = ['Ramp80Rvariable1']
# scenarios = ['RampRpos_revSGradual80']
# scenarios = ['Rpos-03S0_4']
# scenarios = ['Ramp80Rvariable1']
# scenarios = ['RampRposS70']
# scenarios = ['Gradual80R-50']
# scenarios = ['RampRposS80']
# scenarios = ['RampRpos2SGradual80']
# scenarios = ['RampRposSOneHoleGradual80']

# scenarios = ['Gradual80R00', 'RampRposS80', 'RampRposSGradual80']  # for paper figure 6
# scenarios = ['Gradual2_80R00']
# scenarios = ['RampRposRampSurv']
# scenarios = ['ExtremeHole']
# scenarios = ['RampRposS80']
# scenarios = ['RampRposSGradual80']
# scenarios = ['Checking_REXT_2500']
# scenarios = ['CustomForECAPFigure']
# scenarios = ['Step40_80R00']
# scenarios = ['Gradual07_02R00', 'Gradual07_02UR00']


# Actual subject data. For inverse model only
# scenarios = ['S40', 'S42']  # paper "good fit" examples. Figure 7
# scenarios = ['S29', 'S56']  # paper "poor fit" examples. Figure 8
# scenarios = ['A002R', 'A014L', 'A022L', 'A022R', 'A023R', 'A024L']
# scenarios = ['A014L']
# all subjects with CT data
# scenarios = ['RampRposSGradual80', 'S22']
scenarios = ['Gradual80R00', 'RampRposS80', 'RampRposSGradual80', 'S22', 'S27',
            'S29', 'S38', 'S40', 'S41', 'S42', 'S43', 'S46', 'S47', 'S49R', 'S50', 'S52', 'S53', 'S54',
            'S55', 'S56', 'S57']

# File locations
FWD_OUT_PRFIX = 'FWD_OUTPUT/'
FWDOUTPUTDIR = FWD_OUT_PRFIX + ACTR_TEXT + STD_TEXT + TARG_TEXT
INV_OUT_PRFIX = 'INV_OUTPUT/'
INVOUTPUTDIR = INV_OUT_PRFIX + ACTR_TEXT + STD_TEXT + TARG_TEXT

# FIELDTABLE = ['13August2023_MedResolution_Rext125_nonans.dat', '13August2023_MedResolution_Rext250_nonans.dat',
#               '13August2023_MedResolution_Rext500.dat', '13August2023_MedResolution_Rext1500.dat',
#               '13August2023_MedResolution_Rext2500_nonans.dat']
# FIELDTABLE = '13August2023_MedResolution_Rext250_nonans.dat'
# FIELDTABLE = '6Dec2023_MedResolution_Rext70_nonans.dat'
FIELDTABLE = '19Dec2023_MedResolution_Rext500.dat'
