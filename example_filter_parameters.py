from DPE_functions import *

"""
This is an example of how to use the DPE_functions library and Timepix data filters.
At the end, you print out matrices that passed the filter.
"""

# Some input data
folder_data = r'C:\Users\andrej\Documents\FEI\\'
filename_clog = 'ClusterLog.clog'
filename_elist = 'Elist.txt'
filename_out = 'Elist_filtered.txt'

# Number of particles to process
#number_of_particles = 1000

# Calculate new parameters from DPE elist output
# ratios of Energy and Size, and the second pair is BorderPixel and Size:
input_column_number_pairs_for_ratios = [4,7,9,7] 

# for these new pairs make a header that states what the new parameter is:
input_header_text_new_columns = ['E/A', 'BordPx/A']

# for the new pairs state its physical unit: 
input_units_text_new_columns = ['keV/px', '-']

# The number of column of the filter with passed/failed values of 1 or 0
total_number_columns = len(read_elist(folder_data + filename_elist)[0])
number_column_filter = total_number_columns + 1

#filter_parameters = Cluster_filter_multiple_parameter([10, 10000, 100, 6000], [4, 8]) # Energy Height
filter_parameters = Cluster_filter_multiple_parameter([500, 1E4, 70, 200], [4, 7]) # Energy Size 7

# Input file
#clog = read_clog(folder_data + filename_clog)[2]
clog = read_clog_clusters(folder_data + filename_clog)[2]
#clog = read_clog_multiple(folder_data + filename_clog)[2]

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
#number_of_particles = len(clog) - (len(clog) - 1000)
number_of_particles = 3000
print(number_of_particles)
square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering(filtered_elist, clog, number_of_particles)

# Finally, print matrices that satisfied the particle filter parameters and those that didn't
energy_colorbar_max_value = 10000
toa_colorbar_max_value = 5

folder_figures = r'C:/Users/andrej/Documents/FEI/'

try:
    print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'Deposited energy - particles all', folder_figures, '1_all')
except Exception:
    print('There is a problem in Energy All figure - probably no particles passed')
#print_figure_toa(square_matrices[1], toa_colorbar_max_value, 'ToA square matrix - particles all', folder_figures, 'toa_all')
try:
    print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Deposited energy - particles passed', folder_figures, '2_passed')
except Exception:
    print('There is a problem in Energy Passed figure')
#print_figure_toa(square_matrices[3], toa_colorbar_max_value, 'ToA square matrix - particles passed', folder_figures, 'toa_passed')
try:
    print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Deposited energy - particles failed', folder_figures, '3_failed')
except Exception:
    print('There is a problem in Energy Failed figure')
# print_figure_toa(square_matrices[5], toa_colorbar_max_value, 'ToA square matrix - particles failed', folder_figures, 'toa_failed')