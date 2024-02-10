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


# Chapter 5
# Figure 5.2 - 4 segment matrix made of 4 detectors

input_dir = 'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\'
det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
e_name = ['08_MeV', '13_MeV', '22_MeV', '31_MeV']
#rot_name = ['00_angle', '10_angle', '20_angle', '30_angle', '40_angle', '50_angle', '60_angle', '70_angle', '80_angle', '85_angle', '88_angle', '89_angle', '90_angle', '92_angle']
rot_name = ['50_angle']
voltage = ['-450 V', '-300 V', '50 V', '200 V', '200 V']
thickness = np.array([2000, 500, 100, 300, 500])

label_det = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m']
#label_energy = ['08 MeV', '13 MeV', '22 MeV', '31 MeV']
label_energy = ['22 MeV', '31 MeV']
label_angle = ['0$^{\circ}$ angle', '10$^{\circ}$ angle', '20$^{\circ}$ angle', '30$^{\circ}$ angle', '40$^{\circ}$ angle', '50$^{\circ}$ angle', '60$^{\circ}$ angle', '70$^{\circ}$ angle', '80$^{\circ}$ angle', '85$^{\circ}$ angle', '88$^{\circ}$ angle', '89$^{\circ}$ angle', '90$^{\circ}$ angle', '92$^{\circ}$ angle']
mydpi = 300
tickfnt = 14
lin_wd = 1.75

paths_22 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\']

paths_31 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\']

matrix22 = np.zeros([256,256])
matrix31 = np.zeros([256,256])

number_of_particles = np.array([20000, 7000, 7000, 7000])
iterator = 0

OutNames = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_500um']
TitleLabel = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 500 $\mu$m']
OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_5\\U120M\\'
vmax = 5000

for i in range(len(paths_22)):
    matrix_energy = np.zeros([256,256])
    clog_data = read_clog_multiple(paths_22[i])
    for j in range(len(clog_data[:])):
        cluster_size_clog = len(clog_data[j][:])
        if iterator < number_of_particles[i] and cluster_size_clog > 3:
                iterator += 1
                for k in range(cluster_size_clog):
                        x, y = int(clog_data[j][k][0]), int(clog_data[j][k][1])
                        matrix_energy[x, y] += clog_data[j][k][2]
    iterator = 0
    np.savetxt(OutputPath + OutNames[i] + '_22MeV.txt', matrix_energy, fmt="%.3f")
    print_figure_energy(matrix_energy, vmax, TitleLabel[i], OutputPath, OutNames[i] + '_22MeV')

iterator = 0

for i in range(len(paths_31)):
    matrix_energy = np.zeros([256,256])
    clog_data = read_clog_multiple(paths_31[i])
    for j in range(len(clog_data[:])):
        cluster_size_clog = len(clog_data[j][:])
        if iterator < number_of_particles[i] and cluster_size_clog > 3:
                cluster_size_clog = len(clog_data[j][:])
                iterator += 1
                for k in range(cluster_size_clog):
                        x, y = int(clog_data[j][k][0]), int(clog_data[j][k][1])
                        matrix_energy[x, y] += clog_data[j][k][2]
    iterator = 0
    np.savetxt(OutputPath + OutNames[i] + '_31MeV.txt', matrix_energy, fmt="%.3f")
    print_figure_energy(matrix_energy, vmax, TitleLabel[i], OutputPath, OutNames[i] + '_31MeV')

CdTe22 = np.loadtxt(OutputPath + 'CdTe_2000um_22MeV.txt')
GaAs22 = np.loadtxt(OutputPath + 'GaAs_500um_22MeV.txt')
Si10022 = np.loadtxt(OutputPath + 'Si_100um_22MeV.txt')
Si50022 = np.loadtxt(OutputPath + 'Si_500um_22MeV.txt')

matrix22[0:128,128:256] = CdTe22[64:192,64:192]
matrix22[128:256,128:256] = GaAs22[64:192,64:192]
matrix22[0:128,0:128] = Si10022[64:192,64:192]
matrix22[128:256,0:128] = Si50022[64:192,64:192]

CdTe31 = np.loadtxt(OutputPath + 'CdTe_2000um_31MeV.txt')
GaAs31 = np.loadtxt(OutputPath + 'GaAs_500um_31MeV.txt')
Si10031 = np.loadtxt(OutputPath + 'Si_100um_31MeV.txt')
Si50031 = np.loadtxt(OutputPath + 'Si_500um_31MeV.txt')

