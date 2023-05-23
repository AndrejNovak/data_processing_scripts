from DPE_functions import *

def calculate_simple_length(x_coordinates, y_coordinates):
    x_length = max(x_coordinates) - min(x_coordinates)
    y_length = max(y_coordinates) - min(y_coordinates)
    return (np.sqrt(x_length ** 2 + y_length ** 2) * 55 + 55)

OutputPath_straightening = ['Q:\\straightening_test_script\\APCOM\\GaAs\\',
                            'Q:\\straightening_test_script\\APCOM\\Si100\\',
                            'Q:\\straightening_test_script\\APCOM\\Si300\\',
                            'Q:\\straightening_test_script\\APCOM\\Si500\\',
                            'Q:\\straightening_test_script\\APCOM\\CdTe\\',]

OutputName_skeleton = 'skeleton_test'

clog_paths = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\GaAs_500um_new_clusterer\\31_MeV\\80_angle\\',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\Si_100um_new_clusterer\\31_MeV\\80_angle\\',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\Si_300um_new_clusterer\\31_MeV\\80_angle\\',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\Si_500um_new_clusterer\\31_MeV\\80_angle\\',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\CdTe_2000um_new_clusterer\\31_MeV\\80_angle\\']

elist_paths = ['Q:\\DPE_carlos_data_output\\2018_08_01_protons\\GaAs_500um_new_clusterer\\31_MeV\\80_angle\\Elist.txt',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\Si_100um_new_clusterer\\31_MeV\\80_angle\\Elist.txt',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\Si_300um_new_clusterer\\31_MeV\\80_angle\\Elist.txt',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\Si_500um_new_clusterer\\31_MeV\\80_angle\\Elist.txt',
              'Q:\\DPE_carlos_data_output\\2018_08_01_protons\\CdTe_2000um_new_clusterer\\31_MeV\\80_angle\\Elist.txt']

names = ['GaAsCr_500um', 'Si_100um', 'Si_300um', 'Si_500um', 'CdTe_2000um']
#names = ['GaAsCr_500um', 'Si_100um']

number_of_particles = np.array([1000, 1000, 100000, 1000, 2000])


for j in range(len(names)):
    print(f'Working on the {names[j]}')
    elist_data = np.loadtxt(elist_paths[j], skiprows=2, delimiter='\t')
    print(f'Elist length is {len(elist_data[:,0])}')

    size_data = []
    energy_data = []
    length_data = []
    length_width_corrected = []
    elist_let = []
    angle_data = []
    ID_cislo = []
    simple_length = []

    print('Elist finished, now the clog')
    clog = read_clog_multiple(clog_paths[j])
    print(f'The total number of clusters in {names[j]} is {len(clog[:])}')

    if len(elist_data[:,0]) != len(clog):
        print('Warning: Elist and clog are not the same length')
    else:
        print('Success: Elist and clog are the same length')

    
    vmax = 1E5
    OutputName_energy_not_filtered = 'Energy_matrix_'+str(number_of_particles[j])+'_not_filtered' 

    title = str(number_of_particles[j]) + ' in ' + str(names[j] + ' - not filtered')
    print_figure_energy(create_matrix_tpx3_t3pa(clog, number_of_particles[j]), vmax, title, OutputPath_straightening[j], OutputName_energy_not_filtered)
    

    k = 0

    results_txt = np.loadtxt(OutputPath_straightening[j] + names[j] + 'cluster_data.txt', delimiter=' ', skiprows=1)

    #energy_threshold = np.array([20000, 1200, 4000, 4000, 20000])

    print(results_txt[0,0])

    for idx,var in enumerate(np.ndarray.tolist(results_txt[:,0])):
        print(idx, int(var))
        i = int(var)
    #for i in range(len(elist_data[:,0])):
        if elist_data[i,7] > 20 and elist_data[i,4] > 1000 and elist_data[i,2] > 10 and elist_data[i,2] < 245 and elist_data[i,3] > 10 and elist_data[i,3] < 245 and k <= 100 and k <= 100:
            #print(f'Cluster {i} passed and is further processed')
            end_x, end_y = cluster_skeleton_ends_joints(clog[i], i, OutputPath_straightening[j], OutputName_skeleton)
            k += 1

            #if len(end_x) == 2:
                #print(f'{names[j]} cluster {i} has 2 ends and is processed')
                #ID_cislo.append(i)
                #energy_data.append(elist_data[i,4])
                #size_data.append(elist_data[i,7])
                #length_data.append(elist_data[i,13] * 55)
                #length_width_corrected.append(elist_data[i,23] * 55)
                #elist_let.append(elist_data[i,26])
                #simple_length.append(calculate_simple_length(end_x, end_y))
            

    #out_values = np.column_stack((ID_cislo[:-1], energy_data[:-1], size_data[:-1], simple_length[:-1], length_data[:-1], length_width_corrected[:-1], elist_let[:-1]))
    #out_values = np.column_stack((ID_cislo[:-1], simple_length[:-1], length_data[:-1], length_width_corrected[:-1]))
    #np.savetxt(OutputPath_straightening[j] + names[j] + 'cluster_data.txt', out_values, delimiter=',', header='ID, Simple_length, DPE_length, DPE_len_corrected', fmt="%i %.5f %.5f %.5f", comments='')
    #np.savetxt(OutputPath_straightening[j] + names[j] + 'cluster_data.txt', out_values, delimiter=',', header='ID, Energy, Size, Simple_length, DPE_length, DPE_len_corrected, LET', fmt="%i", comments='')


