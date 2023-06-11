from DPE_functions import *

in_path = 'Q:\\DPE_andrej_data_output\\2023_06_12_mouse_xray\\'

all_out_folders = 'Q:\\DPE_andrej_data_output\\2023_06_12_mouse_xray_results\\'

folder_data_main = get_subdirectory_names(in_path)
filename_elist = 'ExtElist.txt'

energy_window = np.array([[5,10],
                          [5,15],
                          [5,20],
                          [10,20],
                          [15,30],
                          [20,40]])
print(np.shape(energy_window))
print(energy_window[0,0], energy_window[0,1])

for idx, var in enumerate(folder_data_main):
    FolderInPath = in_path + var
    print(FolderInPath)

    subfolder_data_main = get_subdirectory_names(FolderInPath)

    for idx2, var2 in enumerate(subfolder_data_main):
        FileInPath = FolderInPath + '\\' + var2 + '\\Files\\'
        print(FileInPath)

        elist_path = FileInPath + filename_elist
        elist_data = np.loadtxt(elist_path, skiprows=2, delimiter=';')
        clog = read_clog_multiple(FileInPath)

        matrix_counts = np.zeros([256, 256])
        matrix_energy = np.zeros([256, 256])

        for i in range(len(energy_window[:,0])):
            for j in range(len(elist_data[:,0])):
                if elist_data[j,4] >= energy_window[j,0] and elist_data[j,4] <= energy_window[j,1] and elist_data[j,7] <= 4:
                    cluster_size_clog = len(clog[j][:])

                    for k in range(cluster_size_clog):
                        x, y = int(clog[j][k][0]), int(clog[j][k][1])

                        matrix_energy[x, y] += clog[j][k][2]
                        matrix_counts[x, y] += 1

            FileOutName = 'matrix_minE_' + str(energy_window[i,0]) + '_maxE_' + str(energy_window[i,1])
            FolderOutPath = all_out_folders + var + '\\' + var2 + '\\'

            energy_colorbar_max_value = 5000
            print_figure_energy(matrix_energy, energy_colorbar_max_value, 'Dep E, range ' + str(energy_window[i,0]) + '- ' + str(energy_window[i,1] + 'keV X-ray photons'), FolderOutPath, FileOutName)
            mydpi = 300
            tickfnt = 16

            if not os.path.exists(FolderOutPath):
                os.makedirs(FolderOutPath)

            title_counts = 'Number of counts, range ' + str(energy_window[i,0]) + '- ' + str(energy_window[i,1]) + 'keV X-ray photons'
            FileOutNameCounts = 'matrix_counts_minE_' + str(energy_window[i,0]) + '_maxE_' + str(energy_window[i,1])

            plt.close()
            plt.cla()
            plt.clf()
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(
                matrix_counts[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
            plt.gca().xaxis.tick_bottom()
            cbar = plt.colorbar(label='Counts [-]', aspect=20*0.8, shrink=0.8) # shrink=0.8
            cbar.set_label(label='Counts [-]', size=tickfnt,
                           weight='regular')   # format="%.1E"
            cbar.ax.tick_params(labelsize=tickfnt)
            # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            plt.clim(1, 5000)
            plt.xlabel('X position [pixel]', fontsize=tickfnt)
            plt.ylabel('Y position [pixel]', fontsize=tickfnt)
            plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
            plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.title(label=title_counts, fontsize=tickfnt)
            plt.savefig(FolderOutPath + FileOutNameCounts + '.png', dpi=mydpi,
                        transparent=True, bbox_inches="tight", pad_inches=0.01)
            np.savetxt(FolderOutPath + FileOutNameCounts + '.txt', matrix_counts, fmt="%.3f")