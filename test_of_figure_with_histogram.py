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

######## TEST OF SKELETON JOINTS AND ENDS MAPPING #############
########### Test of new function for proton track straightening

#OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\'
OutputPath_straightening = 'Q:\\straightening_test_script\\CdTe_31MeV_75deg_test_na_apcom\\'
#OutputPath_straightening = 'Q:\\straightening_test_script\\B3 TPX3 H09 14 225MeV 75deg 20s tot toa\\'
#OutputPath_straightening = 'Q:\\straightening_test_script\\B3 TPX3 H09 15 150MeV 75deg 20s tot toa\\'
#OutputPath_straightening = 'Q:\\straightening_test_script\\B3 TPX3 H09 16 70MeV 75deg 20s tot toa\\'

OutputName_skeleton_neighbours = 'skeleton_test_neighbours'
OutputName2 = 'test_straightening'
OutputName_skeleton = 'skeleton_test'

clog_path = 'C:\\Users\\andrej\\Documents\\FEI\\Vyskum\\DPE_carlos\\output\\protons\\A4\\D04_CdTe_1000um_500Vneg\\52_10ms\\Files\\'
elist_path = 'C:\\Users\\andrej\\Documents\\FEI\\Vyskum\\DPE_carlos\\output\\protons\\A4\\D04_CdTe_1000um_500Vneg\\52_10ms\\Files\\Elist.txt'

#clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\14\\Files\\'
#elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\14\\Files\\Elist.txt'

elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')

size_data = []
energy_data = []
length_data = []
angle_data = []
ID_cislo = []

clog = read_clog_multiple(clog_path)
print(f'The total number of clusters is {len(clog[:])}')

for i in range(len(elist_data[:,0])):
    # obmedzenim na size 200 sa viac-menej filtruju protony
    if elist_data[i,7] > 100 and elist_data[i,4] > 3000:
        print(f'Cluster size is: {elist_data[i,7]} and energy {elist_data[i,4]}')
        straighten_single_cluster_rows(clog[i], i, mm_to_px(elist_data[i, 2]), mm_to_px(elist_data[i, 3]), elist_data[i,8], elist_data[i,8]+100, OutputPath_straightening, OutputName_skeleton)
        cluster_skeleton(clog[i], i, OutputPath_straightening, OutputName_skeleton)
        cluster_skeleton_ends_joints(clog[i], i, OutputPath_straightening, OutputName_skeleton)