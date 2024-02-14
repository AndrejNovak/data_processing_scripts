from DPE_functions import *

lin_wd = 1.75
tickfnt = 18
alpha_val = 0.9
mydpi = 300

E_min = np.array([50,100,150,200,250,300,350,400,450,500,1000,2000,3000,5000])
E_max = 50000
Size_min = np.array([5,10,20,30,40,50,60,70,80,90,100,125,150,200])
Size_max = 1000
Roundness_min = np.array([0.201, 0.301, 0.401, 0.501,0.601,0.701,0.751,0.801,0.851,0.901,0.951,0.981,0.991])
Roundness_max = 1.01

"""
FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\01_80V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '01_80V'
folder_name = '01_80V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            #print('test')
            #print(filtered_elist[0,4], filtered_elist[0,7], filtered_elist[0,10])

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass


FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\02_200V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '02_200V'
folder_name = '02_200V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass

FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\03_0V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '03_0V'
folder_name = '03_0V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass


FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\03_80V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '03_80V'
folder_name = '03_80V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass


FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\04_200V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '04_200V'
folder_name = '04_200V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass


FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\05_80V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '05_80V'
folder_name = '05_80V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass



#
# The part of script that ran in the most previous version
# Commented 05.02.2024
#

FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\06_80V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '06_80V'
folder_name = '06_80V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass


FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\07_80V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '07_80V'
folder_name = '07_80V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass


FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\08_200V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '08_200V'
folder_name = '08_200V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass


FolderInPath = 'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\09_200V\\File\\'
FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_article\\'

print(FolderInPath)
print(FolderOut)
filename_elist = 'EventListExt.advelist'

elist_path = FolderInPath + filename_elist
elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
clog = read_clog_multiple(FolderInPath)

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = 2000

label_to_fig_name = '09_200V'
folder_name = '09_200V\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 10000

            FileOutName = str(label_to_fig_name) + '_E_' + str(E_min[k]) + '_Size_' + str(Size_min[l]) + '_Roundness_' + str(Roundness_min[j])

            #try:
            #    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + label_to_fig_name, FolderOut, FileOutName + '_1_all')
            #except Exception:
            #    pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + label_to_fig_name, FolderOut + folder_name, FileOutName + '_2_passed')
            except Exception:
                pass
            #try:
            #    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + label_to_fig_name, FolderOut, FileOutName + '_3_failed')
            #except Exception:
            #    pass

"""

Paths = ['Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\03_0V\\File\\',
         'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\03_80V\\File\\',
         'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\04_200V\\File\\',
         'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\06_80V\\File\\',
         'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\07_80V\\File\\',
         'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\08_200V\\File\\',
         'Q:\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\09_200V\\File\\']

FolderOut = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_clusters\\'
OutPaths = ['03_0V\\',
            '03_80V\\',
            '04_200V\\',
            '06_80V\\',
            '07_80V\\',
            '08_200V\\',
            '09_200V\\']

energies = ['16_2_MeV',
            '16_2_MeV',
            '16_2_MeV',
            '3_5_MeV',
            '3_5_MeV',
            '3_5_MeV',
            '3_MeV']

number_of_particles = 2000

for i in range(len(Paths)):
    FolderInPath = Paths[i]

    print(FolderInPath)
    print(FolderOut)
    filename_elist = 'EventListExt.advelist'

    elist_path = FolderInPath + filename_elist
    elist_data = np.loadtxt(elist_path, skiprows=2, delimiter='\t')
    clog = read_clog_multiple(FolderInPath)

    OutputPath = FolderOut + OutPaths[i]

    passed_clusters = 0

    for j in range(len(clog)):
        vmax = elist_data[j,8] + 100
        title = str(energies[i]) + ' Cluster #' + str(j)
        OutputName = str(energies[i]) + '_cluster'
        if elist_data[j,4] > 100 and elist_data[j,7] > 8 and passed_clusters <= number_of_particles:
            print_figure_single_cluster_energy_event_parameters(clog[j], elist_data, j, vmax, title, OutputPath, OutputName)
            passed_clusters += 1 