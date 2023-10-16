from DPE_functions import *

lin_wd = 1.75
tickfnt = 18
alpha_val = 0.9
mydpi = 300


"""
#
# PROCESS VAN DE GRAAF FOLDER 11 - 5 MeV
# 

vdg_5MeV_paths = ['Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\11\\', 'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\11\\']
vdf_5MeV_path_out = 'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_11\\'

elist_L06 =  np.loadtxt(vdg_5MeV_paths[0] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07 =  np.loadtxt(vdg_5MeV_paths[1] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')

bins = np.array([9000, 400000])
bins_size = np.array([50,50])

histogram_label = ['L06', 'L07']

title_addition = ', 5 MeV fast neutrons'

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,4], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,4], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdf_5MeV_path_out + 'energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,8], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,8], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdf_5MeV_path_out + 'height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,7], bins=bins_size[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
#plt.xlim(left=1, right=100)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdf_5MeV_path_out + 'size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

elist_LET_L06 = elist_L06[:,4] / (np.sqrt((elist_L06[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07 = elist_L07[:,4] / (np.sqrt((elist_L07[:,13] * 55) ** 2 + 65 ** 2))

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_LET_L06[:], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07[:], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1E-2, right=1E4)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdf_5MeV_path_out + 'LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,4]/elist_L06[:,7], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,4]/elist_L07[:,7], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('E/Size [keV/px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Per-pixel energy distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdf_5MeV_path_out + 'perpxE_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)





#
# PROCESS VAN DE GRAAF FOLDER 07 - 15.5 MeV
# 

vdg_15_5MeV_paths = ['Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\07\\', 'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\07\\']
vdg_path_out = 'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_07\\'

elist_L06 =  np.loadtxt(vdg_15_5MeV_paths[0] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07 =  np.loadtxt(vdg_15_5MeV_paths[1] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')

bins = np.array([9000, 400000])
bins_size = np.array([50,50])

histogram_label = ['L06', 'L07']

title_addition = ', 15.5 MeV fast neutrons'

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,4], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,4], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,8], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,8], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,7], bins=bins_size[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
#plt.xlim(left=1, right=100)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

elist_LET_L06 = elist_L06[:,4] / (np.sqrt((elist_L06[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07 = elist_L07[:,4] / (np.sqrt((elist_L07[:,13] * 55) ** 2 + 65 ** 2))

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_LET_L06[:], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07[:], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1E-2, right=1E4)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,4]/elist_L06[:,7], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,4]/elist_L07[:,7], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('E/Size [keV/px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Per-pixel energy distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'perpxE_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)



#
# PROCESS VAN DE GRAAF FOLDER 08 - 17.5 MeV
# 

vdg_17_5MeV_paths = ['Q:\\DPE_carlos_data_output\\2022_12_VdG\\L06\\08\\', 'Q:\\DPE_carlos_data_output\\2022_12_VdG\\L07\\08\\']
vdg_path_out = 'Q:\\2023_iworid_data_processing\\processing_selected\\VdG_08\\'

elist_L06 =  np.loadtxt(vdg_17_5MeV_paths[0] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07 =  np.loadtxt(vdg_17_5MeV_paths[1] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')

bins = np.array([9000, 400000])
bins_size = np.array([50,50])

histogram_label = ['L06', 'L07']

title_addition = ', 17.5 MeV fast neutrons'

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,4], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,4], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,8], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,8], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,7], bins=bins_size[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
#plt.xlim(left=1, right=100)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

elist_LET_L06 = elist_L06[:,4] / (np.sqrt((elist_L06[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07 = elist_L07[:,4] / (np.sqrt((elist_L07[:,13] * 55) ** 2 + 65 ** 2))

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_LET_L06[:], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07[:], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1E-2, right=1E4)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06[:,4]/elist_L06[:,7], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07[:,4]/elist_L07[:,7], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1, right=1E5)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('E/Size [keV/px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Per-pixel energy distribution' + title_addition)
plt.legend(loc='upper right')
plt.savefig(vdg_path_out + 'perpxE_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

"""

