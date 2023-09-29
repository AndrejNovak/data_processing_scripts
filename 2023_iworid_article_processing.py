from DPE_functions import *

lin_wd = 1.75
tickfnt = 18
alpha_val = 0.85
mydpi = 300

"""
27 31 MeV 00
28 22 MeV 00
29 13 MeV 00
32 31 MeV 45
33 31 MeV 60
38 31 MeV 75
39 31 MeV 85
"""

paths = [
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\39_100ms\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\60deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\85deg\\',
]

paths_new = [
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\28_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\29_100ms\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\'
]

labels = ['31 MeV 0$^{\circ}$', '31 MeV 45$^{\circ}$', '31 MeV 60$^{\circ}$', '31 MeV 75$^{\circ}$', '31 MeV 85$^{\circ}$',
          '226 MeV 0$^{\circ}$', '226 MeV 45$^{\circ}$', '226 MeV 60$^{\circ}$', '226 MeV 75$^{\circ}$', '226 MeV 85$^{\circ}$']

labels_new = ['13 MeV 0$^{\circ}$', '22 MeV 0$^{\circ}$', '31 MeV 0$^{\circ}$', '100 MeV 0$^{\circ}$', '226 MeV 0$^{\circ}$']

out_names = ['rez_00', 'rez_45', 'rez_60', 'rez_75', 'rez_85',
             'ptc_00', 'ptc_45', 'ptc_60', 'ptc_75', 'ptc_85']

out_names_new = ['rez_00_13mev', 'rez_00_22mev', 'rez_00_31mev', 'ptc_00_100mev', 'ptc_00_226mev']

thickness = 65

"""
# Figure 2 - create matrices of deposited energy, not filtered

for idx, var in enumerate(paths):
    FileInPath = var
    FolderInPath = FileInPath + 'Files\\'
    FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\'
    print(FolderInPath)

    #filename_elist = 'ExtElist.txt'
    #elist_path = FolderInPath + filename_elist
    #elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')

    clog = read_clog_multiple(FolderInPath)

    number_of_clusters = 2000
    energy_matrix = create_matrix_tpx3_t3pa(clog, number_of_clusters)[0]

    print(type(energy_matrix))

    energy_colorbar_max_value = 1000

    print_figure_energy(energy_matrix, energy_colorbar_max_value, labels[idx], FolderOut, out_names[idx] + '_all')


# Figure 3 - matrix with two rows, top row is low energy, bottom row is high energy
# 5 submatrices showing all particles detected under different angle of beam incidence

FolderInPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\'
two_row_energy_matrix = np.zeros([160,400])

rez_00deg = np.loadtxt(FolderInPath + 'rez_00_all.txt')
rez_45deg = np.loadtxt(FolderInPath + 'rez_45_all.txt')
rez_60deg = np.loadtxt(FolderInPath + 'rez_60_all.txt')
rez_75deg = np.loadtxt(FolderInPath + 'rez_75_all.txt')
rez_85deg = np.loadtxt(FolderInPath + 'rez_85_all.txt')
ptc_00deg = np.loadtxt(FolderInPath + 'ptc_00_all.txt')
ptc_45deg = np.loadtxt(FolderInPath + 'ptc_45_all.txt')
ptc_60deg = np.loadtxt(FolderInPath + 'ptc_60_all.txt')
ptc_75deg = np.loadtxt(FolderInPath + 'ptc_75_all.txt')
ptc_85deg = np.loadtxt(FolderInPath + 'ptc_85_all.txt')

two_row_energy_matrix[0:80,0:80] = rez_85deg[120:200,175:255]
two_row_energy_matrix[0:80,80:160] = rez_75deg[80:160,80:160]
two_row_energy_matrix[0:80,160:240] = rez_60deg[80:160,80:160]
two_row_energy_matrix[0:80,240:320] = rez_45deg[80:160,80:160] 
two_row_energy_matrix[0:80,320:400] = rez_00deg[80:160,80:160] 

two_row_energy_matrix[80:160,0:80,] = ptc_85deg[80:160,175:255]
two_row_energy_matrix[80:160,80:160] = ptc_75deg[80:160,80:160]
two_row_energy_matrix[80:160,160:240] = ptc_60deg[80:160,80:160]
two_row_energy_matrix[80:160,240:320] = ptc_45deg[80:160,80:160] 
two_row_energy_matrix[80:160,320:400] = ptc_00deg[80:160,80:160] 

energy_colorbar_max_value = 1000
print_figure_energy_iworid_2023(two_row_energy_matrix, energy_colorbar_max_value, ' ', FolderInPath, '03_fig_deposited_energy')



#   Figure 4 - spatial homogeneity of clusters - perpendicular direction 0 degrees, filtered particles


filename_elist = 'ExtElist.txt'
rez_elist_path_00deg = paths_new[2] + 'Files\\' + filename_elist
rez_elist_data_00deg = np.loadtxt(rez_elist_path_00deg, skiprows=2, delimiter=';')

ptc_elist_path_00deg = paths[5] + 'Files\\' + filename_elist
ptc_elist_data_00deg = np.loadtxt(ptc_elist_path_00deg, skiprows=2, delimiter=';')

rez_centroid_matrix = np.zeros([256,256])
ptc_centroid_matrix = np.zeros([256,256])

counter_le = 0
counter_he = 0

for i in range(len(rez_elist_data_00deg[:,0])):
    x_position = int(mm_to_px(rez_elist_data_00deg[i,2]))
    y_position = int(mm_to_px(rez_elist_data_00deg[i,3]))
    
    if rez_elist_data_00deg[i,4] >= 500 and rez_elist_data_00deg[i,7] >= 4 and counter_le < 24000:
        rez_centroid_matrix[x_position, y_position] += rez_elist_data_00deg[i,4]
        counter_le += 1
print(f"Median value of cluster energy is {np.median(rez_elist_data_00deg[:,4])}")

for i in range(len(ptc_elist_data_00deg[:,0])):
    x_position = int(mm_to_px(ptc_elist_data_00deg[i,2]))
    y_position = int(mm_to_px(ptc_elist_data_00deg[i,3]))
    
    if ptc_elist_data_00deg[i,4] >= 40 and ptc_elist_data_00deg[i,7] >= 2 and counter_he < 24000:
        ptc_centroid_matrix[x_position, y_position] += ptc_elist_data_00deg[i,4]
        counter_he += 1
print(f"Median value of cluster energy is {np.median(ptc_elist_data_00deg[:,4])}")

print(f'The count of LE particles is {counter_le}')
print(f'The count of HE particles is {counter_he}')

FolderInPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\'
energy_colorbar_max_value = 7000
print_figure_energy(rez_centroid_matrix, energy_colorbar_max_value, ' ', FolderInPath, '04_fig_dep_E_centroid_rez')
print_figure_energy(ptc_centroid_matrix, energy_colorbar_max_value, ' ', FolderInPath, '04_fig_dep_E_centroid_ptc')
"""

