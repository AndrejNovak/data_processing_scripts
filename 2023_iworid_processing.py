from DPE_functions import *

# Add a list of paths for processing of all Si and SiC measurements on protons and neutrons
# All paths to data to process

# VdG neutrons
#'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06'
#'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07'
#'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05'

#PTC protons
#'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV'
#'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV'

# Rez protons
#'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06'
#'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07'

all_paths = ['Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07',
             'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV',
             'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV',
             'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06',
             'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07',
             'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05']

all_out_folders = ['Q:\\2023_iworid_data_processing\\L07\\VdG\\',
                   'Q:\\2023_iworid_data_processing\\L07\\ptc_100MeV\\',
                   'Q:\\2023_iworid_data_processing\\L07\\ptc_225MeV\\',
                   'Q:\\2023_iworid_data_processing\\L06\\rez\\',
                   'Q:\\2023_iworid_data_processing\\L07\\rez\\',
                   'Q:\\2023_iworid_data_processing\\D05\\VdG\\']

for idx2, var2 in enumerate(all_paths):
    FileInPath = var2
    FolderOut = all_out_folders[idx2]
    folder_data = get_subdirectory_names(FileInPath)
    print(FolderOut)

    #FileInPath = 'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06'
    #folder_data = get_subdirectory_names(FileInPath)
    #FolderOut = 'Q:\\2023_iworid_data_processing\\L06\\VdG\\'

    #filename_clog = 'ClusterLog.clog'
    filename_elist = 'ExtElist.txt'
    filename_out = 'Elist_filtered.txt'

    for idx, var in enumerate(folder_data):
        var = folder_data[idx+8]
        FolderInPath = FileInPath + '\\' + var + '\\Files\\'
        number_of_particles = 200000
        print(idx2, FileInPath)
        print(idx, FolderInPath)
        print(idx, var)

        elist_path = FolderInPath + filename_elist
        #clog_path = FolderInPath + filename_clog

        elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        clog = read_clog_multiple(FolderInPath)

        range_energy_max, range_energy_step = 10000, 200    # parameter Energy 4 max(elist_data[:,4])
        range_height_max, range_height_step = 10000, 500    # parameter Height 8 max(elist_data[:,8])
        range_size_max, range_size_step = max(elist_data[:,7]), 2    # parameter Size 7
        range_linearity_max, range_linearity_step = max(elist_data[:,12]), 1    # parameter Linearity 12
        range_length_max, range_length_step = max(elist_data[:,13]), 2    # parameter Length 13

        input_column_number_pairs_for_ratios = [4,7,9,7] # ratios of Energy and Size, and the second pair is BorderPixel and Size:
        input_header_text_new_columns = ['E/A', 'BordPx/A'] # for these new pairs make a header that states what the new parameter is:
        input_units_text_new_columns = ['keV/px', '-'] # for the new pairs state its physical unit: 

        total_number_columns = len(read_elist(FolderInPath + filename_elist)[0]) # The number of column of the filter with passed/failed values of 1 or 0
        number_column_filter = total_number_columns + 1

        print(f'Energy up to {int(range_energy_max)} with step of {range_energy_step}, number of iterations is {int(range_energy_max / range_energy_step)}.')
        print(f'Height up to {int(range_height_max)} with step of {range_height_step}, number of iterations is {int(range_height_max / range_height_step)}.')
        print(f'Size up to {int(range_size_max)} with step of {range_size_step}, number of iterations is {int(range_size_max / range_size_step)}.')        
        #print(f'Linearity up to {int(range_linearity_max)} with step of {range_linearity_step * 0.1}, number of iterations is {int(range_linearity_max / (range_linearity_step * 0.1))}.')
        print(f'Length up to {int(range_length_max)} with step of {range_length_step}, number of iterations is {int(range_length_max / range_length_step)}.')
        print(f'Total number of iterations is {int(range_energy_max / range_energy_step) + int(range_height_max / range_height_step) + int(range_size_max / range_size_step) + int(range_length_max / range_length_step)}')

        energy_parameter = 0
        height_parameter = 0
        size_parameter = 0
        linearity_parameter = 0
        length_parameter = 0

        for iter_energy in range(0, int(range_energy_max), range_energy_step):
            # Iterate over parameters with a given step
            filter_parameters = Cluster_filter_multiple_parameter([energy_parameter, range_energy_max], [4]) # Energy

            # Read the input elist and make a new columns
            # Print out new Elist file - name, header, units, data
            # First takes the original and writes a second one, then the next one grabs the new one and writes there
            #elist_extended = read_elist_add_new_parameters(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns)
            #write_elist(FolderInPath + filename_out, elist_extended[0], elist_extended[1], elist_extended[2])

            #elist_filter_result = read_elist_filter_parameters(FolderInPath + filename_out,filter_parameters)
            #write_elist(FolderInPath + filename_out, elist_filter_result[0], elist_filter_result[1], elist_filter_result[2])

            # Make a filtered Elist
            #filtered_elist = read_elist_filter(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns, filter_parameters)
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            # For TPX3 t3pa data
            # square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, filename_clog, number_column_filter, number_of_particles)

            # For TPX frame ToT data
            #square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_of_particles)

            #square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering(filtered_elist, clog, number_of_particles)
            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist, clog, number_of_particles)

            # Finally, print matrices that satisfied the particle filter parameters and those that didn't
            energy_colorbar_max_value = 3000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Energy'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Energy_' + str(energy_parameter) + '_keV_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')
                #print(FolderOut + var + '\\' + SubfolderPath + '\\')


            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Deposited energy - particles all', FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
                #print('There is a problem in Energy All figure - probably no particles passed')
            #print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', FolderOutPath, 'toa_all')
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Deposited energy - particles passed', FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
                #print('There is a problem in Energy Passed figure')
            #print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', FolderOutPath, 'toa_passed')
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Deposited energy - particles failed', FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
                #print('There is a problem in Energy Failed figure')
            # print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', FolderOutPath, 'toa_failed')
            energy_parameter += range_energy_step


        for iter_height in range(0, int(range_height_max), range_height_step):
            # Iterate over parameters with a given step
            filter_parameters = Cluster_filter_multiple_parameter([height_parameter, range_height_max], [8]) # Energy Height Size Linearity Length

            # Read the input elist and make a new columns
            # Print out new Elist file - name, header, units, data
            # First takes the original and writes a second one, then the next one grabs the new one and writes there
            #elist_extended = read_elist_add_new_parameters(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns)
            #write_elist(FolderInPath + filename_out, elist_extended[0], elist_extended[1], elist_extended[2])

            #elist_filter_result = read_elist_filter_parameters(FolderInPath + filename_out,filter_parameters)
            #write_elist(FolderInPath + filename_out, elist_filter_result[0], elist_filter_result[1], elist_filter_result[2])

            # Make a filtered Elist
            #filtered_elist = read_elist_filter(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns, filter_parameters)
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

            # For TPX3 t3pa data
            # square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, filename_clog, number_column_filter, number_of_particles)

            # For TPX frame ToT data
            #square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_of_particles)

            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist, clog, number_of_particles)

            # Finally, print matrices that satisfied the particle filter parameters and those that didn't
            energy_colorbar_max_value = 3000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Height'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Height_' + str(height_parameter) + '_keV_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Deposited energy - particles all', FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
                #print('There is a problem in Energy All figure - probably no particles passed')
            #print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', FolderOutPath, 'toa_all')
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Deposited energy - particles passed', FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
                #print('There is a problem in Energy Passed figure')
            #print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', FolderOutPath, 'toa_passed')
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Deposited energy - particles failed', FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
                #print('There is a problem in Energy Failed figure')
            # print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', FolderOutPath, 'toa_failed')
            height_parameter += range_height_step


        for iter_size in range(0, int(range_size_max), range_size_step):
            # Iterate over parameters with a given step
            filter_parameters = Cluster_filter_multiple_parameter([size_parameter, range_size_max], [7]) # Size

            # Read the input elist and make a new columns
            # Print out new Elist file - name, header, units, data
            # First takes the original and writes a second one, then the next one grabs the new one and writes there
            #elist_extended = read_elist_add_new_parameters(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns)
            #write_elist(FolderInPath + filename_out, elist_extended[0], elist_extended[1], elist_extended[2])

            #elist_filter_result = read_elist_filter_parameters(FolderInPath + filename_out,filter_parameters)
            #write_elist(FolderInPath + filename_out, elist_filter_result[0], elist_filter_result[1], elist_filter_result[2])

            # Make a filtered Elist
            #filtered_elist = read_elist_filter(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns, filter_parameters)
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

            # For TPX3 t3pa data
            # square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, filename_clog, number_column_filter, number_of_particles)

            # For TPX frame ToT data
            #square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_of_particles)

            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist, clog, number_of_particles)

            # Finally, print matrices that satisfied the particle filter parameters and those that didn't
            energy_colorbar_max_value = 3000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Size'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Size_' + str(size_parameter) + '_px_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Deposited energy - particles all', FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
                #print('There is a problem in Energy All figure - probably no particles passed')
            #print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', FolderOutPath, 'toa_all')
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Deposited energy - particles passed', FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
                #print('There is a problem in Energy Passed figure')
            #print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', FolderOutPath, 'toa_passed')
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Deposited energy - particles failed', FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
                #print('There is a problem in Energy Failed figure')
            # print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', FolderOutPath, 'toa_failed')
            size_parameter += range_size_step


        for iter_length in range(0, int(range_length_max), range_length_step):
            # Iterate over parameters with a given step
            filter_parameters = Cluster_filter_multiple_parameter([length_parameter, range_length_max], [13]) # Energy Height Size Linearity Length

            # Read the input elist and make a new columns
            # Print out new Elist file - name, header, units, data
            # First takes the original and writes a second one, then the next one grabs the new one and writes there
            #elist_extended = read_elist_add_new_parameters(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns)
            #write_elist(FolderInPath + filename_out, elist_extended[0], elist_extended[1], elist_extended[2])

            #elist_filter_result = read_elist_filter_parameters(FolderInPath + filename_out,filter_parameters)
            #write_elist(FolderInPath + filename_out, elist_filter_result[0], elist_filter_result[1], elist_filter_result[2])

            # Make a filtered Elist
            #filtered_elist = read_elist_filter(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns, filter_parameters)
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)

            # For TPX3 t3pa data
            # square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, filename_clog, number_column_filter, number_of_particles)

            # For TPX frame ToT data
            #square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_of_particles)

            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist, clog, number_of_particles)

            # Finally, print matrices that satisfied the particle filter parameters and those that didn't
            energy_colorbar_max_value = 4000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Length'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Length_' + str(length_parameter) + '_px_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Deposited energy - particles all', FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
                #print('There is a problem in Energy All figure - probably no particles passed')
            #print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', FolderOutPath, 'toa_all')
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Deposited energy - particles passed', FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
                #print('There is a problem in Energy Passed figure')
            #print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', FolderOutPath, 'toa_passed')
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Deposited energy - particles failed', FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
                #print('There is a problem in Energy Failed figure')
            # print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', FolderOutPath, 'toa_failed')
    
            length_parameter += range_length_step

