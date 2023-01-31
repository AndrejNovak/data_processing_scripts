"""
@author: Andrej, STUBA, Bratislava, 2022 + Lukas + Carlos 9 aug 2022
corr_elist_clog.py july2022 with functions to use, andrej, stuba, july2022
edited added functions, carlos+lukas, ADV, Prague 1-9 Aug 2022

python scripts with functions and classes for post-processing the output of DPE_CP
and process further the outputs of DPE_CP

classes
    - cluster_filter

functions
    - read_clog
    - read_elist_filter
    - create_matrix_filter_tpx3_t3pa
    - create_matrix_filter_tpx_f
    - print_fig_E
    - print_fig_ToA

"""

import re
import os
import os.path
import sys
import glob
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
import json

matplotlib.use('Agg')   # To solve issue: Fail to create pixmap with Tk_GetPixmap

# new class, to filter events in elist
# accepts arbitrary CA PAR filter, one, and also more than one
# Lukas+Carlos, ADV, Prague, 8 Aug 2022
class cluster_filter:    
    # edges = border values for given CA PAR 
    # indeces = COL # in elist of given CA PAR, e.g. 4 for E
    def __init__(self, edges = [], indeces = []):
        self.edges = edges
        self.indeces = indeces

    # function to execute the filter
    def pass_filter(self, cluster_var):
        #return True
        for i in range(len(self.indeces)):
            down_edge = self.edges[i]
            up_edge = self.edges[i+1]
            i_var = self.indeces[i]
            #print('pass_filter',down_edge, cluster_var[i_var], up_edge, end='')
            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                #print('True')
                return True
            else: 
                #print('False')
                return False
        
    
# Changing colormap to start at transparent zero
ncolors = 256
color_array = plt.get_cmap('hot_r')(range(ncolors))
color_array[:,-1] = np.linspace(0.0,1.0,ncolors)
map_object = LinearSegmentedColormap.from_list(name='modified_hot',colors=color_array)
plt.register_cmap(cmap=map_object)


#FileIn_ClogPathName = 'script_test_data/09/ClusterLog.clog'
#FileOut_ClogPathName = 'script_test_data/09/Clog_output/'
#FileOut_ClogName = 'script_test_data/09/clog_read_output.txt'

FileIn_ElistPathName = 'ExtElist.txt'
FileOut_ElistPathName = 'ExtElist_output/'
FileOut_ElistName = 'ExtElist_output.txt'


def print_out(FileOutPath, filename, input_data):
    """
    Function for printing output data into classic Elist format
    """
    if not os.path.exists(FileOutPath):
        os.makedirs(FileOutPath)
    with open(FileOutPath + filename, 'w') as f:
        sys.stdout = f
        print(input_data)
        sys.stdout


def read_clog(filename):
    """ 
    Lukas+Andrej+Carlos, 9 Aug 2022
    This script reads through the .clog file and access #of frames, #of events in frame
    and their values [x, y, ToT, ToA] 
    newly solved problem with reading single clusters to single rows / Lukas
    optimized/customized for TPX3 data (maybe also TPX2) in ToT+ToA mode

    print(data[0])          #1. frame
    print(data[0][0])       #1. frame, 1. 4-list
    print(data[0][0][0])    #1. frame, 1. 4-list, 1. value 
    """
    
    inputFile = open(filename)

    
    #lines = inputFile.readlines()

    current_cluster = list()
    all_values = list()
    a = []
    pattern_b = r"\[[^][]*]"
    line_num = 0
    for line in inputFile:
        if line != "\n":
            if (line[0]=="F"):
                unixtime = float(line.split()[2].lstrip("(").rstrip(","))
                #print(unixtime)
                frametime = float(line.split()[3].rstrip(","))
                #print(frametime)

                #all_values.append(current_cluster)
                continue
            current_cluster= []            
            a = (re.findall(pattern_b, line))
            for element in a:
                b = ("".join(element)).rstrip("]").lstrip("[").split(",")
                b = [ float(x) for x in b ]
                current_cluster.append(b)
            all_values.append(current_cluster)
    
    return unixtime, frametime, all_values  # to fix problem with first list being empty, needs solution without copying


def get_column(filename, col_name):
    """
    Use to get a List of specific column from Elist
    col_name = name of the variable from Elist 
    """
    inputFile = open(filename, 'r')
    lines = inputFile.readlines()
    names = []
    units = []
    names.append(lines[0].rstrip().split(';'))
    units.append(lines[1].rstrip().split(';'))

    lines = lines[2:]
    for idx,val in enumerate(names[0][:]):
        if names[0][idx] == col_name:
            col_num = idx
        else:
            pass
    
    # print('\n *** From get_column() you are printing parameter {} in units {} \n'.format(str(names[0][col_num]), str(units[0][col_num])))

    column_data = []
    for line in lines:
        column_data.append(line.rstrip().split(';')[col_num])
    
    return column_data

