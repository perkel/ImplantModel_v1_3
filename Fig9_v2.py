#  Fig_fit_summary.py
#  David Perkel 4 February 2023

from common_params import *  # import common values across all models
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import seaborn as sns
import csv
import scipy.stats as stats


def fig9_summary():
    # Constants
    label_ypos = 1.05
    n_subj = 18
    n_elec = 16

    # Reads a summary file, and tests whether average rpos error is less than chance based on shuffling
    # You need to run the inverse model for all subjects before making this figure
    summary_file_name = INVOUTPUTDIR + 'summary_inverse_fit_results.npy'

    [scenarios, rpos_summary] = np.load(summary_file_name, allow_pickle=True)
    nscen = len(scenarios)
    rpos_vals = np.zeros((nscen, n_elec))
    rpos_fit_vals = np.zeros((nscen, n_elec))
    thresh_err_summary = np.zeros((nscen, 2))
    rpos_err_summary = np.zeros(nscen)
    density_err_summary = np.zeros(nscen)
    dist_corr = np.zeros(nscen)
    dist_corr_p = np.zeros(nscen)

    for i, scen in enumerate(scenarios):
        rpos_fit_vals[i, :] = rpos_summary[i][0]
        rpos_vals[i, :] = rpos_summary[i][1]

    # get detailed data from the CSV summary file
    summary_csv_file_name = INVOUTPUTDIR + 'summary_inverse_fit_results.csv'
    with open(summary_csv_file_name, mode='r') as data_file:
        entire_file = csv.reader(data_file, delimiter=',', quotechar='"')
        for row, row_data in enumerate(entire_file):
            if row == 0:  # skip header row
                pass
            else:
                [_, thresh_err_summary[row-1, 0], thresh_err_summary[row-1, 1],
                 rpos_err_summary[row-1], aaa_temp, dist_corr[row-1], dist_corr_p[row-1]] = row_data
                print(aaa_temp)

        data_file.close()

    # Loop on scenarios again. Compute pairwise mean absolute position error
    mean_errs = np.zeros([nscen, nscen])
    corr_vals = np.zeros([nscen, nscen])
    corr_p = np.zeros([nscen, nscen])

    for i, scen_i in enumerate(scenarios):
        for j, scen_j in enumerate(scenarios):
            rposerrs = np.subtract(rpos_fit_vals[i], rpos_vals[j])
            mean_errs[i, j] = np.mean(np.abs(rposerrs))
            [dist_corr, dist_corr_p] = stats.pearsonr(1.0 - (rpos_fit_vals[i]), 1.0 - (rpos_vals[j]))
            corr_vals[i, j] = dist_corr
            corr_p[i, j] = dist_corr_p

    # now we have the matrix. Let's plot a histogram of all the diagonal values
    diag = np.diag(mean_errs)
    diag_cr = np.diag(corr_vals)

    fig1, axs1 = plt.subplots(2, 2, figsize=(8, 6), width_ratios=[2, 1])
    fig1.tight_layout(pad=3)

    axs1[0, 0].plot(thresh_err_summary[:, 0], thresh_err_summary[:, 1], 'o', color='black')
    axs1[0, 0].plot([0, 0.8], [0, 0.8], linestyle='dashed', color='black')  # line of slope 1.0
    axs1[0, 0].set_xlabel('Monopolar threshold error (dB)')
    axs1[0, 0].set_ylabel('Tripolar thresh. error (dB)')
    axs1[0, 0].spines['top'].set_visible(False)
    axs1[0, 0].spines['right'].set_visible(False)
    axs1[0, 0].text(-0.05, label_ypos, 'A', size=20, weight='bold', transform=axs1[0, 0].transAxes)
    axs1[0, 0].text(0.6, 0.5, 'y = x', size=16)
    axs1[0, 0].set_xlim([0, 1.8])
    axs1[0, 0].set_ylim([-0.05, 0.85])

    # Best fit line to the data
    coeffs = np.polyfit(thresh_err_summary[:, 0], thresh_err_summary[:, 1], 1)
    start_pt = coeffs[1]
    end_pt = coeffs[1] + (coeffs[0]*1.6)
    axs1[0, 0].plot([0, 1.8], [start_pt, end_pt], color='black')

    sns.swarmplot(diag, ax=axs1[0, 1], color='black')
    median = np.median(diag)
    iqrbar = stats.iqr(diag)/2.0
    axs1[0, 1].set_ylabel('Distance error (mm)')
    axs1[0, 1].spines['top'].set_visible(False)
    axs1[0, 1].spines['right'].set_visible(False)
    # plot median and interquartile range
    axs1[0, 1].plot([-0.3, 0.3], [median, median], 'k')  # horizonatl line to indicate median
    axs1[0, 1].plot([-0.15, 0.15], [median-iqrbar, median-iqrbar], 'k')
    axs1[0, 1].plot([-0.15, 0.15], [median+iqrbar, median+iqrbar], 'k')
    axs1[0, 1].plot([0, 0], [median-iqrbar, median+iqrbar], 'k')  # vertical line
    axs1[0, 1].set_xlim([-0.5, 0.5])
    # plt.tick_params(
    #     axis='x',           # changes apply to the x-axis
    #     which='both',       # both major and minor ticks are affected
    #     bottom=False,       # ticks along the bottom edge are off
    #     top=False,          # ticks along the top edge are off
    #     labelbottom=False)  # labels along the bottom edge are off

    axs1[0, 1].set_xticks([])
    axs1[0, 1].text(-0.2, label_ypos, 'B', size=20, weight='bold', transform=axs1[0, 1].transAxes)

    signif = []
    near_signif = []
    not_signif = []

    for idx, diag in enumerate(diag_cr):
        if corr_p[idx, idx] > 0.1:
            not_signif.append(idx)
        elif corr_p[idx, idx] <= 0.1 and corr_p[idx, idx] > 0.05:
            near_signif.append(idx)
        else:
            signif.append(idx)

    sns.swarmplot(diag_cr[signif], ax=axs1[1, 1], color='black')
    sns.swarmplot(diag_cr[near_signif], ax=axs1[1, 1], color='gray')
    # sns.swarmplot(diag_cr[not_signif], ax=axs1[1, 1], color='black', marker='$\circ$', ec="face", s=8)
    sns.swarmplot(diag_cr[not_signif], ax=axs1[1, 1], color='black', marker='$\circ$', s=6)

    median_cr = np.median(diag_cr)
    iqrbar_cr = stats.iqr(diag_cr)/2.0
    axs1[1, 1].set_ylabel('Pearson\'s r')
    axs1[1, 1].spines['top'].set_visible(False)
    axs1[1, 1].spines['right'].set_visible(False)
    axs1[1, 1].plot([-0.3, 0.3], [median_cr, median_cr], 'k')  # horizonatl line to indicate median
    axs1[1, 1].plot([-0.15, 0.15], [median_cr-iqrbar_cr, median_cr-iqrbar_cr], 'k')
    axs1[1, 1].plot([-0.15, 0.15], [median_cr+iqrbar_cr, median_cr+iqrbar_cr], 'k')
    axs1[1, 1].plot([0, 0], [median_cr-iqrbar_cr, median_cr+iqrbar_cr], 'k')  # vertical line
    axs1[1, 1].set_xlim([-0.5, 0.5])
    axs1[0, 1].tick_params(
        axis='x',           # changes apply to the x-axis
        which='both',       # both major and minor ticks are affected
        bottom=False,       # ticks along the bottom edge are off
        top=False,          # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off

    axs1[1, 1].tick_params(
        axis='x',           # changes apply to the x-axis
        which='both',       # both major and minor ticks are affected
        bottom=False,       # ticks along the bottom edge are off
        top=False,          # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    axs1[1, 1].text(-0.05, label_ypos, 'C', size=20, weight='bold', transform=axs1[1, 0].transAxes)

    # Panel D scatter plot of CT and fit electrode positions across all subjects
    # Read data from files with summary data
    # fname = INVOUTPUTDIR + 'summary_actual_position.csv'
    # ct_vals = np.zeros((n_subj, n_elec))
    # with open(fname, mode='r') as data_file:
    #     entire_file = csv.reader(data_file, delimiter=',', quotechar='"')
    #     for row, row_data in enumerate(entire_file):
    #         subject = row_data[0]
    #         for i in range(n_elec):
    #             ct_vals[row, i] = float(row_data[i+1])
    #     data_file.close()

    # fname = INVOUTPUTDIR + 'summary_fit_position.csv'
    # fit_vals = np.zeros((n_subj, n_elec))
    # with open(fname, mode='r') as data_file:
    #     entire_file = csv.reader(data_file, delimiter=',', quotechar='"')
    #     for row, row_data in enumerate(entire_file):
    #         subject = row_data[0]
    #         for i in range(n_elec):
    #             fit_vals[row, i] = float(row_data[i+1])
    #     data_file.close()

    axs1[1, 0].tick_params(
        axis='x',           # changes apply to the x-axis
        which='both',       # both major and minor ticks are affected
        bottom=True,       # ticks along the bottom edge are off
        top=False,          # ticks along the top edge are off
        labelbottom=True)  # labels along the bottom edge are off

    color = iter(cm.rainbow(np.linspace(0, 1, n_subj)))

    for subj in range(n_subj):
        c = next(color)
        ct_dist = 1 - rpos_vals[subj]
        fit_dist = 1 - rpos_fit_vals[subj]
        axs1[1, 0].plot(ct_dist, fit_dist, '.', c=c)  # plot data points
        [slope, intercept] = np.polyfit(ct_dist, fit_dist, 1)
        minx = np.min(ct_dist)
        maxx = np.max(ct_dist)
        axs1[1, 0].plot((minx, maxx), (minx*slope + intercept, maxx*slope + intercept), '-', c=c)  # plot line

    axs1[1, 0].set_xlabel('CT distance (mm)')
    axs1[1, 0].set_ylabel('Fit distance (mm)')
    axs1[1, 0].spines['top'].set_visible(False)
    axs1[1, 0].spines['right'].set_visible(False)
    axs1[1, 0].text(-0.2, label_ypos, 'D', size=20, weight='bold', transform=axs1[1, 1].transAxes)

    # best fit line for all ponts together
    x = 1 - rpos_vals.flatten()
    y = 1 - rpos_fit_vals.flatten()
    [slope, intercept] = np.polyfit(x, y, 1)
    start_pt, end_pt = axs1[1, 0].get_xlim()
    axs1[1, 0].plot([start_pt, end_pt], [(start_pt*slope) + intercept, (end_pt*slope) + intercept], 'black')

    # statistics
    # res = stats.linregress(x, y)

    # Save and display
    figname = INVOUTPUTDIR + 'Fig_fit_summary.pdf'
    plt.savefig(figname, format='pdf', pad_inches=0.1)
    plt.show()


if __name__ == '__main__':
    fig9_summary()
