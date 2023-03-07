from DPE_functions import *

PathIn = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\bias_scan\L06_tpx3'
PathOut = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\Apcom_2023\bias_scan\L06_tpx3\\'
tickfnt = 14

subdirectories = get_subdirectory_names(PathIn)

filtered_data = []
number_of_single_pixel_counts = []

x = np.linspace(0,200,201)

for i in range(len(subdirectories)):
    print(subdirectories[i])
    elist_path = PathIn + subdirectories[i] + '\\Files\\ExtElist.txt'

    if os.path.isfile(PathOut + 'histograms\\L06_tpx3_filtered_data'+str(i)+'V.txt'):
        filtered_data = np.loadtxt(PathOut + 'histograms\\L06_tpx3_filtered_data'+str(i)+'V.txt')
    else:
        am_elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        filtered_data.extend(
            am_elist_data[j, 4]
            for j in range(len(am_elist_data[:, 4]))
            if am_elist_data[j, 7] == 1
        )
        np.savetxt(PathOut + 'histograms\\L06_tpx3_filtered_data'+str(i)+'V.txt', filtered_data)

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
    plt.title(f'Am-241 spectrum single pixel, bias {i}V, L06 TPX3 Si 300$\mu$m')
    plt.savefig(PathOut + 'histograms\\L06_tpx3_histogram_'+str(i)+'V.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(PathOut + 'histograms\\L06_tpx3_histogram_data'+str(i)+'V.txt', np.c_[xs[1:], ys])

    number_of_single_pixel_counts.append(len(filtered_data))

np.savetxt(PathOut + 'number_of_single_pixel_counts_bias_scan_L06.txt', number_of_single_pixel_counts)


plt.close()
plt.clf()
plt.cla()
plt.plot(x, number_of_single_pixel_counts, linewidth=1.75)
plt.xlim(left=0, right=160)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xlabel('Bias voltage [V]', fontsize=tickfnt)
plt.ylabel('Number of counts [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Number of counts at different bias, L06 TPX3 SiC 300$\mu$m')
plt.savefig(PathOut + 'L06_tpx3_total_counts_different_voltage.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)