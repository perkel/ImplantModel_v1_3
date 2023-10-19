# Which scripts generate the figures in Perkel, Goldwyn & Arenberg (2023)

import Fig2_ActivationTables as f2
import plot_neuron_activation as f3
import fig_2D_contour as f4_5
import Fig6 as f6
import Figs_7_8 as f7_8
import Fig9_v2 as f9
import Figs_supp as fs


# Fig 1 is the cartoon schematic. Not generated in python
# Fig 2
f2.fig2_activation_tables()

# Fig 3
f3.plot_neuron_activation()

# Fig 4 & 5
f4_5.fig_2D_contour()

# Fig 6
f6.fig_scenario_inverse_results()

# Figs 7 & 8
use_fwd_model = False
txt_string = ['S40', 'S42']  # 2 subjects to fit side by side Fig 7 of the paper
# txt_string = ['S29', 'S56']  # 2 subjects to fit side by side Fig 8 of the paper
unsupervised = False
f7_8.plot_inverse_results(use_fwd_model, txt_string, unsupervised)

# Fig 9
# NOTE: before funning this figure you will need to run the inverse model for all subjects
# results will be saved in 'summary_inverse_fit_results.csv' and 'summary_inverse_fit_results.npy'
# For now, each run of the inverse model overwrites the summary fit reults from the last one
f9.fig9_summary()

# Supplementary figures
txt_string = ['S22', 'S27', 'S38', 'S41']
fig_name = 'FigS1'

# txt_string = ['S43','S46', 'S47', 'S49R']
# fig_name = 'FigS2'

# txt_string = ['S50', 'S52', 'S53', 'S54']
# fig_name = 'FigS3'

# txt_string = ['S55', 'S57']
# fig_name = 'FigS4'

unsupervised = False

fs.summary_four_subjects(txt_string, fig_name, unsupervised)