matrix31[0:128,128:256] = CdTe31[64:192,64:192]
matrix31[128:256,128:256] = GaAs31[64:192,64:192]
matrix31[0:128,0:128] = Si10031[64:192,64:192]
matrix31[128:256,0:128] = Si50031[64:192,64:192]

print_figure_energy(matrix22, vmax, '', OutputPath, '4_segment_22MeV')
print_figure_energy(matrix31, vmax, '', OutputPath, '4_segment_31MeV')

"""


# Chapter 5
# Figure 5.3 - single clusters

input_dir = 'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\'
det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
e_name = ['08_MeV', '13_MeV', '22_MeV', '31_MeV']
#rot_name = ['00_angle', '10_angle', '20_angle', '30_angle', '40_angle', '50_angle', '60_angle', '70_angle', '80_angle', '85_angle', '88_angle', '89_angle', '90_angle', '92_angle']
rot_name = ['50_angle']
voltage = ['-450 V', '-300 V', '50 V', '200 V', '200 V']
thickness = np.array([2000, 500, 100, 300, 500])

label_det = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m']
#label_energy = ['08 MeV', '13 MeV', '22 MeV', '31 MeV']
label_energy = ['08_MeV', '13_MeV', '22 MeV', '31 MeV']
label_angle = ['0$^{\circ}$ angle', '10$^{\circ}$ angle', '20$^{\circ}$ angle', '30$^{\circ}$ angle', '40$^{\circ}$ angle', '50$^{\circ}$ angle', '60$^{\circ}$ angle', '70$^{\circ}$ angle', '80$^{\circ}$ angle', '85$^{\circ}$ angle', '88$^{\circ}$ angle', '89$^{\circ}$ angle', '90$^{\circ}$ angle', '92$^{\circ}$ angle']
mydpi = 300
tickfnt = 14
lin_wd = 1.75

paths_31 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[3]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\']

paths_elist_31 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[3]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist']

number_of_particles = 20
iterator = 0

OutNames = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
TitleLabel = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m','Si 500 $\mu$m']
OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_5\\U120M\\single_cluster\\50deg\\'
vmax = 2000

for i in range(len(paths_31)):
    elist_data = np.loadtxt(paths_elist_31[i], skiprows=2, delimiter='\t')
    clog_data = read_clog_multiple(paths_31[i])
    
    for j in range(len(elist_data[:,0])):
        if elist_data[j,4] > 300 and elist_data[j,7] > 6 and iterator < number_of_particles:
            title = TitleLabel[i] + ' #' + str(j)
            print_figure_single_cluster_energy(clog_data[j], j, vmax, title, OutputPath, OutNames[i] + '_31MeV')
            iterator += 1
    iterator = 0


# Chapter 5
# Figure 5.4 - single clusters higher angle

input_dir = 'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\'
det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
e_name = ['08_MeV', '13_MeV', '22_MeV', '31_MeV']
#rot_name = ['00_angle', '10_angle', '20_angle', '30_angle', '40_angle', '50_angle', '60_angle', '70_angle', '80_angle', '85_angle', '88_angle', '89_angle', '90_angle', '92_angle']
rot_name = ['50_angle','85_angle']
voltage = ['-450 V', '-300 V', '50 V', '200 V', '200 V']
thickness = np.array([2000, 500, 100, 300, 500])

label_det = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m']
#label_energy = ['08 MeV', '13 MeV', '22 MeV', '31 MeV']
label_energy = ['08_MeV', '13_MeV', '22 MeV', '31 MeV']
label_angle = ['0$^{\circ}$ angle', '10$^{\circ}$ angle', '20$^{\circ}$ angle', '30$^{\circ}$ angle', '40$^{\circ}$ angle', '50$^{\circ}$ angle', '60$^{\circ}$ angle', '70$^{\circ}$ angle', '80$^{\circ}$ angle', '85$^{\circ}$ angle', '88$^{\circ}$ angle', '89$^{\circ}$ angle', '90$^{\circ}$ angle', '92$^{\circ}$ angle']
mydpi = 300
tickfnt = 14
lin_wd = 1.75

paths_31 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[3]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[1]) + '\\File\\',
            'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\']

paths_elist_31 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[3]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[1]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[1]) + '\\File\\EventListExt.advelist']

number_of_particles = 20
iterator = 0

OutNames = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
TitleLabel = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m','Si 500 $\mu$m']
OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_5\\U120M\\single_cluster\\85deg\\'
vmax = 2000

for i in range(len(paths_31)):
    elist_data = np.loadtxt(paths_elist_31[i], skiprows=2, delimiter='\t')
    clog_data = read_clog_multiple(paths_31[i])
    
    for j in range(len(elist_data[:,0])):
        if elist_data[j,4] > 300 and elist_data[j,7] > 6 and iterator < number_of_particles:
            title = TitleLabel[i] + ' #' + str(j)
            print_figure_single_cluster_energy(clog_data[j], j, vmax, title, OutputPath, OutNames[i] + '_31MeV')
            iterator += 1
    iterator = 0


# Chapter 5
# Figure 5.5 - hexbin of 2 parameters

input_dir = 'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\'
det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
e_name = ['08_MeV', '13_MeV', '22_MeV', '31_MeV']
#rot_name = ['00_angle', '10_angle', '20_angle', '30_angle', '40_angle', '50_angle', '60_angle', '70_angle', '80_angle', '85_angle', '88_angle', '89_angle', '90_angle', '92_angle']
rot_name = ['50_angle']
voltage = ['-450 V', '-300 V', '50 V', '200 V', '200 V']
thickness = np.array([2000, 500, 100, 300, 500])

label_det = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m']
#label_energy = ['08 MeV', '13 MeV', '22 MeV', '31 MeV']
label_energy = ['08_MeV', '13_MeV', '22 MeV', '31 MeV']
label_angle = ['0$^{\circ}$ angle', '10$^{\circ}$ angle', '20$^{\circ}$ angle', '30$^{\circ}$ angle', '40$^{\circ}$ angle', '50$^{\circ}$ angle', '60$^{\circ}$ angle', '70$^{\circ}$ angle', '80$^{\circ}$ angle', '85$^{\circ}$ angle', '88$^{\circ}$ angle', '89$^{\circ}$ angle', '90$^{\circ}$ angle', '92$^{\circ}$ angle']
mydpi = 300
tickfnt = 16
lin_wd = 1.75

paths_elist_22 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[3]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist']

paths_elist_31 = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[0]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[1]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[2]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[3]) + '\\' + str(e_name[2]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist',
                'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\' + str(det_name[4]) + '\\' + str(e_name[3]) + '\\' + str(rot_name[0]) + '\\File\\EventListExt.advelist']

OutNames = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um','Si_500um']
TitleLabel = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m','Si 500 $\mu$m']
OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\phd_thesis\\figures\\chapter_5\\U120M\\hexbin\\'

xlim_max22 = np.array([25000, 50000, 1500, 5000, 8000])
ylim_max22 = np.array([700, 80, 30, 80, 175])

xlim_max31 = np.array([35000, 60000, 1600, 5000, 15000])
ylim_max31 = np.array([800, 70, 30, 70, 250])

for i in range(len(paths_elist_22)):
    elist_data = np.loadtxt(paths_elist_22[i], skiprows=2, delimiter='\t')
    
    plt.close('all')
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    plt.hexbin(elist_data[:,4], elist_data[:,7], gridsize = 80, bins='log', cmap='viridis')
    plt.gca().xaxis.tick_bottom()
    #plt.clim(1, )
    cbar = plt.colorbar(label='log10(N)') # shrink=0.8, aspect=20*0.8
    cbar.set_label(label='log10(N)', size=tickfnt, weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label=TitleLabel[i], fontsize=tickfnt)
    plt.xlim([1, xlim_max22[i]])
    plt.ylim([1, ylim_max22[i]])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Size [pixel]', fontsize=tickfnt)
    print(OutputPath + OutNames[i])
    plt.savefig(OutputPath + OutNames[i] + '_hexbin_22MeV.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.1)

for i in range(len(paths_elist_31)):
    elist_data = np.loadtxt(paths_elist_31[i], skiprows=2, delimiter='\t')
    
    plt.close('all')
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    plt.hexbin(elist_data[:,4], elist_data[:,7], gridsize = 80, bins='log', cmap='viridis')
    plt.gca().xaxis.tick_bottom()
    #plt.clim(1, vmax)
    cbar = plt.colorbar(label='log10(N)') # shrink=0.8, aspect=20*0.8,
    cbar.set_label(label='log10(N)', size=tickfnt, weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label=TitleLabel[i], fontsize=tickfnt)
    plt.xlim([1, xlim_max31[i]])
    plt.ylim([1, ylim_max31[i]])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Size [pixel]', fontsize=tickfnt)
    print(OutputPath + OutNames[i] + '_hexbin_31MeV.png')
    plt.savefig(OutputPath + OutNames[i] + '_hexbin_31MeV.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.1)