# new funkce read_elist to include option to filter events (Lukas 8 Aug 22)
def read_elist_filter(filename, new_filter=None):
    """
    Function to read elist (calibrated, output of DPE_CP)
    and applies a filter of clusters according CA PAR
    arbitrary number e.g.
    1 filter (H): [100,500],[8]
    2 filters (H,A): [100,500,10,30],[8,7]
    and adds to the elist a new col at the end to indicate
    1 = filter pass
    0 = filter fail   
    output is the same elist with the added new col at right (COL = 16)
    """
    
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    inputFile.close()  
    splitlines = []
    line_num=0
    # when there is filter entered:
    if new_filter is not None:
    
        for line in lines:
            line_num += 1
            cluster_var = list(line.rstrip().split(";"))
            # for the first heading 2 rows 
            if line_num < 3:
                print('first two rows',line_num)
                cluster_var.append('Filter')
                splitlines.append(cluster_var)
            # for the rest
            else:                    
                #if line_num >= 3 and new_filter is not None:
                #print('ostatni radky',line_num)
                cluster_var = [float(i) for i in list(line.rstrip().split(";"))]
                #print(new_filter.pass_filter(cluster_var))
                if new_filter.pass_filter(cluster_var):
                    #print('Filter ok ', end='') # removes enter
                    cluster_var.append(1)
                else: 
                    #print('False B ')
                    #print('Filter bad ', end='')
                    cluster_var.append(0)
                    #print(cluster_var)
                #print(line_num)                
                splitlines.append(cluster_var)

        # the full elist with extended col output as single object
        return splitlines[0], splitlines[1], splitlines[2:]
        # the elist output split into three objects
        #return splitlines[0], splitlines[1], splitlines[2:]

    else:
        print('No filter, nothing processed')
        #splitlines = inputFile
      

'''
od lukas, mon 8 aug 2022
def read_elist(filename, new_filter=None):
    """
    Function designed to read full Elist
    To access only data use as follows:
    data = getline(filename)[2]
    """
    
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    inputFile.close()  
    splitlines = []
    line_num=0
    for line in lines:
        line_num += 1
        cluster_var = list(line.rstrip().split(";"))
        splitlines.append(cluster_var)
        if line_num >= 3 and new_filter is not None:
            cluster_var = [float(i) for i in list(line.rstrip().split(";"))]
            if new_filter.pass_filter(cluster_var):
                cluster_var.append(1)
            else: cluster_var.append(0)
    return splitlines[0], splitlines[1], splitlines[2:]
'''

def write_elist(filename_out, header, units, data):
    """
    Use this function to re-print input Elist in a form
    that is readable by numpy.loadtxt(filename, skiprows=2)
    """
    with open(filename_out, 'w') as f:
        f.write(' '.join(map(str, header))+'\n')
        f.write(' '.join(map(str, units))+'\n')
        for row in data:
            s = ' '.join(map(str, row))
            f.write(s+'\n')

def create_matrix_filter_tpx3_t3pa(elist_filtered,clog,num_frames):
#def create_matrix_filter(elist_filtered,clog, num_frames, rand):
    """
    Carlos+Lukas+Andrej, ADV, Prague, 8 Aug 2022
    Function to create E and ToA sq matrix for 2D plot of det px matrix
    customized for TPX3 t3pa data, and its DPE_CP clog output with f's of short time e.g. 100 ns
    inputs:
    - elist_filtered which is the DPE_CP output elist with the added COL from cluster_filter
    - clog is the clog calib output of DPE_CP
    - num_frames = # of f to integrate i.e to add to merged plot from beginning i.e. from f zero
        in the clog file output of DPE_CP for TPX3 data a f is created every 100 ns
        for TPX3 t3pa data: Input num_frames is the cluster i.e. event number
        for raw clog frame data: num_frames is the f #
    """
    
    #if rand == 'True':
    #    rand_nums = sorted(random.sample(range(0, len(clog[:])), len(num_frames)))
    #else:
    rand_nums = list(range(0,num_frames))       # list(range(0,num_frames))
    # the sq matrix for all clusters
    matrix_E_all = np.zeros([256,256])
    matrix_ToA_all = np.zeros([256,256])    # the sq matrix for the filter OK clusters
    matrix_E_ok = np.zeros([256,256])
    matrix_ToA_ok = np.zeros([256,256])
    # the sq matrix for the filter REJECTED = BAD clusters
    matrix_E_bad = np.zeros([256,256])
    matrix_ToA_bad = np.zeros([256,256])
    # for cyclus cluster by cluster
    jump = 0
    f_jump = 0
    multiplet_num = 0 # to keep record of multiplet occurrence
    for idx,elist_row in enumerate(rand_nums):
    #for elist_row in enumerate(rand_nums):    
            
        # counter for the drawing of clusters in clog
        #f_num = elist_row - multiplet_num
        f_num = elist_row
        # cluster area from clog
        clu_A_clog = len(clog[f_num][:])
        # cluster area from elist
        clu_A_elist = elist_filtered[2][elist_row][7]
        '''
        print('elist_row = ',elist_row,  ', f_num = ',f_num,', filter = ',elist_filtered[2][elist_row][15])
        print(', clu_A_elist = ',clu_A_elist, ', clu_A_clog = ',clu_A_clog)
        '''
        # ----------------------------
        # for all clusters:
        # ----------------------------
        for j in range(clu_A_clog):
        #for j in len(clog[elist_row][:]):
            x = int(clog[f_num][j][0])
            y = int(clog[f_num][j][1])    
            matrix_E_all[x,y] = matrix_E_all[x,y] + clog[f_num][j][2]
            matrix_ToA_all[x,y] = clog[f_num][j][3]        
        
        # ----------------------------
        # for clusters with OK filter:
        # ----------------------------
        if elist_filtered[2][elist_row][15] == 1:
            #print('sq matrix filter ok')
            # -- to take into account multiplets 
            # these can be resolved in elist, but not in clog
            '''
            if elist_row < num_frames and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                jump = jump + 1 
                multiplet_num = multiplet_num + 1
            '''      
            # for each cluster record in clog:    
            #f_jump = jump
            #print('filter ok, jump = ',jump)
            for j in range(clu_A_clog):
            #for j in len(clog[elist_row][:]):
                    
                        
                #print(elist_row,j)
                #print(clog[elist_row][j])
                #print(elist_row,j,clog[elist_row][j][0],clog[elist_row][j][1])
                x = int(clog[f_num][j][0])
                y = int(clog[f_num][j][1])    
                #x = clog[elist_row][j][0]
                #y = clog[elist_row][j][1]  
                matrix_E_ok[x,y] = matrix_E_ok[x,y] + clog[f_num][j][2]
                matrix_ToA_ok[x,y] = clog[f_num][j][3]
                '''
                toa = []
                for i in range(len(clog[elist_row][:])):
                    toa.append(clog[val][i][3])                
                else:
                    pass
                if max(toa) != 0:
                    matrix_ToA_ok[x,y] = (clog[val][j][3]) / max(toa)
                else:
                    matrix_ToA_ok[x,y] = clog[val][j][3]
                '''
            # ----------------------------------------------------
            # for BAD clusters i.e. which did not pass the filter:
            # ----------------------------------------------------
        else:
            if jump < 1:
                #jump = 0
                #print('sq matrix filter bad')
                #print('filter BAD, jump = ',jump)
                '''
                if elist_row < num_frames and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                    jump = jump + 1 
                    multiplet_num = multiplet_num + 1
                '''

                for j in range(clu_A_clog):
                    x = int(clog[f_num][j][0])
                    y = int(clog[f_num][j][1])
                    matrix_E_bad[x,y] = matrix_E_bad[x,y] + clog[f_num][j][2]
                    matrix_ToA_bad[x,y] = clog[f_num][j][3]
                    
                    '''
                    toa = []
                    for i in range(len(clog[val][:])):
                        toa.append(clog[val][i][3])                
                        matrix_E_bad[x,y] = matrix_E_bad[x,y] + clog[val][j][2]
                    else:
                        pass
                    if max(toa) != 0:
                        matrix_ToA_bad[x,y] = (clog[val][j][3]) / max(toa)
                    else:
                        matrix_ToA_bad[x,y] = clog[val][j][3]                        
                    
        if elist_filtered[2][elist_row][1] < elist_filtered[2][elist_row+1][1]:
            jump = 0
                    '''
            
    return matrix_E_all, matrix_ToA_all, matrix_E_ok, matrix_ToA_ok, matrix_E_bad, matrix_ToA_bad

