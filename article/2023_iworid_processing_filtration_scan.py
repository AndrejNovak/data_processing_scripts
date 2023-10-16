from DPE_functions import *

# Add a list of paths for processing of all Si and SiC measurements on protons and neutrons
# All paths to data to process

# VdG neutrons
#'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\'
#'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\'
#'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\'

#PTC protons
#'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\'
#'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\'

# Rez protons
#'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\'
#'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\'

# OUT FOLDERS
"""
'Q:\\2023_iworid_data_processing\\L06\\VdG\\',
'Q:\\2023_iworid_data_processing\\L07\\VdG\\',
'Q:\\2023_iworid_data_processing\\L07\\ptc_100MeV\\',
'Q:\\2023_iworid_data_processing\\L07\\ptc_225MeV\\',
'Q:\\2023_iworid_data_processing\\L06\\rez\\',
'Q:\\2023_iworid_data_processing\\L07\\rez\\',
'Q:\\2023_iworid_data_processing\\D05\\VdG\\'
"""

all_paths = ['Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\']

all_out_folders = ['Q:\\2023_iworid_data_processing\\L06\\VdG\\']

for idx2, var2 in enumerate(all_paths):
    FileInPath = var2
    FolderOut = all_out_folders[idx2]
    folder_data = get_subdirectory_names(FileInPath)
    print(FolderOut)

    filename_elist = 'ExtElist.txt'
    filename_out = 'Elist_filtered.txt'

    for idx, var in enumerate(folder_data):
        var = folder_data[idx]
        FolderInPath = FileInPath + var + '\\Files\\'
        number_of_particles = 1000
        print(idx2, FileInPath)
        print(idx, FolderInPath)
        print(idx, var)

        elist_path = FolderInPath + filename_elist

        elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        clog = read_clog_multiple(FolderInPath)

        range_energy_max, range_energy_step = 10000, 200    # parameter Energy 4 max(elist_data[:,4])
        range_height_max, range_height_step = 10000, 500    # parameter Height 8 max(elist_data[:,8])
        range_size_max, range_size_step = max(elist_data[:,7]), 2    # parameter Size 7
        range_length_max, range_length_step = max(elist_data[:,13]), 2    # parameter Length 13

        input_column_number_pairs_for_ratios = [4,7,9,7] # ratios of Energy and Size, and the second pair is BorderPixel and Size:
        input_header_text_new_columns = ['E/A', 'BordPx/A'] # for these new pairs make a header that states what the new parameter is:
        input_units_text_new_columns = ['keV/px', '-'] # for the new pairs state its physical unit: 

        total_number_columns = len(read_elist(FolderInPath + filename_elist)[0]) # The number of column of the filter with passed/failed values of 1 or 0
        number_column_filter = total_number_columns + 1

        print(f'Energy up to {int(range_energy_max)} with step of {range_energy_step}, number of iterations is {int(range_energy_max / range_energy_step)}.')
        print(f'Height up to {int(range_height_max)} with step of {range_height_step}, number of iterations is {int(range_height_max / range_height_step)}.')
        print(f'Size up to {int(range_size_max)} with step of {range_size_step}, number of iterations is {int(range_size_max / range_size_step)}.')        
        print(f'Length up to {int(range_length_max)} with step of {range_length_step}, number of iterations is {int(range_length_max / range_length_step)}.')
        print(f'Total number of iterations is {int(range_energy_max / range_energy_step) + int(range_height_max / range_height_step) + int(range_size_max / range_size_step) + int(range_length_max / range_length_step)}')

        energy_parameter = 0
        height_parameter = 0
        size_parameter = 0
        length_parameter = 0

        maximum = 100000000
        
        for iter_energy in range(0, int(range_energy_max), range_energy_step):
            filter_parameters = Cluster_filter_multiple_parameter([energy_parameter, maximum], [4]) # Energy
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 3000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Energy'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Energy_' + str(energy_parameter) + '_keV_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Dep E - all, energy min ' + str(energy_parameter) + ' keV\n Number of all particles is ' + str(square_matrices[6] + square_matrices[7]), FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Dep E - passed, energy min ' + str(energy_parameter) + ' keV\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Dep E - failed, energy min ' + str(energy_parameter) + ' keV\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
            energy_parameter += range_energy_step


        for iter_height in range(0, int(range_height_max), range_height_step):
            filter_parameters = Cluster_filter_multiple_parameter([height_parameter, maximum], [8]) # Energy Height Size Linearity Length
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 3000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Height'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Height_' + str(height_parameter) + '_keV_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Dep E - all, height min ' + str(height_parameter) + ' keV\n Number of all particles is ' + str(square_matrices[6] + square_matrices[7]), FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Dep E - passed, height min ' + str(height_parameter) + ' keV\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Dep E - failed, height min ' + str(height_parameter) + ' keV\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
            height_parameter += range_height_step
        

        for iter_size in range(0, int(range_size_max), range_size_step):
            filter_parameters = Cluster_filter_multiple_parameter([size_parameter, maximum], [7]) # Size

            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 3000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Size'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Size_' + str(size_parameter) + '_px_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Dep E - all, size min ' + str(size_parameter) + ' px\n Number of all particles is ' + str(square_matrices[6] + square_matrices[7]), FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Dep E - passed, size min ' + str(size_parameter) + ' px\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Dep E - failed, size min ' + str(size_parameter) + ' px\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
            size_parameter += range_size_step
        

        for iter_length in range(0, int(range_length_max), range_length_step):
            filter_parameters = Cluster_filter_multiple_parameter([length_parameter, maximum], [13]) # Energy Height Size Linearity Length
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

            energy_colorbar_max_value = 4000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Length'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Length_' + str(length_parameter) + '_px_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Dep E - all, length min ' + str(length_parameter) + ' px\n Number of all particles is ' + str(square_matrices[6] + square_matrices[7]), FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Dep E - passed, length min ' + str(length_parameter) + ' px\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Dep E - failed, length min ' + str(length_parameter) + ' px\n Passed ' +str(square_matrices[6]) + ', Failed ' + str(square_matrices[7]), FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass

            length_parameter += range_length_step