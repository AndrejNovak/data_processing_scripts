from DPE_functions import *

def gaas_core_halo_study(FileInPath, FileInName, FileOutPath, FileOutName, angle, max_toa_diff, num_of_frames):
    all_unix_times = read_clog(FileInPath + FileInName)[0]
    all_frame_times = read_clog(FileInPath + FileInName)[1]
    all_data = read_clog(FileInPath + FileInName)[2]

    maximum_ToA_frame_difference = max_toa_diff     # in nanoseconds 5000

    ToA_values = list()
    ToA_values_halo = list()

    difference = list()

    for i in range(len(all_data[:]) - 1):
        matrix_ToA = np.empty([256,256])

        x_list_first = list()
        y_list_first = list()

        x_list_second = list()
        y_list_second = list()

        first_unix = all_unix_times[i]
        first_meas = all_frame_times[i]

        second_unix = all_unix_times[i+1]
        second_meas = all_frame_times[i+1]

        unix_diff = second_unix - first_unix

        difference.append(unix_diff)

        for j in range(len(all_data[i][:])):
            x_first = int(all_data[i][j][0])
            y_first = int(all_data[i][j][1])

            x_list_first.append(x_first)
            y_list_first.append(y_first)

            matrix_ToA[x_first,y_first] = all_data[i][j][3]

            ToA_values.append(str(all_data[i][j][3]))

            indicator = False

        if unix_diff < maximum_ToA_frame_difference:
            for j in range(len(all_data[i+1][:])):
                x_second = int(all_data[i+1][j][0])
                y_second = int(all_data[i+1][j][1])

                x_list_second.append(x_second)
                y_list_second.append(y_second)

                if (x_second) in x_list_first or (x_second) in x_list_first or (x_second - 1) in x_list_first or (x_second + 1) in x_list_first and (y_second - 1) in y_list_first or (y_second + 1) in y_list_first or (y_second) in y_list_first or (y_second) in y_list_first:
                    matrix_ToA[x_second,y_second] = all_data[i+1][j][3] + unix_diff
                    ToA_values.append(str(all_data[i+1][j][3] + unix_diff))
                    ToA_values_halo.append(str(all_data[i+1][j][3] + unix_diff))
                    indicator = True

        else:
            indicator = False

        if i <= num_of_frames:
            pass
            #print_fig_ToA(matrix_ToA, 50, 'test ToA frame #'+str(i), FileOutPath, FileOutName + '_frame_'+str(i))
            #plot_single_cluster_ToA_gaas(FileOutPath, FileInPath+FileInName, i, indicator, 50)
        else:
            pass

    file = open(FileOutPath + 'ToA_values.txt','w')
    for item in ToA_values:
	    file.write(item+"\n")
    file.close()

    file = open(FileOutPath + 'ToA_values_halo.txt','w')
    for item in ToA_values_halo:
	    file.write(item+"\n")
    file.close()

    hist_data = np.loadtxt(FileOutPath + 'ToA_values.txt')
    hist_data_halo = np.loadtxt(FileOutPath + 'ToA_values_halo.txt')

    title = '$\Delta$ToA, 31 MeV protons, ' +str(angle) + '$\degree$'

    plt.close()
    plt.clf()
    plt.cla()
    tickfnt = 14
    a = plt.hist(hist_data[:], bins=512, histtype = 'step', label=title, linewidth=1.75); ys = a[0]; xs = a[1]
    plt.xlim(left=1, right=1E4) #left=1E3
    #plt.ylim(bottom=1, top=1E5)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('ToA [ns]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(title)
    #plt.title(label_det[i]+' deposited energy distribution, '+str(label_energy[n])+' protons')
    plt.legend(loc='upper right')
    plt.savefig(FileOutPath + 'histogram_ToA_values_' + str(angle) + '.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(FileOutPath + 'histogram_ToA_values_' + str(angle) + '.txt', np.c_[xs[1:],ys])

    plt.close()
    plt.clf()
    plt.cla()
    tickfnt = 14
    b = plt.hist(hist_data_halo[:], bins=100, histtype = 'step', label=title, linewidth=1.75); ys = b[0]; xs = b[1]
    plt.xlim(left=1, right=1E4) #left=1E3
    #plt.ylim(bottom=1, top=1E5)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('ToA [ns]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(title)
    plt.legend(loc='upper left')
    plt.savefig(FileOutPath + 'histogram_ToA_values_halo_' + str(angle) + '.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(FileOutPath + 'histogram_ToA_values_halo_' + str(angle) + '.txt', np.c_[xs[1:],ys])

    plt.close()
    plt.clf()
    plt.cla()
    tickfnt = 14
    c = plt.hist(difference[:], bins=250000, histtype = 'step', label=title, linewidth=1.75); ys = c[0]; xs = c[1]
    plt.xlim(left=1, right=1E8) #left=1E3
    plt.ylim(bottom=1, top=1E5)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Cluster time difference [ns]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(title)
    plt.legend(loc='upper left')
    plt.savefig(FileOutPath + 'histogram_unix_difference_' + str(angle) + '.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(FileOutPath + 'histogram_unix_difference_' + str(angle) + '.txt', np.c_[xs[1:],ys])

    return

angle_names = ['00', '10', '20', '30', '40', '50', '60', '70', '80', '85', '88', '89', '90']

"""
for item in angle_names:
    angle = item

    if angle == '00':
        FileInPath = 'Q:/DPE_andrej_data_output/2023_04_elitech/cluster_diff_19500/GaAs/toa_diff_angle_0/'
        FileInName = 'GaAs_pixtoadiff_6000.clog'
        FileOutPath = 'C:/Users/andrej/Documents/FEI/Vyskum/Data_Processing_Engine/elitech_ToA_figures/angle_' + angle + '/'
        FileOutName = '31MeV_proton_' + angle + 'deg_GaAsCr_ToA'

        gaas_core_halo_study(FileInPath, FileInName, FileOutPath, FileOutName, angle, 5000, 0)
    else:
        FileInPath = 'Q:/DPE_andrej_data_output/2023_04_elitech/cluster_diff_19500/GaAs/toa_diff_angle_' + angle + '/'
        FileInName = 'GaAs_pixtoadiff_6000.clog'
        FileOutPath = 'C:/Users/andrej/Documents/FEI/Vyskum/Data_Processing_Engine/elitech_ToA_figures/angle_' + angle + '/'
        FileOutName = '31MeV_proton_' + angle + 'deg_GaAsCr_ToA'

        gaas_core_halo_study(FileInPath, FileInName, FileOutPath, FileOutName, angle, 5000, 0)

    
    print(f'Angle finished: {angle} degrees')
"""


"""
for idx, var in enumerate(angle_names):
    histogram_ToA_values = np.zeros([512, len(angle_names)])
    histogram_ToA_values_halo = np.zeros([128, 2, len(angle_names)])

    FileInPath = 'C:/Users/andrej/Documents/FEI/Vyskum/Data_Processing_Engine/elitech_ToA_figures/angle_' + var + '/'

    histogram_ToA_values[:,:,idx] = np.loadtxt(FileInPath + 'ToA_values_' + var + '.txt')
    histogram_ToA_values_halo[:,:,idx] = np.loadtxt(FileInPath + 'histogram_ToA_values_halo_' + var + '.txt')


print(histogram_ToA_values[:,:,0])
"""

FileInPath = 'C:/Users/andrej/Documents/FEI/Vyskum/Data_Processing_Engine/elitech_ToA_figures/'

histogram_ToA_1 = np.loadtxt(FileInPath + 'angle_00/ToA_values.txt')
histogram_ToA_2 = np.loadtxt(FileInPath + 'angle_10/ToA_values.txt')
histogram_ToA_3 = np.loadtxt(FileInPath + 'angle_20/ToA_values.txt')
histogram_ToA_4 = np.loadtxt(FileInPath + 'angle_30/ToA_values.txt')
histogram_ToA_5 = np.loadtxt(FileInPath + 'angle_40/ToA_values.txt')
histogram_ToA_6 = np.loadtxt(FileInPath + 'angle_50/ToA_values.txt')
histogram_ToA_7 = np.loadtxt(FileInPath + 'angle_60/ToA_values.txt')
histogram_ToA_8 = np.loadtxt(FileInPath + 'angle_70/ToA_values.txt')
histogram_ToA_9 = np.loadtxt(FileInPath + 'angle_80/ToA_values.txt')
histogram_ToA_10 = np.loadtxt(FileInPath + 'angle_85/ToA_values.txt')
histogram_ToA_11 = np.loadtxt(FileInPath + 'angle_88/ToA_values.txt')
histogram_ToA_12 = np.loadtxt(FileInPath + 'angle_89/ToA_values.txt')
histogram_ToA_13 = np.loadtxt(FileInPath + 'angle_90/ToA_values.txt')

histogram_ToA_halo_1 = np.loadtxt(FileInPath + 'angle_00/ToA_values_halo.txt')
histogram_ToA_halo_2 = np.loadtxt(FileInPath + 'angle_10/ToA_values_halo.txt')
histogram_ToA_halo_3 = np.loadtxt(FileInPath + 'angle_20/ToA_values_halo.txt')
histogram_ToA_halo_4 = np.loadtxt(FileInPath + 'angle_30/ToA_values_halo.txt')
histogram_ToA_halo_5 = np.loadtxt(FileInPath + 'angle_40/ToA_values_halo.txt')
histogram_ToA_halo_6 = np.loadtxt(FileInPath + 'angle_50/ToA_values_halo.txt')
histogram_ToA_halo_7 = np.loadtxt(FileInPath + 'angle_60/ToA_values_halo.txt')
histogram_ToA_halo_8 = np.loadtxt(FileInPath + 'angle_70/ToA_values_halo.txt')
histogram_ToA_halo_9 = np.loadtxt(FileInPath + 'angle_80/ToA_values_halo.txt')
histogram_ToA_halo_10 = np.loadtxt(FileInPath + 'angle_85/ToA_values_halo.txt')
histogram_ToA_halo_11 = np.loadtxt(FileInPath + 'angle_88/ToA_values_halo.txt')
histogram_ToA_halo_12 = np.loadtxt(FileInPath + 'angle_89/ToA_values_halo.txt')
histogram_ToA_halo_13 = np.loadtxt(FileInPath + 'angle_90/ToA_values_halo.txt')



title = '$\Delta$ToA, 31 MeV protons'
FileOutPath = 'C:/Users/andrej/Documents/FEI/Vyskum/Data_Processing_Engine/elitech_ToA_figures/'

bin_size = 512
bin_size_halo = 100

plt.close()
plt.clf()
plt.cla()
tickfnt = 14
plt.hist(histogram_ToA_1[:], bins=bin_size, histtype = 'step', label='0 degrees', linewidth=1.75)
plt.hist(histogram_ToA_2[:], bins=bin_size, histtype = 'step', label='10 degrees', linewidth=1.75)
plt.hist(histogram_ToA_3[:], bins=bin_size, histtype = 'step', label='20 degrees', linewidth=1.75)
plt.hist(histogram_ToA_4[:], bins=bin_size, histtype = 'step', label='30 degrees', linewidth=1.75)
plt.hist(histogram_ToA_5[:], bins=bin_size, histtype = 'step', label='40 degrees', linewidth=1.75)
plt.hist(histogram_ToA_6[:], bins=bin_size, histtype = 'step', label='50 degrees', linewidth=1.75)
plt.hist(histogram_ToA_7[:], bins=bin_size, histtype = 'step', label='60 degrees', linewidth=1.75)
plt.hist(histogram_ToA_8[:], bins=bin_size, histtype = 'step', label='70 degrees', linewidth=1.75)
plt.hist(histogram_ToA_9[:], bins=bin_size, histtype = 'step', label='80 degrees', linewidth=1.75)
plt.hist(histogram_ToA_10[:], bins=bin_size, histtype = 'step', label='85 degrees', linewidth=1.75)
plt.hist(histogram_ToA_11[:], bins=bin_size, histtype = 'step', label='88 degrees', linewidth=1.75)
plt.hist(histogram_ToA_12[:], bins=bin_size, histtype = 'step', label='89 degrees', linewidth=1.75)
plt.hist(histogram_ToA_13[:], bins=bin_size, histtype = 'step', label='90 degrees', linewidth=1.75)
plt.xlim(left=1, right=1E6) #left=1E3
#plt.ylim(bottom=1, top=1E5)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('ToA [ns]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(title)
plt.legend(loc='upper right')
plt.savefig(FileOutPath + 'histogram_ToA_values_all.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
tickfnt = 14
plt.hist(histogram_ToA_halo_1[:], bins=bin_size_halo, histtype = 'step', label='0 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_2[:], bins=bin_size_halo, histtype = 'step', label='10 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_3[:], bins=bin_size_halo, histtype = 'step', label='20 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_4[:], bins=bin_size_halo, histtype = 'step', label='30 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_5[:], bins=bin_size_halo, histtype = 'step', label='40 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_6[:], bins=bin_size_halo, histtype = 'step', label='50 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_7[:], bins=bin_size_halo, histtype = 'step', label='60 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_8[:], bins=bin_size_halo, histtype = 'step', label='70 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_9[:], bins=bin_size_halo, histtype = 'step', label='80 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_10[:], bins=bin_size_halo, histtype = 'step', label='85 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_11[:], bins=bin_size_halo, histtype = 'step', label='88 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_12[:], bins=bin_size_halo, histtype = 'step', label='89 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_13[:], bins=bin_size_halo, histtype = 'step', label='90 degrees', linewidth=1.75)
plt.xlim(left=1, right=1E6) #left=1E3
#plt.ylim(bottom=1, top=1E5)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('ToA [ns]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(title)
plt.legend(loc='upper right')
plt.savefig(FileOutPath + 'histogram_ToA_values_halo_all.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)


plt.close()
plt.clf()
plt.cla()
tickfnt = 14
plt.hist(histogram_ToA_1[:], bins=bin_size, histtype = 'step', label='0 degrees', linewidth=1.75)
plt.hist(histogram_ToA_6[:], bins=bin_size, histtype = 'step', label='50 degrees', linewidth=1.75)
plt.hist(histogram_ToA_13[:], bins=bin_size, histtype = 'step', label='90 degrees', linewidth=1.75)
plt.xlim(left=1, right=1E6) #left=1E3
#plt.ylim(bottom=1, top=1E5)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('ToA [ns]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(title)
plt.legend(loc='upper right')
plt.savefig(FileOutPath + 'histogram_ToA_values_3.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
tickfnt = 14
plt.hist(histogram_ToA_halo_1[:], bins=bin_size_halo, histtype = 'step', label='0 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_6[:], bins=bin_size_halo, histtype = 'step', label='50 degrees', linewidth=1.75)
plt.hist(histogram_ToA_halo_13[:], bins=bin_size_halo, histtype = 'step', label='90 degrees', linewidth=1.75)
plt.xlim(left=1, right=1E6) #left=1E3
#plt.ylim(bottom=1, top=1E5)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('ToA [ns]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(title)
plt.legend(loc='upper right')
plt.savefig(FileOutPath + 'histogram_ToA_values_halo_3.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)