"""
        for iter_linearity in range(0, int(range_linearity_max) * 10, range_linearity_step):
            # Iterate over parameters with a given step
            filter_parameters = Cluster_filter_multiple_parameter([linearity_parameter, range_linearity_max], [12]) #Linearity

            # Read the input elist and make a new columns
            # Print out new Elist file - name, header, units, data
            # First takes the original and writes a second one, then the next one grabs the new one and writes there
            #elist_extended = read_elist_add_new_parameters(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns)
            #write_elist(FolderInPath + filename_out, elist_extended[0], elist_extended[1], elist_extended[2])

            #elist_filter_result = read_elist_filter_parameters(FolderInPath + filename_out,filter_parameters)
            #write_elist(FolderInPath + filename_out, elist_filter_result[0], elist_filter_result[1], elist_filter_result[2])

            # Make a filtered Elist
            #filtered_elist = read_elist_filter(FolderInPath + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns, filter_parameters)
            filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
            
            # For TPX3 t3pa data
            # square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, filename_clog, number_column_filter, number_of_particles)

            # For TPX frame ToT data
            #square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_of_particles)

            square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist, clog, number_of_particles)

            # Finally, print matrices that satisfied the particle filter parameters and those that didn't
            energy_colorbar_max_value = 3000
            toa_colorbar_max_value = 20

            SubfolderPath = 'Linearity'
            FolderOutPath = FolderOut + var + '\\' + SubfolderPath + '\\'
            FileOutName = 'Linearity_' + str(linearity_parameter) + '_'

            if not os.path.exists(FolderOut + var + '\\' + SubfolderPath + '\\'):
                os.makedirs(FolderOut + var + '\\' + SubfolderPath + '\\')

            try:
                print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Deposited energy - particles all', FolderOutPath, FileOutName + '1_all')
            except Exception:
                pass
                #print('There is a problem in Energy All figure - probably no particles passed')
            #print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', FolderOutPath, 'toa_all')
            try:
                print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Deposited energy - particles passed', FolderOutPath, FileOutName + '2_passed')
            except Exception:
                pass
                #print('There is a problem in Energy Passed figure')
            #print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', FolderOutPath, 'toa_passed')
            try:
                print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Deposited energy - particles failed', FolderOutPath, FileOutName + '3_failed')
            except Exception:
                pass
                #print('There is a problem in Energy Failed figure')
            # print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', FolderOutPath, 'toa_failed')
            linearity_parameter += range_linearity_step * 0.1   
"""