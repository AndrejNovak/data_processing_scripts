from DPE_functions import *

#######################################################
# 4 segment matrix s ukazkou roznych experimentov
#
#upravene read_clog_multiple - potom opraviť naspäť

path_L07_ptc = r'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\Files\\'
path_L07_rez = r'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\38_10ms\\Files\\'
path_L07_n_low = r'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\03\\Files\\'
path_L07_n_high = r'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\06\\Files\\'

path_L06_rez = r'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38_10ms\\Files\\'
path_L06_n_low = r'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\03\\Files\\'
path_L06_n_high = r'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\06\\Files\\'

# Histograms generation

elist_L07_ptc = np.loadtxt(path_L07_ptc + 'ExtElist.txt', skiprows=2, delimiter=';')
elist_L07_rez = np.loadtxt(path_L07_rez + 'ExtElist.txt', skiprows=2, delimiter=';')
elist_L07_n_low = np.loadtxt(path_L07_n_low + 'ExtElist.txt', skiprows=2, delimiter=';')
elist_L07_n_high = np.loadtxt(path_L07_n_high + 'ExtElist.txt', skiprows=2, delimiter=';')

elist_L06_rez = np.loadtxt(path_L06_rez + 'ExtElist.txt', skiprows=2, delimiter=';')
elist_L06_n_low = np.loadtxt(path_L06_n_low + 'ExtElist.txt', skiprows=2, delimiter=';')
elist_L06_n_high = np.loadtxt(path_L06_n_high + 'ExtElist.txt', skiprows=2, delimiter=';')

energy_colorbar_max_value = 2E3
name_L07 = ['HE protons - 226 MeV 75 deg', 'LE protons - 31 MeV 75 deg', 'neutrons - 770 keV', 'neutrons - 15.5 MeV']
name_L06 = ['LE protons - 31 MeV 75 deg', 'neutrons - 770 keV', 'neutrons - 15.5 MeV']
folder_figures = r'C:\Users\andrej\Documents\FEI\2023_iworid_prispevok\abstrakt_figures\\'
number_of_events = 1000

lin_wd = 1.75
tickfnt = 16
alpha_val = 0.9
mydpi = 300

bin_energy = np.array([2000000, 400000, 1000000, 2000000, 4096, 4096, 4096])
bin_height = np.array([3000000, 800000, 1000000, 2000000, 4096, 4096, 4096])
bin_size = np.array([90, 80, 40, 86, 60, 18, 70])
bin_let = np.array([2000000, 400000, 1000000, 1000000, 4096, 4096, 4096])
bin_epx = np.array([2000000, 400000, 1000000, 1000000, 4096, 4096, 4096])

test_bins = np.append(np.arange(0, 1000, 40, dtype=int), np.arange(1000, 100000, 400, dtype=int))

