from DPE_functions import *

import time

"""
# Chapter 3
# Figure 3.1 - 150 MeV proton and line graph of deposited energy

#OutputPath_straightening = 'Q:\\2024_straightening_test_script\\B3 16 do dizertacky\\'
#OutputPath_straightening = 'Q:\\2024_straightening_test_script\\B3 15 do dizertacky\\'
OutputPath_straightening = 'Q:\\2024_straightening_test_script\\B3 14 do dizertacky\\'

OutputName_skeleton_neighbours = 'skeleton_test_neighbours'
OutputName2 = 'test_straightening'
OutputName_skeleton = 'skeleton_test'

#clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\16\\File\\'
#elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\16\\File\\EventListExt.advelist'

#clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\'
#elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\EventListExt.advelist'

clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\14\\File\\'
elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\14\\File\\EventListExt.advelist'
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')

size_data = []
energy_data = []
length_data = []
angle_data = []
ID_cislo = []

clog = read_clog_multiple(clog_path)
print(f'The total number of clusters is {len(clog[:])}')

min_pixel_energy = 20

k = 0

for i in range(len(elist_data[:,0])):
    # obmedzenim na size 200 sa viac-menej filtruju protony
    if elist_data[i,7] > 20 and elist_data[i,4] > 5000 and k < 100:
        print(f'Cluster size is: {elist_data[i,7]} and energy {elist_data[i,4]}')
        straighten_single_cluster_rows(clog[i], i, mm_to_px(elist_data[i, 2]), mm_to_px(elist_data[i, 3]), elist_data[i,8], elist_data[i,8]+100, OutputPath_straightening, OutputName_skeleton)
        #cluster_skeleton(clog[i], i, OutputPath_straightening, OutputName_skeleton)
        cluster_skeleton_ends_joints(clog[i], i, min_pixel_energy, OutputPath_straightening, OutputName_skeleton)
        k += 1


# Chapter 3
# Figure 3.5 - example of all cluster parameters calculated by DPE

tic = time.perf_counter()

clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\'
elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\EventListExt.advelist'

elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(clog_path)
print(f'The total number of clusters is {len(clog[:])}')

OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_3\\'

cluster_number = 12683
clog_data = clog[cluster_number]
vmax = elist_data[cluster_number,8] + 100
title = '150 MeV proton, $75^\circ$ elevation angle'
OutputName = 'DPE_output_example'

print_figure_single_cluster_energy_event_parameters(clog_data, elist_data, cluster_number, vmax, title, OutputPath, OutputName)

title = ''
OutputName = 'DPE_output_example_no_colorbar'
print_figure_single_cluster_energy(clog_data, cluster_number, vmax, title, OutputPath, OutputName)

toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")



# Chapter 3
# Figure 3.6 - cluster skeltonization and neighbours

tic = time.perf_counter()

clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\'
elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\EventListExt.advelist'

elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(clog_path)
print(f'The total number of clusters is {len(clog[:])}')

OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_3\\'

cluster_number = 12683
clog_data = clog[cluster_number]
vmax = elist_data[cluster_number,8] + 100
title = '150 MeV proton, $75^\circ$ elevation angle'

#OutputName = 'straightening_test'
#straighten_single_cluster_rows(clog[cluster_number], cluster_number, elist_data[cluster_number, 2], elist_data[cluster_number, 3], elist_data[cluster_number,8], elist_data[cluster_number,8]+100, OutputPath, OutputName)

OutputName = 'skeleton_test'
#cluster_skeleton_ends_joints(clog_data, cluster_number, 0, OutputPath, OutputName)

for i in range(100):
    cluster_skeleton_ends_joints(clog[i], i, 8, OutputPath, OutputName)

toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")


# Chapter 3
# Figure 3.7 - cluster skeltonization - anomaly example

tic = time.perf_counter()

clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\'
elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\EventListExt.advelist'

elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(clog_path)
print(f'The total number of clusters is {len(clog[:])}')

OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_3\\'
OutputName = 'anomaly'

number_of_clusters = 500
number = 0
border_margin_min = 20
border_margin_max = 236

for i in range(len(elist_data[:,0])):
    if elist_data[i,4] > 3500 and elist_data[i,2] > border_margin_min and elist_data[i,2] < border_margin_max and elist_data[i,3] > border_margin_min and elist_data[i,3] < border_margin_max and number < number_of_clusters:
        print(elist_data[i,4])
        cluster_skeleton_ends_joints(clog[i], i, 5, OutputPath, OutputName)
        number =+ 1

toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

"""
# Chapter 3
# Figure 3.8 - cluster straightening example

tic = time.perf_counter()

clog_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\'
elist_path = 'Q:\\DPE_carlos_data_output\\2022_06_krakow\\B3\\H09_TPX3_Si500\\15\\File\\EventListExt.advelist'

elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(clog_path)
print(f'The total number of clusters is {len(clog[:])}')

OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_3\\'

cluster_number = 30655
clog_data = clog[cluster_number]
vmax = elist_data[cluster_number,8] + 100
title = '150 MeV proton, $75^\circ$ elevation angle'

OutputName = 'straightening_test_new'

straighten_single_cluster_rows(clog[cluster_number], cluster_number, elist_data[cluster_number, 2], elist_data[cluster_number, 3], elist_data[cluster_number,8], elist_data[cluster_number,8]+100, OutputPath, OutputName)

toc = time.perf_counter()
print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")
