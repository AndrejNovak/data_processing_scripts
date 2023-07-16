from DPE_functions import *

lin_wd = 1.75
tickfnt = 18
alpha_val = 0.9
mydpi = 300

"""
27 31 MeV 00
32 31 MeV 45
33 31 MeV 60
38 31 MeV 75
39 31 MeV 85
"""

all_paths_energy_deposition = [
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\39_10ms\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\60deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\85deg\\'
]


labels = ['31 MeV 0$^{\circ}$', '31 MeV 45$^{\circ}$', '31 MeV 60$^{\circ}$', '31 MeV 75$^{\circ}$', '31 MeV 85$^{\circ}$',
          '226 MeV 0$^{\circ}$', '226 MeV 45$^{\circ}$', '226 MeV 60$^{\circ}$', '226 MeV 75$^{\circ}$', '226 MeV 85$^{\circ}$']

thickness = 65