"""
plt.close()
plt.clf()
plt.cla()
#plt.hist(elist_L07_ptc[:,4], bins=test_bins, histtype = 'step', label=name_L07[0], linewidth=lin_wd, alpha=alpha_val)
#plt.hist(elist_L07_rez[:,4], bins=test_bins, histtype = 'step', label=name_L07[1], linewidth=lin_wd, alpha=alpha_val)
#plt.hist(elist_L07_n_low[:,4], bins=test_bins, histtype = 'step', label=name_L07[2], linewidth=lin_wd, alpha=alpha_val)
#plt.hist(elist_L07_n_high[:,4], bins=test_bins, histtype = 'step', label=name_L07[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_ptc[:,4], bins=bin_energy[0], histtype = 'step', label=name_L07[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_rez[:,4], bins=bin_energy[1], histtype = 'step', label=name_L07[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_n_low[:,4], bins=bin_energy[2], histtype = 'step', label=name_L07[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_n_high[:,4], bins=bin_energy[3], histtype = 'step', label=name_L07[3], linewidth=lin_wd, alpha=alpha_val)
#plt.hist(elist_L06_rez[:,4], bins=bin_energy[4], histtype = 'step', label=name_L06[0], linewidth=lin_wd, alpha=alpha_val)
#plt.hist(elist_L06_n_low[:,4], bins=bin_energy[5], histtype = 'step', label=name_L06[1], linewidth=lin_wd, alpha=alpha_val)
#plt.hist(elist_L06_n_high[:,4], bins=bin_energy[6], histtype = 'step', label=name_L06[2], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=5, right=1E4)
plt.ylim(bottom=10, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution')
plt.legend(loc='upper right')
plt.savefig(folder_figures + 'L07_histogram_1_energy.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
 
plt.close()
plt.clf()
plt.cla()
#plt.hist(elist_L07_ptc[:,8], bins=test_bins, histtype = 'step', label=name_L07[0], linewidth=lin_wd)
#plt.hist(elist_L07_rez[:,8], bins=test_bins, histtype = 'step', label=name_L07[1], linewidth=lin_wd)
#plt.hist(elist_L07_n_low[:,8], bins=test_bins, histtype = 'step', label=name_L07[2], linewidth=lin_wd)
#plt.hist(elist_L07_n_high[:,8], bins=test_bins, histtype = 'step', label=name_L07[3], linewidth=lin_wd)
plt.hist(elist_L07_ptc[:,8], bins=bin_height[0], histtype = 'step', label=name_L07[0], linewidth=lin_wd)
plt.hist(elist_L07_rez[:,8], bins=bin_height[1], histtype = 'step', label=name_L07[1], linewidth=lin_wd)
plt.hist(elist_L07_n_low[:,8], bins=bin_height[2], histtype = 'step', label=name_L07[2], linewidth=lin_wd)
plt.hist(elist_L07_n_high[:,8], bins=bin_height[3], histtype = 'step', label=name_L07[3], linewidth=lin_wd)
#plt.hist(elist_L06_rez[:,8], bins=bin_height[4], histtype = 'step', label=name_L06[0], linewidth=lin_wd)
#plt.hist(elist_L06_n_low[:,8], bins=bin_height[5], histtype = 'step', label=name_L06[1], linewidth=lin_wd)
#plt.hist(elist_L06_n_high[:,8], bins=bin_height[6], histtype = 'step', label=name_L06[2], linewidth=lin_wd)
plt.xlim(left=5, right=5E3)
plt.ylim(bottom=10, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution')
plt.legend(loc='upper right')
plt.savefig(folder_figures + 'L07_histogram_2_height.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_ptc[:,7], bins=bin_size[0], histtype = 'step', label=name_L07[0], linewidth=lin_wd)
plt.hist(elist_L07_rez[:,7], bins=bin_size[1], histtype = 'step', label=name_L07[1], linewidth=lin_wd)
plt.hist(elist_L07_n_low[:,7], bins=bin_size[2], histtype = 'step', label=name_L07[2], linewidth=lin_wd)
plt.hist(elist_L07_n_high[:,7], bins=bin_size[3], histtype = 'step', label=name_L07[3], linewidth=lin_wd)
#plt.hist(elist_L06_rez[:,7], bins=bin_size[4], histtype = 'step', label=name_L06[0], linewidth=lin_wd)
#plt.hist(elist_L06_n_low[:,7], bins=bin_size[5], histtype = 'step', label=name_L06[1], linewidth=lin_wd)
#plt.hist(elist_L06_n_high[:,7], bins=bin_size[6], histtype = 'step', label=name_L06[2], linewidth=lin_wd)
plt.xlim(left=1, right=1E3)
plt.ylim(bottom=10, top=1E7)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution')
plt.legend(loc='upper right')
plt.savefig(folder_figures + 'L07_histogram_3_size.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

L07_ptc_LET = elist_L07_ptc[:,4] / (np.sqrt((elist_L07_ptc[:,13] * 55) ** 2 + 65**2))
L07_rez_LET = elist_L07_rez[:,4] / (np.sqrt((elist_L07_rez[:,13] * 55) ** 2 + 65**2))
L07_n_low_LET = elist_L07_n_low[:,4] / (np.sqrt((elist_L07_n_low[:,13] * 55) ** 2 + 65**2))
L07_n_high_LET = elist_L07_n_high[:,4] / (np.sqrt((elist_L07_n_high[:,13] * 55) ** 2 + 65**2))

L06_rez_LET = elist_L06_rez[:,4] / (np.sqrt((elist_L06_rez[:,13] * 55) ** 2 + 65**2))
L06_n_low_LET = elist_L06_n_low[:,4] / (np.sqrt((elist_L06_n_low[:,13] * 55) ** 2 + 65**2))
L06_n_high_LET = elist_L06_n_high[:,4] / (np.sqrt((elist_L06_n_high[:,13] * 55) ** 2 + 65**2))

plt.close()
plt.clf()
plt.cla()
#plt.hist(L07_ptc_LET, bins=test_bins, histtype = 'step', label=name_L07[0], linewidth=lin_wd)
#plt.hist(L07_rez_LET, bins=test_bins, histtype = 'step', label=name_L07[1], linewidth=lin_wd)
#plt.hist(L07_n_low_LET, bins=test_bins, histtype = 'step', label=name_L07[2], linewidth=lin_wd)
#plt.hist(L07_n_high_LET, bins=test_bins, histtype = 'step', label=name_L07[3], linewidth=lin_wd)
plt.hist(L07_ptc_LET, bins=bin_let[0], histtype = 'step', label=name_L07[0], linewidth=lin_wd)
plt.hist(L07_rez_LET, bins=bin_let[1], histtype = 'step', label=name_L07[1], linewidth=lin_wd)
plt.hist(L07_n_low_LET, bins=bin_let[2], histtype = 'step', label=name_L07[2], linewidth=lin_wd)
plt.hist(L07_n_high_LET, bins=bin_let[3], histtype = 'step', label=name_L07[3], linewidth=lin_wd)
#plt.hist(L06_rez_LET, bins=bin_let[4], histtype = 'step', label=name_L06[0], linewidth=lin_wd)
#plt.hist(L06_n_low_LET, bins=bin_let[5], histtype = 'step', label=name_L06[1], linewidth=lin_wd)
#plt.hist(L06_n_high_LET, bins=bin_let[6], histtype = 'step', label=name_L06[2], linewidth=lin_wd)
plt.xlim(left=1E-1, right=5E1)
plt.ylim(bottom=10, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution')
plt.legend(loc='upper right')
plt.savefig(folder_figures + 'L07_histogram_4_LET.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
#plt.hist(elist_L07_ptc[:,4]/elist_L07_ptc[:,7], bins=test_bins, histtype = 'step', label=name_L07[0], linewidth=lin_wd)
#plt.hist(elist_L07_rez[:,4]/elist_L07_rez[:,7], bins=test_bins, histtype = 'step', label=name_L07[1], linewidth=lin_wd)
#plt.hist(elist_L07_n_low[:,4]/elist_L07_n_low[:,7], bins=test_bins, histtype = 'step', label=name_L07[2], linewidth=lin_wd)
#plt.hist(elist_L07_n_high[:,4]/elist_L07_n_high[:,7], bins=test_bins, histtype = 'step', label=name_L07[3], linewidth=lin_wd)
plt.hist(elist_L07_ptc[:,4]/elist_L07_ptc[:,7], bins=bin_epx[0], histtype = 'step', label=name_L07[0], linewidth=lin_wd)
plt.hist(elist_L07_rez[:,4]/elist_L07_rez[:,7], bins=bin_epx[1], histtype = 'step', label=name_L07[1], linewidth=lin_wd)
plt.hist(elist_L07_n_low[:,4]/elist_L07_n_low[:,7], bins=bin_epx[2], histtype = 'step', label=name_L07[2], linewidth=lin_wd)
plt.hist(elist_L07_n_high[:,4]/elist_L07_n_high[:,7], bins=bin_epx[3], histtype = 'step', label=name_L07[3], linewidth=lin_wd)
#plt.hist(elist_L06_rez[:,4]/elist_L06_rez[:,7], bins=bin_epx[4], histtype = 'step', label=name_L06[0], linewidth=lin_wd)
#plt.hist(elist_L06_n_low[:,4]/elist_L06_n_low[:,7], bins=bin_epx[5], histtype = 'step', label=name_L06[1], linewidth=lin_wd)
#plt.hist(elist_L06_n_high[:,4]/elist_L06_n_high[:,7], bins=bin_epx[6], histtype = 'step', label=name_L06[2], linewidth=lin_wd)
plt.xlim(left=5, right=1E5)
plt.ylim(bottom=10, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('E/Size [keV/px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Per pixel energy distribution')
plt.legend(loc='upper right')
plt.savefig(folder_figures + 'L07_histogram_5_Epx.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""




print('You can stop now')


clog_protony_ptc_L07 = read_clog_multiple(path_L07_ptc)
clog_protony_rez_L07 = read_clog_multiple(path_L07_rez)
clog_neutrony_low_L07 = read_clog_multiple(path_L07_n_low)
clog_neutrony_high_L07 = read_clog_multiple(path_L07_n_high)

clog_protony_rez_L06 = read_clog_multiple(path_L06_rez)
clog_neutrony_low_L06 = read_clog_multiple(path_L06_n_low)
clog_neutrony_high_L06 = read_clog_multiple(path_L06_n_high)

matrix_protony_ptc_L07 = create_matrix_tpx3_t3pa(clog_protony_ptc_L07, number_of_events)
matrix_protony_rez_L07 = create_matrix_tpx3_t3pa(clog_protony_rez_L07, number_of_events)
matrix_neutrony_low_L07 = create_matrix_tpx3_t3pa(clog_neutrony_low_L07, number_of_events)
matrix_neutrony_high_L07 = create_matrix_tpx3_t3pa(clog_neutrony_high_L07, number_of_events)

matrix_protony_rez_L06 = create_matrix_tpx3_t3pa(clog_protony_rez_L06, number_of_events)
matrix_neutrony_low_L06 = create_matrix_tpx3_t3pa(clog_neutrony_low_L06, number_of_events)
matrix_neutrony_high_L06 = create_matrix_tpx3_t3pa(clog_neutrony_high_L06, number_of_events)

print_figure_energy(matrix_protony_ptc_L07, energy_colorbar_max_value, 'Deposited energy by ' + str(number_of_events) + ' events', folder_figures, str(name_L07[0]))
print_figure_energy(matrix_protony_rez_L07, energy_colorbar_max_value, 'Deposited energy by ' + str(number_of_events) + ' events', folder_figures, str(name_L07[1]))
print_figure_energy(matrix_neutrony_low_L07, energy_colorbar_max_value, 'Deposited energy by ' + str(number_of_events) + ' events', folder_figures, str(name_L07[2]))
print_figure_energy(matrix_neutrony_high_L07, energy_colorbar_max_value, 'Deposited energy by ' + str(number_of_events) + ' events', folder_figures, str(name_L07[3]))

print_figure_energy(matrix_protony_rez_L06, energy_colorbar_max_value, 'Deposited energy by ' + str(number_of_events) + ' events', folder_figures, str(name_L06[0]))
print_figure_energy(matrix_neutrony_low_L06, energy_colorbar_max_value, 'Deposited energy by ' + str(number_of_events) + ' events', folder_figures, str(name_L06[1]))
print_figure_energy(matrix_neutrony_high_L06, energy_colorbar_max_value, 'Deposited energy by ' + str(number_of_events) + ' events', folder_figures, str(name_L06[2]))

#matrix_total_L07 = np.zeros([256,256])
#matrix_total_L06 = np.zeros([256,256])

#matrix_total_L07[0:128,128:256] = matrix_protony_ptc_L07[64:192,64:192]
#matrix_total_L07[128:256,128:256] = matrix_protony_rez_L07[64:192,64:192]
#xmatrix_total_L07[0:128,0:128] = matrix_neutrony_low_L07[64:192,64:192]
#matrix_total_L07[128:256,0:128] = matrix_neutrony_high_L07[64:192,64:192]
#print_figure_energy(matrix_total_L07, energy_colorbar_max_value, 'Deposited energy in TPX3 L07 by ' + str(number_of_events) + ' events', folder_figures, '4_segment_L07')

#matrix_total_L06[128:256,128:256] = matrix_protony_rez_L06[64:192,64:192]
#matrix_total_L06[0:128,0:128] = matrix_neutrony_low_L06[64:192,64:192]
#matrix_total_L06[128:256,0:128] = matrix_neutrony_high_L06[64:192,64:192]
#print_figure_energy(matrix_total_L06, energy_colorbar_max_value, 'Deposited energy in TPX3 L06 by ' + str(number_of_events) + ' events', folder_figures, '4_segment_L06')

matrix_total_L07 = np.zeros([100,100])
matrix_total_L06 = np.zeros([100,100])

matrix_total_L07[0:50,50:100] = matrix_protony_ptc_L07[100:150,100:150]
matrix_total_L07[0:50,0:50] = matrix_protony_rez_L07[100:150,100:150]
matrix_total_L07[50:100,0:50] = matrix_neutrony_low_L07[100:150,100:150]
matrix_total_L07[50:100,50:100] = matrix_neutrony_high_L07[100:150,100:150]
matrix_total_L07[49:50,:] = 1E6
matrix_total_L07[:,49:50] = 1E6
print_figure_energy_iworid_2023(matrix_total_L07, energy_colorbar_max_value, '65 $\mu$m thick SiC TPX3 MiniPIX', folder_figures, '4_segment_L07_50px')

#matrix_total_L06[50:100,50:100] = matrix_protony_rez_L06[100:150,100:150]
#matrix_total_L06[0:50,0:50] = matrix_neutrony_low_L06[100:150,100:150]
#matrix_total_L06[50:100,0:50] = matrix_neutrony_high_L06[100:150,100:150]
#print_figure_energy_iworid_2023(matrix_total_L06, energy_colorbar_max_value, 'Deposited energy in TPX3 L06 by ' + str(number_of_events) + ' events', folder_figures, '4_segment_L06_50px')
