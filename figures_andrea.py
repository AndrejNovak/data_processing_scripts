from DPE_functions import *
#
# VYTVORIT VYSTUPY PRE SINGLE CLUSTRE Z DANYCH ROZSAHOV
#
#     print_figure_single_cluster_energy_event_parameters_old(clog_data, elist_data, cluster_number, vmax, title, OutputPath, OutputName)
#

lin_wd = 2
tickfnt = 18
alpha_val = 0.80
mydpi = 300

clog_paths_X00 = ['\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\03_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\06_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\07_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\01_80V\\File\\']

elist_paths_X00 = [f"{x}EventListExt.advelist" for x in clog_paths_X00]

OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\'
OutputFolder = ['03_80V_3_3MeV', '06_80V_16_2MeV', '07_80V_16_2MeV', '01_80V_14_8MeV']

size_min = np.array([25,  25,  25, 17])
size_max = np.array([130, 130, 130, 65])

energy_min = np.array([1200, 1200, 1200, 1200])
energy_max = np.array([8000, 8000, 8000, 8000])

height_min = np.array([500, 500, 500, 500])
height_max = np.array([1500, 1500, 1500, 1500])

OutNames = ['3_3MeV', '16_2_MeV', '16_2_MeV_2', '14_8MeV']
TitleLabel = ['3.3 MeV', '16.2 MeV', '16.2 MeV measurement 2', '14.8 MeV']
TitleValues = np.array([3.3, 16.2, 16.2, 14.8])

number_of_particles = 2000
vmax = 3000
iterator = 0

effectivity_kapton = np.empty(0)
effectivity_pe = np.empty(0)
effectivity_nolayer = np.empty(0)

pe_xmin = 20
pe_xmax = 251
pe_ymin = 100
pe_ymax = 200

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

    filter_parameters = Cluster_filter_multiple_parameter([pe_xmin, pe_xmax, pe_ymin, pe_ymax, energy_min[i], energy_max[i], size_min[i], size_max[i], height_min[i], height_max[i]], [2,3,4,7,8]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
    
    area_pe = (pe_xmax - pe_xmin) * (pe_ymax - pe_ymin) * 3025 * 1E-8
    effectivity_pe = np.append(effectivity_pe, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe))
    print(f'Neutron energy {TitleLabel[i]}')
    print(f'PE before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}')

    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrej.txt', 'a') as file1:
        file1.write(f'Neutron energy {TitleLabel[i]}:\n')
        file1.write(f'Filter parameters: E min: {energy_min[i]} keV, E max: {energy_max[i]} keV, S min: {size_min[i]} px, S max: {size_max[i]} px, Height min: {height_min[i]} keV, Height max: {height_max[i]} keV\n')
        file1.write(f'PE LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_PE_conversion_layer_andrej')
    
    filter_parameters = Cluster_filter_multiple_parameter([kapton_xmin, kapton_xmax, kapton_ymin, kapton_ymax, energy_min[i], energy_max[i], size_min[i], size_max[i], height_min[i], height_max[i]], [2,3,4,7,8]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_kapton = (kapton_xmax - kapton_xmin) * (kapton_ymax - kapton_ymin) * 3025 * 1E-8
    effectivity_kapton = np.append(effectivity_kapton, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton))
    print(f'Kapton before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}')
    
    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrej.txt', 'a') as file1:
        file1.write(f'Kapton LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_kapton_conversion_layer_andrej')

    filter_parameters = Cluster_filter_multiple_parameter([nolayer_xmin, nolayer_xmax, nolayer_ymin, nolayer_ymax, energy_min[i], energy_max[i], size_min[i], size_max[i], height_min[i], height_max[i]], [2,3,4,7,8]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_nolayer = (nolayer_xmax - nolayer_xmin) * (nolayer_ymax - nolayer_ymin) * 3025 * 1E-8
    effectivity_nolayer = np.append(effectivity_nolayer, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer))
    print(f'No layer before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}')
    
    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrej.txt', 'a') as file1:
        file1.write(f'NO LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}\n\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_no_conversion_layer_andrej')

