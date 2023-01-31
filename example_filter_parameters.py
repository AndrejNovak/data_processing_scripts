from DPE_functions import *

"""
This is an example of how to use the DPE_functions library and Timepix data filters.
At the end, you print out matrices that passed the filter.
"""

# Some input data
folder_data = r'C:\Users\andrej\Documents\FEI\Vyskum\data_carlos_output\2022_12_VdG_L06\01\Files\\'
filename_clog = 'ClusterLog.clog'
filename_elist = 'Elist.txt'
filename_out = 'Elist_filtered.txt'

# Number of particles to process
number_of_particles = 10

# Calculate new parameters from DPE elist output
# ratios of Energy and Size, and the second pair is BorderPixel and Size:
input_column_number_pairs_for_ratios = [4,7,9,7] 

# for these new pairs make a header that states what the new parameter is:
input_header_text_new_columns = ['E/A', 'BordPx/A']

# for the new pairs state its physical unit: 
input_units_text_new_columns = ['keV/px', 'a.u.']

# The number of column of the filter with passed/failed values of 1 or 0
number_column_filter = 17

filter_parameters = Cluster_filter_multiple_parameter([100, 10000, 100, 6000], [4, 8]) # Energy Height

# Input file
clog = read_clog(folder_data + filename_clog)[2]

# Read the input elist and make a new columns
elist_extended = read_elist_add_new_parameters(folder_data + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns)

# Print out new Elist file - name, header, units, data
write_elist(folder_data + filename_out, elist_extended[0], elist_extended[1], elist_extended[2]) 

# Make a filtered Elist
filtered_elist = read_elist_filter(folder_data + filename_elist, input_column_number_pairs_for_ratios, input_header_text_new_columns, input_units_text_new_columns, filter_parameters)

# For TPX3 t3pa data
# square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, filename_clog, number_column_filter, number_of_particles)

# For TPX frame ToT data
square_matrices = create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_of_particles)

# Finally, print matrices that satisfied the particle filter parameters and those that didn't
energy_colorbar_max_value = 1E4
toa_colorbar_max_value = 5

folder_figures = r'C:/Users/andrej/Documents/FEI/'

print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Energy square matrix - particles all', folder_figures, 'energy_all')
print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', folder_figures, 'toa_all')
print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Energy square matrix - particles passed', folder_figures, 'energy_passed')
print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', folder_figures, 'toa_passed')
# print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Energy square matrix - particles failed', folder_figures, 'energy_failed')
# print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', folder_figures, 'toa_failed')