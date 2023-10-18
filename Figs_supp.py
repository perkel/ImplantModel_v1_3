#  summary_four_subjects.py
#  This script takes the four inverse model runs and puts them on a single page


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from common_params import *  # import common values across all models


def summary_four_subjects(subjects, f_name, unsupervised):
    # Key constants to set
    save_fig = True
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=8)

    fig = plt.figure(figsize=(10, 8))
    outer = gridspec.GridSpec(2, 2, wspace=0.2, hspace=0.3)
    xvals = np.arange(0, NELEC) + 1
    l_e = NELEC - 1  # last electrode to plot

    for i, subject in enumerate(subjects):
        data_filename = INVOUTPUTDIR + subject + '_fitResults_' + 'combined.npy'
        [_, _, _, thrsim, thrtargs, _, [fitrposvals, fitsurvvals],
         _, rpos_err_metric, _, ct_vals] = np.load(data_filename, allow_pickle=True)

        # Make plots
        inner = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=outer[i], wspace=0.1, hspace=0.15)

        # All on one plot
        ax = plt.Subplot(fig, inner[0])
        # t = ax.text(0.5, 0.5, 'outer=%d, inner=%d' % (i, j))
        # t.set_ha('center')
        # ax.set_xticks([])
        # ax.set_yticks([])

        ax.plot(xvals+0.1, thrsim[0][0], marker='o', color='lightblue', label='fit MP')
        ax.plot(xvals-0.1, thrtargs[0][0], marker='o', color='blue', label='measured MP')
        ax.plot(xvals[1:l_e]+0.1, thrsim[1][0][1:l_e], marker='o', color='pink', label='fit TP')
        ax.plot(xvals[1:l_e]-0.1, thrtargs[1][0][1:l_e], marker='o', color='red', label='measured TP')
        yl = 'Thresh. (dB)'
        title_text = 'Subject: ' + subject
        # ax.set(xlabel='Electrode number', ylabel=yl, title=title_text)
        ax.set_ylabel(yl, fontsize=8)
        ax.set_title(title_text, fontsize=10)

        ax.set_xlim(0, 17)
        ax.set_ylim(33, 70)
        ax.set_xticks([])
        ax.set_yticks([35, 45, 55, 65])
        # ax.legend(loc='upper right', ncol=2)

        fig.add_subplot(ax)
        ax = plt.Subplot(fig, inner[1])
        ax.plot(xvals[1:l_e]+0.1, 1 - fitrposvals[1:l_e], marker='o', color='gray', label='fit')
        if np.any(ct_vals):
            ax.plot(xvals-0.1, 1 - ct_vals, marker='o', color='black', label='CT estimate')
            # ax.fill_between(xvals-0.1, (1 - ct_vals) - ct_uncertainty, (1 - ct_vals) + ct_uncertainty,
            # color='black', alpha=0.1)

        # ax.plot(xvals, 1 - initvec[0:NELEC], marker='o', color='purple', label='initial guess')
        # ax.set(xlabel='Electrode number', ylabel='Dist. (mm)')
        ax.set_ylabel('Dist. (mm)', fontsize=8)

        ax.set_xlim(0, 17)
        ax.set_ylim(0, 2)
        ax.set_xticks([])
        ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])

        fig.add_subplot(ax)

        ax = plt.Subplot(fig, inner[2])

        ax.plot(xvals[1:l_e], fitsurvvals[1:l_e], marker='o', color='black', label='modeled')
        ax.set_xlabel('Electrode number', fontsize=8)
        ax.set_ylabel('Frac. density', fontsize=8)
        ax.set_xlim(0, 17)
        ax.set_ylim(0, 1)
        ax.set_xticks([2, 4, 6, 8, 10, 12, 14, 16])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])


        # ax.legend()
        # fig_consol.tight_layout()
        fig.add_subplot(ax)
        # could add plots of error (difference between desired/measured and fitted values)
        if save_fig:
            save_file_name = INVOUTPUTDIR + f_name + '.png'
            fig.savefig(save_file_name)
            save_file_name = INVOUTPUTDIR + f_name + '.eps'
            fig.savefig(save_file_name, format='eps')

        # # test correlation figure
        # if not use_fwd_model:
        #     fig2, ax2 = plt.subplots()
        #     ct_dist = 1-ct_vals[1:l_e]
        #     fit_dist = 1 - fitrposvals[1:l_e]
        #     fig2 = plt.plot(ct_dist, fit_dist, 'o')
        #     ax2.set(xlabel='CT distance (mm)', ylabel='fit distance (mm)')
        #     ax2.set_xlim([0, 2])
        #     ax2.set_ylim([0, 2])
        #     fit_corr = np.corrcoef(ct_dist, fit_dist)
    if not unsupervised:
        plt.show()


if __name__ == '__main__':
    txt_string = ['S22', 'S27', 'S38', 'S41']
    fig_name = 'FigS1'

    # txt_string = ['S43','S46', 'S47', 'S49R']
    # fig_name = 'FigS2'

    # txt_string = ['S50', 'S52', 'S53', 'S54']
    # fig_name = 'FigS3'

    # txt_string = ['S55', 'S57']
    # fig_name = 'FigS4'

    unsupervised = False
    summary_four_subjects(txt_string, fig_name, unsupervised)