def create_matrix_filter_tpx_f(elist_filtered,clog,num_frames):
#def create_matrix_filter(elist_filtered,clog, num_frames, rand):
    """
    Carlos+Lukas+Andrej, ADV, Prague, 8 Aug 2022
    Function to create E and ToA sq matrix for 2D plot of det px matrix
    customized for TPX frame data, and its clog output with f
    inputs:
    - elist_filtered is the DPE_CP output elist with additional col from filter
    - clog is the clog calib output of DPE_CP
    - num_frames = # of f to integrate i.e to add to merged plot from beginning i.e. from f zero
        in the clog file output of DPE_CP for TPX data frames
        for TPX frame data ToT: Input num_frames is the cluster i.e. event number
        for raw clog frame data: num_frames is the f #
    """
    
    #if rand == 'True':
    #    rand_nums = sorted(random.sample(range(0, len(clog[:])), len(num_frames)))
    #else:
    rand_nums = list(range(0,num_frames))       # list(range(0,num_frames))
    # the sq matrix for all clusters
    matrix_E_all = np.zeros([256,256])
    #matrix_ToA_all = np.zeros([256,256])    # the sq matrix for the filter OK clusters
    matrix_E_ok = np.zeros([256,256])
    #matrix_ToA_ok = np.zeros([256,256])
    # the sq matrix for the filter REJECTED = BAD clusters
    matrix_E_bad = np.zeros([256,256])
    #matrix_ToA_bad = np.zeros([256,256])
    # for cyclus cluster by cluster
    jump = 0
    f_jump = 0
    multiplet_num = 0 # to keep record of multiplet occurrence
    for idx,elist_row in enumerate(rand_nums):
    #for elist_row in enumerate(rand_nums):    
            
        # counter for the drawing of clusters in clog
        #f_num = elist_row - multiplet_num
        f_num = elist_row
        # cluster area from clog
        clu_A_clog = len(clog[f_num][:])
        # cluster area from elist
        clu_A_elist = elist_filtered[2][elist_row][7]
        '''
        print('elist_row = ',elist_row,  ', f_num = ',f_num,', filter = ',elist_filtered[2][elist_row][15])
        print(', clu_A_elist = ',clu_A_elist, ', clu_A_clog = ',clu_A_clog)
        '''
        # ----------------------------
        # for all clusters:
        # ----------------------------
        for j in range(clu_A_clog):
        #for j in len(clog[elist_row][:]):
            x = int(clog[f_num][j][0])
            y = int(clog[f_num][j][1])    
            matrix_E_all[x,y] = matrix_E_all[x,y] + clog[f_num][j][2]
            #matrix_ToA_all[x,y] = clog[f_num][j][3]        
        
        # ----------------------------
        # for clusters with OK filter:
        # ----------------------------
        if elist_filtered[2][elist_row][15] == 1:
            #print('sq matrix filter ok')
            # -- to take into account multiplets 
            # these can be resolved in elist, but not in clog
            '''
            if elist_row < num_frames and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                jump = jump + 1 
                multiplet_num = multiplet_num + 1
            '''      
            # for each cluster record in clog:    
            #f_jump = jump
            #print('filter ok, jump = ',jump)
            for j in range(clu_A_clog):
            #for j in len(clog[elist_row][:]):
                    
                        
                #print(elist_row,j)
                #print(clog[elist_row][j])
                #print(elist_row,j,clog[elist_row][j][0],clog[elist_row][j][1])
                x = int(clog[f_num][j][0])
                y = int(clog[f_num][j][1])    
                #x = clog[elist_row][j][0]
                #y = clog[elist_row][j][1]  
                matrix_E_ok[x,y] = matrix_E_ok[x,y] + clog[f_num][j][2]
                #matrix_ToA_ok[x,y] = clog[f_num][j][3]
                '''
                toa = []
                for i in range(len(clog[elist_row][:])):
                    toa.append(clog[val][i][3])                
                else:
                    pass
                if max(toa) != 0:
                    matrix_ToA_ok[x,y] = (clog[val][j][3]) / max(toa)
                else:
                    matrix_ToA_ok[x,y] = clog[val][j][3]
                '''
            # ----------------------------------------------------
            # for BAD clusters i.e. which did not pass the filter:
            # ----------------------------------------------------
        else:
            if jump < 1:
                #jump = 0
                #print('sq matrix filter bad')
                #print('filter BAD, jump = ',jump)
                '''
                if elist_row < num_frames and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                    jump = jump + 1 
                    multiplet_num = multiplet_num + 1
                '''

                for j in range(clu_A_clog):
                    x = int(clog[f_num][j][0])
                    y = int(clog[f_num][j][1])
                    matrix_E_bad[x,y] = matrix_E_bad[x,y] + clog[f_num][j][2]
                    #matrix_ToA_bad[x,y] = clog[f_num][j][3]
                                
    return matrix_E_all, matrix_E_ok, matrix_E_bad