np.savetxt('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\\\effectivity_values_andrej.txt', np.c_[TitleValues, effectivity_pe, effectivity_kapton, effectivity_nolayer], delimiter="\t", header="Energy\tPE\tKapton\tNolayer", comments='', fmt='%.4f')

iterator = 0

effectivity_kapton = np.empty(0)
effectivity_pe = np.empty(0)
effectivity_nolayer = np.empty(0)

pe_xmin = 20
pe_xmax = 251
pe_ymin = 100
pe_ymax = 200

kapton_xmin = 5
kapton_xmax = 251
kapton_ymin = 200
kapton_ymax = 251

nolayer_xmin = 5
nolayer_xmax = 251
nolayer_ymin = 5
nolayer_ymax = 80

energy_min = 500
size_min = 20
roundness_min = 0.9

for i in range(len(clog_paths_X00)):
    elist_data = np.loadtxt(elist_paths_X00[i], skiprows=2, delimiter='\t')
    clog_data = read_clog_multiple(clog_paths_X00[i])

    filter_parameters = Cluster_filter_multiple_parameter([pe_xmin, pe_xmax, pe_ymin, pe_ymax, energy_min, 100000000000, size_min, 100000000000, roundness_min, 2], [2,3,4,7,10]) # X, Y, Energy, Size, Roundness
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
    
    area_pe = (pe_xmax - pe_xmin) * (pe_ymax - pe_ymin) * 3025 * 1E-8
    effectivity_pe = np.append(effectivity_pe, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe))
    print(f'Neutron energy {TitleLabel[i]}')
    print(f'PE before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}')

    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrea.txt', 'a') as file1:
        file1.write(f'Neutron energy {TitleLabel[i]}:\n')
        file1.write(f'Filter parameters: E min: {energy_min} keV, S min: {size_min}, R: {roundness_min} \n')
        file1.write(f'PE LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_PE_conversion_layer_andrea')
    
    filter_parameters = Cluster_filter_multiple_parameter([kapton_xmin, kapton_xmax, kapton_ymin, kapton_ymax, energy_min, 100000000000, size_min, 100000000000, roundness_min, 2], [2,3,4,7,10]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_kapton = (kapton_xmax - kapton_xmin) * (kapton_ymax - kapton_ymin) * 3025 * 1E-8
    effectivity_kapton = np.append(effectivity_kapton, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton))
    print(f'Kapton before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}')
    
    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrea.txt', 'a') as file1:
        file1.write(f'Kapton LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_kapton_conversion_layer_andrea')

    filter_parameters = Cluster_filter_multiple_parameter([nolayer_xmin, nolayer_xmax, nolayer_ymin, nolayer_ymax, energy_min, 100000000000, size_min, 100000000000, roundness_min, 2], [2,3,4,7,10]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_nolayer = (nolayer_xmax - nolayer_xmin) * (nolayer_ymax - nolayer_ymin) * 3025 * 1E-8
    effectivity_nolayer = np.append(effectivity_nolayer, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer))
    print(f'No layer before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}')
    
    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrea.txt', 'a') as file1:
        file1.write(f'NO LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}\n\n')
    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_no_conversion_layer_andrea')

np.savetxt('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\effectivity_values_andrea.txt', np.c_[TitleValues, effectivity_pe, effectivity_kapton, effectivity_nolayer], delimiter="\t", header="Energy\tPE\tKapton\tNolayer", comments='', fmt='%.4f')

energy_min = 500
size_min = 20
roundness_min = 0.5

effectivity_kapton = np.empty(0)
effectivity_pe = np.empty(0)
effectivity_nolayer = np.empty(0)

