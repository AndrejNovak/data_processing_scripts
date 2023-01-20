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
from scipy.optimize import curve_fit
import pandas as pd

#matplotlib.use('Agg')   # To solve issue: Fail to create pixmap with Tk_GetPixmap

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


class cluster_filter:
    # new class, to filter events in elist
    # accepts arbitrary CA PAR filter, one, and also more than one
    # Lukas+Carlos, ADV, Prague, 8 Aug 2022
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


class cluster_filter_ONE_PAR:
    # new class, to filter events in elist
    # accepts arbitrary CA PAR filter, one, and also more than one
    # Lukas+Carlos, ADV, Prague, 8 Aug 2022
    # edges = border values for given CA PAR 
    # indeces = COL # in elist of given CA PAR, e.g. 4 for E
    def __init__(self, edges = [], indeces = []):
        self.edges = edges
        self.indeces = indeces

    # function to execute the filter
    def pass_filter(self, cluster_var):
        #return True
        #lenka = len(self.indeces)
        for i in range(len(self.indeces)):
            #print('lenka = ',lenka,', i = ',i)
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


class cluster_filter_MULTI_PAR: 
    # Carlos modified, ok, July 2022
    # edges = border values for given CA PAR 
    # indeces = COL # in elist of given CA PAR, e.g. 4 for E
    def __init__(self, edges = [], indeces = []):
        self.edges = edges
        self.indeces = indeces

    #def ok_filter(self, ok_step):
    #    ok_step = list(range(len(self.indeces))

    # function to execute the filter
    def pass_filter(self, cluster_var):
        #return True
        #lenka = len(self.indeces)  
        ok = 0  # counter of OK steps       
        for i in range(len(self.indeces)):
            #print('lenka = ',lenka,', i = ',i)
            down_edge = self.edges[i*2]
            up_edge = self.edges[(i*2)+1]
            i_var = self.indeces[i]
            #print('pass_filter',down_edge, cluster_var[i_var], up_edge, end='')
            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                ok = ok + 1
                #print('True')
                #return True
            else: 
                #print('False')
                return False
        if ok == len(self.indeces):
            return True


class cluster_filter_MULTI_PAR_RATIOS: 
    # from Lukas' cluster_filter class
    # Carlos modified/extended, ok, Aug 2022
    # same as cluster_filter_MULTI_PAR with newly added RATIOS of CA PARs
    # edges = border values for given CA PAR 
    # indeces = COL # in elist of given CA PAR, e.g. 4 for E
    # edges_ratio = border values for the ratio(s) of pairs of CA PARs
    # ind_pair_ratio = COL # in elist of pair of CA PAR for ratio(s)
    def __init__(self, edges = [], indeces = [], edges_ratio = [], ind_pair_ratio = []):
        # -- for the single CA PAR --
        self.edges = edges
        self.indeces = indeces
        # -- for the ratio --
        self.edges_ratio = edges_ratio
        self.ind_pair_ratio = ind_pair_ratio

    #def ok_filter(self, ok_step):
    #    ok_step = list(range(len(self.indeces))

    # function to execute the filter
    def pass_filter(self, cluster_var):
        #return True
        #lenka = len(self.indeces)  
        ok = 0  # counter of OK steps for the single CA PAR filters   
        ok_rat = 0  # counter of OK steps for the RATIOS of CA PARs
        for i in range(len(self.indeces)):
            #print('lenka = ',lenka,', i = ',i)
            # -- for the single CA PAR filtering --
            down_edge = self.edges[i*2]
            up_edge = self.edges[(i*2)+1]
            i_var = self.indeces[i]
            #print('pass_filter',down_edge, cluster_var[i_var], up_edge, end='')
            #if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                ok = ok + 1
                #print('True')
                #return True
            else: 
                #print('False')
                return False
        if ok == len(self.indeces):
            # -- for the ratios between two CA PAR --
            num_rat_filters = int(len(self.ind_pair_ratio)/2)
            for k in range(num_rat_filters):
                # --
                down_edge_ratio = self.edges_ratio[k*2]
                up_edge_ratio = self.edges_ratio[(k*2)+1]
                k_var_ratio_top = self.ind_pair_ratio[k*2]            
                k_var_ratio_bot = self.ind_pair_ratio[(k*2)+1]  
                # -- ratio for given clu
                ratio_clu = (cluster_var[k_var_ratio_top]/cluster_var[k_var_ratio_bot])
                if (ratio_clu >= down_edge_ratio and ratio_clu <= up_edge_ratio):
                    ok_rat = ok_rat + 1
                else:
                    return False
            if ok_rat == num_rat_filters:
                return True


def print_out(FileOutPath, filename, input_data):
    """
    *** OLD FUNCTION, CURRENTLY NOT IN USE***
    Function for printing output data into classic Elist format
    """
    if not os.path.exists(FileOutPath):
        os.makedirs(FileOutPath)
    with open(FileOutPath + filename, 'w') as f:
        sys.stdout = f
        print(input_data)
        sys.stdout


def read_clog(FileInPath, filename):
    """ 
    This function reads through the .clog file and can access Unix_time and Acquisition_time of every frame,
    #of frames, #of events in frame and their values [x, y, ToT, ToA].
    For printing Unix_time use: read_clog(filename)[0]
    For printing Acquisition_time use: read_clog(filename)[1]
    For printing full data use: read_clog(filename)[2]

    When using 'data = read_clog(FileInPath, filename)[2]', you can traverse the data on level of Frames, 
    registered values (group of 4 values - [x, y, ToT, ToA]) and selected value from one of the 
    four possible - x or y or ToT or ToA.

    To access first layer (selected frame) use: data[0]
    To access second layer (selected 4-group of selected frame) use: data[0][0]
    To access third layer (selected value from selected 4-group of selected frame) use: data[0][0][0] 
    """
    
    inputFile = open(FileInPath + filename)
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


def get_column(FileInPath, filename, col_name):
    """
    From Elist extract a specific column based on the exact name of the column
    Function returns a list of data in python list format
    col_name = name of the variable from Elist

    Example, select column with Energy values:
    selected_column = get_column('path/to/Elist.txt', 'E') 
    """
    inputFile = open(FileInPath + filename, 'r')
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


def read_elist_make_ext_elist(filename,col_num_pairs_for_ratios,header_txt_new_cols,units_txt_new_cols):
    """
    # new funkce read_elist to include option to filter events (Lukas 8 Aug 22)
    Function to read elist (calibrated, output of DPE_CP)
    it newly calculates RATIOS of pairs of CA PAR
    and puts them into new COLs
    output is the same elist with the added new COLs at right (COL = 16+17+...)
    ---- syntax of input variables ----
    - filename = elist (output of DPE CP, stored in Files DIR output)
    - col_num_pairs_for_ratios = e.g. = [4,7,9,7] # E,A,  BordPx,A
    - header_txt_new_cols = e.g. = ['E/A','BordPx/A']
    - units_txt_new_cols = e.g. = ['keV/px','a.u.']
    """
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    # -- add new cols

                
    # --
    inputFile.close()  
    splitlines = []
    
    # when there is filter entered:
    clu_cou_all = 0 # counter of all clusters
    #clu_cou_ok = 0 # counter of OK clu's
    #clu_cou_bad = 0 # counter of rejected clu's
    num_pairs_new_cols = int(len(col_num_pairs_for_ratios)/2)
    line_num=0
    #if new_filter is not None:
    
    for line in lines:
            line_num += 1
            cluster_var = list(line.rstrip().split(";"))
            # for the first heading 2 rows 
            if line_num < 3:
                if line_num == 1:                
                    print('first row = ',line_num)
                    for k in range(num_pairs_new_cols):
                        cluster_var.append(header_txt_new_cols[k])
                    splitlines.append(cluster_var)
                else:                    
                    print('second row = ',line_num)
                    for k in range(num_pairs_new_cols):
                        cluster_var.append(units_txt_new_cols[k])
                    splitlines.append(cluster_var)
                #if line_num >= 3 and new_filter is not None:
                #print('ostatni radky',line_num)
            else:
                cluster_var = [float(i) for i in list(line.rstrip().split(";"))]
                #print(new_filter.pass_filter(cluster_var))
                clu_cou_all = clu_cou_all + 1
                for i in range(num_pairs_new_cols):
                    #new_col_value = 10
                    new_col_value = cluster_var[col_num_pairs_for_ratios[i*2]]/cluster_var[col_num_pairs_for_ratios[(i*2)+1]]
                    cluster_var.append(new_col_value)
                    # --
                splitlines.append(cluster_var)
    print('all clusters thru = ', clu_cou_all)
        #print('OK clusters = ', clu_cou_ok)
        #print('bad clusters = ', clu_cou_bad)

        # the full elist with extended col output as single object
    return splitlines[0], splitlines[1], splitlines[2:]
        # the elist output split into three objects
        #return splitlines[0], splitlines[1], splitlines[2:]

    #else:
        #print('No new columns, nothing processed')
        #splitlines = inputFile