def create_matrix(data, num_frames, rand):
    """
    Function to create E and ToA sq matrix for 2D plot of det px matrix
    - data is the clog calib output of DPE_CP
    - num_frames = # of f to integrate i.e to add to merged plot from beginning i.e. from f zero
        in the clog file output of DPE_CP for TPX3 data a f is created every 100 ns
        for TPX3 t3pa data: Input num_frames is the cluster i.e. event number
        for raw clog frame data: num_frames is the f #
    - rand = determines whether random numbers are chosen or not
    """
    
    if rand == 'True':
        rand_nums = sorted(random.sample(range(0, len(data[:])), len(num_frames)))
    else:
        rand_nums = list(range(0,num_frames))       # list(range(0,num_frames))

    matrix_E = np.zeros([256,256])
    matrix_ToA = np.zeros([256,256])

    for idx,val in enumerate(rand_nums):
        for j in range(len(data[val][:])):
            x = int(data[val][j][0])
            y = int(data[val][j][1])
            toa = []
            for i in range(len(data[val][:])):
                toa.append(data[val][i][3])
            
                matrix_E[x,y] = matrix_E[x,y] + data[val][j][2]
            else:
                pass
            if max(toa) != 0:
                matrix_ToA[x,y] = (data[val][j][3]) / max(toa)
            else:
                matrix_ToA[x,y] = data[val][j][3]
            
    return matrix_E, matrix_ToA


def calibrate_frame(a_path, b_path, c_path, t_path, matrix):
    """
    Function that recalculated uncalibrated ToT matrix to Energy
    using input calibration matrices (their names or full path)
    """
    a = np.loadtxt(a_path)
    b = np.loadtxt(b_path)
    c = np.loadtxt(c_path)
    t = np.loadtxt(t_path)

    tot = np.zeros([256,256])
    for i in range(256):
        for j in range(256):
            if matrix[i,j] > 0.8:
                tot[i,j] = (a[i,j] * t[i,j] + matrix[i,j] + np.abs(np.sqrt((a[i,j] * t[i,j] + b[i,j] - matrix[i,j])**2 + 4 * a[i,j] * c[i,j]))) / (2 * a[i,j])
            else:
                tot[i,j] = 0
    
    return tot


def print_fig_E(matrix, OutputName):
    """
    Function to store i.e. write out an existing or previously 
    generated sq matrix E in txt and png files 
    to disc, following use of e.g. create_matrix 
    """
    tickfnt = 14
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    #plt.matshow(matrix[:,:], origin='lower', cmap='viridis', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='viridis', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8).set_label(label='Energy [keV]',size=tickfnt,weight='regular')   # format="%.1E"
    plt.clim(1,None)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    if not os.path.exists('DPE_figures/2D_frame_E'):
        os.makedirs('DPE_figures/2D_frame_E')
    plt.savefig('DPE_figures/2D_frame_E/' + OutputName + '.png', dpi=200, transparent=True, bbox_inches="tight", pad_inches=0.01)
    #np.savetxt('DPE_figures/2D_frame_E/' + OutputName + '.txt', matrix)
    np.savetxt('DPE_figures/2D_frame_E/' + OutputName + '.txt', matrix, fmt='%8.1f')