for i in range(len(clog_paths_X00)):
    elist_data = np.loadtxt(elist_paths_X00[i], skiprows=2, delimiter='\t')
    clog_data = read_clog_multiple(clog_paths_X00[i])

    filter_parameters = Cluster_filter_multiple_parameter([pe_xmin, pe_xmax, pe_ymin, pe_ymax, energy_min, 100000000000, size_min, 100000000000, roundness_min, 2], [2,3,4,7,10]) # X, Y, Energy, Size, Roundness
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
    
    area_pe = (pe_xmax - pe_xmin) * (pe_ymax - pe_ymin) * 3025 * 1E-8
    effectivity_pe = np.append(effectivity_pe, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe))
    print(f'Neutron energy {TitleLabel[i]}')
    print(f'PE before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}')

    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrea.txt', 'a') as file1:
        file1.write(f'Neutron energy {TitleLabel[i]}:\n')
        file1.write(f'Filter parameters: E min: {energy_min} keV, S min: {size_min}, R: {roundness_min} \n')
        file1.write(f'PE LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_pe} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_pe)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_PE_conversion_layer_andrea_2')
    
    filter_parameters = Cluster_filter_multiple_parameter([kapton_xmin, kapton_xmax, kapton_ymin, kapton_ymax, energy_min, 100000000000, size_min, 100000000000, roundness_min, 2], [2,3,4,7,10]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_kapton = (kapton_xmax - kapton_xmin) * (kapton_ymax - kapton_ymin) * 3025 * 1E-8
    effectivity_kapton = np.append(effectivity_kapton, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton))
    print(f'Kapton before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}')
    
    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrea.txt', 'a') as file1:
        file1.write(f'Kapton LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_kapton} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_kapton)}\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_kapton_conversion_layer_andrea_2')

    filter_parameters = Cluster_filter_multiple_parameter([nolayer_xmin, nolayer_xmax, nolayer_ymin, nolayer_ymax, energy_min, 100000000000, size_min, 100000000000, roundness_min, 2], [2,3,4,7,10]) # X, Y, Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

    area_nolayer = (nolayer_xmax - nolayer_xmin) * (nolayer_ymax - nolayer_ymin) * 3025 * 1E-8
    effectivity_nolayer = np.append(effectivity_nolayer, (len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer))
    print(f'No layer before: {len(elist_data[:,0])}, after: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}')
    
    with open('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\neutron_conversion_layer_and_without_analysis_andrea.txt', 'a') as file1:
        file1.write(f'NO LAYER: Before filtering {len(elist_data[:,0])}, after {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])}, percent remained: {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/len(elist_data[:,0]) * 100}, duration: {(elist_data[-1,5] - elist_data[0,5]) * 1E-9} s, area {area_nolayer} cm2, filtered events per second {len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)}, filtered events per second per cm2 {(len(filtered_elist[filtered_elist[:,-1] == 1][:,0])/((elist_data[-1,5] - elist_data[0,5]) * 1E-9)) * (1/area_nolayer)}\n\n')

    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog_data, number_of_particles)
    print_figure_energy(square_matrices[2], vmax, TitleLabel[i] + ', filtered, X00 Si 500 $\mu$m', OutputPath, OutNames[i] + '_X00_no_conversion_layer_andrea_2')

np.savetxt('C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\effectivity_values_andrea_2.txt', np.c_[TitleValues, effectivity_pe, effectivity_kapton, effectivity_nolayer], delimiter="\t", header="Energy\tPE\tKapton\tNolayer", comments='', fmt='%.4f')


lin_wd = 2
tickfnt = 18
alpha_val = 0.80
mydpi = 300
vmax = 3000
number_of_particles = 200

OutNames = ['3_3MeV', '16_2MeV', '16_2MeV_2', '14_8MeV']
TitleLabel = ['3.3 MeV', '16.2 MeV', '16.2 MeV measurement 2', '14.8 MeV']
TitleValues = np.array([3.3, 16.2, 16.2, 14.8])

clog_paths_X00 = ['\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\03_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\06_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\07_80V\\File\\',
                  '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\01_80V\\File\\']

elist_paths_X00 = [f"{x}EventListExt.advelist" for x in clog_paths_X00]

OutputPath = 'C:\\Users\\andrej\\Documents\\FEI\\data_processing_scripts\\figures_andrea\\'

