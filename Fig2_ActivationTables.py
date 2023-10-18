#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:04:55 2020

@author: perkel
"""

import pickle
import matplotlib.pyplot as plt
from common_params import *


def fig2_activation_tables():

    with open(FIELDTABLE, 'rb') as combined_data:
        data = pickle.load(combined_data)
    combined_data.close()

    fp = data[0]
    v_vals = data[1]
    act_vals = data[2]

    fig2, ax2 = plt.subplots(figsize=(9, 6))
    ax2.tick_params(axis='both', labelsize=14)
    ax3 = ax2.twinx()  # second y axis
    rpos = [-0.5, 0.0, 0.5]  # radial positions

    # helper to calculate the fall-off over 1 mm
    # r_idx = 1  # hard coded -- not great, but this gives values of internal resistivity of 250 ohm-cm
    falloff_dist = 1.0
    temp0 = np.array(fp['zEval'])
    z_falloff_idx = np.argmin(np.abs(temp0 - falloff_dist))
    z_falloff_vals = np.zeros((len(rpos), 2))
    for i, val in enumerate(rpos):
        rpos_idx = np.argmin(np.abs(fp['relec'] - val))
        if i == 0:
            ax2.plot(fp['zEval'], np.abs(act_vals[rpos_idx, :]), marker='o', label='Activation')
            ax3.plot(fp['zEval'], np.abs(v_vals[rpos_idx, 1, :]), marker='o', markerfacecolor='white',
                     linestyle=(0, (5, 10)), label='Voltage')

        else:
            ax2.plot(fp['zEval'], np.abs(act_vals[rpos_idx, :]), marker='o')
            ax3.plot(fp['zEval'], np.abs(v_vals[rpos_idx, 1, :]), marker='o', markerfacecolor='white',
                     linestyle=(0, (5, 10)))

        # Calculate falloff fraction over fall-off distance
        z_falloff_vals[i, 0] = np.abs(act_vals[rpos_idx, z_falloff_idx]) / np.abs(act_vals[rpos_idx, 0])
        z_falloff_vals[i, 1] = np.abs(v_vals[rpos_idx, 1, z_falloff_idx]) / np.abs(v_vals[rpos_idx, 1, 0])
        print('Act fall-off over ', falloff_dist, ' mm: for rpos: ', val, ' = ', z_falloff_vals[i, 0])
        print('Voltage fall-off over ', falloff_dist, ' mm: for rpos: ', val, ' = ', z_falloff_vals[i, 1])

    ax2.set_xlabel('Z position (mm)', fontsize=18)
    ax2.set_ylabel('Activation', fontsize=18)
    ax2.set(xlim=[-0.2, 4.2])
    ax3.set_ylabel('Voltage', fontsize=18)
    ax3.tick_params(axis='both', labelsize=14)
    ax2.legend(prop={'size': 14})
    leg2 = ax2.get_legend()
    leg2.legend_handles[0].set_color('black')
    ax3.legend(loc=(0.745, 0.82), prop={'size': 14})
    leg3 = ax3.get_legend()
    leg3.legend_handles[0].set_color('black')
    plt.savefig('Fig2_ActivationTables.eps', format='eps')

    plt.show()


if __name__ == '__main__':
    fig2_activation_tables()