matrix_gaas = np.loadtxt(OutputPath_straightening[0] + 'Energy_matrix_' + str(number_of_particles[0]) + '_not_filtered.txt')
matrix_si100 = np.loadtxt(OutputPath_straightening[1] + 'Energy_matrix_' + str(number_of_particles[1]) + '_not_filtered.txt')
matrix_si300 = np.loadtxt(OutputPath_straightening[2] + 'Energy_matrix_' + str(number_of_particles[2]) + '_not_filtered.txt')
matrix_si500 = np.loadtxt(OutputPath_straightening[3] + 'Energy_matrix_' + str(number_of_particles[3]) + '_not_filtered.txt')
matrix_cdte = np.loadtxt(OutputPath_straightening[4] + 'Energy_matrix_' + str(number_of_particles[4]) + '_not_filtered.txt')

matrix_total = np.zeros([240,160])

matrix_total[0:80,80:160] = matrix_cdte[0:80,100:180]
matrix_total[80:160,80:160] = matrix_gaas[80:160,80:160]
matrix_total[0:80,0:80] = matrix_si100[80:160,80:160]
matrix_total[80:160,0:80] = matrix_si300[80:160,80:160]
matrix_total[160:240,0:80] = matrix_si500[80:160,80:160]
matrix_total[79:80,:] = 1E7
matrix_total[159:160,:] = 1E7
matrix_total[:,79:80] = 1E7

vmax = 1E5
print_figure_energy_apcom_2023(matrix_total, vmax, 'Energy deposited in each detector', 'Q:\\straightening_test_script\\APCOM\\', '5_segment_total_deposited_energy')


filtered_data_gaas = np.loadtxt(OutputPath_straightening[0] + names[0] + 'cluster_data.txt', delimiter=' ', skiprows=1)
filtered_data_si100 = np.loadtxt(OutputPath_straightening[1] + names[1] + 'cluster_data.txt', delimiter=' ', skiprows=1)
filtered_data_si300 = np.loadtxt(OutputPath_straightening[2] + names[2] + 'cluster_data.txt', delimiter=' ', skiprows=1)
filtered_data_si500 = np.loadtxt(OutputPath_straightening[3] + names[3] + 'cluster_data.txt', delimiter=' ', skiprows=1)
filtered_data_cdte = np.loadtxt(OutputPath_straightening[4] + names[4] + 'cluster_data.txt', delimiter=' ', skiprows=1)

lin_wd = 2
tickfnt = 20
mydpi = 300
right_x = 6000
bin_size = 128
alpha_value = 0.9