#
# PROCESS Rez all angle - 31 MeV
# 

rez_paths = ['Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\27_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\32_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\33_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\38_10ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L06\\39_100ms\\',
'Q:\\DPE_carlos_data_output\\2023_03_protons\\data_AA\\L07\\39_100ms\\']
rez_path_out = 'Q:\\2023_iworid_data_processing\\processing_selected\\rez\\'


elist_L06_00deg =  np.loadtxt(rez_paths[0] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_00deg =  np.loadtxt(rez_paths[1] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L06_45deg =  np.loadtxt(rez_paths[2] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_45deg =  np.loadtxt(rez_paths[3] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L06_60deg =  np.loadtxt(rez_paths[4] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_60deg =  np.loadtxt(rez_paths[5] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L06_75deg =  np.loadtxt(rez_paths[6] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_75deg =  np.loadtxt(rez_paths[7] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L06_88deg =  np.loadtxt(rez_paths[8] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_88deg =  np.loadtxt(rez_paths[9] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')

bins = np.array([2048, 300000])
bins_size = np.array([60,128])

histogram_label = ['00 deg', '45 deg', '60 deg', '75 deg', '88 deg']

title_addition_L06 = ', L06, 31 MeV protons'
title_addition_L07 = ', L07, 31 MeV protons'

y_top_limit = 1E5

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06_00deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_45deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_60deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_75deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_88deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E5)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution' + title_addition_L06)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L06_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,4], bins=bins[1], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,4], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_60deg[:,4], bins=bins[1], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,4], bins=bins[1], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,4], bins=bins[1], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E5)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L07_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06_00deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_45deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_60deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_75deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_88deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E4)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution' + title_addition_L06)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L06_height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,8], bins=bins[1], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,8], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_60deg[:,8], bins=bins[1], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,8], bins=bins[1], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,8], bins=bins[1], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E5)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L07_height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L06_00deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_45deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_60deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_75deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L06_88deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution' + title_addition_L06)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L06_size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_60deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L07_size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

elist_LET_L06_00deg = elist_L06_00deg[:,4] / (np.sqrt((elist_L06_00deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L06_45deg = elist_L06_45deg[:,4] / (np.sqrt((elist_L06_45deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L06_60deg = elist_L06_60deg[:,4] / (np.sqrt((elist_L06_60deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L06_75deg = elist_L06_75deg[:,4] / (np.sqrt((elist_L06_75deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L06_88deg = elist_L06_88deg[:,4] / (np.sqrt((elist_L06_88deg[:,13] * 55) ** 2 + 65 ** 2))

elist_LET_L07_00deg = elist_L07_00deg[:,4] / (np.sqrt((elist_L07_00deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_45deg = elist_L07_45deg[:,4] / (np.sqrt((elist_L07_45deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_60deg = elist_L07_60deg[:,4] / (np.sqrt((elist_L07_60deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_75deg = elist_L07_75deg[:,4] / (np.sqrt((elist_L07_75deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_88deg = elist_L07_88deg[:,4] / (np.sqrt((elist_L07_88deg[:,13] * 55) ** 2 + 65 ** 2))

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_LET_L06_00deg[:], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L06_45deg[:], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L06_60deg[:], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L06_75deg[:], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L06_88deg[:], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1E-1, right=1E2)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution' + title_addition_L06)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L06_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_LET_L07_00deg[:], bins=bins[1], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_45deg[:], bins=bins[1], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_60deg[:], bins=bins[1], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_75deg[:], bins=bins[1], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_88deg[:], bins=bins[1], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1E-1, right=1E4)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(rez_path_out + 'L07_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)




#
# PROCESS PTC all angle - 100 MeV
# 

ptc_paths = [
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\100MeV\\90deg\\']
ptc_path_out = 'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\100MeV\\'

elist_L07_00deg =  np.loadtxt(ptc_paths[0] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_45deg =  np.loadtxt(ptc_paths[1] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_75deg =  np.loadtxt(ptc_paths[2] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_88deg =  np.loadtxt(ptc_paths[3] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_90deg =  np.loadtxt(ptc_paths[4] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')

bins = np.array([600000])
bins_size = np.array([60])

histogram_label = ['00 deg', '45 deg', '75 deg', '88 deg', '90 deg']

title_addition_L07 = ', L07, 100 MeV protons'

y_top_limit = 1E6


plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_90deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E5)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E5)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_90deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

elist_LET_L07_00deg = elist_L07_00deg[:,4] / (np.sqrt((elist_L07_00deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_45deg = elist_L07_45deg[:,4] / (np.sqrt((elist_L07_45deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_75deg = elist_L07_75deg[:,4] / (np.sqrt((elist_L07_75deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_88deg = elist_L07_88deg[:,4] / (np.sqrt((elist_L07_88deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_90deg = elist_L07_90deg[:,4] / (np.sqrt((elist_L07_90deg[:,13] * 55) ** 2 + 65 ** 2))
        
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_LET_L07_00deg[:], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_45deg[:], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_75deg[:], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_88deg[:], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_90deg[:], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1E-1, right=1E4)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)



#
# PROCESS PTC all angle - 226 MeV
# 

ptc_paths = [
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\00deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\45deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\75deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\88deg\\',
'Q:\\DPE_carlos_data_output\\2022_10_ptc\\226MeV\\90deg\\']
ptc_path_out = 'Q:\\2023_iworid_data_processing\\processing_selected\\ptc\\226MeV\\'

elist_L07_00deg =  np.loadtxt(ptc_paths[0] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_45deg =  np.loadtxt(ptc_paths[1] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_75deg =  np.loadtxt(ptc_paths[2] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_88deg =  np.loadtxt(ptc_paths[3] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')
elist_L07_90deg =  np.loadtxt(ptc_paths[4] + '\\Files\\Elist.txt', skiprows=2, delimiter=';')

bins = np.array([600000])
bins_size = np.array([80])

histogram_label = ['00 deg', '45 deg', '75 deg', '88 deg', '90 deg']

title_addition_L07 = ', L07, 226 MeV protons'

y_top_limit = 1E6

   
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_90deg[:,4], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E5)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Deposited energy distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_energy_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,8], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=10, right=1E5)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Height [keV]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster height distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_height_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(elist_L07_00deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_45deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_75deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_88deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_L07_90deg[:,7], bins=bins_size[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Size [px]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Cluster size distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_size_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

elist_LET_L07_00deg = elist_L07_00deg[:,4] / (np.sqrt((elist_L07_00deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_45deg = elist_L07_45deg[:,4] / (np.sqrt((elist_L07_45deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_75deg = elist_L07_75deg[:,4] / (np.sqrt((elist_L07_75deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_88deg = elist_L07_88deg[:,4] / (np.sqrt((elist_L07_88deg[:,13] * 55) ** 2 + 65 ** 2))
elist_LET_L07_90deg = elist_L07_90deg[:,4] / (np.sqrt((elist_L07_90deg[:,13] * 55) ** 2 + 65 ** 2))
        
plt.close()
plt.clf()
plt.cla()
plt.hist(elist_LET_L07_00deg[:], bins=bins[0], histtype = 'step', label=histogram_label[0], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_45deg[:], bins=bins[0], histtype = 'step', label=histogram_label[1], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_75deg[:], bins=bins[0], histtype = 'step', label=histogram_label[2], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_88deg[:], bins=bins[0], histtype = 'step', label=histogram_label[3], linewidth=lin_wd, alpha=alpha_val)
plt.hist(elist_LET_L07_90deg[:], bins=bins[0], histtype = 'step', label=histogram_label[4], linewidth=lin_wd, alpha=alpha_val)
plt.xlim(left=1E-1, right=1E4)
plt.ylim(bottom=1, top=y_top_limit)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [count]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('LET distribution' + title_addition_L07)
plt.legend(loc='upper right')
plt.savefig(ptc_path_out + 'L07_LET_histogram.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)