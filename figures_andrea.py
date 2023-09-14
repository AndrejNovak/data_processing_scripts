from DPE_functions import *

lin_wd = 1.75
tickfnt = 18
alpha_val = 0.9
mydpi = 300


"""
all_paths = [
'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\08_200V\\',
'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\09_200V\\'
]

all_out_folders = [
'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\',
'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\'
]

label = ['3.5 MeV neutrons', '3 MeV neutrons']

for idx, var in enumerate(all_paths):
    FileInPath = var
    FolderInPath = FileInPath + 'Files\\'
    FolderOut = all_out_folders[idx]
    print(FolderInPath)
    print(FolderOut)
    filename_elist = 'ExtElist.txt'

    elist_path = FolderInPath + filename_elist
    elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
    clog = read_clog_multiple(FolderInPath)

    if len(elist_data[:,0]) == len(clog[:]):
        print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
    else:
        print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

    E_min = np.array([0,500,2000,4000])
    E_max = np.array([50000,50000,50000,50000])
    Size_min = np.array([0,15,30,60])
    Size_max = np.array([10000,10000,10000,10000])

    number_of_particles = len(elist_data[:,0])

    label_to_fig_name = label[idx]

    for k in range(len(E_min)):
        print(f'Filter for Energy range {E_min[k]}-{E_max[k]} keV and size range {Size_min[k]}-{Size_max[k]} px')
        filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max[k], Size_min[k], Size_max[k]], [4,7]) # Energy, Size
        filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
        square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

        energy_colorbar_max_value = 10000

        FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '-' + str(E_max[k]) + '_Size_' + str(Size_min[k]) + '-' + str(Size_max[k])

        #try:
        #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label[idx], FolderOut, FileOutName + '_1_all')
        #except Exception:
        #    pass
        try:
            print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label[idx], FolderOut, FileOutName + '_2_passed')
        except Exception:
            pass
        #try:
        #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label[idx], FolderOut, FileOutName + '_3_failed')
        #except Exception:
        #    pass



'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\02_200V\\',
'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\',
"""

#FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\02_200V\\Files\\'
FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\04_200V\\Files\\'

FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'ExtElist.txt'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

E_min = np.array([100,200,300,400,500])
E_max = np.array([50000,50000,50000,50000,50000])
Size_min = np.array([25,50,75,100,150])
Size_max = np.array([10000,10000,10000,10000,10000])

number_of_particles = len(elist_data[:,0])

label_to_fig_name = '14.8 MeV neutrons'
label_to_fig_name = '16.2 MeV neutrons'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        print(f'Filter for Energy range {E_min[k]}-{E_max[k]} keV and size range {Size_min[l]}-{Size_max[l]} px')
        filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max[k], Size_min[l], Size_max[l]], [4,7]) # Energy, Size
        filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
        square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

        energy_colorbar_max_value = 10000

        FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) 

        #try:
        #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
        #except Exception:
        #    pass
        try:
            print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut, FileOutName + '_2_passed')
        except Exception:
            pass
        #try:
        #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
        #except Exception:
        #    pass