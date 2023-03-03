from DPE_functions import *

clog_path = r'Q:\DPE_carlos_data_output\2021_10_krakow\Si500um\06\10\Files\ClusterLog.clog'
elist_path = r'Q:\DPE_carlos_data_output\2021_10_krakow\Si500um\06\10\Files\ExtElist.txt'
vmax = 1E3
title = 'Test'
OutputPath = r'C:/Users/andrej/Documents/FEI/'
OutputName = 'test_figure'
OutputNameElist = 'Elist_coincidence.txt'

#print_figure_single_cluster_energy_histograms(clog_path, 1, vmax, title, OutputPath, OutputName)
#print_figure_single_cluster_count_histograms(clog_path, 9, OutputPath, OutputName)

#write_elist_add_coincidence(elist_path, OutputPath, OutputNameElist)

am_elist_data = np.loadtxt('E:\\DPE_andrej_data_output\\2023_02_24_Am241_time_spectra\\X00_tpx2\\000\\Files\\ExtElist.txt', skiprows=2, delimiter=';')

filtered_data = np.empty([0])

for i in range(1000000):
    if am_elist_data[i,7] == 1:
        filtered_data = np.append(filtered_data, am_elist_data[i,4])

tickfnt=12

plt.close()
plt.clf()
plt.cla()
plt.hist(filtered_data[:,4], bins=2048, histtype = 'step', linewidth=1.75)
plt.xlim(left=0, right=200)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.legend(loc='upper right')
plt.show()
#plt.savefig('X00_Am241_1ps_clusters.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)