from DPE_functions import *

"""
Spracovanie údajov z L06 a L07 SiC pre iworid abstrakt 

1) zobraziť vybranú ukážku zo 4 meraní - 2x protóny, 2x neutróny
    - 2 matice vedľa seba, každá rozdelená na 4 segmenty - L06 jedna, L07 druhá
2) Histogramy vybraných parametrov z daných experimentov pre oba L06 a L07
3) Ak bude priestor, spraviť aj spektrá vybraných clusterov
"""

#upravene read_clog_multiple - potom opraviť naspäť
path_L07_ptc = r'Q:\DPE_carlos_data_output\2022_10_ptc\226MeV\75deg\Files\\'
path_L07_rez = r'Q:\DPE_carlos_data_output\2023_03_protons\data_AA\L07\38_10ms\Files\\'
path_L07_n_low = r'Q:\DPE_carlos_data_output\2022_12_VdG\L07\03\Files\\'
path_L07_n_high = r'Q:\DPE_carlos_data_output\2022_12_VdG\L07\06\Files\\'

path_L06_rez = r'Q:\DPE_carlos_data_output\2023_03_protons\data_AA\L06\38_10ms\Files\\'
path_L06_n_low = r'Q:\DPE_carlos_data_output\2022_12_VdG\L06\03\Files\\'
path_L06_n_high = r'Q:\DPE_carlos_data_output\2022_12_VdG\L06\06\Files\\'

clog_protony_ptc_L07 = read_clog_multiple(path_L07_ptc)
clog_protony_rez_L07 = read_clog_multiple(path_L07_rez)
clog_neutrony_low_L07 = read_clog_multiple(path_L07_n_low)
clog_neutrony_high_L07 = read_clog_multiple(path_L07_n_high)

clog_protony_rez_L06 = read_clog_multiple(path_L06_rez)
clog_neutrony_low_L06 = read_clog_multiple(path_L06_n_low)
clog_neutrony_high_L06 = read_clog_multiple(path_L06_n_high)

number_of_events = 1000

matrix_protony_ptc_L07 = create_matrix_tpx3_t3pa(clog_protony_ptc_L07, number_of_events)
matrix_protony_rez_L07 = create_matrix_tpx3_t3pa(clog_protony_rez_L07, number_of_events)
matrix_neutrony_low_L07 = create_matrix_tpx3_t3pa(clog_neutrony_low_L07, number_of_events)
matrix_neutrony_high_L07 = create_matrix_tpx3_t3pa(clog_neutrony_high_L07, number_of_events)

matrix_protony_rez_L06 = create_matrix_tpx3_t3pa(clog_protony_rez_L06, number_of_events)
matrix_neutrony_low_L06 = create_matrix_tpx3_t3pa(clog_neutrony_low_L06, number_of_events)
matrix_neutrony_high_L06 = create_matrix_tpx3_t3pa(clog_neutrony_high_L06, number_of_events)

energy_colorbar_max_value = 1E4
name_L07 = ['L07 PTC - 226 MeV 75 deg', 'L07 Rez - 31 MeV 75 deg', 'L07 VdG - 770 keV', 'L07 VdG - 15.5 MeV']
name_L06 = ['L06 Rez - 31 MeV 75 deg', 'L06 VdG - 770 keV', 'L06 VdG - 15.5 MeV']
folder_figures = r'C:\Users\andrej\Documents\FEI\2023_iworid_prispevok\abstrakt_figures\\'

print_figure_energy(matrix_protony_ptc_L07, energy_colorbar_max_value, 'Deposited energy by' + str(number_of_events) + 'events', folder_figures, str(name_L07[0]))
print_figure_energy(matrix_protony_rez_L07, energy_colorbar_max_value, 'Deposited energy by' + str(number_of_events) + 'events', folder_figures, str(name_L07[1]))
print_figure_energy(matrix_neutrony_low_L07, energy_colorbar_max_value, 'Deposited energy by' + str(number_of_events) + 'events', folder_figures, str(name_L07[2]))
print_figure_energy(matrix_neutrony_high_L07, energy_colorbar_max_value, 'Deposited energy by' + str(number_of_events) + 'events', folder_figures, str(name_L07[3]))

print_figure_energy(matrix_protony_rez_L06, energy_colorbar_max_value, 'Deposited energy by' + str(number_of_events) + 'events', folder_figures, str(name_L06[0]))
print_figure_energy(matrix_neutrony_low_L06, energy_colorbar_max_value, 'Deposited energy by' + str(number_of_events) + 'events', folder_figures, str(name_L06[1]))
print_figure_energy(matrix_neutrony_high_L06, energy_colorbar_max_value, 'Deposited energy by' + str(number_of_events) + 'events', folder_figures, str(name_L06[2]))

matrix_total_L07 = np.zeros([256,256])
matrix_total_L06 = np.zeros([256,256])

matrix_total_L07[0:128,128:256] = matrix_protony_ptc_L07[64:192,64:192]
matrix_total_L07[128:256,128:256] = matrix_protony_rez_L07[64:192,64:192]
matrix_total_L07[0:128,0:128] = matrix_neutrony_low_L07[64:192,64:192]
matrix_total_L07[128:256,0:128] = matrix_neutrony_high_L07[64:192,64:192]
print_figure_energy(matrix_total_L07, energy_colorbar_max_value, 'Deposited energy in TPX3 L07', folder_figures, '4_segment_L07')

matrix_total_L06[128:256,128:256] = matrix_protony_rez_L06[64:192,64:192]
matrix_total_L06[0:128,0:128] = matrix_neutrony_low_L06[64:192,64:192]
matrix_total_L06[128:256,0:128] = matrix_neutrony_high_L06[64:192,64:192]
print_figure_energy(matrix_total_L06, energy_colorbar_max_value, 'Deposited energy in TPX3 L06', folder_figures, '4_segment_L06')