from DPE_functions import *

"""
FileInPath = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\07\\Files\\'

read_clog_multiple(FileInPath)

FilePath = 'Q:\\timepix_config_calib_files\\minipix_tpx2\\X00-W1698 500 um Si\\'
filename = 'X00_mask.txt'

print(check_if_position_is_in_mask(FilePath, filename, 12, 12))
"""

"""
####### TEST OF NEW CLOG READING - per cluster reading and cluster smoothening #########

vmax = 1E3
title = 'Test'
OutputName = 'test_figure'
OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\'

clog_path = 'C:\\Users\\andrej\\Documents\\FEI\\ClusterLog_smooth_cluster.clog'
elist_path = 'C:\\Users\\andrej\\Documents\\FEI\\Elist_smooth.txt'
cluster_number = 2

print_figure_single_cluster_energy_smooth(clog_path, cluster_number, vmax, title, OutputPath, OutputName)
"""

########### Test of new function for proton track straightening
OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\'
#OutputPath_straightening = 'Q:\\straightening_test_script\\B3 TPX3 H09 14 225MeV 75deg 20s tot toa\\'
#OutputPath_straightening = 'Q:\\straightening_test_script\\B3 TPX3 H09 15 150MeV 75deg 20s tot toa\\'
OutputPath_straightening = 'Q:\\straightening_test_script\\B3 TPX3 H09 16 70MeV 75deg 20s tot toa\\'
OutputName2 = 'test_straightening'
OutputName_skeleton = 'skeleton_test'

clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\14\\Files\\'
elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\14\\Files\\Elist.txt'

elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')

size_data = []
energy_data = []
length_data = []
angle_data = []
ID_cislo = []
vmax = 3E3

clog = read_clog_multiple(clog_path)
print(f'The total number of clusters is {len(clog[:])}')

#for i in range(1):
for i in range(len(elist_data[:,0])):
    if elist_data[i,7] > 80 and elist_data[i,4] > 3000:
        print(f'Cluster size is: {elist_data[i,7]} and energy {elist_data[i,4]}')
        #ID_cislo.append(elist_data[i,1])
        #size_data.append(elist_data[i,7])
        #energy_data.append(elist_data[i,4])
        #length_data.append(elist_data[i,12])
        #angle_data.append(elist_data[i,11])
        straighten_single_cluster_rows(clog[i], i, mm_to_px(elist_data[i, 2]), mm_to_px(elist_data[i, 3]), elist_data[i,8], elist_data[i,8]+100, OutputPath_straightening, OutputName2)
        cluster_skeleton(clog[i], i, OutputPath_straightening, OutputName_skeleton)
        
		
#OutputNameTxt = 'info_txt'
#out_values = np.column_stack((ID_cislo, energy_data, size_data, length_data, angle_data))
#np.savetxt(OutputPath + OutputNameTxt + '.txt', out_values, delimiter=',', header='Event, Energy, Size, Length, Angle', comments='')

####### TEST OF NEW CLOG READING #########

"""
clog_path = 'Q:\\DPE_carlos_data_output\\2021_10_krakow\\Si500um\\06\\10\\Files\\ClusterLog.clog'
elist_path = 'Q:\\DPE_carlos_data_output\\2021_10_krakow\\Si500um\\06\\10\\Files\\ExtElist.txt'
vmax = 1E3
title = 'Test'
OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\'
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
"""