def read_elist_filter(filename,col_num_pairs_for_ratios,header_txt_new_cols,units_txt_new_cols,new_filter=None):
    """
    # new funkce read_elist to include option to filter events (Lukas 8 Aug 22)
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
    clu_cou_all = 0 # counter of all clusters
    clu_cou_ok = 0 # counter of OK clu's
    clu_cou_bad = 0 # counter of rejected clu's
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
                clu_cou_all = clu_cou_all + 1
                if new_filter.pass_filter(cluster_var):
                    #print('Filter ok ', end='') # removes enter
                    clu_cou_ok = clu_cou_ok + 1
                    cluster_var.append(1)
                else: 
                    #print('False B ')
                    clu_cou_bad = clu_cou_bad + 1
                    #print('Filter bad ', end='')
                    cluster_var.append(0)
                    #print(cluster_var)
                #print(line_num)                
                splitlines.append(cluster_var)
        print('all clusters = ', clu_cou_all)
        print('OK clusters = ', clu_cou_ok)
        print('bad clusters = ', clu_cou_bad)

        # the full elist with extended col output as single object
        return splitlines[0], splitlines[1], splitlines[2:]
        # the elist output split into three objects
        #return splitlines[0], splitlines[1], splitlines[2:]

    else:
        print('No filter, nothing processed')
        #splitlines = inputFile
   

def read_elist_make_ext_filter(filename,col_num_pairs_for_ratios,header_txt_new_cols,units_txt_new_cols,new_filter=None):
    """
    Carlos, 23aug2022
    Function to read elist (calibrated, output of DPE_CP)
    it newly calculates RATIOS of pairs of CA PAR
    and puts them into new COLs
    and then applies a filter of clusters according CA PAR incl. the new RATIOS
    and adds to the elist a new col at the end to indicate
    1 = filter pass
    0 = filter fail   
    output is the same elist with the added new COLs at right (COL = 16+17+...)
    core/template from Lukas+Andrej, modified Carlos 23aug2022
    output is the same elist with the added new col at right (COL = 18)
    ---- syntax of input variables ----
    - filename = elist (output of DPE CP, stored in Files DIR output)
    - col_num_pairs_for_ratios = e.g. = [4,7,9,7] # E,A,  BordPx,A
    - header_txt_new_cols = e.g. = ['E/A','BordPx/A']
    - units_txt_new_cols = e.g. = ['keV/px','a.u.']
    - new_filter = e.g. [90,5000,4500,5.E5,0.9,1.7,4,300,30,5000],[8,4,10,7,15]) # H E R A, E/A, 
    """
    
    print('--- read elist ext filt running ---')
    inputFile = open(filename,"r")
    lines = inputFile.readlines()
    inputFile.close()  
    splitlines = []
    
    num_pairs_new_cols = int(len(col_num_pairs_for_ratios)/2)
    line_num=0
    # when there is filter entered:
    clu_cou_all = 0 # counter of all clusters
    clu_cou_ok = 0 # counter of OK clu's
    clu_cou_bad = 0 # counter of rejected clu's
    if new_filter is not None:
    
        for line in lines:
            line_num += 1
            cluster_var = list(line.rstrip().split(";"))
            # for the first heading 2 rows 
            if line_num < 3:
                if line_num == 1:                
                    print('first row = ',line_num)
                    # -- the new COLs of RATIOS of CA PARs
                    for k in range(num_pairs_new_cols):
                        cluster_var.append(header_txt_new_cols[k])
                    # -- the new COL of FILTER
                    cluster_var.append('Filter')
                    splitlines.append(cluster_var)
                else:                    
                    print('second row = ',line_num)
                    # -- the new COLs of RATIOS of CA PARs
                    for k in range(num_pairs_new_cols):
                        cluster_var.append(units_txt_new_cols[k])
                    # -- the new COL of FILTER
                    cluster_var.append('1 = ok')
                    splitlines.append(cluster_var)
                #if line_num >= 3 and new_filter is not None:
                #print('ostatni radky',line_num)
                print('first two rows done',line_num)
                #splitlines.append(cluster_var)
            # for the rest
            else:                    
                #if line_num >= 3 and new_filter is not None:
                #print('ostatni radky',line_num)
                cluster_var = [float(i) for i in list(line.rstrip().split(";"))]
                #print(new_filter.pass_filter(cluster_var))
                clu_cou_all = clu_cou_all + 1
                # -- make and add the new COLs of RATIOS of CA PARs
                for i in range(num_pairs_new_cols):
                    #new_col_value = 10
                    new_col_value = round(cluster_var[col_num_pairs_for_ratios[i*2]]/cluster_var[col_num_pairs_for_ratios[(i*2)+1]],3)
                    cluster_var.append(new_col_value)
                    # --
                # -- apply make the filter
                if new_filter.pass_filter(cluster_var):
                    #print('Filter ok ', end='') # removes enter
                    clu_cou_ok = clu_cou_ok + 1
                    cluster_var.append(1)
                else: 
                    #print('False B ')
                    clu_cou_bad = clu_cou_bad + 1
                    #print('Filter bad ', end='')
                    cluster_var.append(0)
                    #print(cluster_var)
                #print(line_num)                
                splitlines.append(cluster_var)
        # -- end of adding new COLS and of filtering
        print('all clusters = ', clu_cou_all)
        print('OK clusters = ', clu_cou_ok)
        print('bad clusters = ', clu_cou_bad)
        # --
        print('--- read elist ext filt done ---')    
        # the full elist with extended col output as single object
        return splitlines[0], splitlines[1], splitlines[2:]
        # the elist output split into three objects
        #return splitlines[0], splitlines[1], splitlines[2:]        
        
    else:
        print('No filter, nothing processed')
        #splitlines = inputFile


def write_elist(filename_out, header, units, data):
    """
    *** UNNECESSARY FUNCTION, numpy.loadtxt(skiprows=2) is already possible with classic Elist ***
    Use this function to re-print input Elist in a form
    that is readable by numpy.loadtxt(filename, skiprows=2)
    """
    with open(filename_out, 'w') as f:
        f.write(' '.join(map(str, header))+'\n')
        f.write(' '.join(map(str, units))+'\n')
        for row in data:
            s = ';'.join(map(str, row))
            f.write(s+'\n')


def create_matrix_filter_tpx3_t3pa(elist_filtered,clog,num_col_filter,num_frames):
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
        if elist_filtered[2][elist_row][num_col_filter] == 1:
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


def create_matrix_filter_tpx_f(elist_filtered,clog,num_col_filter,num_particles):
#def create_matrix_filter(elist_filtered,clog, num_frames, rand):
    """
    Carlos+Lukas+Andrej, ADV, Prague, 8 Aug 2022
    Function to create E and ToA sq matrix for 2D plot of det px matrix
    customized for TPX frame data, and its clog output with f
    inputs:
    - elist_filtered is the DPE_CP output elist with additional col from filter
    - clog is the clog calib output of DPE_CP
    - num_particles = # of events to integrate i.e to add to merged plot from beginning i.e. from f zero
        in the clog file output of DPE_CP for TPX data frames
        for TPX frame data ToT: Input num_particles is the cluster i.e. event number
        for raw clog frame data: num_particles is the f #
    """
    print('--- crea_matr_filt_tpx_f running ---')
    #if rand == 'True':
    #    rand_nums = sorted(random.sample(range(0, len(clog[:])), len(num_frames)))
    #else:
    rand_nums = list(range(0,num_particles))       # list(range(0,num_frames))
    # the sq matrix for all clusters
    matrix_E_all = np.zeros([256,256])
    #matrix_ToA_all = np.zeros([256,256])    # the sq matrix for the filter OK clusters
    matrix_E_ok = np.zeros([256,256])
    #matrix_ToA_ok = np.zeros([256,256])
    # the sq matrix for the filter REJECTED = BAD clusters
    matrix_E_bad = np.zeros([256,256])
    #matrix_ToA_bad = np.zeros([256,256])
    # int counters of clu's according filter
    c_all = 0
    c_ok = 0
    c_bad = 0
    # for cyclus cluster by cluster
    jump = 0
    #f_jump = 0
    #multiplet_num = 0 # to keep record of multiplet occurrence
    for idx,elist_row in enumerate(rand_nums):
    #for elist_row in enumerate(rand_nums):    
            
        # counter for the drawing of clusters in clog
        #f_num = elist_row - multiplet_num
        f_num = elist_row
        # cluster area from clog
        clu_A_clog = len(clog[f_num][:])
        # cluster area from elist
        #clu_A_elist = elist_filtered[2][elist_row][7]
        
        #print('elist_row = ',elist_row,  ', f_num = ',f_num,', filter = ',elist_filtered[2][elist_row][15])
        #print(', clu_A_elist = ',clu_A_elist, ', clu_A_clog = ',clu_A_clog)
        c_all = c_all + 1            
        
        #print('<< ALL clusters >>')
        # ----------------------------
        # for all clusters:
        # ----------------------------
        for j in range(clu_A_clog):
        #for j in len(clog[elist_row][:]):
            #print('all clu, clu px # = ',j)
            x = int(clog[f_num][j][0])
            y = int(clog[f_num][j][1])    
            matrix_E_all[x,y] = matrix_E_all[x,y] + clog[f_num][j][2]
            #matrix_ToA_all[x,y] = clog[f_num][j][3]        
        
        # ----------------------------
        # for clusters with OK filter:
        # ----------------------------
        if elist_filtered[2][elist_row][num_col_filter] == 1:
            #print('<< sq matrix filter ok >>')
            # -- to take into account multiplets 
            # these can be resolved in elist, but not in clog
            '''
            if elist_row < num_particles and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                jump = jump + 1 
                multiplet_num = multiplet_num + 1
            '''      
            # for each cluster record in clog:    
            #f_jump = jump
            #print('filter ok, jump = ',jump)
            c_ok = c_ok + 1            
            
            for j in range(clu_A_clog):
            #for j in len(clog[elist_row][:]):
                    
                #print('OK clu, clu px # = ',j)
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
                c_bad = c_bad + 1                            
                '''
                if elist_row < num_particles and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                    jump = jump + 1 
                    multiplet_num = multiplet_num + 1
                '''

                for j in range(clu_A_clog):
                    #print('BAD clu, clu px # = ',j)
                    x = int(clog[f_num][j][0])
                    y = int(clog[f_num][j][1])
                    matrix_E_bad[x,y] = matrix_E_bad[x,y] + clog[f_num][j][2]
                    #matrix_ToA_bad[x,y] = clog[f_num][j][3]
                    
    print('all clu = ',c_all)
    print('all ok = ',c_ok)
    print('all bad = ',c_bad)
    # --
    print('--- crea_matr_filt_tpx_f done ---')
    #return matrix_E_all, matrix_E_ok, matrix_E_bad
    return matrix_E_all, matrix_E_ok, matrix_E_bad, c_all, c_ok, c_bad


def calibrate_frame(a_path, b_path, c_path, t_path, matrix):
    """
    *** Rewritten from Carlos's MATLAB script ***
    
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


