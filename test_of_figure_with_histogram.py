from DPE_functions import *

clog_path = r'C:\Users\andrej\Documents\FEI\ClusterLog.clog'
vmax = 1E3
title = 'Test'
OutputPath = r'C:/Users/andrej/Documents/FEI/'
OutputName = 'test_figure'

#print_figure_single_cluster_energy_histograms(clog_path, 1, vmax, title, OutputPath, OutputName)
print_figure_single_cluster_count_histograms(clog_path, 1, OutputPath, OutputName)
