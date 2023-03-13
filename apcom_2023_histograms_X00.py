from DPE_functions import *

PathIn = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\X00_tpx2'
PathOut = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\X00_tpx2'
tickfnt = 16

subdirectories = get_subdirectory_names(PathIn)

filtered_data = []
number_of_single_pixel_counts = []

x = np.linspace(0,149,150)

for i in range(len(subdirectories)):
    print(subdirectories[i])
    elist_path = PathIn + '\\' + subdirectories[i] + '\\Files\\ExtElist.txt'
    print(elist_path)

    if os.path.isfile(PathOut + '\\histograms\\X00_tpx2_filtered_data_'+str(i)+'.txt'):
        filtered_data = np.loadtxt(PathOut + '\\histograms\\X00_tpx2_filtered_data_'+str(i)+'.txt')
    else:
        am_elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        filtered_data.extend(
            am_elist_data[j, 4]
            for j in range(len(am_elist_data[:, 4]))
            if am_elist_data[j, 7] == 1
        )
        np.savetxt(PathOut + '\\histograms\\X00_tpx2_filtered_data_'+str(i)+'.txt', filtered_data)

    plt.close()
    plt.clf()
    plt.cla()
    a = plt.hist(filtered_data, bins=2048, histtype = 'step', linewidth=1.75)
    ys = a[0]
    xs = a[1]
    plt.xlim(left=0, right=200)
    plt.ylim(bottom=1, top=1E6)
    plt.yscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Number of counts [-]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(f'Am-241 spectrum single pixel, measurement #{i}, X00 TPX2 Si 500$\mu$m')
    plt.savefig(PathOut + '\\histograms\\X00_tpx2_histogram_'+str(i)+'.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(PathOut + '\\histograms\\X00_tpx2_histogram_data'+str(i)+'.txt', np.c_[xs[1:], ys])

    number_of_single_pixel_counts.append(len(filtered_data))

np.savetxt(PathOut + 'number_of_single_pixel_counts_X00.txt', number_of_single_pixel_counts)


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
plt.title('Number of counts in all measurements at 200V bias, X00 TPX2 Si 500$\mu$m')
plt.savefig(PathOut + 'X00_tpx2_total_counts_200V.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)