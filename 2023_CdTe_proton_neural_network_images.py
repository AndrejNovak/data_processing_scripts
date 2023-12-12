from DPE_functions import *

paths = [
    'Q:\\DPE_carlos_data_output\\2022_06_krakow\\A3\\D04_TPX3_CdTe1000\\',
    'Q:\\DPE_carlos_data_output\\2022_06_krakow\\C2\\D04_TPX3_CdTe1000\\',
    'Q:\\DPE_carlos_data_output\\2022_06_krakow\\C3\\D04_TPX3_CdTe1000\\',
    'Q:\\DPE_carlos_data_output\\2022_06_krakow\\C5\\D04_TPX3_CdTe1000\\',
    'Q:\\DPE_carlos_data_output\\2022_06_krakow\\C6\\D04_TPX3_CdTe1000\\'
]

output_paths = [
    'Q:\\2023_CdTe_protons_neural_network_training\\A3\\',
    'Q:\\2023_CdTe_protons_neural_network_training\\C2\\',
    'Q:\\2023_CdTe_protons_neural_network_training\\C3\\',
    'Q:\\2023_CdTe_protons_neural_network_training\\C5\\',
    'Q:\\2023_CdTe_protons_neural_network_training\\C6\\'
]

output_subfolder_names = ['A3', 'C1', 'C2', 'C3', 'C5', 'C6']

for idx, var in enumerate(paths):
    subdirectories = get_subdirectory_names(var)
    print(subdirectories) 

    for j in range(len(subdirectories)):    
        FileInPath = var + subdirectories[j] + '\\'
        FolderInPath = FileInPath + 'File\\'

        print(FolderInPath)

        clog = read_clog_multiple(FolderInPath)
        clog_length = len(clog)
        max_number_of_clusters = 4000   #4000

        print(f'The clog length is {clog_length}')

        if clog_length > 4000:
            for k in range(max_number_of_clusters):
                print_figure_single_cluster_energy_neural_network(clog[k], k, 3000, output_paths[idx] + subdirectories[j] + '\\', 'cluster')
        else:
            pass