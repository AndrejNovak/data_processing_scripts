from DPE_functions import *

# Add a list of paths for processing of all Si and SiC measurements on protons and neutrons
# All paths to data to process
"""
VdG neutrons
08 - 17.5 MeV
11 - 5 MeV

*** IN ***
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\08\\', *** WARNING *** Elist and Clog not of the same length 2700093 57824
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\08\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\11\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\11\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\11\\'

*** OUT ***
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\L06\\', *** WARNING *** Elist and Clog not of the same length 2700093 57824
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
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\'

*** OUT ***
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\00deg\\'


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

lin_wd = 1.75
tickfnt = 18
alpha_val = 0.9
mydpi = 300


all_paths = [
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\07\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\07\\',
'Q:\\DPE_carlos_data_output\\2022_12_VdG\\D05\\07\\',
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
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\28_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\28_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\29_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\29_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\30_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\30_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\31_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\31_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\34_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\34_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\35_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\35_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\36_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\36_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\37_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\37_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\39_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\39_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\40_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\40_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\41_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\41_500ms\\'
]

all_out_folders = [
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_07\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_07\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_07\\D05\\',
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
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_13MeV\\L07\\'
]

labels = ['SiC L06 VdG', 'SiC L07 VdG', 'Si D05 VdG', 'SiC L06 VdG', 'SiC L07 VdG', 'Si D05 VdG', 'SiC L06 VdG', 'SiC L07 VdG', 'Si D05 VdG',
          'SiC L07 100 MeV', 'SiC L07 100 MeV', 'SiC L07 100 MeV', 'SiC L07 100 MeV','SiC L07 100 MeV','SiC L07 226 MeV','SiC L07 226 MeV','SiC L07 226 MeV','SiC L07 226 MeV','SiC L07 226 MeV',
          'SiC L06 31 MeV 00deg','SiC L07 31 MeV 00deg','SiC L06 31 MeV 45deg','SiC L07 31 MeV 45deg','SiC L06 13 MeV 60deg','SiC L07 31 MeV 60deg','SiC L06 31 MeV 75deg','SiC L07 31 MeV 75deg',
          'SiC L06 20 MeV 00deg','SiC L07 20 MeV 00deg','SiC L06 13 MeV 00deg','SiC L07 13 MeV 00deg','SiC L06 13 MeV 45deg','SiC L07 13 MeV 45deg','SiC L06 20 MeV 45deg','SiC L07 20 MeV 45deg',
          'SiC L06 20 MeV 60deg','SiC L07 20 MeV 60deg','SiC L06 13 MeV 60deg','SiC L07 13 MeV 60deg','SiC L06 13 MeV 75deg','SiC L07 13 MeV 75deg','SiC L06 20 MeV 75deg','SiC L07 20 MeV 75deg',
          'SiC L06 31 MeV 85deg','SiC L07 31 MeV 85deg','SiC L06 20 MeV 85deg','SiC L07 20 MeV 85deg','SiC L06 13 MeV 85deg','SiC L07 13 MeV 85deg']

thicknesses = np.array([65, 65, 500, 65, 65, 500, 65, 65, 500, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65])


"""
all_paths = [
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\90deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\28_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\28_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\29_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\29_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\30_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\30_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\31_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\31_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\34_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\34_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\35_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\35_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\36_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\36_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\37_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\37_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\39_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\39_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\40_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\40_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\41_500ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\41_500ms\\'
]

all_out_folders = [
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\90deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\88deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\75deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\45deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\00deg\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\00deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\45deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\60deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_13MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\75deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_31MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_31MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_20MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_20MeV\\L07\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_13MeV\\L06\\',
'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\85deg_13MeV\\L07\\'
]

labels = ['SiC L07 100 MeV', 'SiC L07 100 MeV', 'SiC L07 100 MeV', 'SiC L07 100 MeV','SiC L07 100 MeV','SiC L07 226 MeV','SiC L07 226 MeV','SiC L07 226 MeV','SiC L07 226 MeV','SiC L07 226 MeV',
          'SiC L06 31 MeV 00deg','SiC L07 31 MeV 00deg','SiC L06 31 MeV 45deg','SiC L07 31 MeV 45deg','SiC L06 13 MeV 60deg','SiC L07 31 MeV 60deg','SiC L06 31 MeV 75deg','SiC L07 31 MeV 75deg',
          'SiC L06 20 MeV 00deg','SiC L07 20 MeV 00deg','SiC L06 13 MeV 00deg','SiC L07 13 MeV 00deg','SiC L06 13 MeV 45deg','SiC L07 13 MeV 45deg','SiC L06 20 MeV 45deg','SiC L07 20 MeV 45deg',
          'SiC L06 20 MeV 60deg','SiC L07 20 MeV 60deg','SiC L06 13 MeV 60deg','SiC L07 13 MeV 60deg','SiC L06 13 MeV 75deg','SiC L07 13 MeV 75deg','SiC L06 20 MeV 75deg','SiC L07 20 MeV 75deg',
          'SiC L06 31 MeV 85deg','SiC L07 31 MeV 85deg','SiC L06 20 MeV 85deg','SiC L07 20 MeV 85deg','SiC L06 13 MeV 85deg','SiC L07 13 MeV 85deg']

