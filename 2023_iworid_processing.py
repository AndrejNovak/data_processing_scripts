from DPE_functions import *

# Add a list of paths for processing of all Si and SiC measurements on protons and neutrons
folder_data = ['C:\Users\andrej\Documents\FEI\\'

]

FolderOut = [

]   # na koniec dať \\

filename_clog = 'ClusterLog.clog'
filename_elist = 'ExtElist.txt'
filename_out = 'Elist_filtered.txt'

for idx, var in folder_data:
    FolderIn = var
    number_of_particles = 3000
    print(idx, FolderIn)

    elist_path = FolderIn + filename_elist
    clog_path = FolderIn + filename_clog
    
    elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
    clog = read_clog_multiple(folder_data + filename_clog)

    range_energy_max, range_energy_step = max(elist_data[:,4]), 100    # parameter Energy 4
    range_height_max, range_height_step = max(elist_data[:,8]), 100    # parameter Height 8
    range_size_max, range_size_step = max(elist_data[:,7]), 10    # parameter Size 7
    range_linearity_max, range_linearity_step = max(elist_data[:,12]), 0.1    # parameter Linearity 12
    range_length_max, range_length_step = max(elist_data[:,13]), 1    # parameter Length 13

    input_column_number_pairs_for_ratios = [4,7,9,7] # ratios of Energy and Size, and the second pair is BorderPixel and Size:
    input_header_text_new_columns = ['E/A', 'BordPx/A'] # for these new pairs make a header that states what the new parameter is:
    input_units_text_new_columns = ['keV/px', '-'] # for the new pairs state its physical unit: 

    total_number_columns = len(read_elist( + filename_elist)[0]) # The number of column of the filter with passed/failed values of 1 or 0
    number_column_filter = total_number_columns + 1

    for iter_energy in range(0, range_energy_max, range_energy_step):
        for iter_height in range(0, range_height_max, range_height_step):
            for iter_size in range(0, range_size_max, range_size_step):
                for iter_linearity in range(0, range_linearity_max, range_linearity_step):
                    for iter_length in range(0, range_length_max, range_length_step):    
                        energy_parameter = iter_energy * range_energy_step
                        height_parameter = iter_height * range_height_step
                        size_parameter = iter_size * range_size_step
                        linearity_parameter = iter_linearity * range_linearity_step
                        length_parameter = iter_length * range_length_step

                        # Iterate over parameters with a given step
                        filter_parameters = Cluster_filter_multiple_parameter([energy_parameter, range_energy_max, height_parameter, range_height_max, size_parameter, range_size_max, linearity_parameter, range_linearity_max, length_parameter, range_linearity_max], [4, 8, 7, 12, 13]) # Energy Height Size Linearity Length

                        # Read the input elist and make a new columns
                        # Print out new Elist file - name, header, units, data
                        # First takes the original and writes a second one, then the next one grabs the new one and writes there
                        elist_extended = read_elist_add_new_parameters(folder_data + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns)
                        write_elist(folder_data + filename_out, elist_extended[0], elist_extended[1], elist_extended[2])

                        elist_filter_result = read_elist_filter_parameters(folder_data + filename_out,filter_parameters)
                        write_elist(folder_data + filename_out, elist_filter_result[0], elist_filter_result[1], elist_filter_result[2])

                        # Make a filtered Elist
                        filtered_elist = read_elist_filter(folder_data + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns, filter_parameters)

                        # For TPX3 t3pa data
                        # square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, filename_clog, number_column_filter, number_of_particles)

                        # For TPX frame ToT data
                        #square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_of_particles)

                        square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering(filtered_elist, clog, number_of_particles)

                        # Finally, print matrices that satisfied the particle filter parameters and those that didn't
                        energy_colorbar_max_value = 3000
                        toa_colorbar_max_value = 20

                        SubfolderPath = 'E_' + str(energy_parameter) + '_Height_' + str(height_parameter) + '_Size_' + str(size_parameter) + '_Linearity_' + str(linearity_parameter) + '_Length_' + str(length_parameter)
                        FolderOutPath = FolderOut + SubfolderPath

                        if not os.path.exists(FolderOut + SubfolderPath):
                            os.makedirs(FolderOut + SubfolderPath)

                        try:
                            print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Deposited energy - particles all', FolderOutPath, '1_all')
                        except Exception:
                            print('There is a problem in Energy All figure - probably no particles passed')
                        #print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', FolderOutPath, 'toa_all')
                        try:
                            print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Deposited energy - particles passed', FolderOutPath, '2_passed')
                        except Exception:
                            print('There is a problem in Energy Passed figure')
                        #print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', FolderOutPath, 'toa_passed')
                        try:
                            print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Deposited energy - particles failed', FolderOutPath, '3_failed')
                        except Exception:
                            print('There is a problem in Energy Failed figure')
                        # print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', FolderOutPath, 'toa_failed')