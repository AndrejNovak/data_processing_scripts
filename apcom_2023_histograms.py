from DPE_functions import *

PathIn = r'Q:\DPE_andrej_output\2023_02_24_Am241_time_spectra\X00_tpx2'
PathOut = r'C:\Users\andrej\Documents\FEI\2023_APCOM_prispevok\figures\\'
clog_path = r'Q:\DPE_andrej_output\2023_02_24_Am241_time_spectra\X00_tpx2\\'
elist_path = r'Q:\DPE_andrej_output\2023_02_24_Am241_time_spectra\X00_tpx2\\'
vmax = 1E3
title = 'Test'
OutputPath = r'C:/Users/andrej/Documents/FEI/'
OutputName = 'test_figure'
OutputNameElist = 'Elist_coincidence.txt'

#write_elist_add_coincidence(elist_path, OutputPath, OutputNameElist)

subdirectories = get_subdirectory_names(PathIn)

filtered_data = []
number_of_single_pixel_counts = []

x = np.linspace(0,150,1)
print(x)

for i in range(len(subdirectories)):
    print(subdirectories[i])
    elist_path = PathIn + subdirectories[i] + '\\Files\\ExtElist.txt'

    if os.path.isfile(PathOut + 'histograms\\X00_tpx2_histogram_data'+str(i)+'.txt'):
        filtered_data = np.loadtxt(PathOut + 'histograms\\X00_tpx2_histogram_data'+str(i)+'.txt')
    else:
        am_elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        filtered_data.extend(
            am_elist_data[j, 4]
            for j in range(len(am_elist_data[:, 0]))
            if am_elist_data[j, 7] == 1
        )
        np.savetxt(PathOut + 'histograms\\X00_tpx2_histogram_data'+str(i)+'.txt', filtered_data)

    number_of_single_pixel_counts.append(len(filtered_data))

    tickfnt = 14

    plt.close()
    plt.clf()
    plt.cla()
    a = plt.hist(filtered_data[:], bins=2048, histtype = 'step', linewidth=1.75)
    ys = a[0]
    xs = a[1]
    plt.xlim(left=0, right=200)
    plt.ylim(bottom=1, top=1E6)
    plt.yscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Number of counts [-]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.savefig(PathOut + 'histograms\\X00_tpx2_histogram_'+str(i)+'.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(PathOut + 'histograms\\X00_tpx2_histogram'+str(i)+'.txt', np.c_[xs[1:], ys])

plt.close()
plt.clf()
plt.cla()
plt.plot(x, number_of_single_pixel_counts, linewidth=1.75)
plt.xlim(left=0, right=150)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xlabel('Measurement number [-]', fontsize=tickfnt)
plt.ylabel('Number of counts [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.savefig(PathOut + 'X00_tpx2_total_counts_200V.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)



"""

for i in range(1000000):
    if am_elist_data[i,7] == 1:
        filtered_data = np.append(filtered_data, am_elist_data[i,4])

tickfnt=12

plt.close()
plt.clf()
plt.cla()
plt.hist(filtered_data[:,4], bins=2048, histtype = 'step', linewidth=1.75)
plt.xlim(left=0, right=200)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.legend(loc='upper right')
plt.show()
#plt.savefig('X00_Am241_1ps_clusters.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)

"""