#
# NEXT TASK - distribution of energy, LET and track length
# 31 MeV multiple angles, 226 MeV multiple angles, plotted in each
# print out as txt and then plot as a dashed or full line

filename_elist = 'ExtElist.txt'

rez_elist_path_00deg_31mev = paths_new[0] + 'Files\\' + filename_elist
rez_elist_path_00deg_22mev = paths_new[1] + 'Files\\' + filename_elist
rez_elist_path_00deg_13mev = paths_new[2] + 'Files\\' + filename_elist
ptc_elist_path_00deg_100mev = paths_new[3] + 'Files\\' + filename_elist
ptc_elist_path_00deg_226mev = paths_new[4] + 'Files\\' + filename_elist

rez_elist_data_00deg_31mev = np.loadtxt(rez_elist_path_00deg_31mev, skiprows=2, delimiter=';')
rez_elist_data_00deg_22mev = np.loadtxt(rez_elist_path_00deg_22mev, skiprows=2, delimiter=';')
rez_elist_data_00deg_13mev = np.loadtxt(rez_elist_path_00deg_13mev, skiprows=2, delimiter=';')
ptc_elist_data_00deg_100mev = np.loadtxt(ptc_elist_path_00deg_100mev, skiprows=2, delimiter=';')
ptc_elist_data_00deg_226mev = np.loadtxt(ptc_elist_path_00deg_226mev, skiprows=2, delimiter=';')

rez_elist_path_00deg = paths[0] + 'Files\\' + filename_elist
rez_elist_path_45deg = paths[1] + 'Files\\' + filename_elist
rez_elist_path_60deg = paths[2] + 'Files\\' + filename_elist
rez_elist_path_75deg = paths[3] + 'Files\\' + filename_elist
rez_elist_path_85deg = paths[4] + 'Files\\' + filename_elist

rez_elist_data_00deg = np.loadtxt(rez_elist_path_00deg, skiprows=2, delimiter=';')
rez_elist_data_45deg = np.loadtxt(rez_elist_path_45deg, skiprows=2, delimiter=';')
rez_elist_data_60deg = np.loadtxt(rez_elist_path_60deg, skiprows=2, delimiter=';')
rez_elist_data_75deg = np.loadtxt(rez_elist_path_75deg, skiprows=2, delimiter=';')
rez_elist_data_85deg = np.loadtxt(rez_elist_path_85deg, skiprows=2, delimiter=';')

ptc_elist_path_00deg = paths[5] + 'Files\\' + filename_elist
ptc_elist_path_45deg = paths[6] + 'Files\\' + filename_elist
ptc_elist_path_60deg = paths[7] + 'Files\\' + filename_elist
ptc_elist_path_75deg = paths[8] + 'Files\\' + filename_elist
ptc_elist_path_85deg = paths[9] + 'Files\\' + filename_elist

ptc_elist_data_00deg = np.loadtxt(ptc_elist_path_00deg, skiprows=2, delimiter=';')
ptc_elist_data_45deg = np.loadtxt(ptc_elist_path_45deg, skiprows=2, delimiter=';')
ptc_elist_data_60deg = np.loadtxt(ptc_elist_path_60deg, skiprows=2, delimiter=';')
ptc_elist_data_75deg = np.loadtxt(ptc_elist_path_75deg, skiprows=2, delimiter=';')
ptc_elist_data_85deg = np.loadtxt(ptc_elist_path_85deg, skiprows=2, delimiter=';')

#Non-filtered distributions

energy_minimum = 0
energy_maximum = 4000
size_minimum = 4
size_maximum = 20000

y_top_limit = 1E5
y_bottom_limit = 5

#bins = np.array([1500, 600000, 2000000])
bins = np.array([256, 1024, 1024])
bins_length = np.array([70, 128])

FolderInPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\'
"""
plt.close()
plt.clf()
plt.cla()
a = plt.hist(rez_elist_data_00deg, bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(rez_elist_data_45deg, bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(rez_elist_data_60deg, bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(rez_elist_data_75deg, bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(rez_elist_data_85deg, bins=bins[0], histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
f = plt.hist(ptc_elist_data_00deg, bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(ptc_elist_data_45deg, bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(ptc_elist_data_60deg, bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(ptc_elist_data_75deg, bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(ptc_elist_data_85deg, bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '06_fig_all_energy_histogram_not_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
f = plt.hist(ptc_elist_data_00deg, bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(ptc_elist_data_45deg, bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(ptc_elist_data_60deg, bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(ptc_elist_data_75deg, bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(ptc_elist_data_85deg, bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '06_fig_rez_energy_histogram_not_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
f = plt.hist(ptc_elist_data_00deg, bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(ptc_elist_data_45deg, bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(ptc_elist_data_60deg, bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(ptc_elist_data_75deg, bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(ptc_elist_data_85deg, bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '06_fig_ptc_energy_histogram_not_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

y_top_limit = 1E5

plt.close()
plt.clf()
plt.cla()
a = plt.hist(rez_elist_data_00deg[:,13], bins=150, histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(rez_elist_data_45deg[:,13], bins=50, histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(rez_elist_data_60deg[:,13], bins=88, histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(rez_elist_data_75deg[:,13], bins=36, histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(rez_elist_data_85deg[:,13], bins=60, histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
f = plt.hist(ptc_elist_data_00deg[:,13], bins=124, histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(ptc_elist_data_45deg[:,13], bins=224, histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(ptc_elist_data_60deg[:,13], bins=150, histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(ptc_elist_data_75deg[:,13], bins=200, histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(ptc_elist_data_85deg[:,13], bins=238, histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E4)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('3D track length [$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster 3D length distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '07_fig_all_length_histogram_non_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
a = plt.hist(rez_elist_data_00deg[:,13], bins=150, histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(rez_elist_data_45deg[:,13], bins=50, histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(rez_elist_data_60deg[:,13], bins=88, histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(rez_elist_data_75deg[:,13], bins=36, histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(rez_elist_data_85deg[:,13], bins=60, histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E4)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('3D track length [$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster 3D length distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '07_fig_rez_length_histogram_non_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
f = plt.hist(ptc_elist_data_00deg[:,13], bins=124, histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(ptc_elist_data_45deg[:,13], bins=224, histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(ptc_elist_data_60deg[:,13], bins=150, histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(ptc_elist_data_75deg[:,13], bins=200, histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(ptc_elist_data_85deg[:,13], bins=238, histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E4)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('3D track length [$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster 3D length distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '07_fig_ptc_length_histogram_non_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

y_top_limit = 1E4

let_a = (rez_elist_data_00deg[:,4] / np.sqrt((rez_elist_data_00deg[:,13] * 55)**2 + thickness**2)) / np.max(rez_elist_data_00deg[:,4]),
let_b = (rez_elist_data_45deg[:,4] / np.sqrt((rez_elist_data_45deg[:,13] * 55)**2 + thickness**2)) / np.max(rez_elist_data_45deg[:,4]),
let_c = (rez_elist_data_60deg[:,4] / np.sqrt((rez_elist_data_60deg[:,13] * 55)**2 + thickness**2)) / np.max(rez_elist_data_60deg[:,4]),
let_d = (rez_elist_data_75deg[:,4] / np.sqrt((rez_elist_data_75deg[:,13] * 55)**2 + thickness**2)) / np.max(rez_elist_data_75deg[:,4]),
let_e = (rez_elist_data_85deg[:,4] / np.sqrt((rez_elist_data_85deg[:,13] * 55)**2 + thickness**2)) / np.max(rez_elist_data_85deg[:,4]),
let_f = (ptc_elist_data_00deg[:,4] / np.sqrt((ptc_elist_data_00deg[:,13] * 55)**2 + thickness**2)) / np.max(ptc_elist_data_00deg[:,4]),
let_g = (ptc_elist_data_45deg[:,4] / np.sqrt((ptc_elist_data_45deg[:,13] * 55)**2 + thickness**2)) / np.max(ptc_elist_data_45deg[:,4]),
let_h = (ptc_elist_data_60deg[:,4] / np.sqrt((ptc_elist_data_60deg[:,13] * 55)**2 + thickness**2)) / np.max(ptc_elist_data_60deg[:,4]),
let_i = (ptc_elist_data_75deg[:,4] / np.sqrt((ptc_elist_data_75deg[:,13] * 55)**2 + thickness**2)) / np.max(ptc_elist_data_75deg[:,4]),
let_j = (ptc_elist_data_85deg[:,4] / np.sqrt((ptc_elist_data_85deg[:,13] * 55)**2 + thickness**2)) / np.max(ptc_elist_data_85deg[:,4]),

plt.close()
plt.clf()
plt.cla()
a = plt.hist(let_a, bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(let_b, bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(let_c, bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(let_d, bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(let_e, bins=bins[0], histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
f = plt.hist(let_f, bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(let_g, bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(let_h, bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(let_i, bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(let_j, bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.1, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '08_fig_all_LET_histogram_non_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
a = plt.hist(let_a, bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(let_b, bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(let_c, bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(let_d, bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(let_e, bins=bins[0], histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.1, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '08_fig_rez_LET_histogram_non_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
f = plt.hist(let_f, bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(let_g, bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(let_h, bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(let_i, bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(let_j, bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.1, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '08_fig_ptc_LET_histogram_non_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""

filter_parameters_rez_00_31mev = Cluster_filter_multiple_parameter([180, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_00deg_31mev = read_elist_filter_numpy(rez_elist_data_00deg_31mev, filter_parameters_rez_00_31mev)

filter_parameters_rez_00_22mev = Cluster_filter_multiple_parameter([300, 900, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_00deg_22mev = read_elist_filter_numpy(rez_elist_data_00deg_22mev, filter_parameters_rez_00_22mev)

filter_parameters_rez_00_13mev = Cluster_filter_multiple_parameter([500, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_00deg_13mev = read_elist_filter_numpy(rez_elist_data_00deg_13mev, filter_parameters_rez_00_13mev)

filter_parameters_ptc_00_100mev = Cluster_filter_multiple_parameter([90, energy_maximum, 2, size_maximum], [4,7]) # Energy, Size
filtered_ptc_elist_data_00deg_100mev = read_elist_filter_numpy(ptc_elist_data_00deg_100mev, filter_parameters_ptc_00_100mev)

filter_parameters_ptc_00_226mev = Cluster_filter_multiple_parameter([40, energy_maximum, 2, size_maximum], [4,7]) # Energy, Size
filtered_ptc_elist_data_00deg_226mev = read_elist_filter_numpy(ptc_elist_data_00deg_226mev, filter_parameters_ptc_00_226mev)



"""
filter_parameters_rez_00 = Cluster_filter_multiple_parameter([160, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_00deg = read_elist_filter_numpy(rez_elist_data_00deg, filter_parameters_rez_00)

filter_parameters_rez_45 = Cluster_filter_multiple_parameter([290, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_45deg = read_elist_filter_numpy(rez_elist_data_45deg, filter_parameters_rez_45)

filter_parameters_rez_60 = Cluster_filter_multiple_parameter([440, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_60deg = read_elist_filter_numpy(rez_elist_data_60deg, filter_parameters_rez_60)

filter_parameters_rez_75 = Cluster_filter_multiple_parameter([600, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_75deg = read_elist_filter_numpy(rez_elist_data_75deg, filter_parameters_rez_75)

filter_parameters_rez_85 = Cluster_filter_multiple_parameter([700, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_rez_elist_data_85deg = read_elist_filter_numpy(rez_elist_data_85deg, filter_parameters_rez_85)

filter_parameters_ptc_00 = Cluster_filter_multiple_parameter([180, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_ptc_elist_data_00deg = read_elist_filter_numpy(ptc_elist_data_00deg, filter_parameters_ptc_00)

filter_parameters_ptc_45 = Cluster_filter_multiple_parameter([240, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_ptc_elist_data_45deg = read_elist_filter_numpy(ptc_elist_data_45deg, filter_parameters_ptc_45)

filter_parameters_ptc_60 = Cluster_filter_multiple_parameter([240, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_ptc_elist_data_60deg = read_elist_filter_numpy(ptc_elist_data_60deg, filter_parameters_ptc_60)

filter_parameters_ptc_75 = Cluster_filter_multiple_parameter([240, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_ptc_elist_data_75deg = read_elist_filter_numpy(ptc_elist_data_75deg, filter_parameters_ptc_75)

filter_parameters_ptc_85 = Cluster_filter_multiple_parameter([450, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy, Size
filtered_ptc_elist_data_85deg = read_elist_filter_numpy(ptc_elist_data_85deg, filter_parameters_ptc_85)
"""

plt.close()
plt.clf()
plt.cla()
a = plt.hist(filtered_rez_elist_data_00deg_13mev[filtered_rez_elist_data_00deg_13mev[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels_new[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(filtered_rez_elist_data_00deg_22mev[filtered_rez_elist_data_00deg_22mev[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels_new[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(filtered_rez_elist_data_00deg_31mev[filtered_rez_elist_data_00deg_31mev[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels_new[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(filtered_ptc_elist_data_00deg_100mev[filtered_ptc_elist_data_00deg_100mev[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels_new[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(filtered_ptc_elist_data_00deg_226mev[filtered_ptc_elist_data_00deg_226mev[:,-1] == 1][:,4], bins=bins[2], histtype = 'step', label=labels_new[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=45, right=1E4)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '00_fig_energy_histogram_00deg.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
a_ys = a[0] / np.max(a[0])
a_xs = a[1]
b_ys = b[0] / np.max(b[0])
b_xs = b[1]
c_ys = c[0] / np.max(c[0])
c_xs = c[1]
d_ys = d[0] / np.max(d[0])
d_xs = d[1]
e_ys = e[0] / np.max(e[0])
e_xs = e[1]
np.savetxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[0]) + '.txt', np.c_[a_xs[1:], a_ys])
np.savetxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[1]) + '.txt', np.c_[b_xs[1:], b_ys])
np.savetxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[2]) + '.txt', np.c_[c_xs[1:], c_ys])
np.savetxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[3]) + '.txt', np.c_[d_xs[1:], d_ys])
np.savetxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[4]) + '.txt', np.c_[e_xs[1:], e_ys])

a = np.loadtxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[0]) + '.txt')
b = np.loadtxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[1]) + '.txt')
c = np.loadtxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[2]) + '.txt')
d = np.loadtxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[3]) + '.txt')
e = np.loadtxt(FolderInPath+ 'normalised_energy_histogram_values_' + str(out_names_new[4]) + '.txt')

plt.close()
plt.clf()
plt.cla()
plt.plot(a[:,0], a[:,1], label=labels_new[0], linewidth=lin_wd, alpha=alpha_val)
plt.plot(b[:,0], b[:,1], label=labels_new[1], linewidth=lin_wd, alpha=alpha_val)
plt.plot(c[:,0], c[:,1], label=labels_new[2], linewidth=lin_wd, alpha=alpha_val)
plt.plot(d[:,0], d[:,1], label=labels_new[3], linewidth=lin_wd, alpha=alpha_val)
plt.plot(e[:,0], e[:,1], label=labels_new[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=45, right=1E4)
plt.ylim(bottom=0, top=1.1)
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Normalised particle count [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '00_fig_energy_histogram_00deg_normalised.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)





let_a = filtered_rez_elist_data_00deg_31mev[filtered_rez_elist_data_00deg_31mev[:,-1] == 1][:,4] / thickness
let_b = filtered_rez_elist_data_00deg_22mev[filtered_rez_elist_data_00deg_22mev[:,-1] == 1][:,4] / thickness
let_c = filtered_rez_elist_data_00deg_13mev[filtered_rez_elist_data_00deg_13mev[:,-1] == 1][:,4] / thickness
let_d = filtered_ptc_elist_data_00deg_100mev[filtered_ptc_elist_data_00deg_100mev[:,-1] == 1][:,4] / thickness
let_e = filtered_ptc_elist_data_00deg_226mev[filtered_ptc_elist_data_00deg_226mev[:,-1] == 1][:,4] / thickness

plt.close()
plt.clf()
plt.cla()
a = plt.hist(let_c, bins=bins[0], histtype = 'step', label=labels_new[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(let_b, bins=bins[0], histtype = 'step', label=labels_new[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(let_a, bins=bins[0], histtype = 'step', label=labels_new[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(let_d, bins=bins[1], histtype = 'step', label=labels_new[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(let_e, bins=bins[2], histtype = 'step', label=labels_new[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.7, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '00_fig_LET_histogram_00deg.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
a_ys = a[0] / np.max(a[0])
a_xs = a[1]
b_ys = b[0] / np.max(b[0])
b_xs = b[1]
c_ys = c[0] / np.max(c[0])
c_xs = c[1]
d_ys = d[0] / np.max(d[0])
d_xs = d[1]
e_ys = e[0] / np.max(e[0])
e_xs = e[1]
np.savetxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[0]) + '.txt', np.c_[a_xs[1:], a_ys])
np.savetxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[1]) + '.txt', np.c_[b_xs[1:], b_ys])
np.savetxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[2]) + '.txt', np.c_[c_xs[1:], c_ys])
np.savetxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[3]) + '.txt', np.c_[d_xs[1:], d_ys])
np.savetxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[4]) + '.txt', np.c_[e_xs[1:], e_ys])

a = np.loadtxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[0]) + '.txt')
b = np.loadtxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[1]) + '.txt')
c = np.loadtxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[2]) + '.txt')
d = np.loadtxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[3]) + '.txt')
e = np.loadtxt(FolderInPath+ 'normalised_let_histogram_values_' + str(out_names_new[4]) + '.txt')

plt.close()
plt.clf()
plt.cla()
plt.plot(a[:,0], a[:,1], label=labels_new[0], linewidth=lin_wd, alpha=alpha_val)
plt.plot(b[:,0], b[:,1], label=labels_new[1], linewidth=lin_wd, alpha=alpha_val)
plt.plot(c[:,0], c[:,1], label=labels_new[2], linewidth=lin_wd, alpha=alpha_val)
plt.plot(d[:,0], d[:,1], label=labels_new[3], linewidth=lin_wd, alpha=alpha_val)
plt.plot(e[:,0], e[:,1], label=labels_new[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.7, right=100)
plt.ylim(bottom=0, top=1.1)
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Normalised particle count [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '00_fig_LET_histogram_00deg_normalised.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)




plt.close()
plt.clf()
plt.cla()
a = plt.hist(filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
f = plt.hist(filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=100, right=1E5)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_a_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""
a_ys = a[0]
a_xs = a[1]
b_ys = b[0]
b_xs = b[1]
c_ys = c[0]
c_xs = c[1]
d_ys = d[0]
d_xs = d[1]
e_ys = e[0]
e_xs = e[1]
f_ys = f[0]
f_xs = f[1]
g_ys = g[0]
g_xs = g[1]
h_ys = h[0]
h_xs = h[1]
i_ys = i[0]
i_xs = i[1]
j_ys = j[0]
j_xs = j[1]

np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[0]) + '.txt', np.c_[a_xs[1:], a_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[1]) + '.txt', np.c_[b_xs[1:], b_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[2]) + '.txt', np.c_[c_xs[1:], c_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[3]) + '.txt', np.c_[d_xs[1:], d_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[4]) + '.txt', np.c_[e_xs[1:], e_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[5]) + '.txt', np.c_[f_xs[1:], f_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[6]) + '.txt', np.c_[g_xs[1:], g_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[7]) + '.txt', np.c_[h_xs[1:], h_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[8]) + '.txt', np.c_[i_xs[1:], i_ys])
np.savetxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[9]) + '.txt', np.c_[j_xs[1:], j_ys])

a = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[0]) + '.txt')
b = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[1]) + '.txt')
c = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[2]) + '.txt')
d = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[3]) + '.txt')
e = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[4]) + '.txt')
f = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[5]) + '.txt')
g = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[6]) + '.txt')
h = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[7]) + '.txt')
i = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[8]) + '.txt')
j = np.loadtxt(FolderInPath+ 'energy_histogram_values_' + str(out_names[9]) + '.txt')

plt.close()
plt.clf()
plt.cla()
plt.plot(a[:,0], a[:,1], label=labels[0], linewidth=lin_wd, alpha=alpha_val)
plt.plot(b[:,0], b[:,1], label=labels[1], linewidth=lin_wd, alpha=alpha_val)
plt.plot(c[:,0], c[:,1], label=labels[2], linewidth=lin_wd, alpha=alpha_val)
plt.plot(d[:,0], d[:,1], label=labels[3], linewidth=lin_wd, alpha=alpha_val)
plt.plot(e[:,0], e[:,1], label=labels[4], linewidth=lin_wd, alpha=alpha_val)
plt.plot(f[:,0], f[:,1], linestyle='dashed', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
plt.plot(g[:,0], g[:,1], linestyle='dashed', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
plt.plot(h[:,0], h[:,1], linestyle='dashed', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
plt.plot(i[:,0], i[:,1], linestyle='dashed', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
plt.plot(j[:,0], j[:,1], linestyle='dashed', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=100, right=1E5)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_a_energy_histogram_dashed_lines.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""

plt.close()
plt.clf()
plt.cla()
a = plt.hist(filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,4], bins=1024, histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=100, right=1E5)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_aa_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
f = plt.hist(filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=100, right=1E5)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_ab_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

#
# Track length
#
y_top_limit = 1E5

plt.close()
plt.clf()
plt.cla()
a = plt.hist(np.sqrt((filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=150, histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(np.sqrt((filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=50, histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(np.sqrt((filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=88, histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(np.sqrt((filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=36, histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(np.sqrt((filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=60, histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
f = plt.hist(np.sqrt((filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=124, histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(np.sqrt((filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=224, histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(np.sqrt((filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=150, histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(np.sqrt((filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=200, histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(np.sqrt((filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=238, histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=65, right=1E4)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('3D track length [$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster 3D length distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_b_length_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""
a_ys = a[0]
a_xs = a[1]
b_ys = b[0]
b_xs = b[1]
c_ys = c[0]
c_xs = c[1]
d_ys = d[0]
d_xs = d[1]
e_ys = e[0]
e_xs = e[1]
f_ys = f[0]
f_xs = f[1]
g_ys = g[0]
g_xs = g[1]
h_ys = h[0]
h_xs = h[1]
i_ys = i[0]
i_xs = i[1]
j_ys = j[0]
j_xs = j[1]

np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[0]) + '.txt', np.c_[a_xs[1:], a_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[1]) + '.txt', np.c_[b_xs[1:], b_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[2]) + '.txt', np.c_[c_xs[1:], c_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[3]) + '.txt', np.c_[d_xs[1:], d_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[4]) + '.txt', np.c_[e_xs[1:], e_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[5]) + '.txt', np.c_[f_xs[1:], f_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[6]) + '.txt', np.c_[g_xs[1:], g_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[7]) + '.txt', np.c_[h_xs[1:], h_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[8]) + '.txt', np.c_[i_xs[1:], i_ys])
np.savetxt(FolderInPath+ 'length_histogram_values_' + str(out_names[9]) + '.txt', np.c_[j_xs[1:], j_ys])

a = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[0]) + '.txt')
b = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[1]) + '.txt')
c = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[2]) + '.txt')
d = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[3]) + '.txt')
e = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[4]) + '.txt')
f = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[5]) + '.txt')
g = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[6]) + '.txt')
h = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[7]) + '.txt')
i = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[8]) + '.txt')
j = np.loadtxt(FolderInPath+ 'length_histogram_values_' + str(out_names[9]) + '.txt')

plt.close()
plt.clf()
plt.cla()
plt.plot(a[:,0], a[:,1], label=labels[0], linewidth=lin_wd, alpha=alpha_val)
plt.plot(b[:,0], b[:,1], label=labels[1], linewidth=lin_wd, alpha=alpha_val)
plt.plot(c[:,0], c[:,1], label=labels[2], linewidth=lin_wd, alpha=alpha_val)
plt.plot(d[:,0], d[:,1], label=labels[3], linewidth=lin_wd, alpha=alpha_val)
plt.plot(e[:,0], e[:,1], label=labels[4], linewidth=lin_wd, alpha=alpha_val)
plt.plot(f[:,0], f[:,1], linestyle='dashed', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
plt.plot(g[:,0], g[:,1], linestyle='dashed', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
plt.plot(h[:,0], h[:,1], linestyle='dashed', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
plt.plot(i[:,0], i[:,1], linestyle='dashed', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
plt.plot(j[:,0], j[:,1], linestyle='dashed', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=65, right=1E4)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Length distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_b_length_histogram_dashed_lines.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""


#
# LET
#
y_top_limit = 1E4

let_a = filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,4] / np.sqrt((filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_b = filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,4] / np.sqrt((filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_c = filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,4] / np.sqrt((filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_d = filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,4] / np.sqrt((filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_e = filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,4] / np.sqrt((filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_f = filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,4] / np.sqrt((filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_g = filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,4] / np.sqrt((filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_h = filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,4] / np.sqrt((filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_i = filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,4] / np.sqrt((filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),
let_j = filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,4] / np.sqrt((filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,13] * 55)**2 + thickness**2),

plt.close()
plt.clf()
plt.cla()
a = plt.hist(let_a, bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(let_b, bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(let_c, bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(let_d, bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(let_e, bins=bins[0], histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.7, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_ca_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
f = plt.hist(let_f, bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(let_g, bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(let_h, bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(let_i, bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(let_j, bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.7, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_cb_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
a = plt.hist(let_a, bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
b = plt.hist(let_b, bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
c = plt.hist(let_c, bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
d = plt.hist(let_d, bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
e = plt.hist(let_e, bins=bins[0], histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
f = plt.hist(let_f, bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
g = plt.hist(let_g, bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
h = plt.hist(let_h, bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
i = plt.hist(let_i, bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
j = plt.hist(let_j, bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.7, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_c_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""
a_ys = a[0]
a_xs = a[1]
b_ys = b[0]
b_xs = b[1]
c_ys = c[0]
c_xs = c[1]
d_ys = d[0]
d_xs = d[1]
e_ys = e[0]
e_xs = e[1]
f_ys = f[0]
f_xs = f[1]
g_ys = g[0]
g_xs = g[1]
h_ys = h[0]
h_xs = h[1]
i_ys = i[0]
i_xs = i[1]
j_ys = j[0]
j_xs = j[1]


np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[0]) + '.txt', np.c_[a_xs[1:], a_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[1]) + '.txt', np.c_[b_xs[1:], b_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[2]) + '.txt', np.c_[c_xs[1:], c_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[3]) + '.txt', np.c_[d_xs[1:], d_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[4]) + '.txt', np.c_[e_xs[1:], e_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[5]) + '.txt', np.c_[f_xs[1:], f_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[6]) + '.txt', np.c_[g_xs[1:], g_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[7]) + '.txt', np.c_[h_xs[1:], h_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[8]) + '.txt', np.c_[i_xs[1:], i_ys])
np.savetxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[9]) + '.txt', np.c_[j_xs[1:], j_ys])

a = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[0]) + '.txt')
b = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[1]) + '.txt')
c = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[2]) + '.txt')
d = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[3]) + '.txt')
e = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[4]) + '.txt')
f = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[5]) + '.txt')
g = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[6]) + '.txt')
h = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[7]) + '.txt')
i = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[8]) + '.txt')
j = np.loadtxt(FolderInPath+ 'LET_histogram_values_' + str(out_names[9]) + '.txt')

plt.close()
plt.clf()
plt.cla()
plt.plot(a[:,0], a[:,1], label=labels[0], linewidth=lin_wd, alpha=alpha_val)
plt.plot(b[:,0], b[:,1], label=labels[1], linewidth=lin_wd, alpha=alpha_val)
plt.plot(c[:,0], c[:,1], label=labels[2], linewidth=lin_wd, alpha=alpha_val)
plt.plot(d[:,0], d[:,1], label=labels[3], linewidth=lin_wd, alpha=alpha_val)
plt.plot(e[:,0], e[:,1], label=labels[4], linewidth=lin_wd, alpha=alpha_val)
plt.plot(f[:,0], f[:,1], linestyle='dashed', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
plt.plot(g[:,0], g[:,1], linestyle='dashed', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
plt.plot(h[:,0], h[:,1], linestyle='dashed', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
plt.plot(i[:,0], i[:,1], linestyle='dashed', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
plt.plot(j[:,0], j[:,1], linestyle='dashed', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=0.7, right=100)
plt.ylim(bottom=y_bottom_limit, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(FolderInPath + '05_fig_c_LET_histogram_dashed_lines.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""

"""
###################################################################################################
#
# Finding the optimal binning - Track length
#
###################################################################################################

filename_elist = 'ExtElist.txt'

rez_elist_path_00deg = paths[0] + 'Files\\' + filename_elist
rez_elist_path_45deg = paths[1] + 'Files\\' + filename_elist
rez_elist_path_60deg = paths[2] + 'Files\\' + filename_elist
rez_elist_path_75deg = paths[3] + 'Files\\' + filename_elist
rez_elist_path_85deg = paths[4] + 'Files\\' + filename_elist

rez_elist_data_00deg = np.loadtxt(rez_elist_path_00deg, skiprows=2, delimiter=';')
rez_elist_data_45deg = np.loadtxt(rez_elist_path_45deg, skiprows=2, delimiter=';')
rez_elist_data_60deg = np.loadtxt(rez_elist_path_60deg, skiprows=2, delimiter=';')
rez_elist_data_75deg = np.loadtxt(rez_elist_path_75deg, skiprows=2, delimiter=';')
rez_elist_data_85deg = np.loadtxt(rez_elist_path_85deg, skiprows=2, delimiter=';')

ptc_elist_path_00deg = paths[5] + 'Files\\' + filename_elist
ptc_elist_path_45deg = paths[6] + 'Files\\' + filename_elist
ptc_elist_path_60deg = paths[7] + 'Files\\' + filename_elist
ptc_elist_path_75deg = paths[8] + 'Files\\' + filename_elist
ptc_elist_path_85deg = paths[9] + 'Files\\' + filename_elist

ptc_elist_data_00deg = np.loadtxt(ptc_elist_path_00deg, skiprows=2, delimiter=';')
ptc_elist_data_45deg = np.loadtxt(ptc_elist_path_45deg, skiprows=2, delimiter=';')
ptc_elist_data_60deg = np.loadtxt(ptc_elist_path_60deg, skiprows=2, delimiter=';')
ptc_elist_data_75deg = np.loadtxt(ptc_elist_path_75deg, skiprows=2, delimiter=';')
ptc_elist_data_85deg = np.loadtxt(ptc_elist_path_85deg, skiprows=2, delimiter=';')

energy_minimum = 0
energy_maximum = 10000000
size_minimum = 0
size_maximum = 20000

filter_parameters = Cluster_filter_multiple_parameter([energy_minimum, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy

filtered_rez_elist_data_00deg = read_elist_filter_numpy(rez_elist_data_00deg, filter_parameters)
filtered_rez_elist_data_45deg = read_elist_filter_numpy(rez_elist_data_45deg, filter_parameters)
filtered_rez_elist_data_60deg = read_elist_filter_numpy(rez_elist_data_60deg, filter_parameters)
filtered_rez_elist_data_75deg = read_elist_filter_numpy(rez_elist_data_75deg, filter_parameters)
filtered_rez_elist_data_85deg = read_elist_filter_numpy(rez_elist_data_85deg, filter_parameters)

filtered_ptc_elist_data_00deg = read_elist_filter_numpy(ptc_elist_data_00deg, filter_parameters)
filtered_ptc_elist_data_45deg = read_elist_filter_numpy(ptc_elist_data_45deg, filter_parameters)
filtered_ptc_elist_data_60deg = read_elist_filter_numpy(ptc_elist_data_60deg, filter_parameters)
filtered_ptc_elist_data_75deg = read_elist_filter_numpy(ptc_elist_data_75deg, filter_parameters)
filtered_ptc_elist_data_85deg = read_elist_filter_numpy(ptc_elist_data_85deg, filter_parameters)

y_top_limit = 1E6

FolderInPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\histogram_binning\\'

for number in range(300):
    if number == 0:
        binning = 2
    else:
        binning = number * 2

    plt.close()
    plt.clf()
    plt.cla()
    a = plt.hist(filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'a_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    b = plt.hist(filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'b_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    c = plt.hist(filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'c_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    d = plt.hist(filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'd_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    e = plt.hist(filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'e_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    f = plt.hist(filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'f_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    g = plt.hist(filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'g_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    h = plt.hist(filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'h_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    i = plt.hist(filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'i_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    j = plt.hist(filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,13] * 55, bins=binning, histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'j_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)



#
# NEXT TASK - distribution of energy, LET and track length
# 31 MeV multiple angles, 226 MeV multiple angles, plotted in each
# print out as txt and then plot as a dashed or full line

filename_elist = 'ExtElist.txt'

rez_elist_path_00deg = paths[0] + 'Files\\' + filename_elist
rez_elist_path_45deg = paths[1] + 'Files\\' + filename_elist
rez_elist_path_60deg = paths[2] + 'Files\\' + filename_elist
rez_elist_path_75deg = paths[3] + 'Files\\' + filename_elist
rez_elist_path_85deg = paths[4] + 'Files\\' + filename_elist

rez_elist_data_00deg = np.loadtxt(rez_elist_path_00deg, skiprows=2, delimiter=';')
rez_elist_data_45deg = np.loadtxt(rez_elist_path_45deg, skiprows=2, delimiter=';')
rez_elist_data_60deg = np.loadtxt(rez_elist_path_60deg, skiprows=2, delimiter=';')
rez_elist_data_75deg = np.loadtxt(rez_elist_path_75deg, skiprows=2, delimiter=';')
rez_elist_data_85deg = np.loadtxt(rez_elist_path_85deg, skiprows=2, delimiter=';')

ptc_elist_path_00deg = paths[5] + 'Files\\' + filename_elist
ptc_elist_path_45deg = paths[6] + 'Files\\' + filename_elist
ptc_elist_path_60deg = paths[7] + 'Files\\' + filename_elist
ptc_elist_path_75deg = paths[8] + 'Files\\' + filename_elist
ptc_elist_path_85deg = paths[9] + 'Files\\' + filename_elist

ptc_elist_data_00deg = np.loadtxt(ptc_elist_path_00deg, skiprows=2, delimiter=';')
ptc_elist_data_45deg = np.loadtxt(ptc_elist_path_45deg, skiprows=2, delimiter=';')
ptc_elist_data_60deg = np.loadtxt(ptc_elist_path_60deg, skiprows=2, delimiter=';')
ptc_elist_data_75deg = np.loadtxt(ptc_elist_path_75deg, skiprows=2, delimiter=';')
ptc_elist_data_85deg = np.loadtxt(ptc_elist_path_85deg, skiprows=2, delimiter=';')

energy_minimum = 0
energy_maximum = 10000000
size_minimum = 0
size_maximum = 20000

for number in range(300):
    if number == 0:
        energy_minimum = 1
    else:
        energy_minimum = number * 5

    filter_parameters = Cluster_filter_multiple_parameter([energy_minimum, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy

    filtered_rez_elist_data_00deg = read_elist_filter_numpy(rez_elist_data_00deg, filter_parameters)
    filtered_rez_elist_data_45deg = read_elist_filter_numpy(rez_elist_data_45deg, filter_parameters)
    filtered_rez_elist_data_60deg = read_elist_filter_numpy(rez_elist_data_60deg, filter_parameters)
    filtered_rez_elist_data_75deg = read_elist_filter_numpy(rez_elist_data_75deg, filter_parameters)
    filtered_rez_elist_data_85deg = read_elist_filter_numpy(rez_elist_data_85deg, filter_parameters)

    filtered_ptc_elist_data_00deg = read_elist_filter_numpy(ptc_elist_data_00deg, filter_parameters)
    filtered_ptc_elist_data_45deg = read_elist_filter_numpy(ptc_elist_data_45deg, filter_parameters)
    filtered_ptc_elist_data_60deg = read_elist_filter_numpy(ptc_elist_data_60deg, filter_parameters)
    filtered_ptc_elist_data_75deg = read_elist_filter_numpy(ptc_elist_data_75deg, filter_parameters)
    filtered_ptc_elist_data_85deg = read_elist_filter_numpy(ptc_elist_data_85deg, filter_parameters)

    bins = np.array([2048, 600000])

    y_top_limit = 1E5

    FolderInPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\histogram_energy_separately\\'

    plt.close()
    plt.clf()
    plt.cla()
    a = plt.hist(filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'a_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    b = plt.hist(filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'b_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    c = plt.hist(filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'c_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    d = plt.hist(filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'd_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    e = plt.hist(filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,4], bins=bins[0], histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'e_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    f = plt.hist(filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'f_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    g = plt.hist(filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'g_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    h = plt.hist(filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'h_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    i = plt.hist(filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'i_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    j = plt.hist(filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,4], bins=bins[1], histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E5)
    plt.ylim(bottom=1, top=y_top_limit)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Deposited energy distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'j_energy_histogram_' + str(energy_minimum) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)



#
# 3D Track length
#

filename_elist = 'ExtElist.txt'

rez_elist_path_00deg = paths[0] + 'Files\\' + filename_elist
rez_elist_path_45deg = paths[1] + 'Files\\' + filename_elist
rez_elist_path_60deg = paths[2] + 'Files\\' + filename_elist
rez_elist_path_75deg = paths[3] + 'Files\\' + filename_elist
rez_elist_path_85deg = paths[4] + 'Files\\' + filename_elist

rez_elist_data_00deg = np.loadtxt(rez_elist_path_00deg, skiprows=2, delimiter=';')
rez_elist_data_45deg = np.loadtxt(rez_elist_path_45deg, skiprows=2, delimiter=';')
rez_elist_data_60deg = np.loadtxt(rez_elist_path_60deg, skiprows=2, delimiter=';')
rez_elist_data_75deg = np.loadtxt(rez_elist_path_75deg, skiprows=2, delimiter=';')
rez_elist_data_85deg = np.loadtxt(rez_elist_path_85deg, skiprows=2, delimiter=';')

ptc_elist_path_00deg = paths[5] + 'Files\\' + filename_elist
ptc_elist_path_45deg = paths[6] + 'Files\\' + filename_elist
ptc_elist_path_60deg = paths[7] + 'Files\\' + filename_elist
ptc_elist_path_75deg = paths[8] + 'Files\\' + filename_elist
ptc_elist_path_85deg = paths[9] + 'Files\\' + filename_elist

ptc_elist_data_00deg = np.loadtxt(ptc_elist_path_00deg, skiprows=2, delimiter=';')
ptc_elist_data_45deg = np.loadtxt(ptc_elist_path_45deg, skiprows=2, delimiter=';')
ptc_elist_data_60deg = np.loadtxt(ptc_elist_path_60deg, skiprows=2, delimiter=';')
ptc_elist_data_75deg = np.loadtxt(ptc_elist_path_75deg, skiprows=2, delimiter=';')
ptc_elist_data_85deg = np.loadtxt(ptc_elist_path_85deg, skiprows=2, delimiter=';')

energy_minimum = 0
energy_maximum = 10000000
size_minimum = 0
size_maximum = 20000

filter_parameters = Cluster_filter_multiple_parameter([energy_minimum, energy_maximum, size_minimum, size_maximum], [4,7]) # Energy

filtered_rez_elist_data_00deg = read_elist_filter_numpy(rez_elist_data_00deg, filter_parameters)
filtered_rez_elist_data_45deg = read_elist_filter_numpy(rez_elist_data_45deg, filter_parameters)
filtered_rez_elist_data_60deg = read_elist_filter_numpy(rez_elist_data_60deg, filter_parameters)
filtered_rez_elist_data_75deg = read_elist_filter_numpy(rez_elist_data_75deg, filter_parameters)
filtered_rez_elist_data_85deg = read_elist_filter_numpy(rez_elist_data_85deg, filter_parameters)

filtered_ptc_elist_data_00deg = read_elist_filter_numpy(ptc_elist_data_00deg, filter_parameters)
filtered_ptc_elist_data_45deg = read_elist_filter_numpy(ptc_elist_data_45deg, filter_parameters)
filtered_ptc_elist_data_60deg = read_elist_filter_numpy(ptc_elist_data_60deg, filter_parameters)
filtered_ptc_elist_data_75deg = read_elist_filter_numpy(ptc_elist_data_75deg, filter_parameters)
filtered_ptc_elist_data_85deg = read_elist_filter_numpy(ptc_elist_data_85deg, filter_parameters)

y_top_limit = 1E6

FolderInPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\histogram_binning_3D_length\\'

for number in range(300):
    if number == 0:
        binning = 2
    else:
        binning = number * 2

    plt.close()
    plt.clf()
    plt.cla()
    a = plt.hist(np.sqrt((filtered_rez_elist_data_00deg[filtered_rez_elist_data_00deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[0], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'a_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    b = plt.hist(np.sqrt((filtered_rez_elist_data_45deg[filtered_rez_elist_data_45deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[1], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'b_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    c = plt.hist(np.sqrt((filtered_rez_elist_data_60deg[filtered_rez_elist_data_60deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[2], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'c_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    d = plt.hist(np.sqrt((filtered_rez_elist_data_75deg[filtered_rez_elist_data_75deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[3], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'd_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    e = plt.hist(np.sqrt((filtered_rez_elist_data_85deg[filtered_rez_elist_data_85deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[4], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'e_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    f = plt.hist(np.sqrt((filtered_ptc_elist_data_00deg[filtered_ptc_elist_data_00deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[5], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'f_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    g = plt.hist(np.sqrt((filtered_ptc_elist_data_45deg[filtered_ptc_elist_data_45deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[6], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'g_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    h = plt.hist(np.sqrt((filtered_ptc_elist_data_60deg[filtered_ptc_elist_data_60deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[7], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'h_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    i = plt.hist(np.sqrt((filtered_ptc_elist_data_75deg[filtered_ptc_elist_data_75deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[8], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'i_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    j = plt.hist(np.sqrt((filtered_ptc_elist_data_85deg[filtered_ptc_elist_data_85deg[:,-1] == 1][:,13] * 55)**2 + thickness**2), bins=binning, histtype = 'step', label=labels[9], linewidth=lin_wd, alpha=alpha_val)
    plt.xlim(left=1, right=1E4)
    plt.ylim(bottom=1, top=y_top_limit)
    linwid = 2
    plt.axvline(x = 65, color = 'black', linestyle = '-', linewidth = linwid)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Track length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [count]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Cluster 3D length distribution')
    plt.legend(loc='upper right')
    plt.savefig(FolderInPath + 'j_length_histogram_' + str(binning) + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""