def print_fig_E(matrix, vmax, title, OutputPath, OutputName):

    # Changing colormap to start at transparent zero
    ncolors = 256
    color_array = plt.get_cmap('hot_r')(range(ncolors))
    color_array[:,-1] = np.linspace(0.0,1.0,ncolors)
    map_object = LinearSegmentedColormap.from_list(name='modified_hot',colors=color_array)
    plt.register_cmap(cmap=map_object)

    mydpi = 300
    tickfnt = 14

    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)
    else:
        pass

    plt.close()
    plt.cla()
    plt.clf()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    cbar = plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='Energy [keV]',size=tickfnt,weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.clim(1,vmax)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(label = title, fontsize=tickfnt+4)
    plt.savefig(OutputPath + OutputName + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '.txt', matrix)


def print_fig_ToA(matrix, vmax, OutputPath, OutputName):
    tickfnt = 14
    mydpi = 300

    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)
    else:
        pass
    
    plt.close()
    plt.cla()
    plt.clf()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1,:])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(label='ToA [ns]', shrink=0.8, aspect=20*0.8).set_label(label='ToA [ns]',size=tickfnt,weight='regular')   # format="%.1E"
    plt.clim(1,vmax)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '.txt', matrix, fmt="%.3f")


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


def plot_single_cluster(output_path, add_path, clog_path, frame_number):
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
    plt.clim(1,500)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    cbar = plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='Energy [keV]',size=tickfnt,weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label = 'Cluster #'+str(frame_number), fontsize=tickfnt)
    plt.ylim([min(y)-diff_y/2-margin, max(y)+diff_y/2+margin])
    plt.xlim([min(x)-diff_x/2-margin, max(x)+diff_x/2+margin])
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    if not os.path.exists(output_path + '/' + str(add_path)):
        os.makedirs(output_path + '/' + str(add_path))
    plt.savefig(output_path + '/' + str(add_path) + '/' + str(add_path) + '_cluster_' + str(frame_number) + '.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(output_path + '/' + str(add_path) + '/' + str(add_path) + '_cluster_' + str(frame_number) + '.txt', matrix)


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


input_dir = 'DPE_carlos_data_output//2018_08_01_protons//'
det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
#e_name = ['08_MeV', '13_MeV', '22_MeV', '31_MeV']
e_name = ['22_MeV', '31_MeV']
#rot_name = ['00_angle', '10_angle', '20_angle', '30_angle', '40_angle', '50_angle', '60_angle', '70_angle', '80_angle', '85_angle', '88_angle', '89_angle', '90_angle', '92_angle']
rot_name = ['50_angle']
voltage = ['-450 V', '-300 V', '50 V', '200 V', '200 V']
thickness = np.array([2000, 500, 100, 300, 500])

label_det = ['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m']
#label_energy = ['08 MeV', '13 MeV', '22 MeV', '31 MeV']
label_energy = ['22 MeV', '31 MeV']
label_angle = ['0$^{\circ}$ angle', '10$^{\circ}$ angle', '20$^{\circ}$ angle', '30$^{\circ}$ angle', '40$^{\circ}$ angle', '50$^{\circ}$ angle', '60$^{\circ}$ angle', '70$^{\circ}$ angle', '80$^{\circ}$ angle', '85$^{\circ}$ angle', '88$^{\circ}$ angle', '89$^{\circ}$ angle', '90$^{\circ}$ angle', '92$^{\circ}$ angle']
mydpi = 300
tickfnt = 14
lin_wd = 1.75


#mat = frame_matrix(input_dir + det_name[0] + '//' + e_name[0] + '//' + rot_name[0] + '//Files//ClusterLog.clog', 41)
#print_fig_ToA(mat, 'ToA_Test')


#Script for numpy and cluster_coincidence creation
for i in range(len(det_name)):
    for j in range(len(e_name)):
        for k in range(len(rot_name)):
            path = input_dir + det_name[i] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'

            coincidence_exists = os.path.exists(path + 'cluster_coincidence.txt')

            if coincidence_exists == False:
                print('Printing cluster coincidence for', det_name[i], e_name[j], rot_name[k])
                data = np.loadtxt(path + 'ExtElist.txt', skiprows=2, delimiter=';')
                eventid = np.loadtxt(path + 'ExtElist.txt', skiprows=2, delimiter=';', usecols=1, dtype='int')
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

#pokus = np.loadtxt("//147.175.96.33/fei_data/test.txt")
#print(pokus)


def func(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

data = np.loadtxt('filtered_LET_hist_Si_500um.txt')
data[0,1] = 0

popt, pcov = curve_fit(func, data[:,0], data[:,1])
print(popt)

"""
# Corrected formula for Length 2D and therefore improved LET results
for j in range(3):
    i = j+1
    CdTe = np.loadtxt('DPE_carlos_data_output/new_clusterer/CdTe31_elist'+str(i)+'.txt' ,skiprows=2)
    GaAs = np.loadtxt('DPE_carlos_data_output/new_clusterer/GaAs31_elist'+str(i)+'.txt' ,skiprows=2)
    Si100 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si10031_elist'+str(i)+'.txt' ,skiprows=2)
    Si300 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si30031_elist'+str(i)+'.txt' ,skiprows=2)
    Si500 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si50031_elist'+str(i)+'.txt' ,skiprows=2)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(CdTe[:,4], bins=2048, histtype = 'step', label=label_det[0], linewidth=lin_wd)
    plt.hist(GaAs[:,4], bins=8192, histtype = 'step', label=label_det[1], linewidth=lin_wd)
    plt.hist(Si100[:,4], bins=2048, histtype = 'step', label=label_det[2], linewidth=lin_wd)
    plt.hist(Si300[:,4], bins=2048, histtype = 'step', label=label_det[3], linewidth=lin_wd)
    plt.hist(Si500[:,4], bins=2048, histtype = 'step', label=label_det[4], linewidth=lin_wd)
    #plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
    #plt.ylim(bottom=1, top=ymax_let[j])
    plt.xlim(left=30, right=1E5) #left=1E2
    plt.ylim(bottom=1, top=1E5)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
    plt.legend(loc='upper right')
    plt.savefig('iworid_LET_corrected/Energy.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

    plt.close()
    plt.clf()
    plt.cla()
    plt.hist(CdTe[:,26], bins=2048, histtype = 'step', label=label_det[0], linewidth=lin_wd)
    plt.hist(GaAs[:,26], bins=8192, histtype = 'step', label=label_det[1], linewidth=lin_wd)
    plt.hist(Si100[:,26], bins=2048, histtype = 'step', label=label_det[2], linewidth=lin_wd)
    plt.hist(Si300[:,26], bins=2048, histtype = 'step', label=label_det[3], linewidth=lin_wd)
    plt.hist(Si500[:,26], bins=2048, histtype = 'step', label=label_det[4], linewidth=lin_wd)
    #plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
    #plt.ylim(bottom=1, top=ymax_let[j])
    plt.xlim(left=1E-1, right=1E2) #left=1E2
    plt.ylim(bottom=1, top=1E5)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title('Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
    plt.legend(loc='upper right')
    plt.savefig('iworid_LET_corrected/LET_method_' +str(i)+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)


CdTe1 = np.loadtxt('DPE_carlos_data_output/new_clusterer/CdTe31_elist1.txt' ,skiprows=2)
GaAs1 = np.loadtxt('DPE_carlos_data_output/new_clusterer/GaAs31_elist1.txt' ,skiprows=2)
Si1001 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si10031_elist1.txt' ,skiprows=2)
Si3001 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si30031_elist1.txt' ,skiprows=2)
Si5001 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si50031_elist1.txt' ,skiprows=2)

CdTe2 = np.loadtxt('DPE_carlos_data_output/new_clusterer/CdTe31_elist2.txt' ,skiprows=2)
GaAs2 = np.loadtxt('DPE_carlos_data_output/new_clusterer/GaAs31_elist2.txt' ,skiprows=2)
Si1002 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si10031_elist2.txt' ,skiprows=2)
Si3002 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si30031_elist2.txt' ,skiprows=2)
Si5002 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si50031_elist2.txt' ,skiprows=2)

CdTe3 = np.loadtxt('DPE_carlos_data_output/new_clusterer/CdTe31_elist3.txt' ,skiprows=2)
GaAs3 = np.loadtxt('DPE_carlos_data_output/new_clusterer/GaAs31_elist3.txt' ,skiprows=2)
Si1003 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si10031_elist3.txt' ,skiprows=2)
Si3003 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si30031_elist3.txt' ,skiprows=2)
Si5003 = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si50031_elist3.txt' ,skiprows=2)

plt.close()
plt.clf()
plt.cla()
plt.hist(CdTe1[:,26], bins=2048, histtype = 'step', label=label_det[0]+str("method 1"), linewidth=lin_wd)
plt.hist(CdTe2[:,26], bins=2048, histtype = 'step', label=label_det[0]+str("method 2"), linewidth=lin_wd)
plt.hist(CdTe3[:,26], bins=2048, histtype = 'step', label=label_det[0]+str("method 3"), linewidth=lin_wd)
#plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
#plt.ylim(bottom=1, top=ymax_let[j])
plt.xlim(left=1E-1, right=1E2) #left=1E2
plt.ylim(bottom=1, top=1E5)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_LET_corrected/CdTe_2000um_LET_method_' +str(1)+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(GaAs1[:,26], bins=2048, histtype = 'step', label=label_det[1]+str(" method 1"), linewidth=lin_wd)
plt.hist(GaAs2[:,26], bins=2048, histtype = 'step', label=label_det[1]+str(" method 2"), linewidth=lin_wd)
plt.hist(GaAs3[:,26], bins=2048, histtype = 'step', label=label_det[1]+str(" method 3"), linewidth=lin_wd)
#plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
#plt.ylim(bottom=1, top=ymax_let[j])
plt.xlim(left=1E-1, right=1E2) #left=1E2
plt.ylim(bottom=1, top=1E5)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_LET_corrected/GaAs_500um_LET_method_' +str(1)+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(Si1001[:,26], bins=2048, histtype = 'step', label=label_det[2]+str(" method 1"), linewidth=lin_wd)
plt.hist(Si1002[:,26], bins=2048, histtype = 'step', label=label_det[2]+str(" method 2"), linewidth=lin_wd)
plt.hist(Si1003[:,26], bins=2048, histtype = 'step', label=label_det[2]+str(" method 3"), linewidth=lin_wd)
#plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
#plt.ylim(bottom=1, top=ymax_let[j])
plt.xlim(left=1E-1, right=1E2) #left=1E2
plt.ylim(bottom=1, top=1E5)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_LET_corrected/Si_100um_LET_method_' +str(1)+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(Si3001[:,26], bins=2048, histtype = 'step', label=label_det[3]+str(" method 1"), linewidth=lin_wd)
plt.hist(Si3002[:,26], bins=2048, histtype = 'step', label=label_det[3]+str(" method 2"), linewidth=lin_wd)
plt.hist(Si3003[:,26], bins=2048, histtype = 'step', label=label_det[3]+str(" method 3"), linewidth=lin_wd)
#plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
#plt.ylim(bottom=1, top=ymax_let[j])
plt.xlim(left=1E-1, right=1E2) #left=1E2
plt.ylim(bottom=1, top=1E5)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_LET_corrected/Si_300um_LET_method_' +str(1)+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.hist(Si5001[:,26], bins=2048, histtype = 'step', label=label_det[4]+str(" method 1"), linewidth=lin_wd)
plt.hist(Si5002[:,26], bins=2048, histtype = 'step', label=label_det[4]+str(" method 2"), linewidth=lin_wd)
plt.hist(Si5003[:,26], bins=2048, histtype = 'step', label=label_det[4]+str(" method 3"), linewidth=lin_wd)
#plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
#plt.ylim(bottom=1, top=ymax_let[j])
plt.xlim(left=1E-1, right=1E2) #left=1E2
plt.ylim(bottom=1, top=1E5)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_LET_corrected/Si_500um_LET_method_' +str(1)+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""

"""
# Corrected Length2D and therefore LET - NOW FILTERED
ndet = 2

#data = np.loadtxt('DPE_carlos_data_output/new_clusterer/CdTe31_elist1.txt' ,skiprows=2)
#data = np.loadtxt('DPE_carlos_data_output/new_clusterer/GaAs31_elist1.txt' ,skiprows=2)
data = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si10031_elist1.txt' ,skiprows=2)
#data = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si30031_elist1.txt' ,skiprows=2)
#data = np.loadtxt('DPE_carlos_data_output/new_clusterer/Si50031_elist1.txt' ,skiprows=2)

data_filtered = np.empty([len(data[:,0]),2])

emin31 = np.array([2E4, 2E3, 175, 1E3, 2E3]) #275
emax31 = np.array([4E4, 3E4, 1E3, 4E3, 4E3]) #1E3
sizemin31 = np.array([300, 20, 5, 25, 45]) #5
sizemax31 = np.array([700, 50, 45, 100, 70]) #45
heightmin31 = np.array([370, 300, 50, 100, 150]) #50
heightmax31 = np.array([700, 600, 450, 500, 500]) #450
linearitymin31 = np.array([0.8, 0.8, 0.6, 0.75, 0.8]) #0.65
linearitymax31 = np.array([0.95, 0.9, 0.95, 0.9, 0.9]) #0.95
len2Dmin31 = np.array([50, 8, 1, 8, 11]) #2
len2Dmax31 = np.array([60, 12, 8, 15, 15]) #8

e_min = emin31[ndet]
e_max = emax31[ndet]
size_min = sizemin31[ndet]
size_max = sizemax31[ndet]
height_min = heightmin31[ndet]
height_max = heightmax31[ndet]
linearity_min = linearitymin31[ndet]
linearity_max = linearitymax31[ndet]
len2D_min = len2Dmin31[ndet]
len2D_max = len2Dmax31[ndet]
xmin = 10
xmax = 255
ymin = 55
ymax = 255

for i in range(len(data[:,0])):
    if data[i,4] >= e_min and data[i,4] < e_max and data[i,12] >= linearity_min and data[i,12] < linearity_max and data[i,7] >= size_min and data[i,7] < size_max and data[i,8] >= height_min and data[i,8] < height_max and data[i,2] > xmin and data[i,2] < xmax and data[i,3] > ymin and data[i,3] < ymax and data[i,13] >= len2D_min and data[i,13] < len2D_max:    # 8 height, 4 energy, 7 size, 12 linearity
    #if data[i,4] >= e_min and data[i,4] < e_max:    # 8 height, 4 energy, 7 size, 12 linearity
        print("gut")
        data_filtered[i,0] = data[i,4]
        data_filtered[i,1] = data[i,26]
    else:
        #print("nicht gut")
        pass

plt.close()
plt.clf()
plt.cla()
a = plt.hist(data_filtered[:,0], bins=512, histtype = 'step', label=label_det[ndet], linewidth=lin_wd); ys = a[0]; xs = a[1]
plt.xlim(left=1E2, right=1E5) #left=1E3
plt.ylim(bottom=1, top=1.5E3)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(label_det[ndet]+' deposited energy distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_LET_corrected/filtered_Energy_'+det_name[ndet]+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt('iworid_LET_corrected/filtered_Energy_hist_'+det_name[ndet]+'.txt', np.c_[xs[1:],ys])

plt.close()
plt.clf()
plt.cla()
d = plt.hist(data_filtered[:,1], bins=512, histtype = 'step', label=label_det[ndet], linewidth=lin_wd); ys = d[0]; xs = d[1]
plt.xlim(left=0.01, right=150) #left=1E-1
plt.ylim(bottom=1, top=1.5E3)
#plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(label_det[ndet]+'Filtered Linear energy transfer distribution, '+str(label_energy[1])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_LET_corrected/filtered_LET_'+det_name[ndet]+'.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt('iworid_LET_corrected/filtered_LET_hist_'+det_name[ndet]+'.txt', np.c_[xs[1:],ys])
"""

"""
# Loaded Histograms Corrected Length2D and therefore LET filtere
CdTe_energy = np.loadtxt('iworid_LET_corrected/filtered_Energy_hist_CdTe_2000um.txt')
GaAs_energy = np.loadtxt('iworid_LET_corrected/filtered_Energy_hist_GaAs_500um.txt')
Si100_energy = np.loadtxt('iworid_LET_corrected/filtered_Energy_hist_Si_100um.txt')
Si300_energy = np.loadtxt('iworid_LET_corrected/filtered_Energy_hist_Si_300um.txt')
Si500_energy = np.loadtxt('iworid_LET_corrected/filtered_Energy_hist_Si_500um.txt')

CdTe_LET = np.loadtxt('iworid_LET_corrected/filtered_LET_hist_CdTe_2000um.txt')
GaAs_LET = np.loadtxt('iworid_LET_corrected/filtered_LET_hist_GaAs_500um.txt')
Si100_LET = np.loadtxt('iworid_LET_corrected/filtered_LET_hist_Si_100um.txt')
Si300_LET = np.loadtxt('iworid_LET_corrected/filtered_LET_hist_Si_300um.txt')
Si500_LET = np.loadtxt('iworid_LET_corrected/filtered_LET_hist_Si_500um.txt')

CdTe_energy[0,1] = 0
GaAs_energy[0,1] = 0
Si100_energy[0,1] = 0
Si300_energy[0,1] = 0
Si500_energy[0,1] = 0

CdTe_LET[0,1] = 0
GaAs_LET[0,1] = 0
Si100_LET[0,1] = 0
Si300_LET[0,1] = 0
Si500_LET[0,1] = 0

plt.close()
plt.clf()
plt.cla()
plt.plot(CdTe_energy[:,0], CdTe_energy[:,1], GaAs_energy[:,0], GaAs_energy[:,1], Si100_energy[:,0], Si100_energy[:,1], Si300_energy[:,0], Si300_energy[:,1], Si500_energy[:,0], Si500_energy[:,1])
plt.xlim(left=1E2, right=1E5)
plt.ylim(bottom=1, top=1.5E3)
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.title('Filtered energy distribution, 31 MeV protons, 50$^{\circ}$ angle', fontsize=tickfnt)
plt.legend(['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m'], loc='upper right')
plt.xscale('log')
plt.yscale('log')
plt.tick_params(labelsize=tickfnt)
plt.tick_params(labelsize=tickfnt)
plt.savefig('iworid_LET_corrected/Filtered_Energy_31MeV.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.plot(CdTe_LET[:,0], CdTe_LET[:,1], GaAs_LET[:,0], GaAs_LET[:,1], Si100_LET[:,0], Si100_LET[:,1], Si300_LET[:,0], Si300_LET[:,1], Si500_LET[:,0], Si500_LET[:,1])
plt.xlim(left=0, right=15)
plt.ylim(bottom=1, top=1.5E3)
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.title('Filtered LET distribution, 31 MeV protons, 50$^{\circ}$ angle', fontsize=tickfnt)
plt.legend(['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m'], loc='upper right')
#plt.xscale('log')
plt.yscale('log')
plt.tick_params(labelsize=tickfnt)
plt.tick_params(labelsize=tickfnt)
plt.savefig('iworid_LET_corrected/Filtered_LET_31MeV.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""





"""
f1 = open('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/time_plot/CdTe_22_SamplingList.json')
f2 = open('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/time_plot/GaAs_22_SamplingList.json')
f3 = open('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/time_plot/Si100_22_SamplingList.json')
f4 = open('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/time_plot/Si300_22_SamplingList.json')
f5 = open('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/time_plot/Si500_22_SamplingList.json')
dataCdTe = json.load(f1)
dataGaAs = json.load(f2)
dataSi100 = json.load(f3)
dataSi300 = json.load(f4)
dataSi500 = json.load(f5)

xpoints = np.linspace(1,len(dataGaAs['T_Sampling']), len(dataGaAs['T_Sampling']))
fluxCdTe = dataCdTe['Flux_Class_1']
fluxGaAs = dataGaAs['Flux_Class_1']
fluxSi100 = dataSi100['Flux_Class_1']
fluxSi300 = dataSi300['Flux_Class_1']
fluxSi500 = dataSi500['Flux_Class_1']

doseCdTe = dataCdTe['DoseRate_Class_1']
doseGaAs = dataGaAs['DoseRate_Class_1']
doseSi100 = dataSi100['DoseRate_Class_1']
doseSi300 = dataSi300['DoseRate_Class_1']
doseSi500 = dataSi500['DoseRate_Class_1']

plt.close()
plt.clf()
plt.cla()
#plt.plot(xpoints, count_par, marker="o", markerfacecolor='#1f77b4', markeredgecolor='#1f77b4', markersize = 5.0, linewidth=1, linestyle='solid', color='black')
plt.plot(xpoints, fluxCdTe, xpoints, fluxGaAs, xpoints, fluxSi100, xpoints, fluxSi300, xpoints, fluxSi500, marker="o", markersize = 5.0, linewidth=1)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
plt.xlim(left=0, right=31)
plt.ylim(bottom=0, top=4E2)
plt.ylabel('Flux [cm${}^{2}$ s${}^{-1}$]', fontsize=tickfnt)
plt.xlabel('Time [s]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.legend(labels=['CdTe 2000 $\mu$m','GaAs 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m'] ,loc='upper right')
plt.title('Total flux of 22 MeV protons')
plt.savefig('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Flux_22.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.plot(xpoints, doseCdTe, xpoints, doseGaAs, xpoints, doseSi100, xpoints, doseSi300, xpoints, doseSi500, marker="o", markersize = 5.0, linewidth=1)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
plt.xlim(left=0, right=31)
plt.ylim(bottom=0, top=6E3)
plt.ylabel('Dose rate [$\mu$Gy/h]', fontsize=tickfnt)
plt.xlabel('Time [s]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.legend(['CdTe 2000 $\mu$m', 'GaAs 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m'] ,loc='upper right')
plt.title('Total dose rate of 22 MeV protons')
plt.savefig('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Dose_rate_22.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""

"""
# 4 segment matrix made of 4 detectors

CdTe22 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/CdTe_2000um_22_MeV_E_clog_particles_7000.txt')
GaAs22 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/GaAs_500um_22_MeV_E_clog_particles_7000.txt')
Si10022 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/Si_100um_22_MeV_E_clog_particles_7000.txt')
Si50022 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/Si_500um_22_MeV_E_clog_particles_7000.txt')

CdTe31 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/CdTe_2000um_31_MeV_E_clog_particles_7000.txt')
GaAs31 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/GaAs_500um_31_MeV_E_clog_particles_7000.txt')
Si10031 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/Si_100um_31_MeV_E_clog_particles_7000.txt')
Si50031 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/clog/Si_500um_31_MeV_E_clog_particles_7000.txt')

matrix22 = np.zeros([256,256])
matrix31 = np.zeros([256,256])

matrix22[0:128,128:256] = CdTe22[64:192,64:192]
matrix22[128:256,128:256] = GaAs22[64:192,64:192]
matrix22[0:128,0:128] = Si10022[64:192,64:192]
matrix22[128:256,0:128] = Si50022[64:192,64:192]

matrix31[0:128,128:256] = CdTe31[64:192,64:192]
matrix31[128:256,128:256] = GaAs31[64:192,64:192]
matrix31[0:128,0:128] = Si10031[64:192,64:192]
matrix31[128:256,0:128] = Si50031[64:192,64:192]

print_fig_E(matrix22, 1E5, '22 MeV, 50$^{\circ}$ angle','C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/', '4_detector_clog_22MeV')
print_fig_E(matrix31, 1E5, '31 MeV, 50$^{\circ}$ angle','C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/', '4_detector_clog_31MeV')
"""

"""
# Load filtered Energy and LET histograms

CdTe = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/CdTe_2000um_energy_filtered_hist_data.txt')
GaAs = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/GaAs_500um_energy_filtered_hist_data.txt')
Si100 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_100um_energy_filtered_hist_data.txt')
Si300 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_300um_energy_filtered_hist_data.txt')
Si500 = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_500um_energy_filtered_hist_data.txt')

CdTe[0,1] = 0
GaAs[0,1] = 0
Si100[0,1] = 0
Si300[0,1] = 0
Si500[0,1] = 0

np.savetxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/CdTe_2000um_energy_filtered_hist_data.txt', CdTe)
np.savetxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/GaAs_500um_energy_filtered_hist_data.txt', GaAs)
np.savetxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_100um_energy_filtered_hist_data.txt', Si100)
np.savetxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_300um_energy_filtered_hist_data.txt', Si300)
np.savetxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_500um_energy_filtered_hist_data.txt', Si500)

plt.close()
plt.clf()
plt.cla()
plt.plot(CdTe[:,0], CdTe[:,1], GaAs[:,0], GaAs[:,1], Si100[:,0], Si100[:,1], Si300[:,0], Si300[:,1], Si500[:,0], Si500[:,1])
plt.xlim(left=1E2, right=1E5)
plt.ylim(bottom=1, top=1E4)
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.title('Filtered energy distribution, 31 MeV protons, 50$^{\circ}$ angle', fontsize=tickfnt)
plt.legend(['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m'], loc='upper right')
plt.xscale('log')
plt.yscale('log')
plt.tick_params(labelsize=tickfnt)
plt.tick_params(labelsize=tickfnt)
plt.savefig('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Filtered_Energy_31MeV.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

CdTeLET = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/CdTe_2000um_LET_filtered_hist_data.txt')
GaAsLET = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/GaAs_500um_LET_filtered_hist_data.txt')
Si100LET = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_100um_LET_filtered_hist_data.txt')
Si300LET = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_300um_LET_filtered_hist_data.txt')
Si500LET = np.loadtxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/filtered/31MeV/Si_500um_LET_filtered_hist_data.txt')

CdTeLET[0,1] = 0
GaAsLET[0,1] = 0
Si100LET[0,1] = 0
Si300LET[0,1] = 0
Si500LET[0,1] = 0

plt.close()
plt.clf()
plt.cla()
plt.plot(CdTeLET[:,0], CdTeLET[:,1], GaAsLET[:,0], GaAsLET[:,1], Si100LET[:,0], Si100LET[:,1], Si300LET[:,0], Si300LET[:,1], Si500LET[:,0], Si500LET[:,1])
plt.xlim(left=0, right=20)
plt.ylim(bottom=1, top=1E4)
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.title('Filtered LET distribution, 31 MeV protons, 50$^{\circ}$ angle', fontsize=tickfnt)
plt.legend(['CdTe 2000 $\mu$m','GaAs:Cr 500 $\mu$m', 'Si 100 $\mu$m', 'Si 300 $\mu$m', 'Si 500 $\mu$m'], loc='upper right')
#plt.xscale('log')
plt.yscale('log')
plt.tick_params(labelsize=tickfnt)
plt.tick_params(labelsize=tickfnt)
plt.savefig('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Filtered_LET_31MeV.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)


# Si 300um Energy and LET plot

np.savetxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Si_300um_energy_forLandau.txt', Si300[:,:])
np.savetxt('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Si_300um_LET_forLandau.txt', Si300LET[:,:])

plt.close()
plt.clf()
plt.cla()
plt.plot(Si300[:,0], Si300[:,1])
plt.xlim(left=1E2, right=1E5)
plt.ylim(bottom=1, top=1E4)
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.legend(['Si 300 $\mu$m'], loc='upper right')
plt.title('Filtered energy distribution, 31 MeV protons, 50$^{\circ}$ angle', fontsize=tickfnt)
plt.xscale('log')
plt.yscale('log')
plt.tick_params(labelsize=tickfnt)
plt.tick_params(labelsize=tickfnt)
plt.savefig('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Filtered_Si300_31MeV_energy.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

plt.close()
plt.clf()
plt.cla()
plt.plot(Si300LET[:,0], Si300LET[:,1])
plt.xlim(left=0, right=10)
plt.ylim(bottom=1, top=1E4)
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.legend(['Si 300 $\mu$m'], loc='upper right')
plt.title('Filtered LET distribution, 31 MeV protons, 50$^{\circ}$ angle', fontsize=tickfnt)
#plt.xscale('log')
plt.yscale('log')
plt.tick_params(labelsize=tickfnt)
plt.tick_params(labelsize=tickfnt)
plt.savefig('C:/Users/andrej/Documents/FEI/2022_IWORID_prispevok/figures/Filtered_Si300_31MeV_LET.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""

"""
#1D histogram related part
pathCdTe = []
pathGaAs = []
pathSi100 = []
pathSi300 = []
pathSi500 = []

ymax_linearity = np.array([1E5, 1E5, 1E5, 1E5])
ymax_energy = np.array([1E5, 1E5, 1E5, 1E5])
ymax_size = np.array([1E5, 1E5, 1E5, 1E5])
ymax_height = np.array([1E5, 1E5, 1E5, 1E5])
ymax_let = np.array([1E5, 1E5, 1E5, 1E5])

xmax_linearity = np.array([1, 1, 1, 1])
xmax_energy = np.array([1E4, 1E5, 1E5, 1E5])
xmax_size = np.array([1E3, 1E3, 1E4, 1E4])
xmax_height = np.array([1E4, 1E4, 1E4, 1E4])
xmax_let = np.array([1E2, 1E3, 1E2, 1E2])

bin_linearity = np.array([[512, 64, 64, 64, 64], [512, 64, 64, 64, 64], [512, 128, 64, 64, 64], [512, 128, 64, 64, 64]])
bin_energy = np.array([[128, 128, 32, 32, 16], [128, 64, 32, 32, 32], [256, 512, 64, 64, 64], [256, 256, 128, 128, 128]])
bin_size = np.array([[128, 32, 32, 32, 32], [128, 64, 32, 32, 32], [256, 128, 32, 32, 32], [256, 128, 64, 64, 64]])
bin_height = np.array([[512, 1024, 256, 256, 256], [512, 1024, 256, 256, 256], [512, 1024, 256, 256, 256], [512, 1024, 256, 256, 256]])
bin_let = np.array([[128, 256, 128, 128, 128], [128, 256, 128, 128, 128], [128, 256, 128, 128, 128], [128, 256, 128, 128, 128]])

for j in range(len(e_name)):
    for k in range(len(rot_name)):
        print('all detectors', e_name[j], rot_name[k])
        pathCdTe = input_dir + det_name[0] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathGaAs = input_dir + det_name[1] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi100 = input_dir + det_name[2] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi300 = input_dir + det_name[3] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi500 = input_dir + det_name[4] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'

        CdTe = np.loadtxt(pathCdTe + 'ExtElist.txt', skiprows=2, delimiter=';')
        GaAs = np.loadtxt(pathGaAs + 'ExtElist.txt', skiprows=2, delimiter=';')
        Si100 = np.loadtxt(pathSi100 + 'ExtElist.txt', skiprows=2, delimiter=';')
        Si300 = np.loadtxt(pathSi300 + 'ExtElist.txt', skiprows=2, delimiter=';')
        Si500 = np.loadtxt(pathSi500 + 'ExtElist.txt', skiprows=2, delimiter=';')
        
        
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe[:,12], bins=bin_linearity[j, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,12], bins=bin_linearity[j, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,12], bins=bin_linearity[j, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,12], bins=bin_linearity[j, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,12], bins=bin_linearity[j, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=0, right=xmax_linearity[j])
        plt.ylim(bottom=1, top=ymax_linearity[j])
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
        #plt.hist(CdTe[:,4], bins=bin_energy[j, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        #plt.hist(GaAs[:,4], bins=bin_energy[j, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        #plt.hist(Si100[:,4], bins=bin_energy[j, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        #plt.hist(Si300[:,4], bins=bin_energy[j, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        #plt.hist(Si500[:,4], bins=bin_energy[j, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.hist(CdTe[:,4], bins=2048, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,4], bins=2048, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,4], bins=2048, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,4], bins=2048, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,4], bins=2048, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        #plt.xlim(left=1, right=xmax_energy[j]) #left=1E3
        #plt.ylim(bottom=1, top=ymax_energy[j])
        plt.xlim(left=30, right=1E5) #left=1E3
        plt.ylim(bottom=1, top=1E5)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Deposited energy distribution, '+str(label_energy[j+3])+' protons, ' + str(label_angle[5]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Energy.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
        plt.close()
        plt.clf()
        plt.cla()
        #plt.hist(CdTe[:,7], bins=bin_size[j, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        #plt.hist(GaAs[:,7], bins=bin_size[j, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        #plt.hist(Si100[:,7], bins=bin_size[j, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        #plt.hist(Si300[:,7], bins=bin_size[j, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        #plt.hist(Si500[:,7], bins=bin_size[j, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.hist(CdTe[:,7], bins=300, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,7], bins=128, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,7], bins=190, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,7], bins=210, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,7], bins=280, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        #plt.xlim(left=1, right=xmax_size[j]) #left=1E1
        #plt.ylim(bottom=1, top=ymax_size[j])
        plt.xlim(left=1, right=1E4) #left=1E1
        plt.ylim(bottom=1, top=1E5)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Size [px]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster size distribution, '+str(label_energy[j+3])+' protons, ' + str(label_angle[5]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Size.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
        
        plt.close()
        plt.clf()
        plt.cla()
        #plt.hist(CdTe[:,8], bins=bin_height[j, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        #plt.hist(GaAs[:,8], bins=bin_height[j, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        #plt.hist(Si100[:,8], bins=bin_height[j, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        #plt.hist(Si300[:,8], bins=bin_height[j, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        #plt.hist(Si500[:,8], bins=bin_height[j, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.hist(CdTe[:,8], bins=512, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs[:,8], bins=15000, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100[:,8], bins=128, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300[:,8], bins=128, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500[:,8], bins=128, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        #plt.xlim(left=1, right=xmax_height[j]) #left=1E1
        #plt.ylim(bottom=1, top=ymax_height[j])
        plt.xlim(left=30, right=1E5) #left=1E1
        plt.ylim(bottom=1, top=1E5)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Height [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Cluster height distribution, '+str(label_energy[j+3])+' protons, ' + str(label_angle[5]))
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
        #plt.hist(CdTe_LET, bins=bin_let[j, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        #plt.hist(GaAs_LET, bins=bin_let[j, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        #plt.hist(Si100_LET, bins=bin_let[j, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        #plt.hist(Si300_LET, bins=bin_let[j, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        #plt.hist(Si500_LET, bins=bin_let[j, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.hist(CdTe_LET, bins=1024, histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs_LET, bins=4096, histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100_LET, bins=256, histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300_LET, bins=256, histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500_LET, bins=256, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        #plt.xlim(left=1E-2, right=xmax_let[j]) #left=1E2
        #plt.ylim(bottom=1, top=ymax_let[j])
        plt.xlim(left=1E-1, right=1E2) #left=1E2
        plt.ylim(bottom=1, top=1E5)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Linear energy transfer distribution, '+str(label_energy[j+3])+' protons, ' + str(label_angle[5]))
        plt.legend(loc='upper right')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/LET.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""

"""
#1D filtered histogram related part

pathCdTe = []
pathGaAs = []
pathSi100 = []
pathSi300 = []
pathSi500 = []

e_name = ['22_MeV', '31_MeV']

ymax_linearity = np.array([1E5, 1E5, 1E5, 1E5])
ymax_energy = np.array([1E5, 1E5, 1E5, 1E5])
ymax_size = np.array([1E5, 1E5, 1E5, 1E5])
ymax_height = np.array([1E5, 1E5, 1E5, 1E5])
ymax_let = np.array([1E5, 1E5, 1E5, 1E5])

xmax_linearity = np.array([1, 1, 1, 1])
xmax_energy = np.array([1E4, 1E5, 1E5, 1E5])
xmax_size = np.array([1E3, 1E3, 1E4, 1E4])
xmax_height = np.array([1E4, 1E4, 1E4, 1E4])
xmax_let = np.array([1E2, 1E3, 1E2, 1E2])

bin_linearity = np.array([[512, 64, 64, 64, 64], [512, 64, 64, 64, 64], [512, 128, 64, 64, 64], [512, 128, 64, 64, 64]])
bin_energy = np.array([[128, 256, 32, 32, 16], [128, 128, 32, 32, 32], [256, 256, 32, 32, 32], [256, 256, 64, 64, 64]])
bin_size = np.array([[128, 32, 32, 32, 32], [128, 64, 32, 32, 32], [256, 128, 32, 32, 32], [256, 128, 64, 64, 64]])
bin_height = np.array([[512, 1024, 256, 256, 256], [512, 1024, 256, 256, 256], [512, 1024, 256, 256, 256], [512, 1024, 256, 256, 256]])
bin_let = np.array([[128, 256, 128, 128, 128], [128, 256, 128, 128, 128], [128, 256, 128, 128, 128], [128, 256, 128, 128, 128]])

for j in range(len(e_name)):
    for k in range(len(rot_name)):
        print(e_name[j], rot_name[k])
        pathCdTe = input_dir + det_name[0] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathGaAs = input_dir + det_name[1] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi100 = input_dir + det_name[2] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi300 = input_dir + det_name[3] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'
        pathSi500 = input_dir + det_name[4] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'

        CdTe = np.loadtxt(pathCdTe + 'ExtElist.txt', skiprows=2, delimiter=';')
        GaAs = np.loadtxt(pathGaAs + 'ExtElist.txt', skiprows=2, delimiter=';')
        Si100 = np.loadtxt(pathSi100 + 'ExtElist.txt', skiprows=2, delimiter=';')
        Si300 = np.loadtxt(pathSi300 + 'ExtElist.txt', skiprows=2, delimiter=';')
        Si500 = np.loadtxt(pathSi500 + 'ExtElist.txt', skiprows=2, delimiter=';')

        CdTe_filtered = np.empty([len(CdTe), 5])
        GaAs_filtered = np.empty([len(GaAs), 5])
        Si100_filtered = np.empty([len(Si100), 5])
        Si300_filtered = np.empty([len(Si300), 5])
        Si500_filtered = np.empty([len(Si500), 5])

        e_min = 350
        size_min = 10
        height_min = 31

        CdTe_LET = CdTe[:,4] / (np.sqrt((CdTe[:,13] * 55) ** 2 + 2000**2))
        GaAs_LET = GaAs[:,4] / (np.sqrt((GaAs[:,13] * 55) ** 2 + 500**2))
        Si100_LET = Si100[:,4] / (np.sqrt((Si100[:,13] * 55) ** 2 + 100**2))
        Si300_LET = Si300[:,4] / (np.sqrt((Si300[:,13] * 55) ** 2 + 300**2))
        Si500_LET = Si500[:,4] / (np.sqrt((Si500[:,13] * 55) ** 2 + 500**2))

        for i in range(len(CdTe[:,0])):
            if CdTe[i,4] >= e_min and CdTe[i,7] >= size_min:    # 8 height, 4 energy, 7 size, 12 linearity
                CdTe_filtered[i,0] = CdTe[i,12]
                CdTe_filtered[i,1] = CdTe[i,4]
                CdTe_filtered[i,2] = CdTe[i,7]
                CdTe_filtered[i,3] = CdTe[i,8]
                CdTe_filtered[i,4] = CdTe_LET[i]
        else:
            pass

        for i in range(len(GaAs[:,0])):
            if GaAs[i,4] >= e_min and GaAs[i,7] >= size_min:    # 8 height, 4 energy, 7 size, 12 linearity
                GaAs_filtered[i,0] = GaAs[i,12]
                GaAs_filtered[i,1] = GaAs[i,4]
                GaAs_filtered[i,2] = GaAs[i,7]
                GaAs_filtered[i,3] = GaAs[i,8]
                GaAs_filtered[i,4] = GaAs_LET[i]
        else:
            pass

        for i in range(len(Si100[:,0])):
            if Si100[i,4] >= e_min and Si100[i,7] >= size_min:    # 8 height, 4 energy, 7 size, 12 linearity
                Si100_filtered[i,0] = Si100[i,12]
                Si100_filtered[i,1] = Si100[i,4]
                Si100_filtered[i,2] = Si100[i,7]
                Si100_filtered[i,3] = Si100[i,8]
                Si100_filtered[i,4] = Si100_LET[i]
        else:
            pass
        
        for i in range(len(Si300[:,0])):
            if Si300[i,4] >= e_min and Si300[i,7] >= size_min:    # 8 height, 4 energy, 7 size, 12 linearity
                Si300_filtered[i,0] = Si300[i,12]
                Si300_filtered[i,1] = Si300[i,4]
                Si300_filtered[i,2] = Si300[i,7]
                Si300_filtered[i,3] = Si300[i,8]
                Si300_filtered[i,4] = Si300_LET[i]
        else:
            pass

        for i in range(len(Si500[:,0])):
            if Si500[i,4] >= e_min and Si500[i,7] >= size_min:    # 8 height, 4 energy, 7 size, 12 linearity
                Si500_filtered[i,0] = Si500[i,12]
                Si500_filtered[i,1] = Si500[i,4]
                Si500_filtered[i,2] = Si500[i,7]
                Si500_filtered[i,3] = Si500[i,8]
                Si500_filtered[i,4] = Si500_LET[i]
        else:
            pass

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe_filtered[:,0], bins=bin_linearity[j+2, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs_filtered[:,0], bins=bin_linearity[j+2, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100_filtered[:,0], bins=bin_linearity[j+2, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300_filtered[:,0], bins=bin_linearity[j+2, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500_filtered[:,0], bins=bin_linearity[j+2, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=0, right=xmax_linearity[j+2])
        plt.ylim(bottom=1, top=ymax_linearity[j+2])
        plt.yscale('log')
        plt.xlabel('Linearity [-]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Filtered Particle linearity distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        if not os.path.exists('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/'):
            os.makedirs('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/Linearity_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe_filtered[:,1], bins=bin_energy[j+2, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs_filtered[:,1], bins=bin_energy[j+2, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100_filtered[:,1], bins=bin_energy[j+2, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300_filtered[:,1], bins=bin_energy[j+2, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500_filtered[:,1], bins=bin_energy[j+2, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1, right=xmax_energy[j+2]) #left=1E3
        plt.ylim(bottom=1, top=ymax_energy[j+2])
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Filtered Deposited energy distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        if not os.path.exists('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/'):
            os.makedirs('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/Energy_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe_filtered[:,2], bins=bin_size[j+2, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs_filtered[:,2], bins=bin_size[j+2, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100_filtered[:,2], bins=bin_size[j+2, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300_filtered[:,2], bins=bin_size[j+2, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500_filtered[:,2], bins=bin_size[j+2, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1, right=xmax_size[j+2]) #left=1E1
        plt.ylim(bottom=1, top=ymax_size[j+2])
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Size [px]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Filtered Cluster size distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        if not os.path.exists('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/'):
            os.makedirs('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/Size_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe_filtered[:,3], bins=bin_height[j+2, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs_filtered[:,3], bins=bin_height[j+2, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100_filtered[:,3], bins=bin_height[j+2, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300_filtered[:,3], bins=bin_height[j+2, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500_filtered[:,3], bins=bin_height[j+2, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1, right=xmax_height[j+2]) #left=1E1
        plt.ylim(bottom=1, top=ymax_height[j+2])
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Height [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Filtered Cluster height distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        if not os.path.exists('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/'):
            os.makedirs('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/Height_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)

        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(CdTe_filtered[:,4], bins=bin_let[j+2, 0], histtype = 'step', label=label_det[0], linewidth=lin_wd)
        plt.hist(GaAs_filtered[:,4], bins=bin_let[j+2, 1], histtype = 'step', label=label_det[1], linewidth=lin_wd)
        plt.hist(Si100_filtered[:,4], bins=bin_let[j+2, 2], histtype = 'step', label=label_det[2], linewidth=lin_wd)
        plt.hist(Si300_filtered[:,4], bins=bin_let[j+2, 3], histtype = 'step', label=label_det[3], linewidth=lin_wd)
        plt.hist(Si500_filtered[:,4], bins=bin_let[j+2, 4], histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1E-2, right=xmax_let[j+2]) #left=1E-1
        plt.ylim(bottom=1, top=ymax_let[j+2])
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Filtered Linear energy transfer distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        if not os.path.exists('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/'):
            os.makedirs('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/LET_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""


"""
#1D 1 detector histogram print
#bin_energy = np.array([2048, 2048, 2048, 2048, 2048])

for j in range(len(e_name)):
    for k in range(len(rot_name)):
        print(e_name[j], rot_name[k])
        path = input_dir + det_name[4] + '//' + e_name[j] + '//' + rot_name[k] + '//Files//'

        data = np.loadtxt(path + 'ExtElist.txt', skiprows=2, delimiter=';')
        data_filtered = np.empty([len(data), 5])

        e_min = 2E3
        size_min = 10
        height_min = 10
        linearity_min = 0.5
        xmin = 0.5
        xmax = 14
        ymin = 0.5
        ymax = 14

        data_LET = data[:,4] / (np.sqrt((data[:,13] * 55) ** 2 + 500**2))

        for i in range(len(data[:,0])):
            if data[i,4] >= e_min and data[i,7] >= size_min and data[i,2]>xmin and data[i,2]<xmax and data[i,3]>ymin and data[i,3]<ymax:    # 8 height, 4 energy, 7 size, 12 linearity
                data_filtered[i,0] = data[i,12]
                data_filtered[i,1] = data[i,4]
                data_filtered[i,2] = data[i,7]
                data_filtered[i,3] = data[i,8]
                data_filtered[i,4] = data_LET[i]
        else:
            pass
        
        
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(data[:,4], bins=4096, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1, right=1E5) #left=1E3
        plt.ylim(bottom=1, top=1E4)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title(label_det[4]+'deposited energy distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        if not os.path.exists('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/'):
            os.makedirs('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Si500um_energy.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
        
        
        plt.close()
        plt.clf()
        plt.cla()
        plt.hist(data_filtered[:,1], bins=1024, histtype = 'step', label=label_det[4], linewidth=lin_wd)
        plt.xlim(left=1, right=1E5) #left=1E3
        plt.ylim(bottom=1, top=1E4)
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy [keV]', fontsize=tickfnt)
        plt.ylabel('Particles [cnt]', fontsize=tickfnt)
        plt.tick_params(axis='x', labelsize=tickfnt)
        plt.tick_params(axis='y', labelsize=tickfnt)
        plt.title('Filtered'+label_det[4]+'deposited energy distribution, '+str(label_energy[j])+' protons, ' + str(label_angle[k]))
        plt.legend(loc='upper right')
        if not os.path.exists('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/'):
            os.makedirs('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/')
        plt.savefig('iworid_figures/1D/'+str(e_name[j])+'/'+str(rot_name[k])+'/Filtered/Si500um_energy_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
"""       



#1D 1 detector histogram print
#bin_energy = np.array([2048, 2048, 2048, 2048, 2048])
#det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
"""
std_name22 = ['CdTe22MeV.txt', 'GaAs22MeV.txt', 'Si10022MeV.txt', 'Si30022MeV.txt', 'Si50022MeV.txt']
std_name31 = ['CdTe31MeV.txt', 'GaAs31MeV.txt', 'Si10031MeV.txt', 'Si30031MeV.txt', 'Si50031MeV.txt']

ne = 0
ndet = 4

print(det_name[ndet], e_name[ne], rot_name[0])
path = input_dir + det_name[ndet] + '//' + e_name[ne] + '//' + rot_name[0] + '//Files//'

data = np.loadtxt(path + 'ExtElist.txt', skiprows=2, delimiter=';')
data_filtered = np.empty([len(data), 6])

print(std_name31[ndet])

data_std = np.loadtxt('std_data_50angle/'+std_name22[ndet], skiprows=2, usecols=(16), delimiter=';')
print(data_std[0:10])

emin31 = np.array([2E4, 2E3, 275, 1E3, 2E3])
emax31 = np.array([4E4, 3E4, 1E3, 4E3, 4E3])
sizemin31 = np.array([300, 20, 5, 25, 45])
sizemax31 = np.array([700, 50, 45, 100, 70])
heightmin31 = np.array([370, 300, 50, 100, 150])
heightmax31 = np.array([700, 600, 450, 500, 500])
linearitymin31 = np.array([0.8, 0.8, 0.65, 0.75, 0.8])
linearitymax31 = np.array([0.95, 0.9, 0.95, 0.9, 0.9])
len2Dmin31 = np.array([50, 8, 2, 8, 11])
len2Dmax31 = np.array([60, 12, 8, 15, 15])

emin22 = np.array([1.5E4, 2E3, 275, 1E3, 2E3])
emax22 = np.array([4E4, 3E4, 1E3, 5E3, 8E3])
sizemin22 = np.array([200, 10, 4, 20, 40])
sizemax22 = np.array([600, 50, 60, 100, 200])
heightmin22 = np.array([200, 150, 25, 200, 200])
heightmax22 = np.array([700, 700, 450, 500, 500])
linearitymin22 = np.array([0.75, 0.77, 0.6, 0.7, 0.8])
linearitymax22 = np.array([0.95, 0.9, 0.95, 0.9, 0.9])
len2Dmin22 = np.array([30, 7, 1, 5, 10])
len2Dmax22 = np.array([60, 15, 8, 20, 30])

e_min = emin22[ndet]
e_max = emax22[ndet]
size_min = sizemin22[ndet]
size_max = sizemax22[ndet]
height_min = heightmin22[ndet]
height_max = heightmax22[ndet]
linearity_min = linearitymin22[ndet]
linearity_max = linearitymax22[ndet]
len2D_min = len2Dmin22[ndet]
len2D_max = len2Dmax22[ndet]
xmin = 0.55
xmax = 13.53
ymin = 0.55
ymax = 13.53

c = 2.5

data_LET = data[:,4] / (np.sqrt((data[:,13] * 55 - c * data_std[:] * 55) ** 2 + thickness[ndet] ** 2))

for i in range(len(data[:,0])):
    if data[i,4] >= e_min and data[i,4] < e_max and data[i,12] >= linearity_min and data[i,12] < linearity_max and data[i,7] >= size_min and data[i,7] < size_max and data[i,8] >= height_min and data[i,8] < height_max and data[i,2] > xmin and data[i,2] < xmax and data[i,3] > ymin and data[i,3] < ymax and data[i,13] >= len2D_min and data[i,13] < len2D_max:    # 8 height, 4 energy, 7 size, 12 linearity
        data_filtered[i,0] = data[i,12]
        data_filtered[i,1] = data[i,4]
        data_filtered[i,2] = data[i,7]
        data_filtered[i,3] = data[i,8]
        data_filtered[i,4] = data_LET[i]
        data_filtered[i,5] = data[i,5] * 1E-9
    else:
        pass
        
for i in range(len(data_filtered[:,1])):
    if data_filtered[i,1] < e_min and data_filtered[i,1]>0:
        data_filtered[i,1] = 0
        #print('wth')
    else:
        pass

# Sort time data into buckets
df = pd.DataFrame(data=data_filtered[:,5], columns=["data"])
bins = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])

df["bucket"] = pd.cut(df.data, bins)
print(df)
np.histogram(data_filtered[:,5], bins)
x, y = np.histogram(data, bins)

y_new = np.linspace(1,30,30)
#print(y_new)
#print(x,y)
plt.close()
plt.clf()
plt.cla()
plt.rcParams["figure.figsize"] = (11.7, 8.3)
plt.scatter(y_new, x)
plt.xlabel('Time [s]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.show()


plt.close()
plt.clf()
plt.cla()
a = plt.hist(data[:,4], bins=4096, histtype = 'step', label=label_det[ndet], linewidth=lin_wd); ys = a[0]; xs = a[1]
plt.xlim(left=1, right=1E5) #left=1E3
plt.ylim(bottom=1, top=1E4)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(label_det[ndet]+' deposited energy distribution, '+str(label_energy[ne])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
#if not os.path.exists('iworid_figures/1D/'+str(e_name[3])+'/'+str(rot_name[5])+'/'):
#    os.makedirs('iworid_figures/1D/'+str(e_name[3])+'/'+str(rot_name[5])+'/')
plt.savefig('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/'+det_name[ndet]+'_energy.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/'+det_name[ndet]+'_energy_hist_data.txt', np.c_[xs[1:],ys])
        
plt.close()
plt.clf()
plt.cla()
b = plt.hist(data_filtered[:,1], bins=512, histtype = 'step', label=label_det[ndet], linewidth=lin_wd); ys = b[0]; xs = b[1]
plt.xlim(left=1, right=2E3) #left=1E3
plt.ylim(bottom=1, top=1E4)
plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title('Filtered'+label_det[ndet]+' deposited energy distribution, '+str(label_energy[ne])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/Filtered/'+det_name[ndet]+'_energy_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/Filtered/'+det_name[ndet]+'_energy_filtered_hist_data.txt', np.c_[xs[1:],ys])

plt.close()
plt.clf()
plt.cla()
c = plt.hist(data_LET, bins=4096, histtype = 'step', label=label_det[ndet], linewidth=lin_wd); ys = c[0]; xs = c[1]
plt.xlim(left=1E-2, right=5) #left=1E2
plt.ylim(bottom=1, top=1E4)
#plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(label_det[ndet]+'Linear energy transfer distribution, '+str(label_energy[ne])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/'+det_name[ndet]+'_LET.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/'+det_name[ndet]+'_LET_hist_data.txt', np.c_[xs[1:],ys])

plt.close()
plt.clf()
plt.cla()
d = plt.hist(data_filtered[:,4], bins=512, histtype = 'step', label=label_det[ndet], linewidth=lin_wd); ys = d[0]; xs = d[1]
plt.xlim(left=1E-2, right=10) #left=1E-1
plt.ylim(bottom=1, top=1E4)
#plt.xscale('log')
plt.yscale('log')
plt.xlabel('LET [keV/$\mu$m]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(label_det[ndet]+'Filtered Linear energy transfer distribution, '+str(label_energy[ne])+' protons, ' + str(label_angle[5]))
plt.legend(loc='upper right')
plt.savefig('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/Filtered/'+det_name[ndet]+'_LET_filtered.png', dpi=mydpi, transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt('iworid_figures/1D/'+str(e_name[ne])+'/'+str(rot_name[0])+'/Filtered/'+det_name[ndet]+'_LET_filtered_hist_data.txt', np.c_[xs[1:],ys])
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
            #elist = np.loadtxt(path + 'ExtElist.txt', skiprows=2, delimiter=';')
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
            print(det_name[i], e_name[j], rot_name[k])
            clog = read_clog(path + 'ClusterLog.clog')[2]
            elist = np.loadtxt(path + 'ExtElist.txt', skiprows=2, delimiter=';')

            xlin = np.linspace(0, 14.08, 141) #141
            ylin = np.linspace(0, 14.08, 141)

            xlin2 = np.linspace(0, 255, 256)
            ylin2 = np.linspace(0, 255, 256)

            xelist2 = int(elist[:,2])
            yelist2 = int(elist[:,3])


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
                matrix_e[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] += eelist[iter]
                matrix_size[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] += sizeelist[iter]
                matrix_height[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] += heightelist[iter]
                matrix_length[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] += lengthelist[iter]
                matrix_length_3D[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] += length3Delist[iter]
                matrix_let[int(xelist[iter] * nasobok), int(yelist[iter] * nasobok)] += letelist[iter]

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
            #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
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
            #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
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
            #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
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
            #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
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
            #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_length_3D[::-1,:])), origin='lower', cmap='modified_hot')
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='3D Length [$\mu$m]', shrink=0.8, aspect=20*0.8).set_label(label='3D Length [$\mu$m]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(0,60000)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
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
            #plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
            # If the orientation of matrix doesnt fit, use this instead
            plt.matshow(np.flip(np.rot90(matrix_let[::-1,:])), origin='lower', cmap='modified_hot')
            plt.gca().xaxis.tick_bottom()
            plt.colorbar(label='LET [keV/$\mu$m]', shrink=0.8, aspect=20*0.8).set_label(label='LET [keV/$\mu$m]',size=tickfnt,weight='regular')   # format="%.1E"
            plt.clim(0,10)    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
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
            clog = read_clog(path,'ClusterLog.clog')[2]
            matrix = np.zeros([256,256])
            bad = 0
            good = 0
            other_good = 0
            num_of_particles = 7000

            #print(len(np.all(clog[:] > 0 and clog[:] < 1000), axis=0))

            for l in range(num_of_particles):   #range(len(clog[:]))
                x = []
                y = []
                for m in range(len(clog[l][:])):
                    if len(clog[l][:]) > 0 and len(clog[l][:]) < 1000:
                        good += 1
                        x.append(clog[l][m][0])
                        y.append(clog[l][m][1])
                        matrix[int(x[m]), int(y[m])] = matrix[int(x[m]), int(y[m])] + clog[l][m][2]
                    else:
                        bad += 1
                        pass
            
            print(det_name[i], e_name[j], rot_name[k], 'total ', len(clog[:]), ', good ', good, ', bad', bad, ', maybe true good, nope', other_good)

            clog_title = str(label_det[i]) + ', bias ' + str(voltage[i])
            OutputPath = 'iworid_figures/2D/clog/'+str(det_name[i])+'/'+str(e_name[j])+'/'+str(rot_name[k])+'/'
            OutputName = str(det_name[i]) + '_' + str(e_name[j]) + '_E_clog_particles_' + str(num_of_particles)

            print_fig_E(matrix, 1E6, clog_title, OutputPath, OutputName)
"""