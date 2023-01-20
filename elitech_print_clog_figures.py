import re
import os
import os.path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from PIL import Image
import glob

#matplotlib.use('Agg')   # To solve issue: Fail to create pixmap with Tk_GetPixmap

# Changing colormap to start at transparent zero
ncolors = 256
color_array = plt.get_cmap('hot_r')(range(ncolors))
color_array[:,-1] = np.linspace(0.0,1.0,ncolors)
map_object = LinearSegmentedColormap.from_list(name='modified_hot',colors=color_array)
plt.register_cmap(cmap=map_object)

def read_elist(filename):
    """
    Access full Elist data including header

    Example, return header and units:
    header, units, _ = read_elist('path/to/Elist.txt')

    Example, return data only
    data = read_elist('path/to/Elist.txt')[2]
    """
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    inputFile.close()  
    splitlines = []
    for line in lines:
        splitlines.append(list(line.rstrip().split(";")))
    return splitlines[0], splitlines[1], splitlines[2:]


def read_clog(filename):
    """ 
    This function reads through the .clog file and can access Unix_time and Acquisition_time of every frame,
    #of frames, #of events in frame and their values [x, y, ToT, ToA].
    For printing Unix_time use: read_clog(filename)[0]
    For printing Acquisition_time use: read_clog(filename)[1]
    For printing full data use: read_clog(filename)[2]

    When using 'data = read_clog(filename)[2]', you can traverse the data on level of Frames, 
    registered values (group of 4 values - [x, y, ToT, ToA]) and selected value from one of the 
    four possible - x or y or ToT or ToA.

    To access first layer (selected frame) use: data[0]
    To access second layer (selected 4-group of selected frame) use: data[0][0]
    To access third layer (selected value from selected 4-group of selected frame) use: data[0][0][0] 
    """
    
    inputFile = open(filename)
    lines = inputFile.readlines()
    current_cluster = list()
    all_values = list()
    a = []
    pattern_b = r"\[[^][]*]"
    for line in lines:
        if line != "\n":
            if (line.split()[0]=="Frame"):
                unixtime = float(line.split()[2].lstrip("(").rstrip(","))
                #print(unixtime)
                frametime = float(line.split()[3].rstrip(","))
                #print(frametime)

                all_values.append(current_cluster)
                current_cluster= []
                continue
            a = (re.findall(pattern_b, line))
            for element in a:
                b = ("".join(element)).rstrip("]").lstrip("[").split(",")
                b = [ float(x) for x in b ]
                current_cluster.append(b)
    
    return unixtime, frametime, all_values[1:].copy()  # to fix problem with first list being empty, needs solution without copying


def plot_single_cluster(output_path, append_to_folders, add_path, clog_path, frame_number):
    clog = read_clog(clog_path)[2]
    tickfnt = 14
    margin = 5
    matrix = np.zeros([256,256])

    i=0
    x = []
    y = []
    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    i = 0
    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] += clog[frame_number][i][2]

    if (max(x)-min(x)) < (max(y)-min(y)):
        diff_x = np.abs((max(x)-min(x))-(max(y)-min(y)))
    else:
        diff_x = 0
    if (max(y)-min(y)) < (max(x)-min(x)):
        diff_y = np.abs((max(y)-min(y))-(max(x)-min(x)))
    else:
        diff_y = 0

    plt.close()
    plt.cla()
    plt.clf()
    plt.subplot()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    plt.clim(1,1E3)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    cbar = plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='Energy [keV]',size=tickfnt,weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label = 'Pix-ToA-Diff ' + str(diff) + ', Cluster #'+str(frame_number), fontsize=tickfnt)
    plt.xlim([min(x)-diff_x/2-margin, max(x)+diff_x/2+margin])
    plt.ylim([min(y)-diff_y/2-margin, max(y)+diff_y/2+margin])
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    if not os.path.exists(output_path + '/angle_' +append_to_folders + '/cluster_' + str(frame_number)):
        os.makedirs(output_path + '/angle_' +append_to_folders + '/cluster_' + str(frame_number))
    plt.savefig(output_path + '/angle_' +append_to_folders + '/cluster_' + str(frame_number) + '/' + str(add_path) + '_cluster_' + str(frame_number) + '.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(output_path + '/angle_' +append_to_folders + '/cluster_' + str(frame_number) + '/' + str(add_path) + '_cluster_' + str(frame_number) + '.txt', matrix)


main_folder = 'Q:/DPE_andrej_data_output/2023_04_elitech/'
folders_proton = 'toa_diff_angle_'
append_to_folders = ['0', '10', '20', '30', '40', '50', '60', '70', '80', '85', '88', '89', '90']
angle_He = ['00', '30', '45', '60', '75', '85', '88', '90', '60', '60', '60', '60', '60', '60', '60', '60', '60', '60', '60', '60', '60']
voltage_He = ['150V', '150V', '150V', '150V', '150V', '150V', '150V', '150V', '150V', '00V', '25V', '50V', '75V', '100V', '125V', '150V', '175V', '200V', '225V', '250V', '275V', '300V']

num_of_single_clusters = 10

for j in range(len(append_to_folders)):
    for k in range(30):
        diff = 100 * (k+1)
        path = main_folder + folders_proton + str(append_to_folders[j])
        output_path = main_folder + '/single_cluster_figures_protons/'
        elist_path = path + '/GaAs_elist_pixtoadiff_' + str(diff) + '.txt'
        clog_path = path + '/GaAs_pixtoadiff_' + str(diff) + '.clog'

        for m in range(num_of_single_clusters):
            plot_single_cluster(output_path, append_to_folders[j], diff, clog_path, int(m))

"""
# Try to print gif
frames = []
i = 0
for j in range(len(append_to_folders)):
    for k in range(30):
        diff = 100 * (k + 1)
        output_path = main_folder + '/single_cluster_figures_protons/'

        for m in range(num_of_single_clusters):
            imgs = (output_path + '/angle_' + str(append_to_folders[j]) + 'cluster_' + str(m) + '/*.png")
            for i in imgs:
                new_frame = Image.open(i)
                frames.append(new_frame)

    # Save the png images into a GIF file that loops forever
    frames[0].save(output_path + 'angle_' + str(append_to_folders[j]) + '.gif', format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=300, loop=0)
"""