thicknesses = np.array([65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65,65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65])
"""

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
    Size_min = 30
    Size_max = 100
    """

    """
    # Heavier
    E_min = 2000
    E_max = 50000
    Size_min = 30
    Size_max = 1000
    """

    E_min = np.array([0,500,2000,2000])
    E_max = np.array([500,2000,8000,50000])
    Size_min = np.array([0,4,30,30])
    Size_max = np.array([4,30,100,1000])

    number_of_particles = np.array([4000,2000,2000,2000])

    for k in range(len(E_min)):
        print(f'Filter for Energy range {E_min[k]}-{E_max[k]} keV and size range {Size_min[k]}-{Size_max[k]} px')
        filter_parameters = Cluster_filter_multiple_parameter([E_min[k], E_max[k], Size_min[k], Size_max[k]], [4,7]) # Energy, Size
        filtered_elist = read_elist_filter_numpy(elist_data, filter_parameters)
        square_matrices = create_matrix_filter_tpx3_t3pa_for_filtering_numpy_input(filtered_elist[:,-1], clog, number_of_particles[k])

        energy_colorbar_max_value = 3000

        FileOutName = 'E_' + str(E_min[k]) + '-' + str(E_max[k]) + '_Size_' + str(Size_min[k]) + '-' + str(Size_max[k])

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

        number_of_single_clusters = 20
        passed_clusters = 0

        filtered_energy = np.empty([0])
        filtered_height = np.empty([0])
        filtered_size = np.empty([0])
        filtered_length = np.empty([0])

        for i in range(len(filtered_elist[:,0])):
            if filtered_elist[i,-1] == 1 and passed_clusters < number_of_single_clusters:
                passed_clusters +=1
                try:
                    print_figure_single_cluster_energy(clog[i], i, energy_colorbar_max_value, 'Cluster #' + str(i) + '\nEnergy '+str(int(filtered_elist[i,4])) + ' keV, Size ' + str(int(filtered_elist[i,7])) + ' px', FolderOut + '\\' + FileOutName + '\\', 'Cluster')
                    print_figure_single_cluster_toa_tpx(clog[i], i, 30, 'Cluster #' + str(i) + ' ToA', FolderOut + '\\' + FileOutName + '\\', 'ToA_Cluster')
                except Exception:
                    pass
            if passed_clusters == number_of_single_clusters:
                break
        
        filtered_energy = filtered_elist[filtered_elist[:,-1] == 1][:,4]
        filtered_height = filtered_elist[filtered_elist[:,-1] == 1][:,8]
        filtered_size = filtered_elist[filtered_elist[:,-1] == 1][:,7]
        filtered_length = filtered_elist[filtered_elist[:,-1] == 1][:,13]

        filtered_let = filtered_energy[:] / (np.sqrt((filtered_length[:] * 55) ** 2 + thicknesses[idx]**2))
        filtered_perpx = filtered_energy[:] / filtered_size[:]

        bin_energy = 4096
        bin_size = 100

        histogram_type = 'scott' # 'sturge', 'doane', 'rice', 'scott', 'freedman-diaconis', 'knuth', 'bayesian blocks'

        print(f'{len(filtered_energy)} particles passed filter Energy range {E_min[k]}-{E_max[k]} keV and size range {Size_min[k]}-{Size_max[k]} px')

        if not os.path.exists(FolderOut + '\\histograms_' + histogram_type + '\\'):
            os.makedirs(FolderOut + '\\histograms_' + histogram_type + '\\')

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_energy[:], bins=np.histogram_bin_edges(filtered_energy[:], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd, alpha=alpha_val)
        #plt.xlim(left=5, right=1E4)
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Deposited energy distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\filtered_energy_histogram' + FileOutName + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_height[:], bins=np.histogram_bin_edges(filtered_height[:], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=5, right=5E3)
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Height [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster height distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\filtered_height_histogram' + FileOutName + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_size[:], bins=np.histogram_bin_edges(filtered_size[:], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=1, right=1E3)
        #plt.ylim(bottom=10, top=1E7)
        plt.yscale('log')
        #plt.xscale('log')
        plt.xlabel('Size [px]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster size distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\filtered_size_histogram' + FileOutName + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_let[:], bins=np.histogram_bin_edges(filtered_let[:], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=1E-1, right=5E1)
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('LET distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\filtered_LET_histogram' + FileOutName + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_perpx[:], bins=np.histogram_bin_edges(filtered_perpx[:], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=5, right=1E5)
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('E/Size [keV/px]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Per-pixel energy distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\filtered_perpxE_histogram' + FileOutName + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)


        # ALL NON FILTERED HISTOGRAMS
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_elist[:,4], bins=np.histogram_bin_edges(filtered_elist[:,4], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd, alpha=alpha_val)
        #plt.xlim(left=5, right=1E4)
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Deposited energy distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\All_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_elist[:,8], bins=np.histogram_bin_edges(filtered_elist[:,8], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=0, right=1E4) # comment, this is because of the REZ histograms
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Height [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster height distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\All_height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_elist[:,7], bins=np.histogram_bin_edges(filtered_elist[:,7], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=1, right=1E3)
        #plt.ylim(bottom=10, top=1E7)
        plt.yscale('log')
        #plt.xscale('log')
        plt.xlabel('Size [px]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster size distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\All_size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        elist_LET = filtered_elist[:,4] / (np.sqrt((filtered_elist[:,13] * 55) ** 2 + thicknesses[idx]**2))

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(elist_LET[:], bins=np.histogram_bin_edges(elist_LET[:], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=1E-1, right=1E2) # comment, this is because of the REZ histograms
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('LET distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\All_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(filtered_elist[:,4]/filtered_elist[:,7], bins=np.histogram_bin_edges(filtered_elist[:,4]/filtered_elist[:,7], bins=histogram_type), histtype = 'step', label=labels[idx], linewidth=lin_wd)
        #plt.xlim(left=5, right=1E5)
        #plt.ylim(bottom=10, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('E/Size [keV/px]', fontsize=tickfnt)
        plt.ylabel('Particles [count]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Per-pixel energy distribution')
        plt.legend(loc='upper right')
        plt.savefig(FolderOut + '\\histograms_' + histogram_type + '\\All_perpxE_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)