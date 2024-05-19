from DPE_functions import *

lin_wd = 2
tickfnt = 18
alpha_val = 0.80
mydpi = 300

clog_paths_X00 = ['\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\06_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\07_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\01_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\03_80V\\File\\']

elist_paths_X00 = [f"{x}EventListExt.advelist" for x in clog_paths_X00]

OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_nim_new\\'
OutputFolder = ['06_80V_3_5MeV', '07_80V_3_5MeV', '01_80V_14_8MeV', '03_80V_16_2MeV']

size_min = np.array([15,  15,  20, 20])
size_max = np.array([150, 150, 200, 200])

energy_min = np.array([800, 800, 1200, 1200])
energy_max = np.array([10000, 10000, 10000, 10000])

height_min = np.array([350, 350, 400, 400])
height_max = np.array([2000, 2000, 2000, 2000])

OutNames = ['3_5MeV', '3_5MeV_2', '14_8MeV', '16_2MeV']
TitleLabel = ['3.5 MeV', '3.5 MeV', '14.8 MeV', '16.2 MeV']
TitleValues = np.array([3.5, 3.5, 14.8, 16.2])

number_of_particles = 1000
number_of_particles_clusters = 200
vmax = 3000

effectivity_kapton = np.empty(0)
effectivity_pe = np.empty(0)
effectivity_nolayer = np.empty(0)

pe_xmin = 15
pe_xmax = 251
pe_ymin = 110
pe_ymax = 195

kapton_xmin = 5
kapton_xmax = 251
kapton_ymin = 200
kapton_ymax = 251

nolayer_xmin = 5
nolayer_xmax = 251
nolayer_ymin = 5
nolayer_ymax = 80

for i in range(len(clog_paths_X00)):
    elist_data = np.loadtxt(elist_paths_X00[i], skiprows=2, delimiter='\t')
    clog_data = read_clog_multiple(clog_paths_X00[i])
    number_of_particles = len(elist_data[:,0])

    filter_parameters = Cluster_filter_multiple_parameter([pe_xmin, pe_xmax, pe_ymin, pe_ymax, energy_min[i], energy_max[i], size_min[i], size_max[i], height_min[i], height_max[i]], [2,3,4,7,8]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
    
    area_pe = (pe_xmax - pe_xmin) * (pe_ymax - pe_ymin) * 3025 * 1E-8
    effectivity_pe = np.append(effectivity_pe, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe))
    print(f'Neutron energy {TitleLabel[i]}')
    print(f'PE before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}')

    with open(OutputPath + 'neutron_conversion_layer_analysis.txt', 'a') as file1:
        file1.write(f'Neutron energy {TitleLabel[i]}:\n')
        file1.write(f'Filter parameters: E min: {energy_min[i]} keV, E max: {energy_max[i]} keV, S min: {size_min[i]} px, S max: {size_max[i]} px, Height min: {height_min[i]} keV, Height max: {height_max[i]} keV\n')
        file1.write(f'PE LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_PE_conversion_layer')
    
    filter_parameters = Cluster_filter_multiple_parameter([kapton_xmin, kapton_xmax, kapton_ymin, kapton_ymax, energy_min[i], energy_max[i], size_min[i], size_max[i], height_min[i], height_max[i]], [2,3,4,7,8]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_kapton = (kapton_xmax - kapton_xmin) * (kapton_ymax - kapton_ymin) * 3025 * 1E-8
    effectivity_kapton = np.append(effectivity_kapton, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton))
    print(f'Kapton before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}')
    
    with open(OutputPath + 'neutron_conversion_layer_analysis.txt', 'a') as file1:
        file1.write(f'Kapton LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_kapton_conversion_layer')

    filter_parameters = Cluster_filter_multiple_parameter([nolayer_xmin, nolayer_xmax, nolayer_ymin, nolayer_ymax, energy_min[i], energy_max[i], size_min[i], size_max[i], height_min[i], height_max[i]], [2,3,4,7,8]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_nolayer = (nolayer_xmax - nolayer_xmin) * (nolayer_ymax - nolayer_ymin) * 3025 * 1E-8
    effectivity_nolayer = np.append(effectivity_nolayer, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer))
    print(f'No layer before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}')
    
    with open(OutputPath + 'neutron_conversion_layer_analysis.txt', 'a') as file1:
        file1.write(f'NO LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}\n\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_no_conversion_layer')

np.savetxt(OutputPath + 'effectivity_values_andrej.txt', np.c_[TitleValues, effectivity_pe, effectivity_kapton, effectivity_nolayer], delimiter="\t", header="Energy\tPE\tKapton\tNolayer", comments='', fmt='%.7f')

for i in range(len(clog_paths_X00)):
    elist_data = np.loadtxt(elist_paths_X00[i], skiprows=2, delimiter='\t')
    clog_data = read_clog_multiple(clog_paths_X00[i])
    number_of_particles = len(elist_data[:,0])

    if len(elist_data[:,0]) == len(clog_data[:]):
        print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog_data[:]))
    else:
        print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog_data[:]))

    iterator = 0
    for j in range(len(clog_data[:])):
        if elist_data[j,4] > energy_min[i] and elist_data[j,7] > size_min[i] and elist_data[j,8] > height_min[i] and iterator < number_of_particles_clusters:
            print_figure_single_cluster_energy_event_parameters(clog_data[j], elist_data, j, vmax, '', OutputPath + 'single_cluster\\' + OutNames[i], '\\cluster_'+str(j))
            iterator += 1


"""
E_min = np.array([50,100,150,200,250,300,350,400,450,500,1000,2000,3000,5000])
E_max = 50000
Size_min = np.array([5,10,20,30,40,50,60,70,80,90,100,125,150,200])
Size_max = 1000
Roundness_min = np.array([0.201, 0.301, 0.401, 0.501,0.601,0.701,0.751,0.801,0.851,0.901,0.951,0.981,0.991])
Roundness_max = 1.01

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
"""