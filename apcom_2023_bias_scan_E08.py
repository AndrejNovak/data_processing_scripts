from DPE_functions import *

PathIn = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\E08_Am241_bias_scan'
PathOut = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\E08_Am241_bias_scan'
#MaskPath = r'Q:\timepix_config_calib_files\minipix_tpx2\X00-W1698 500 um Si\\'
#MaskName = 'X00_mask.txt'
#mask = np.loadtxt(MaskPath + MaskName)

tickfnt = 16
x = np.linspace(0,200,201)

if os.path.isfile(PathOut + '\\number_of_single_pixel_counts_bias_scan_E08.txt'):
    number_of_single_pixel_counts = np.loadtxt(PathOut + '\\number_of_single_pixel_counts_bias_scan_E08.txt')
    plt.close()
    plt.clf()
    plt.cla()
    plt.plot(x, number_of_single_pixel_counts, linewidth=2)
    plt.xlim(left=0, right=100)
    #plt.ylim(bottom=1E6, top=6E6)
    plt.xlabel('Bias voltage [V]', fontsize=tickfnt)
    plt.ylabel('Number of counts [-]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Number of counts at different bias, E08 TPX Si 300 $\mu$m')
    plt.savefig(PathOut + '\\E08_tpx_total_counts_different_voltage.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)

subdirectories = get_subdirectory_names(PathIn)

number_of_single_pixel_counts = []
counts = []
counts_error = []
c_value = []
c_value_error = []
x_mean_value = []
x_mean_value_error = []
sigma_value = []
sigma_value_error = []

for i in range(len(subdirectories)-1):
    filtered_data = []
    print(subdirectories[i])
    elist_path = PathIn + '\\' + subdirectories[i] + '\\Files\\ExtElist.txt'
    print(elist_path)

    if os.path.isfile(PathOut + '\\histograms\\E08_tpx_filtered_data_'+str(i)+'V.txt'):
        filtered_data = np.loadtxt(PathOut + '\\histograms\\E08_tpx_filtered_data_'+str(i)+'V.txt')
    else:
        am_elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        filtered_data.extend(
            am_elist_data[j, 4]
            for j in range(len(am_elist_data[:, 4]))
            if am_elist_data[j, 7] == 1 and am_elist_data[j,4] < 65 #and check_if_position_is_in_mask(mask, am_elist_data[j,2], am_elist_data[j,3]) == False
        )
        np.savetxt(PathOut + '\\histograms\\E08_tpx_filtered_data_'+str(i)+'V.txt', filtered_data)

    number_of_single_pixel_counts.append(len(filtered_data))

    plt.close()
    plt.clf()
    plt.cla()
    a = plt.hist(filtered_data, bins=4096, histtype = 'step', linewidth=1.75)
    ys = a[0]
    xs = a[1]
    plt.xlim(left=0, right=100)
    #plt.ylim(bottom=1, top=1E6)
    plt.yscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Number of counts [-]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(f'Am-241 spectrum single pixel, bias {i}V, E08 TPX Si 300$\mu$m')
    plt.savefig(PathOut + '\\histograms\\E08_tpx_histogram_'+str(i)+'V.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(PathOut + '\\histograms\\E08_tpx_histogram_data_'+str(i)+'V.txt', np.c_[xs[1:], ys])

    histogram_data = np.loadtxt(PathOut + '\\histograms\\E08_tpx_histogram_data_'+str(i)+'V.txt')
    x_hist, y_hist = histogram_data[3073:,0], histogram_data[3073:,1]
    mean = sum(x_hist*y_hist)/sum(y_hist)                  
    sigma = sum(y_hist*(x_hist-mean)**2)/sum(y_hist) 

    param_optimised,param_covariance_matrix = curve_fit(gauss_fitting, x_hist,y_hist,p0=[max(y_hist),mean,sigma],maxfev=10000)
    
    counts.append(sum(y_hist))
    counts_error.append(np.sqrt(sum(y_hist)))
    c_value.append(param_optimised[0])
    c_value_error.append(np.sqrt(param_covariance_matrix[0,0]))
    x_mean_value.append(param_optimised[1])
    x_mean_value_error.append(np.sqrt(param_covariance_matrix[1,1]))
    sigma_value.append(param_optimised[2])
    sigma_value_error.append(np.sqrt(param_covariance_matrix[2,2]))

np.savetxt(PathOut + '\\number_of_single_pixel_counts_bias_scan_E08.txt', number_of_single_pixel_counts)

out_values = np.column_stack((counts, counts_error, c_value, c_value_error, x_mean_value, x_mean_value_error, sigma_value, sigma_value_error))
np.savetxt(PathOut + '\\gauss_fit_results.txt', out_values, delimiter=';', header='Counts, Counts_error, c, c_error, x_mean, x_mean_error, sigma, sigma_error')

plt.close()
plt.clf()
plt.cla()
plt.plot(x, number_of_single_pixel_counts, linewidth=2)
plt.xlim(left=0, right=200)
#plt.ylim(bottom=1E6, top=6E6)
plt.xlabel('Bias voltage [V]', fontsize=tickfnt)
plt.ylabel('Number of counts [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Number of counts at different bias, E08 TPX Si 300 $\mu$m')
plt.savefig(PathOut + '\\E08_tpx_total_counts_different_voltage.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)  

plt.close()
plt.clf()
plt.cla()
plt.plot(x, counts, linewidth=2)
plt.xlim(left=0, right=200)
#plt.ylim(bottom=1E6, top=6E6)
plt.xlabel('Bias voltage [V]', fontsize=tickfnt)
plt.ylabel('Number of counts [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Number of counts in Am-241 peak at different bias, E08 TPX Si 300 $\mu$m')
plt.savefig(PathOut + '\\E08_tpx_total_counts_Am241_different_voltage.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)  