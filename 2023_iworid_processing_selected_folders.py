from DPE_functions import *

# Add a list of paths for processing of all Si and SiC measurements on protons and neutrons
# All paths to data to process
"""
VdG neutrons
08 - 17.5 MeV
11 - 5 MeV

*** IN ***
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\11\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\11\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\11\\'

*** OUT ***
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\D05\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_11\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_11\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_11\\D05\\'


PTC protons - 100 MeV
*** IN ***
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\00deg\\'

*** OUT ***
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\00deg\\'



*** IN ***
PTC protons - 225 MeV
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\00deg\\'

*** OUT ***
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\00deg\\'


Rez protons - 31 MeV
27 - 00 deg
32 - 45 deg
33 - 60 deg
38 - 75 deg

*** IN ***
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\27\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\32\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\32\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\33\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\33\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\38\\'

*** OUT ***
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg\\'
"""

all_paths = [
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\11\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\11\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\11\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\225MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\27\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\32\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\32\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\33\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\33\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\38\\']

all_out_folders = [
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\D05\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_11\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_11\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_11\\D05\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\225MeV\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg\\']

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

    """
    # X-ray / Gamma
    E_min = 0
    E_max = 500
    Size_min = 0
    Size_max = 4
    """

    """
    # Mid energy particles
    E_min = 500
    E_max = 2000
    Size_min = 4
    Size_max = 30
    """

    """
    # Heavy
    E_min = 2000
    E_max = 8000
    Size_min = 4
    Size_max = 100
    """

    E_min = 0
    E_max = 500
    Size_min = 0
    Size_max = 4

    number_of_particles = 3000

    filter_parameters = Cluster_filter_multiple_parameter([E_min, E_max, Size_min, Size_max], [4,7]) # Energy, Size
    filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
    square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles)

    energy_colorbar_max_value = 3000

    FileOutName = 'E_' + str(E_min) + '-' + str(E_max) + '_Size_' + str(Size_min) + '-' + str(Size_max)

    try:
        print_figure_energy(square_matrices[0], energy_colorbar_max_value, 'All - ' + FileOutName, FolderOut, FileOutName + '_1_all')
    except Exception:
        pass
    try:
        print_figure_energy(square_matrices[2], energy_colorbar_max_value, 'Passed - ' + FileOutName, FolderOut, FileOutName + '_2_passed')
    except Exception:
        pass
    try:
        print_figure_energy(square_matrices[4], energy_colorbar_max_value, 'Failed - ' + FileOutName, FolderOut, FileOutName + '_3_failed')
    except Exception:
        pass

    number_of_single_clusters = 10
    passed_clusters = 0

    for i in range(len(filtered_elist[:,0])):
        if filtered_elist[i,-1] == 1 and passed_clusters < number_of_single_clusters:
            #print(clog[i])
            print_figure_single_cluster_energy(clog[i], i, energy_colorbar_max_value, 'Cluster #' + str(i) + '\nEnergy '+str(int(filtered_elist[i,4])) + ' keV, Size ' + str(int(filtered_elist[i,7])) + ' px', FolderOut + '\\' + FileOutName + '\\', 'Cluster')
            passed_clusters +=1