for j in range(len(names)):
    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_gaas[:,1], bins=bin_size, histtype = 'step', label=names[0], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si100[:,1], bins=bin_size, histtype = 'step', label=names[1], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si300[:,1], bins=bin_size, histtype = 'step', label=names[2], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si500[:,1], bins=bin_size, histtype = 'step', label=names[3], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_cdte[:,1], bins=bin_size, histtype = 'step', label=names[4], linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Simple length', fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_gaas[:,2], bins=bin_size, histtype = 'step', label=names[0], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si100[:,2], bins=bin_size, histtype = 'step', label=names[1], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si300[:,2], bins=bin_size, histtype = 'step', label=names[2], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si500[:,2], bins=bin_size, histtype = 'step', label=names[3], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_cdte[:,2], bins=bin_size, histtype = 'step', label=names[4], linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('DPE simple length', fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length_DPE.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_gaas[:,3], bins=bin_size, histtype = 'step', label=names[0], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si100[:,3], bins=bin_size, histtype = 'step', label=names[1], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si300[:,3], bins=bin_size, histtype = 'step', label=names[2], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si500[:,3], bins=bin_size, histtype = 'step', label=names[3], linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_cdte[:,3], bins=bin_size, histtype = 'step', label=names[4], linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('DPE corrected simple length', fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length_DPE_corrected.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_gaas[:,1], bins=bin_size, histtype = 'step', label='Simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_gaas[:,2], bins=bin_size, histtype = 'step', label='DPE simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_gaas[:,3], bins=bin_size, histtype = 'step', label='DPE corrected', linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Length calculation - ' + str(names[0]), fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length_'+str(names[0])+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_si100[:,1], bins=bin_size, histtype = 'step', label='Simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si100[:,2], bins=bin_size, histtype = 'step', label='DPE simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si100[:,3], bins=bin_size, histtype = 'step', label='DPE corrected', linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Length calculation - '+str(names[1]), fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length_'+str(names[1])+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    
    
    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_si300[:,1], bins=bin_size, histtype = 'step', label='Simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si300[:,2], bins=bin_size, histtype = 'step', label='DPE simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si300[:,3], bins=bin_size, histtype = 'step', label='DPE corrected', linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Length calculation - '+str(names[2]), fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length_'+str(names[2])+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_si500[:,1], bins=bin_size, histtype = 'step', label='Simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si500[:,2], bins=bin_size, histtype = 'step', label='DPE simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_si500[:,3], bins=bin_size, histtype = 'step', label='DPE corrected', linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Length calculation - '+str(names[3]), fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length_'+str(names[3])+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(filtered_data_cdte[:,1], bins=bin_size, histtype = 'step', label='Simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_cdte[:,2], bins=bin_size, histtype = 'step', label='DPE simple', linewidth=lin_wd, alpha = alpha_value)
    plt.hist(filtered_data_cdte[:,3], bins=bin_size, histtype = 'step', label='DPE corrected', linewidth=lin_wd, alpha = alpha_value)
    plt.xlim(left=0, right=right_x)
    plt.ylim(bottom=1, top=1E4)
    plt.yscale('log')
    plt.xlabel('Length [$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Length calculation - '+str(names[4]), fontsize=tickfnt)
    plt.legend(loc='upper right', fontsize=14)
    plt.savefig('Q:\\straightening_test_script\\APCOM\\simple_length_'+str(names[4])+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    

number_of_clusters = 100
"""
for j in range(len(names)):
    print(f'Working on the {names[j]}')
    elist_data = np.loadtxt(elist_paths[j], skiprows=2, delimiter='\t')
    print(f'Elist length is {len(elist_data[:,0])}')

    print('Elist finished, now the clog')
    clog = read_clog_multiple(clog_paths[j])
    print(f'The total number of clusters in {names[j]} is {len(clog[:])}')

    if len(elist_data[:,0]) != len(clog):
        print('Warning: Elist and clog are not the same length')
    else:
        print('Success: Elist and clog are the same length')

    results_txt = np.loadtxt(OutputPath_straightening[j] + names[j] + 'cluster_data.txt', delimiter=' ', skiprows=1)
    
    matrix_new = np.zeros([256, 256])
    counter = 0
    
    # samostatne vytvoriť CdTe - protony sa zachytavaju na zaciatku senzora - prerobit poziciu tej matice

    for idx,var in enumerate(np.ndarray.tolist(results_txt[:,0])):
        if counter < number_of_clusters and idx < number_of_clusters:
            #print(idx, int(var))
            m = int(var)
            #print(f'Counter value is {counter} and idx is {idx}')
            cluster_size_clog = len(clog[m][:])
            #print(cluster_size_clog)
            
            for k in range(cluster_size_clog):
                x, y = int(clog[m][k][0]), int(clog[m][k][1])
                matrix_new[x, y] += clog[m][k][2]
        counter += 1
    
    OutputName_energy_filtered = 'Energy_matrix_'+str(number_of_clusters)+'_filtered'
    title = str(number_of_clusters) + ' in ' + str(names[j] + ' - filtered')

    print_figure_energy(matrix_new, vmax, title, OutputPath_straightening[j], OutputName_energy_filtered)
"""
matrix_gaas = np.loadtxt(OutputPath_straightening[0] + 'Energy_matrix_'+str(number_of_clusters)+'_filtered.txt')
matrix_si100 = np.loadtxt(OutputPath_straightening[1] + 'Energy_matrix_'+str(number_of_clusters)+'_filtered.txt')
matrix_si300 = np.loadtxt(OutputPath_straightening[2] + 'Energy_matrix_'+str(number_of_clusters)+'_filtered.txt')
matrix_si500 = np.loadtxt(OutputPath_straightening[3] + 'Energy_matrix_'+str(number_of_clusters)+'_filtered.txt')
matrix_cdte = np.loadtxt(OutputPath_straightening[4] + 'Energy_matrix_'+str(number_of_clusters)+'_filtered.txt')

matrix_total = np.zeros([240,160])

matrix_total[0:80,80:160] = matrix_cdte[0:80,100:180] # 80:160
matrix_total[80:160,80:160] = matrix_gaas[80:160,80:160]
matrix_total[0:80,0:80] = matrix_si100[80:160,80:160]
matrix_total[80:160,0:80] = matrix_si300[80:160,80:160]
matrix_total[160:240,0:80] = matrix_si500[80:160,80:160]
matrix_total[79:80,:] = 1E7
matrix_total[159:160,:] = 1E7
matrix_total[:,79:80] = 1E7

print_figure_energy_apcom_2023(matrix_total, vmax, 'Energy deposited in each detector', 'Q:\\straightening_test_script\\APCOM\\', '5_segment_total_deposited_energy_filtered')


"""
# Pre vypocet odchylky medzi dvoma typmi vypoctu

for j in range(len(names)):
    print(f'Working on the {names[j]} ')

    results_txt = np.loadtxt(OutputPath_straightening[j] + names[j] + 'cluster_data.txt', delimiter=' ', skiprows=1)

    """