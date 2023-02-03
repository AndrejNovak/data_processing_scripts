from DPE_functions import *

clog_path = r'Q:\DPE_carlos_data_output\2021_10_krakow\Si500um\06\10\Files\ClusterLog.clog'
elist_path = r'Q:\DPE_carlos_data_output\2021_10_krakow\Si500um\06\10\Files\ExtElist.txt'
vmax = 1E3
title = 'Test'
OutputPath = r'C:/Users/andrej/Documents/FEI/'
OutputName = 'test_figure'
OutputNameElist = 'Elist_coincidence.txt'

#print_figure_single_cluster_energy_histograms(clog_path, 1, vmax, title, OutputPath, OutputName)
print_figure_single_cluster_count_histograms(clog_path, 9, OutputPath, OutputName)

write_elist_add_coincidence(elist_path, OutputPath, OutputNameElist)