for i in range(len(clog_paths_X00)):
    elist_data = np.loadtxt(elist_paths_X00[i], skiprows=2, delimiter='\t')
    clog_data = read_clog_multiple(clog_paths_X00[i])

    if len(elist_data[:,0]) == len(clog_data[:]):
        print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog_data[:]))
    else:
        print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog_data[:]))

    iterator = 0
    for j in range(len(clog_data[:])):
        if elist_data[j,4] > 1000 and elist_data[j,7] > 15 and elist_data[j,8] > 300 and iterator < number_of_particles:
            print_figure_single_cluster_energy_event_parameters(clog_data[j], elist_data, j, vmax, '', OutputPath + 'single_cluster\\' + OutNames[i], '\\cluster_'+str(j))
            iterator += 1

all_paths = [
'\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\08_200V\\',
'\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\09_200V\\'
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
        #print(f'Filter range for Energy {E_min[k]}-{E_max[k]} keV, size {Size_min[k]}-{Size_max[k]} px')
        filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max[k], Size_min[k], Size_max[k]], [4,7]) # Energy, Size
        filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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



FolderInPath = '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\02_200V\\Files\\'
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

E_min = np.array([100,150,200,250,300,350,400,450,500])
E_max = 50000
Size_min = np.array([10,20,30,40,50,60,70,80,90,100,125,150])
Size_max = 1000
Roundness_min = np.array([0.501,0.601,0.701,0.751,0.801,0.851,0.901,0.951,0.981,0.991])
Roundness_max = 1.01

number_of_particles = len(elist_data[:,0])

label_to_fig_name = '14.8 MeV neutrons'
folder_name = '14_8MeV\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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


FolderInPath = '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\04_200V\\Files\\'
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

number_of_particles = len(elist_data[:,0])

#label_to_fig_name = '14.8 MeV neutrons'
label_to_fig_name = '16.2 MeV neutrons'
folder_name = '16_2MeV\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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

            
FolderInPath = '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\02_200V\\Files\\'
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

number_of_particles = 2000

label_to_fig_name = '14.8 MeV neutrons'
folder_name = '14_8MeV_2000_particles\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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


FolderInPath = '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\04_200V\\Files\\'
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

number_of_particles = 2000

#label_to_fig_name = '14.8 MeV neutrons'
label_to_fig_name = '16.2 MeV neutrons'
folder_name = '16_2MeV_2000_particles\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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


E_min = np.array([100,150,200,250,300,350,400,450,500])
E_max = 50000
Size_min = np.array([10,20,30,40,50,60,70,80,90,100,125,150])
Size_max = 1000
Roundness_min = np.array([0.501,0.601,0.701,0.751,0.801,0.851,0.901,0.951,0.981,0.991])
Roundness_max = 1.01

FolderInPath = '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\08_200V\\Files\\'
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

number_of_particles = 2000

label_to_fig_name = '3.5 MeV neutrons'
folder_name = '3_5MeV_2000_particles\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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


if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = len(elist_data[:,0])

label_to_fig_name = '3.5 MeV neutrons'
folder_name = '3_5MeV\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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


FolderInPath = '\\\\147.175.96.62\\FEI_data\\DPE_andrej_data_output\\2023_05_16_TPX2_VdG\\X00\\09_200V\\Files\\'
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

number_of_particles = 2000

#label_to_fig_name = '14.8 MeV neutrons'
label_to_fig_name = '3 MeV neutrons'
folder_name = '3MeV_2000_particles\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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

if len(elist_data[:,0]) == len(clog[:]):
    print('Great! The Elist and Clog are of the same length', len(elist_data[:,0]), len(clog[:]))
else:
    print('Really bad! The Elist and Clog are NOT of the same length', len(elist_data[:,0]), len(clog[:]))

number_of_particles = len(elist_data[:,0])

label_to_fig_name = '3 MeV neutrons'
folder_name = '3MeV\\'

for k in range(len(E_min)):
    for l in range(len(Size_min)):
        for j in range(len(Roundness_min)):
            print(f'Filter range for Energy {E_min[k]}-{E_max} keV, size {Size_min[l]}-{Size_max} px, roundness {Roundness_min[j]}-{Roundness_max}.')
            filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max, Size_min[l], Size_max, Roundness_min[j], Roundness_max], [4,7,10]) # Energy, Size
            filtered_elist = read_elist_filter_numpy_old(elist_data, filter_parameters)
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