from DPE_functions import *

lin_wd = 1.75
tickfnt = 18
alpha_val = 0.9
mydpi = 300

"""
27 31 MeV 00
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
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\39_10ms\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\60deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\85deg\\'
]

labels = ['31 MeV 0$^{\circ}$', '31 MeV 45$^{\circ}$', '31 MeV 60$^{\circ}$', '31 MeV 75$^{\circ}$', '31 MeV 85$^{\circ}$',
          '226 MeV 0$^{\circ}$', '226 MeV 45$^{\circ}$', '226 MeV 60$^{\circ}$', '226 MeV 75$^{\circ}$', '226 MeV 85$^{\circ}$']

out_names = ['rez_00', 'rez_45', 'rez_60', 'rez_75', 'rez_85',
             'ptc_00', 'ptc_45', 'ptc_60', 'ptc_75', 'ptc_85']

thickness = 65

"""
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
"""

FolderInPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\iworid_article_figures\\'
two_row_energy_matrix = np.zeros([400,160])

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

two_row_energy_matrix[0:80,80:160] = rez_00deg[80:160,80:160]
two_row_energy_matrix[80:160,80:160] = rez_45deg[80:160,80:160]
two_row_energy_matrix[160:240,80:160] = rez_60deg[80:160,80:160]
two_row_energy_matrix[240:320,80:160] = rez_75deg[80:160,80:160]
two_row_energy_matrix[320:400,80:160] = rez_85deg[120:200,175:255]

two_row_energy_matrix[0:80,0:80] = ptc_00deg[80:160,80:160]
two_row_energy_matrix[80:160,0:80] = ptc_45deg[80:160,80:160]
two_row_energy_matrix[160:240,0:80] = ptc_60deg[80:160,80:160]
two_row_energy_matrix[240:320,0:80] = ptc_75deg[80:160,80:160]
two_row_energy_matrix[320:400,0:80] = ptc_85deg[80:160,175:255]

energy_colorbar_max_value = 1000
print_figure_energy_iworid_2023(two_row_energy_matrix, energy_colorbar_max_value, ' ', FolderInPath, '03_fig_deposited_energy')

#
#   NEXT TASK - spatial homogeneity of clusters - perpendicular direction 0 degrees, filtered particles
#




"""
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

rez_clog_00deg = read_clog_multiple(paths[0]+ 'Files\\')
rez_clog_45deg = read_clog_multiple(paths[1]+ 'Files\\')
rez_clog_60deg = read_clog_multiple(paths[2]+ 'Files\\')
rez_clog_75deg = read_clog_multiple(paths[3]+ 'Files\\')
rez_clog_85deg = read_clog_multiple(paths[4]+ 'Files\\')

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

ptc_clog_00deg = read_clog_multiple(paths[5]+ 'Files\\')
ptc_clog_45deg = read_clog_multiple(paths[6]+ 'Files\\')
ptc_clog_60deg = read_clog_multiple(paths[7]+ 'Files\\')
ptc_clog_75deg = read_clog_multiple(paths[8]+ 'Files\\')
ptc_clog_85deg = read_clog_multiple(paths[9]+ 'Files\\')

"""