def print_fig_ToA(matrix, OutputName):
    """
    Function to store i.e. write out the generated sq matrix E in txt and png
    to disc, following use of e.g. create_matrix 
    """
    tickfnt = 14
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='viridis')
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(label='ToA [ns]', shrink=0.8, aspect=20*0.8).set_label(label='ToA [ns]',size=tickfnt,weight='regular')   # format="%.1E"
    plt.clim(0,None)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    if not os.path.exists('DPE_figures/2D_frame_ToA'):
        os.makedirs('DPE_figures/2D_frame_ToA')
    plt.savefig('DPE_figures/2D_frame_ToA/' + OutputName + '.png', dpi=200, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt('DPE_figures/2D_frame_ToA/' + OutputName + '.txt', matrix)


def parameter_filter(data_column, min_value, max_value):
    """
    Find out which elements of column data passed filter
    Use passed filter index number to select cluster number from clog file 
    For data_column use function get_column(filename, col_name)
    Example: parameter_filter(get_column('Elist.txt', 'E'), 1, 1E3)
    """
    passed = []
    bad = []
    print(len(data_column))
    for idx, val in enumerate(data_column):
        if float(val) >= min_value and float(val) <= max_value:
            passed.append(int(idx))
        else:
            bad.append(int(idx))
    
    return passed, bad


def plot_single_cluster(elist_path, clog_path, frame_number, parameter, flabel):
    elist = read_elist(elist_path, parameter)
    clog = read_clog(clog_path)
    tickfnt = 14
    margin = 5
    matrix = np.zeros([256,256])

    i=0
    x = []
    y = []
    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

        matrix[int(x[i]), int(y[i])] = elist[frame_number]

    if (max(x)-min(x)) < (max(y)-min(y)):
        diff_x = np.abs((max(x)-min(x))-(max(y)-min(y)))
    else:
        diff_x = 0
    if (max(y)-min(y)) < (max(x)-min(x)):
        diff_y = np.abs((max(y)-min(y))-(max(x)-min(x)))
    else:
        diff_y = 0

    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='viridis')
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(label=flabel, shrink=0.8, aspect=20*0.8).set_label(label=flabel,size=tickfnt,weight='regular')   # format="%.1E"
    plt.clim(0,None)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.title(label = 'Parameter ' + str(parameter) + ' - cluster #'+str(frame_number), fontsize=tickfnt)
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.xlim([min(y)-diff_y/2-margin, max(y)+diff_y/2+margin])
    plt.ylim([min(x)-diff_x/2-margin, max(x)+diff_x/2+margin])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    if not os.path.exists('DPE_figures/2D_frame_'+parameter):
        os.makedirs('DPE_figures/2D_frame_'+parameter)
    plt.savefig('DPE_figures/2D_frame_'+parameter+'/cluster_' + str(frame_number) + '.png', dpi=200, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt('DPE_figures/2D_frame_/' + parameter+'/cluster_' + str(frame_number) + '.txt', matrix)

"""
def frame_matrix(clog_path,filename,frame_number):
    clog = read_clog(filename)
    matrix = np.zeros([256,256])

    for j in range(len(clog[frame_number][:])):
        x = int(clog[frame_number][j][0])
        y = int(clog[frame_number][j][1])
        matrix[x,y] = matrix[x,y] + clog[frame_number][j][2]

    return matrix
"""

def frame_matrix_tpx3(clog_path,filename,frame_number):
    """
    Carlos, from Andrej's script, 4 Aug 2022'
    input is the clog calib file of output of DPE_CP
    it reads the clog calib file, finds one f, and makes it
    (it draws it and stores it - calling the print_fig_E funkce)
    the output is stored in a new automatic DIR within the Files DIR of DPE_CP output
    for TPX3 data in ToT+ToA
    """
    clog = read_clog(filename)[2]
    matrix_tot = np.zeros([256,256]) # tot
    matrix_toa = np.zeros([256,256]) # toa

    for j in range(len(clog[frame_number][:])):
        x = int(clog[frame_number][j][0]) # x coord
        y = int(clog[frame_number][j][1]) # y coord
        matrix_tot[x,y] = matrix_tot[x,y] + clog[frame_number][j][2] # tot
        matrix_toa[x,y] = matrix_toa[x,y] + clog[frame_number][j][3] # toa

    return matrix_tot, matrix_toa

def frame_matrix_tpx(clog_path,filename,frame_number):
    """
    Carlos, from Andrej's script, 4 Aug 2022'
    same as frame_matrix_tpx3
    for TPX data in ToT
    """
    clog = read_clog(filename)[2]
    matrix_tot = np.zeros([256,256]) # tot
    #matrix_toa = np.zeros([256,256]) # toa

    for j in range(len(clog[frame_number][:])):
        x = int(clog[frame_number][j][0]) # x coord
        y = int(clog[frame_number][j][1]) # y coord
        matrix_tot[x,y] = matrix_tot[x,y] + clog[frame_number][j][2] # tot
        #matrix_toa[x,y] = matrix_toa[x,y] + clog[frame_number][j][3] # toa

    return matrix_tot


"""

def frame_matrix(clog_path, filename, frame_number):
    # finds a single frame in the clog file
    # makes it into a sq matrix = single frame
    clog = read_clog(filename)[2]
    matrix = np.zeros([256,256])

    for j in range(len(clog[frame_number][:])):
        x = int(clog[frame_number][j][0])
        y = int(clog[frame_number][j][1])
        matrix[x,y] = matrix[x,y] + clog[frame_number][j][2]

    return matrix
`

input_dir = 'DPE_carlos_data_output//2018_08_01_protons//'
det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
e_name = ['08_MeV', '13_MeV', '22_MeV', '31_MeV']
rot_name = ['00_angle', '10_angle', '20_angle', '30_angle', '40_angle', '50_angle', '60_angle', '70_angle', '80_angle', '85_angle', '88_angle', '89_angle', '90_angle', '92_angle']
voltage = ['-450 V', '-300 V', '50 V', '200 V', '200 V']
thickness = np.array([2000, 500, 100, 300, 500])

label_det = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m']
label_energy = ['08 MeV', '13 MeV', '22 MeV', '31 MeV']
label_angle = ['0$^{\circ}$ angle', '10$^{\circ}$ angle', '20$^{\circ}$ angle', '30$^{\circ}$ angle', '40$^{\circ}$ angle', '50$^{\circ}$ angle', '60$^{\circ}$ angle', '70$^{\circ}$ angle', '80$^{\circ}$ angle', '85$^{\circ}$ angle', '88$^{\circ}$ angle', '89$^{\circ}$ angle', '90$^{\circ}$ angle', '92$^{\circ}$ angle']
mydpi = 300
tickfnt = 14
lin_wd = 1.75



#Script for numpy and cluster_coincidence creation
for i in range(len(det_name)):
    for j in range(len(e_name)):
        for k in range(len(rot_name)):
            path = input_dir + det_name[i] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
            
            numpy_exists = os.path.exists(path + 'ExtElist_numpy.txt')
            coincidence_exists = os.path.exists(path + 'cluster_coincidence.txt')
            
            if numpy_exists == False:
                print('Printing numpy elist for', det_name[i], e_name[j], rot_name[k])
                header, units, data_elist = read_elist(path+'ExtElist.txt')
                write_elist(path+'ExtElist_numpy.txt', header, units, data_elist)
            else:
                pass

            if coincidence_exists == False:
                print('Printing cluster coincidence for', det_name[i], e_name[j], rot_name[k])
                data = np.loadtxt(path + 'ExtElist_numpy.txt', skiprows=2)
                eventid = np.loadtxt(path + 'ExtElist_numpy.txt', skiprows=2, usecols=1, dtype='int')
                count = np.bincount(eventid)
                events = np.arange(0, len(count), 1)

                boo = np.array([])
                for number in range(len(count)-1):
                    #print(number)
                    if count[number] > 1:
                        boo = np.append(boo, 1)
                    else:
                        boo = np.append(boo, 0)

                out = np.column_stack((events[:-1], count[:-1], boo))
                np.savetxt(path+'cluster_coincidence.txt', out, fmt='%i', delimiter='\t', header='Event, Count, Is_Coincidence')
            else:
                pass

            #cluster_coincidence = np.loadtxt(path + 'cluster_coincidence.txt', skiprows=1)

            #for m in range(len(cluster_coincidence[:,0])):
"""


"""
#1D histogram related part

pathCdTe = []
pathGaAs = []
pathSi100 = []
pathSi300 = []
pathSi500 = []

for j in range(len(e_name)):
    for k in range(len(rot_name)):
        print(e_name[j], rot_name[k])
        pathCdTe = input_dir + det_name[0] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathGaAs = input_dir + det_name[1] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi100 = input_dir + det_name[2] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi300 = input_dir + det_name[3] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi500 = input_dir + det_name[4] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'

        CdTe = np.loadtxt(pathCdTe + 'ExtElist_numpy.txt', skiprows=2)
        GaAs = np.loadtxt(pathGaAs + 'ExtElist_numpy.txt', skiprows=2)
        Si100 = np.loadtxt(pathSi100 + 'ExtElist_numpy.txt', skiprows=2)
        Si300 = np.loadtxt(pathSi300 + 'ExtElist_numpy.txt', skiprows=2)
        Si500 = np.loadtxt(pathSi500 + 'ExtElist_numpy.txt', skiprows=2)

        #bin = np.array([700, 128, 128, 128, 128])
        binE = 300

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe[:,12], bins=512, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,12], bins=512, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,12], bins=512, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,12], bins=512, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,12], bins=512, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=0, right=1)
        plt.ylim(bottom=1, top=None)
        plt.yscale('log')
        plt.xlabel('Linearity [-]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Particle linearity distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Linearity.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe[:,4], bins=512, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,4], bins=512, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,4], bins=512, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,4], bins=512, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,4], bins=512, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1E3, right=1E5)
        plt.ylim(bottom=1, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Deposited energy distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Energy.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe[:,7], bins=512, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,7], bins=216, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,7], bins=256, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,7], bins=200, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,7], bins=512, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1E1, right=1E4)
        plt.ylim(bottom=1, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Size [px]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster size distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Size.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe[:,8], bins=512, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,8], bins=4096, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,8], bins=binE, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,8], bins=binE, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,8], bins=binE, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1E1, right=1E4)
        plt.ylim(bottom=1, top=1E6)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Height [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster height distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Height.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        CdTe_LET = CdTe[:,4] / (np.sqrt((CdTe[:,13] * 55) ** 2 + 2000**2))
        GaAs_LET = GaAs[:,4] / (np.sqrt((GaAs[:,13] * 55) ** 2 + 500**2))
        Si100_LET = Si100[:,4] / (np.sqrt((Si100[:,13] * 55) ** 2 + 100**2))
        Si300_LET = Si300[:,4] / (np.sqrt((Si300[:,13] * 55) ** 2 + 300**2))
        Si500_LET = Si500[:,4] / (np.sqrt((Si500[:,13] * 55) ** 2 + 500**2))

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe_LET, bins=128, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs_LET, bins=350, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100_LET, bins=128, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300_LET, bins=128, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500_LET, bins=128, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1E-1, right=1E2)
        plt.ylim(bottom=1, top=1E6)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Linear energy transfer distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/LET.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""        

"""
# Cast na single clustre

path = []
num = 100
tickfnt = 14
margin = 5
#xmin = np.array([30, 30, 170, 10, 70])
#xmax = np.array([110, 110, 250, 90, 150])
#ymin = np.array([130, 120, 200, 10, 110])
#ymax = np.array([210, 200, 280, 90, 190])

for i in range(len(det_name)):
    for j in range(len(e_name)):
        for k in range(len(rot_name)):
            print(det_name[i], e_name[j], rot_name[k])
            path = input_dir + det_name[i] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
            clog = read_clog(path + 'ClusterLog.clog')[2]
            #elist = np.loadtxt(path + 'ExtElist_numpy.txt', skiprows=2)
            #coincidence = np.loadtxt(path + 'cluster_coincidence.txt', skiprows=1, usecols=2, dtype='int')
            rand_nums = sorted(random.sample(range(0, len(clog[:])), num))

            #val = selected_clusters[i]
            #for idx, val in enumerate(selected_clusters):
            #result = np.where(elist[:,1] == val)
            #print(len(clog[val][:]))

            #print(val, result[0][0], coincidence[val])

            for m in range(len(rand_nums)):
                if len(clog[rand_nums[m]][:]) > 5 and len(clog[rand_nums[m]][:]) < 1000:   #5, 50;  and elist[int(result[0][0]),4] > 10;  and elist[int(result[0][0]),4] > 10
                    print(m, rand_nums[m])
                    matrix = np.zeros([256,256])
                        
                    n=0
                    x = []
                    y = []
                    for n in range(len(clog[rand_nums[m]][:])):
                        x.append(clog[rand_nums[m]][n][0])
                        y.append(clog[rand_nums[m]][n][1])
                        matrix[int(x[n]), int(y[n])] = matrix[int(x[n]), int(y[n])] + clog[rand_nums[m]][n][2]

                    if (max(x)-min(x)) < (max(y)-min(y)):
                        diff_x = np.abs((max(x)-min(x))-(max(y)-min(y)))
                    else:
                        diff_x = 0
                    if (max(y)-min(y)) < (max(x)-min(x)):
                        diff_y = np.abs((max(y)-min(y))-(max(x)-min(x)))
                    else:
                        diff_y = 0

                    plt.close()
                    plt.clf()
                    plt.cla()
                    plt.rcParams["figure.figsize"] = (11.7, 8.3)
                    #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
                    # If the orientation of matrix doesnt fit, use this instead
                    plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
                    plt.gca().xaxis.tick_bottom()
                    plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8).set_label(label='Energy [keV]',size=tickfnt,weight='regular')   # format="%.1E"
                    plt.clim(1,1E3)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
                    #plt.title(label = str(labels[i]) + ' - Cluster #' + str(val), fontsize=tickfnt)
                    plt.title(label = str(label_det[i]) + ', bias ' + str(voltage[i]), fontsize=tickfnt+4)
                    plt.xlabel('X position [px]', fontsize=tickfnt)
                    plt.ylabel('Y position [px]', fontsize=tickfnt)
                    plt.xlim([min(x)-diff_x/2-margin, max(x)+diff_x/2+margin])
                    plt.ylim([min(y)-diff_y/2-margin, max(y)+diff_y/2+margin])
                    #plt.xlim([xmin[i], xmax[i]])
                    #plt.ylim([ymin[i], ymax[i]])
                    plt.tick_params(axis='x', labelsize=tickfnt)
                    plt.tick_params(axis='y', labelsize=tickfnt)
                    plt.savefig('iworid_figures/Single_cluster/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/cluster_'+str(rand_nums[m])+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
                    np.savetxt('iworid_figures/Single_cluster/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/cluster_'+str(rand_nums[m])+'.txt', matrix)    
                else:
                    pass
"""


"""
#2D related part

path = []

for i in range(len(det_name)):
    for j in range(len(e_name)):
        for k in range(len(rot_name)):
            path = input_dir + det_name[i] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
            print(path)
            clog = read_clog(path + 'ClusterLog.clog')[2]
            elist = np.loadtxt(path + 'ExtElist_numpy.txt', skiprows=2)

            xlin = np.linspace(0, 14.08, 141)
            ylin = np.linspace(0, 14.08, 141)

            matrix = np.zeros([256,256])
            matrix_e = np.zeros([len(xlin),len(ylin)])
            matrix_size = np.zeros([len(xlin),len(ylin)])
            matrix_height = np.zeros([len(xlin),len(ylin)])
            matrix_length = np.zeros([len(xlin),len(ylin)])
            matrix_length_3D = np.zeros([len(xlin),len(ylin)])
            matrix_let = np.zeros([len(xlin),len(ylin)])

            dec = 1
            xelist = np.around(elist[:,2], decimals=dec)
            yelist = np.around(elist[:,3], decimals=dec)
            eelist = np.around(elist[:,4], decimals=dec)
            sizeelist = np.around(elist[:,7], decimals=dec)
            heightelist = np.around(elist[:,8], decimals=dec)
            lengthelist = np.around(elist[:,13], decimals=dec) * 55
            length3Delist = np.around(np.sqrt((elist[:,13] * 55)**2 + thickness[i]**2), decimals=dec)
            letelist = np.around(elist[:,4] / (np.sqrt(((elist[:,13]) * 55) ** 2 + thickness[i] ** 2)), decimals=dec)

            #print(min(xelist), max(xelist))
            #print(min(yelist), max(yelist))

            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/x_elist.txt', xelist, fmt="%.3f")
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/y_elist.txt', yelist, fmt="%.3f")
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/E_elist.txt', eelist, fmt="%.3f")
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Size_elist.txt', sizeelist, fmt="%.3f")
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Height_elist.txt', heightelist, fmt="%.3f")
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Length_elist.txt', lengthelist, fmt="%.3f")

            nasobok = 10

            for iter in range(len(elist[:,0])):
                matrix_e[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] = eelist[iter]
                matrix_size[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] = sizeelist[iter]
                matrix_height[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] = heightelist[iter]
                matrix_length[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] = lengthelist[iter]
                matrix_length_3D[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] = length3Delist[iter]
                matrix_let[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] = letelist[iter]

            np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/matrix_E_elist.txt', matrix_e, fmt="%.1f")
            np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/matrix_Size_elist.txt', matrix_size, fmt="%.1f")
            np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/matrix_Height_elist.txt', matrix_height, fmt="%.1f")
            np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/matrix_Length_elist.txt', matrix_length, fmt="%.1f")
            np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/matrix_Length_3D_elist.txt', matrix_length_3D, fmt="%.1f")
            np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/matrix_LET_elist.txt', matrix_let, fmt="%.1f")

            plt.close()
            plt.clf()
            plt.cla()
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_e[::-1,:])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8).set_label(label='Energy [keV]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(1,1E6)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            #plt.title(label = str(det_name[i]) + ' - Cluster #' + str(val), fontsize=tickfnt)
            plt.xlabel('X position [mm]', fontsize=tickfnt)
            plt.ylabel('Y position [mm]', fontsize=tickfnt)
            #plt.xlim([min, max])
            #plt.ylim([min, max])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.xticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.yticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.savefig('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/E_elist.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/E_elist.txt', matrix_e)

            plt.close()
            plt.clf()
            plt.cla()
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_size[::-1,:])), origin='lower', cmap='modified_hot')
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='Cluster size [px]', shrink=0.8, aspect=20*0.8).set_label(label='Size [px]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(0,1000)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            #plt.title(label = str(det_name[i]) + ' - Cluster #' + str(val), fontsize=tickfnt)
            plt.xlabel('X position [mm]', fontsize=tickfnt)
            plt.ylabel('Y position [mm]', fontsize=tickfnt)
            #plt.xlim([min, max])
            #plt.ylim([min, max])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.xticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.yticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.savefig('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Size_elist.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Size_elist.txt', matrix_size)
        
            plt.close()
            plt.clf()
            plt.cla()
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_height[::-1,:])), origin='lower', cmap='modified_hot')
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='Cluster height [keV]', shrink=0.8, aspect=20*0.8).set_label(label='Height [keV]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(0,2000)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            #plt.title(label = str(det_name[i]) + ' - Cluster #' + str(val), fontsize=tickfnt)
            plt.xlabel('X position [mm]', fontsize=tickfnt)
            plt.ylabel('Y position [mm]', fontsize=tickfnt)
            #plt.xlim([min, max])
            #plt.ylim([min, max])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.xticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.yticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.savefig('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Height_elist.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Height_elist.txt', matrix_height)

            plt.close()
            plt.clf()
            plt.cla()
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_length[::-1,:])), origin='lower', cmap='modified_hot')
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='Length [$\mu$m]', shrink=0.8, aspect=20*0.8).set_label(label='Length [$\mu$m]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(0,6000)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            #plt.title(label = str(det_name[i]) + ' - Cluster #' + str(val), fontsize=tickfnt)
            plt.xlabel('X position [mm]', fontsize=tickfnt)
            plt.ylabel('Y position [mm]', fontsize=tickfnt)
            #plt.xlim([min, max])
            #plt.ylim([min, max])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.xticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.yticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.savefig('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Length_elist.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Length_elist.txt', matrix_length)

            plt.close()
            plt.clf()
            plt.cla()
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_length_3D[::-1,:])), origin='lower', cmap='modified_hot')
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='3D Length [$\mu$m]', shrink=0.8, aspect=20*0.8).set_label(label='3D Length [$\mu$m]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(0,None)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            #plt.title(label = str(det_name[i]) + ' - Cluster #' + str(val), fontsize=tickfnt)
            plt.xlabel('X position [mm]', fontsize=tickfnt)
            plt.ylabel('Y position [mm]', fontsize=tickfnt)
            #plt.xlim([min, max])
            #plt.ylim([min, max])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.xticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.yticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.savefig('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Length_3D_elist.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/Length_3D_elist.txt', matrix_length_3D)


            plt.close()
            plt.clf()
            plt.cla()
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            #plt.matshow(matrix[:,:], origin='lower', cmap='viridis')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_let[::-1,:])), origin='lower', cmap='modified_hot')
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='LET [keV/$\mu$m]', shrink=0.8, aspect=20*0.8).set_label(label='LET [keV/$\mu$m]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(0,None)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            #plt.title(label = str(det_name[i]) + ' - Cluster #' + str(val), fontsize=tickfnt)
            plt.xlabel('X position [mm]', fontsize=tickfnt)
            plt.ylabel('Y position [mm]', fontsize=tickfnt)
            #plt.xlim([min, max])
            #plt.ylim([min, max])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.xticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.yticks([0, 20, 40, 60, 80, 100, 120, 140], ['0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4'])
            plt.savefig('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/LET_elist.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
            #np.savetxt('iworid_figures/2D/elist/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/LET_elist.txt', matrix_let)
"""



"""
path = []

for i in range(len(det_name)):
    for j in range(len(e_name)):
        for k in range(len(rot_name)):
            #print(det_name[i], e_name[j], rot_name[k])
            path = input_dir + det_name[i] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
            clog = read_clog(path + 'ClusterLog.clog')[2]
            matrix = np.zeros([256,256])
            counting = 0
            good = 0

            for l in range(len(clog[:])):
                x = []
                y = []
                for m in range(len(clog[l][:])):
                    if len(clog[l][:]) < 1000:
                        #good = good + 1
                        x.append(clog[l][m][0])
                        y.append(clog[l][m][1])
                        matrix[int(x[m]), int(y[m])] = matrix[int(x[m]), int(y[m])] + clog[l][m][2]
                    else:
                        #counting = counting + 1
                        pass
    
            print(det_name[i], 'total ', len(clog[:]), ', good ', good, ', bad', counting)
            plt.rcParams["figure.figsize"] = (11.7, 8.3)
            #plt.matshow(matrix[:,:], origin='lower', cmap='viridis', norm=colors.LogNorm())
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='Energy per pixel [keV/px]', shrink=0.8, aspect=20*0.8).set_label(label='Energy per pixel [keV/px]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(1,1E6)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
            plt.xlabel('X position [px]', fontsize=tickfnt)
            plt.ylabel('Y position [px]', fontsize=tickfnt)
            plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
            plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
            plt.tick_params(axis='x', labelsize=tickfnt)
            plt.tick_params(axis='y', labelsize=tickfnt)
            plt.title(label = str(labels[i]) + ', bias ' + str(voltage[i]), fontsize=tickfnt+4)
            plt.savefig('iworid_figures/2D/clog/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/E_clog.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
            np.savetxt('iworid_figures/2D/clog/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/E_clog.txt', matrix)

            cislo = cislo + 1
"""