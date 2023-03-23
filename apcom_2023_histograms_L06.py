from DPE_functions import *

PathIn = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\L06_Am241'
PathOut = r'Q:\DPE_andrej_data_output\2023_02_24_Am241_time_spectra\L06_Am241'
MaskPath = r'Q:\timepix_config_calib_files\minipix_tpx3\L06-W0048_SiC_300u_MiniPIX\\'
MaskName = 'L06_mask.txt'
mask = np.loadtxt(MaskPath + MaskName)

tickfnt = 16
x = np.linspace(0,149,150)

subdirectories = get_subdirectory_names(PathIn)

if os.path.isfile(PathOut + '\\number_of_single_pixel_counts_L06.txt'):
    number_of_single_pixel_counts = np.loadtxt(PathOut + '\\number_of_single_pixel_counts_L06.txt')
    plt.close()
    plt.clf()
    plt.cla()
    plt.plot(x, number_of_single_pixel_counts, linewidth=1.75)
    plt.xlim(left=0, right=160)
    #plt.ylim(bottom=1, top=1E6)
    #plt.yscale('log')
    plt.xlabel('Measurement number [-]', fontsize=tickfnt)
    plt.ylabel('Number of counts [-]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Number of counts in all measurements at 200V bias, L06 TPX3 SiC 300$\mu$m')
    plt.savefig(PathOut + '\\L06_tpx3_total_counts_200V.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)  

number_of_single_pixel_counts = []

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

    if os.path.isfile(PathOut + '\\histograms\\L06_tpx3_filtered_data_'+str(i)+'.txt'):
        filtered_data = np.loadtxt(PathOut + '\\histograms\\L06_tpx3_filtered_data_'+str(i)+'.txt')
    else:
        am_elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        filtered_data.extend(
            am_elist_data[j, 4]
            for j in range(len(am_elist_data[:, 4]))
            if am_elist_data[j, 7] == 1 and am_elist_data[j,4] < 70 and check_if_position_is_in_mask(mask, am_elist_data[j,2], am_elist_data[j,3]) == False
        )
        np.savetxt(PathOut + '\\histograms\\L06_tpx3_filtered_data_'+str(i)+'.txt', filtered_data)

    plt.close()
    plt.clf()
    plt.cla()
    a = plt.hist(filtered_data, bins=4096, histtype = 'step', linewidth=1.75)
    ys = a[0]
    xs = a[1]
    plt.xlim(left=0, right=150)
    #plt.ylim(bottom=1, top=1E7)
    plt.yscale('log')
    plt.xlabel('Energy [keV]', fontsize=tickfnt)
    plt.ylabel('Number of counts [-]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(f'Am-241 spectrum single pixel, measurement #{i}, L06 TPX3 SiC 300$\mu$m')
    plt.savefig(PathOut + '\\histograms\\L06_tpx3_histogram_'+str(i)+'.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(PathOut + '\\histograms\\L06_tpx3_histogram_data_'+str(i)+'.txt', np.c_[xs[1:], ys])

    number_of_single_pixel_counts.append(len(filtered_data))

    histogram_data = np.loadtxt(PathOut + '\\histograms\\L06_tpx3_histogram_data_'+str(i)+'.txt')
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

np.savetxt(PathOut + '\\number_of_single_pixel_counts_L06.txt', number_of_single_pixel_counts)

out_values = np.column_stack((counts, counts_error, c_value, c_value_error, x_mean_value, x_mean_value_error, sigma_value, sigma_value_error))
np.savetxt(PathOut + '\\gauss_fit_results.txt', out_values, delimiter=';', header='Counts, Counts_error, c, c_error, x_mean, x_mean_error, sigma, sigma_error')


plt.close()
plt.clf()
plt.cla()
plt.plot(x, number_of_single_pixel_counts, linewidth=1.75)
plt.xlim(left=0, right=160)
#plt.ylim(bottom=1, top=1E6)
#plt.yscale('log')
plt.xlabel('Measurement number [-]', fontsize=tickfnt)
plt.ylabel('Number of counts [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Number of counts in all measurements at 200V bias, L06 TPX3 SiC 300$\mu$m')
plt.savefig(PathOut + '\\L06_tpx3_total_counts_200V.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.plot(x, counts, linewidth=1.75)
plt.xlim(left=0, right=160)
#plt.ylim(bottom=1, top=1E6)
#plt.yscale('log')
plt.xlabel('Measurement number [-]', fontsize=tickfnt)
plt.ylabel('Number of counts [-]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Number of counts in Am-241 peak at 200V bias, L06 TPX3 SiC 300$\mu$m')
plt.savefig(PathOut + '\\L06_tpx3_Am241_counts_200V.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)