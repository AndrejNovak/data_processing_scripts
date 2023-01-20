import re
import os
import os.path
import sys
import glob
import fnmatch
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
import json
from scipy.optimize import curve_fit
import pandas as pd

# matplotlib.use('Agg')   # To solve issue: Fail to create pixmap with Tk_GetPixmap

"""
Changing colormap to start at transparent zero
This code creates a new colormap called "modified_hot" by modifying the original "hot_r" colormap.
The colormap is created by using the "get_cmap()" function from matplotlib to retrieve the "hot_r" 
colormap and then applying it to a range of 256 colors. The last column of the color_array is then 
set to a range of values from 0 to 1 with a length of 256 using the numpy linspace function. 
The LinearSegmentedColormap.from_list method is used to create a new colormap object from the 
modified color array and then the new colormap is registered using the matplotlib's 
"register_cmap()" function so that it can be used later.
"""

ncolors = 256
color_array = plt.get_cmap('hot_r')(range(ncolors))
color_array[:, -1] = np.linspace(0.0, 1.0, ncolors)
map_object = LinearSegmentedColormap.from_list(
    name='modified_hot', colors=color_array)
plt.register_cmap(cmap=map_object)


class cluster_filter:
    """
    Lukas+Carlos, ADV, Prague, 8 Aug 2022
    Cluster_filter class is used to filter events in elist based on given criteria. The class takes 
    two inputs in its constructor, "edges" and "indeces". The "edges" is a list of border values for 
    a given cluster analysis (CA) parameter (PAR) and "indeces" is a list of column numbers in the 
    elist of the given cluster analysis parameter (CA PAR).

    The class has one method called "pass_filter" that takes a variable "cluster_var" as input. 
    The function iterates over the range of indeces, and for each index it defines a lower edge and
    an upper edge using the elements in the edges list. It also defines a variable "i_var" which is 
    the element of indeces list at the current index. The function then compares the "i_var"-th element
    of the cluster_var to the defined lower and upper edge and returns true if the element is within 
    the range, otherwise false.

    edges = border values for the given CA PAR
    indeces = COL in elist of the given CA PAR, e.g. 4 for Energy
    """

    def __init__(self, edges=[], indeces=[]):
        self.edges = edges
        self.indeces = indeces

    def pass_filter(self, cluster_var):
        for i in range(len(self.indeces)):
            down_edge = self.edges[i]
            up_edge = self.edges[i+1]
            i_var = self.indeces[i]

            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                return True
            else:
                return False


class cluster_filter_ONE_PAR:
    """
    Lukas + Carlos, ADV, Prague, 8 Aug 2022
    Cluster_filter_ONE_PAR is a class used to filter events in elist based on given criteria. The class takes
    two inputs in its constructor, "edges" and "indeces". The "edges" is a list of border values for a given 
    cluster analysis parameter (CA PAR) and "indeces" is a list of column numbers in the elist of the given CA PAR.

    The class has one method called "pass_filter" that takes a variable "cluster_var" as input. The function iterates
    over the range of indeces, and for each index it defines a lower edge and an upper edge using the elements in the 
    edges list. It also defines a variable i_var which is the element of indeces list at the current index. 
    The function then compares the i_var-th element of the cluster_var to the defined lower and upper edge and returns 
    true if the element is within the range, otherwise false. This class is similar to the first class "cluster_filter", 
    the only difference is the class name, the rest of the code is identical.

    edges = border values for the given CA PAR
    indeces = COL in elist of the given CA PAR, e.g. 4 for Energy
    """

    def __init__(self, edges=[], indeces=[]):
        self.edges = edges
        self.indeces = indeces

    def pass_filter(self, cluster_var):
        for i in range(len(self.indeces)):
            down_edge = self.edges[i]
            up_edge = self.edges[i+1]
            i_var = self.indeces[i]

            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                return True
            else:
                return False


class cluster_filter_MULTI_PAR:
    """
    Carlos modified, July 2022
    Cluster_filter_MULTI_PAR is a class used to filter events in elist based on multiple criteria. 
    The class takes two inputs in its constructor, "edges" and "indeces". "Edges" is a list of border 
    values for a given cluster analysis parameter (CA PAR) and "indeces" is a list of column numbers 
    in the elist of the given CA PAR.

    The class has one method called "pass_filter" that takes a variable "cluster_var" as input. 
    The function iterates over the range of indeces, and for each index it defines a lower edge and 
    an upper edge using the elements in the edges list. It also defines a variable i_var which is the element 
    of indeces list at the current index. The function then compares the i_var-th element of the cluster_var 
    to the defined lower and upper edge. If the element is within the range, the ok counter is incremented by 1, 
    if not the function returns false.

    At the end of the loop, if the ok counter is equal to the length of indeces, it means that all the criteria passed, 
    so the function returns True. This class is similar to the first two classes "cluster_filter" and 
    "cluster_filter_ONE_PAR" but it allows multiple criteria to be passed.

    edges = border values for the given CA PAR
    indeces = COL in elist of the given CA PAR, e.g. 4 for Energy
    """

    def __init__(self, edges=[], indeces=[]):
        self.edges = edges
        self.indeces = indeces

    def pass_filter(self, cluster_var):
        ok = 0

        for i in range(len(self.indeces)):
            down_edge = self.edges[i*2]
            up_edge = self.edges[(i*2)+1]
            i_var = self.indeces[i]

            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                ok = ok + 1
            else:
                return False
        if ok == len(self.indeces):
            return True


class cluster_filter_MULTI_PAR_RATIOS:
    """
    From Lukas' cluster_filter class; Carlos modified/extended, Aug 2022
    same as cluster_filter_MULTI_PAR with newly added RATIOS of CA PARs

    This class is similar to the "cluster_filter_MULTI_PAR_RATIOS" class, but with a more detailed description
    of the class and its methods. It is a class that is used to filter events in a list (elist) based on 
    multiple criteria including ratios of different parameters. The class takes four inputs in its constructor, 
    "edges", "indeces", "edges_ratio" and "ind_pair_ratio". "edges" is a list of border values for a given cluster 
    analysis parameter (CA PAR), "indeces" is a list of column numbers in the elist of the given CA PAR. 
    "edges_ratio" is a list of border values for the ratio(s) of pairs of CA PARs, and "ind_pair_ratio" is a list 
    of column numbers in the elist of pair of CA PAR for ratio(s).

    The class has one method called "pass_filter" that takes a variable "cluster_var" as input. The function first 
    iterates over the range of indeces and for each index it defines a lower edge and an upper edge using the elements 
    in the edges list. It also defines a variable i_var which is the element of indeces list at the current index. 
    The function then compares the i_var-th element of the cluster_var to the defined lower and upper edge. If the element 
    is within the range, the ok counter is incremented by 1, if not the function returns false.

    At the end of the loop, if the ok counter is equal to the length of indeces, it means that all the single CA PAR 
    criteria passed. The function then iterates over the range of the ind_pair_ratio, for each index, it defines 
    a lower edge and an upper edge for the ratio of the i_var-th element of the cluster_var to the defined lower 
    and upper edge. If the ratio is within the range, the ok_rat counter is incremented by 1, if not

    edges = border values for the given CA PAR
    indeces = COL number in elist of the given CA PAR, e.g. 4 for Energy
    ind_pair_ratio = COL number in elist of pair of CA PAR for ratio(s)    
    """

    def __init__(self, edges=[], indeces=[], edges_ratio=[], ind_pair_ratio=[]):
        self.edges = edges
        self.indeces = indeces

        self.edges_ratio = edges_ratio
        self.ind_pair_ratio = ind_pair_ratio

    def pass_filter(self, cluster_var):
        ok = 0
        ok_rat = 0

        for i in range(len(self.indeces)):
            down_edge = self.edges[i*2]
            up_edge = self.edges[(i*2)+1]
            i_var = self.indeces[i]

            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                ok = ok + 1
            else:
                return False

        if ok == len(self.indeces):
            num_rat_filters = int(len(self.ind_pair_ratio)/2)

            for k in range(num_rat_filters):
                down_edge_ratio = self.edges_ratio[k*2]
                up_edge_ratio = self.edges_ratio[(k*2)+1]
                k_var_ratio_top = self.ind_pair_ratio[k*2]
                k_var_ratio_bot = self.ind_pair_ratio[(k*2)+1]

                ratio_clu = (cluster_var[k_var_ratio_top] /
                             cluster_var[k_var_ratio_bot])
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


def read_clog(full_filename):
    """ 
    This function reads through the .clog file and can access Unix_time and Acquisition_time of every frame,
    number of frames, number of events in frame and their values [x, y, ToT, ToA].
    For printing Unix times of all frames use: read_clog(filename)[0]
    For printing Acquisition time of each frame use: read_clog(filename)[1]
    For printing full cluster data use: read_clog(filename)[2]

    When using 'data = read_clog(FileInPath, filename)[2]', you can traverse the data on level of Frames, 
    registered values (group of 4 values - [x, y, ToT, ToA]) and selected value from one of the 
    four possible - x or y or ToT or ToA.

    To access first layer (selected frame) use: data[0]
    To access second layer (selected 4-group of selected frame) use: data[0][0]
    To access third layer (selected value from selected 4-group of selected frame) use: data[0][0][0] 
    """

    inputFile = open(full_filename)
    lines = inputFile.readlines()
    current_cluster = list()
    all_values = list()
    frames_unix_time = list()
    frame_times = list()
    a = []
    pattern_b = r"\[[^][]*]"
    for line in lines:
        if line != "\n":
            if (line.split()[0] == "Frame"):
                unixtime = float(line.split()[2].lstrip("(").rstrip(","))
                frames_unix_time.append(unixtime)
                # print(unixtime)
                meas_time = float(line.split()[3].rstrip(","))
                frame_times.append(meas_time)
                # print(frametime)

                all_values.append(current_cluster)
                current_cluster = []
                continue
            a = (re.findall(pattern_b, line))
            for element in a:
                b = ("".join(element)).rstrip("]").lstrip("[").split(",")
                b = [float(x) for x in b]
                current_cluster.append(b)

    # to fix problem with first list being empty, needs solution without copying
    return frames_unix_time[:], frame_times[:], all_values[1:].copy()


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
    for idx, val in enumerate(names[0][:]):
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
    inputFile = open(filename, "r")
    lines = inputFile.readlines()
    inputFile.close()
    splitlines = []
    for line in lines:
        splitlines.append(list(line.rstrip().split(";")))
    return splitlines[0], splitlines[1], splitlines[2:]


def read_elist_make_ext_elist(filename, col_num_pairs_for_ratios, header_txt_new_cols, units_txt_new_cols):
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
    inputFile = open(filename, "r")
    lines = inputFile.readlines()
    # -- add new cols

    # --
    inputFile.close()
    splitlines = []

    # when there is filter entered:
    clu_cou_all = 0  # counter of all clusters
    # clu_cou_ok = 0 # counter of OK clu's
    # clu_cou_bad = 0 # counter of rejected clu's
    num_pairs_new_cols = int(len(col_num_pairs_for_ratios)/2)
    line_num = 0
    # if new_filter is not None:

    for line in lines:
        line_num += 1
        cluster_var = list(line.rstrip().split(";"))
        # for the first heading 2 rows
        if line_num < 3:
            if line_num == 1:
                print('first row = ', line_num)
                for k in range(num_pairs_new_cols):
                    cluster_var.append(header_txt_new_cols[k])
                splitlines.append(cluster_var)
            else:
                print('second row = ', line_num)
                for k in range(num_pairs_new_cols):
                    cluster_var.append(units_txt_new_cols[k])
                splitlines.append(cluster_var)
            # if line_num >= 3 and new_filter is not None:
            # print('ostatni radky',line_num)
        else:
            cluster_var = [float(i) for i in list(line.rstrip().split(";"))]
            # print(new_filter.pass_filter(cluster_var))
            clu_cou_all = clu_cou_all + 1
            for i in range(num_pairs_new_cols):
                # new_col_value = 10
                new_col_value = cluster_var[col_num_pairs_for_ratios[i*2]
                                            ]/cluster_var[col_num_pairs_for_ratios[(i*2)+1]]
                cluster_var.append(new_col_value)
                # --
            splitlines.append(cluster_var)
    print('all clusters thru = ', clu_cou_all)
    # print('OK clusters = ', clu_cou_ok)
    # print('bad clusters = ', clu_cou_bad)

    # the full elist with extended col output as single object
    return splitlines[0], splitlines[1], splitlines[2:]
    # the elist output split into three objects
    # return splitlines[0], splitlines[1], splitlines[2:]

    # else:
    # print('No new columns, nothing processed')
    # splitlines = inputFile


def read_elist_filter(filename, col_num_pairs_for_ratios, header_txt_new_cols, units_txt_new_cols, new_filter=None):
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

    inputFile = open(filename, "r")
    lines = inputFile.readlines()
    inputFile.close()
    splitlines = []

    line_num = 0
    # when there is filter entered:
    clu_cou_all = 0  # counter of all clusters
    clu_cou_ok = 0  # counter of OK clu's
    clu_cou_bad = 0  # counter of rejected clu's
    if new_filter is not None:

        for line in lines:
            line_num += 1
            cluster_var = list(line.rstrip().split(";"))
            # for the first heading 2 rows
            if line_num < 3:
                print('first two rows', line_num)
                cluster_var.append('Filter')
                splitlines.append(cluster_var)
            # for the rest
            else:
                # if line_num >= 3 and new_filter is not None:
                # print('ostatni radky',line_num)
                cluster_var = [float(i)
                               for i in list(line.rstrip().split(";"))]
                # print(new_filter.pass_filter(cluster_var))
                clu_cou_all = clu_cou_all + 1
                if new_filter.pass_filter(cluster_var):
                    # print('Filter ok ', end='') # removes enter
                    clu_cou_ok = clu_cou_ok + 1
                    cluster_var.append(1)
                else:
                    # print('False B ')
                    clu_cou_bad = clu_cou_bad + 1
                    # print('Filter bad ', end='')
                    cluster_var.append(0)
                    # print(cluster_var)
                # print(line_num)
                splitlines.append(cluster_var)
        print('all clusters = ', clu_cou_all)
        print('OK clusters = ', clu_cou_ok)
        print('bad clusters = ', clu_cou_bad)

        # the full elist with extended col output as single object
        return splitlines[0], splitlines[1], splitlines[2:]
        # the elist output split into three objects
        # return splitlines[0], splitlines[1], splitlines[2:]

    else:
        print('No filter, nothing processed')
        # splitlines = inputFile


def read_elist_make_ext_filter(filename, col_num_pairs_for_ratios, header_txt_new_cols, units_txt_new_cols, new_filter=None):
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
    inputFile = open(filename, "r")
    lines = inputFile.readlines()
    inputFile.close()
    splitlines = []

    num_pairs_new_cols = int(len(col_num_pairs_for_ratios)/2)
    line_num = 0
    # when there is filter entered:
    clu_cou_all = 0  # counter of all clusters
    clu_cou_ok = 0  # counter of OK clu's
    clu_cou_bad = 0  # counter of rejected clu's
    if new_filter is not None:

        for line in lines:
            line_num += 1
            cluster_var = list(line.rstrip().split(";"))
            # for the first heading 2 rows
            if line_num < 3:
                if line_num == 1:
                    print('first row = ', line_num)
                    # -- the new COLs of RATIOS of CA PARs
                    for k in range(num_pairs_new_cols):
                        cluster_var.append(header_txt_new_cols[k])
                    # -- the new COL of FILTER
                    cluster_var.append('Filter')
                    splitlines.append(cluster_var)
                else:
                    print('second row = ', line_num)
                    # -- the new COLs of RATIOS of CA PARs
                    for k in range(num_pairs_new_cols):
                        cluster_var.append(units_txt_new_cols[k])
                    # -- the new COL of FILTER
                    cluster_var.append('1 = ok')
                    splitlines.append(cluster_var)
                # if line_num >= 3 and new_filter is not None:
                # print('ostatni radky',line_num)
                print('first two rows done', line_num)
                # splitlines.append(cluster_var)
            # for the rest
            else:
                # if line_num >= 3 and new_filter is not None:
                # print('ostatni radky',line_num)
                cluster_var = [float(i)
                               for i in list(line.rstrip().split(";"))]
                # print(new_filter.pass_filter(cluster_var))
                clu_cou_all = clu_cou_all + 1
                # -- make and add the new COLs of RATIOS of CA PARs
                for i in range(num_pairs_new_cols):
                    # new_col_value = 10
                    new_col_value = round(
                        cluster_var[col_num_pairs_for_ratios[i*2]]/cluster_var[col_num_pairs_for_ratios[(i*2)+1]], 3)
                    cluster_var.append(new_col_value)
                    # --
                # -- apply make the filter
                if new_filter.pass_filter(cluster_var):
                    # print('Filter ok ', end='') # removes enter
                    clu_cou_ok = clu_cou_ok + 1
                    cluster_var.append(1)
                else:
                    # print('False B ')
                    clu_cou_bad = clu_cou_bad + 1
                    # print('Filter bad ', end='')
                    cluster_var.append(0)
                    # print(cluster_var)
                # print(line_num)
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
        # return splitlines[0], splitlines[1], splitlines[2:]

    else:
        print('No filter, nothing processed')
        # splitlines = inputFile


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


def create_matrix_filter_tpx3_t3pa(elist_filtered, clog, num_col_filter, num_frames):
    # def create_matrix_filter(elist_filtered,clog, num_frames, rand):
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

    # if rand == 'True':
    #    rand_nums = sorted(random.sample(range(0, len(clog[:])), len(num_frames)))
    # else:
    rand_nums = list(range(0, num_frames))       # list(range(0,num_frames))
    # the sq matrix for all clusters
    matrix_E_all = np.zeros([256, 256])
    # the sq matrix for the filter OK clusters
    matrix_ToA_all = np.zeros([256, 256])
    matrix_E_ok = np.zeros([256, 256])
    matrix_ToA_ok = np.zeros([256, 256])
    # the sq matrix for the filter REJECTED = BAD clusters
    matrix_E_bad = np.zeros([256, 256])
    matrix_ToA_bad = np.zeros([256, 256])
    # for cyclus cluster by cluster
    jump = 0
    f_jump = 0
    multiplet_num = 0  # to keep record of multiplet occurrence
    for idx, elist_row in enumerate(rand_nums):
        # for elist_row in enumerate(rand_nums):

        # counter for the drawing of clusters in clog
        # f_num = elist_row - multiplet_num
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
            # for j in len(clog[elist_row][:]):
            x = int(clog[f_num][j][0])
            y = int(clog[f_num][j][1])
            matrix_E_all[x, y] = matrix_E_all[x, y] + clog[f_num][j][2]
            matrix_ToA_all[x, y] = clog[f_num][j][3]

        # ----------------------------
        # for clusters with OK filter:
        # ----------------------------
        if elist_filtered[2][elist_row][num_col_filter] == 1:
            # print('sq matrix filter ok')
            # -- to take into account multiplets
            # these can be resolved in elist, but not in clog
            '''
            if elist_row < num_frames and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                jump = jump + 1 
                multiplet_num = multiplet_num + 1
            '''
            # for each cluster record in clog:
            # f_jump = jump
            # print('filter ok, jump = ',jump)
            for j in range(clu_A_clog):
                # for j in len(clog[elist_row][:]):

                # print(elist_row,j)
                # print(clog[elist_row][j])
                # print(elist_row,j,clog[elist_row][j][0],clog[elist_row][j][1])
                x = int(clog[f_num][j][0])
                y = int(clog[f_num][j][1])
                # x = clog[elist_row][j][0]
                # y = clog[elist_row][j][1]
                matrix_E_ok[x, y] = matrix_E_ok[x, y] + clog[f_num][j][2]
                matrix_ToA_ok[x, y] = clog[f_num][j][3]
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
                # jump = 0
                # print('sq matrix filter bad')
                # print('filter BAD, jump = ',jump)
                '''
                if elist_row < num_frames and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                    jump = jump + 1 
                    multiplet_num = multiplet_num + 1
                '''

                for j in range(clu_A_clog):
                    x = int(clog[f_num][j][0])
                    y = int(clog[f_num][j][1])
                    matrix_E_bad[x, y] = matrix_E_bad[x, y] + clog[f_num][j][2]
                    matrix_ToA_bad[x, y] = clog[f_num][j][3]

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


def create_matrix_filter_tpx_f(elist_filtered, clog, num_col_filter, num_particles):
    # def create_matrix_filter(elist_filtered,clog, num_frames, rand):
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
    # if rand == 'True':
    #    rand_nums = sorted(random.sample(range(0, len(clog[:])), len(num_frames)))
    # else:
    rand_nums = list(range(0, num_particles))       # list(range(0,num_frames))
    # the sq matrix for all clusters
    matrix_E_all = np.zeros([256, 256])
    # matrix_ToA_all = np.zeros([256,256])    # the sq matrix for the filter OK clusters
    matrix_E_ok = np.zeros([256, 256])
    # matrix_ToA_ok = np.zeros([256,256])
    # the sq matrix for the filter REJECTED = BAD clusters
    matrix_E_bad = np.zeros([256, 256])
    # matrix_ToA_bad = np.zeros([256,256])
    # int counters of clu's according filter
    c_all = 0
    c_ok = 0
    c_bad = 0
    # for cyclus cluster by cluster
    jump = 0
    # f_jump = 0
    # multiplet_num = 0 # to keep record of multiplet occurrence
    for idx, elist_row in enumerate(rand_nums):
        # for elist_row in enumerate(rand_nums):

        # counter for the drawing of clusters in clog
        # f_num = elist_row - multiplet_num
        f_num = elist_row
        # cluster area from clog
        clu_A_clog = len(clog[f_num][:])
        # cluster area from elist
        # clu_A_elist = elist_filtered[2][elist_row][7]

        # print('elist_row = ',elist_row,  ', f_num = ',f_num,', filter = ',elist_filtered[2][elist_row][15])
        # print(', clu_A_elist = ',clu_A_elist, ', clu_A_clog = ',clu_A_clog)
        c_all = c_all + 1

        # print('<< ALL clusters >>')
        # ----------------------------
        # for all clusters:
        # ----------------------------
        for j in range(clu_A_clog):
            # for j in len(clog[elist_row][:]):
            # print('all clu, clu px # = ',j)
            x = int(clog[f_num][j][0])
            y = int(clog[f_num][j][1])
            matrix_E_all[x, y] = matrix_E_all[x, y] + clog[f_num][j][2]
            # matrix_ToA_all[x,y] = clog[f_num][j][3]

        # ----------------------------
        # for clusters with OK filter:
        # ----------------------------
        if elist_filtered[2][elist_row][num_col_filter] == 1:
            # print('<< sq matrix filter ok >>')
            # -- to take into account multiplets
            # these can be resolved in elist, but not in clog
            '''
            if elist_row < num_particles and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                jump = jump + 1 
                multiplet_num = multiplet_num + 1
            '''
            # for each cluster record in clog:
            # f_jump = jump
            # print('filter ok, jump = ',jump)
            c_ok = c_ok + 1

            for j in range(clu_A_clog):
                # for j in len(clog[elist_row][:]):

                # print('OK clu, clu px # = ',j)
                # print(elist_row,j)
                # print(clog[elist_row][j])
                # print(elist_row,j,clog[elist_row][j][0],clog[elist_row][j][1])
                x = int(clog[f_num][j][0])
                y = int(clog[f_num][j][1])
                # x = clog[elist_row][j][0]
                # y = clog[elist_row][j][1]
                matrix_E_ok[x, y] = matrix_E_ok[x, y] + clog[f_num][j][2]
                # matrix_ToA_ok[x,y] = clog[f_num][j][3]
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
                # jump = 0
                # print('sq matrix filter bad')
                # print('filter BAD, jump = ',jump)
                c_bad = c_bad + 1
                '''
                if elist_row < num_particles and elist_filtered[2][elist_row][1] == elist_filtered[2][elist_row+1][1]:
                    jump = jump + 1 
                    multiplet_num = multiplet_num + 1
                '''

                for j in range(clu_A_clog):
                    # print('BAD clu, clu px # = ',j)
                    x = int(clog[f_num][j][0])
                    y = int(clog[f_num][j][1])
                    matrix_E_bad[x, y] = matrix_E_bad[x, y] + clog[f_num][j][2]
                    # matrix_ToA_bad[x,y] = clog[f_num][j][3]

    print('all clu = ', c_all)
    print('all ok = ', c_ok)
    print('all bad = ', c_bad)
    # --
    print('--- crea_matr_filt_tpx_f done ---')
    # return matrix_E_all, matrix_E_ok, matrix_E_bad
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

    tot = np.zeros([256, 256])
    for i in range(256):
        for j in range(256):
            if matrix[i, j] > 0.8:
                tot[i, j] = (a[i, j] * t[i, j] + matrix[i, j] + np.abs(np.sqrt((a[i, j] *
                             t[i, j] + b[i, j] - matrix[i, j])**2 + 4 * a[i, j] * c[i, j]))) / (2 * a[i, j])
            else:
                tot[i, j] = 0

    return tot


def print_fig_E(matrix, vmax, title, OutputPath, OutputName):

    # Changing colormap to start at transparent zero
    ncolors = 256

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
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(
        matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    cbar = plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='Energy [keV]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.clim(1, vmax)
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.savefig(OutputPath + OutputName + '.png', dpi=mydpi,
                transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '.txt', matrix)


def print_fig_ToA(matrix, vmax, title, OutputPath, OutputName):
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
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
    # If the orientation of matrix doesnt fit, use this instead
    # cmap='modified_hot' 'viridis'
    plt.matshow(np.flip(np.rot90(matrix[::-1, :])),
                origin='lower', cmap='viridis')
    plt.gca().xaxis.tick_bottom()
    cbar = plt.colorbar(label='ToA [ns]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='ToA [ns]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.clim(1, vmax)
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.savefig(OutputPath + OutputName + '.png', dpi=mydpi,
                transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '.txt', matrix)


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
        rand_nums = sorted(random.sample(
            range(0, len(data[:])), len(num_frames)))
    else:
        # list(range(0,num_frames))
        rand_nums = list(range(0, num_frames))

    matrix_E = np.zeros([256, 256])
    matrix_ToA = np.zeros([256, 256])

    for idx, val in enumerate(rand_nums):
        for j in range(len(data[val][:])):
            x = int(data[val][j][0])
            y = int(data[val][j][1])
            toa = []
            for i in range(len(data[val][:])):
                toa.append(data[val][i][3])

                matrix_E[x, y] = matrix_E[x, y] + data[val][j][2]
            else:
                pass
            if max(toa) != 0:
                matrix_ToA[x, y] = (data[val][j][3]) / max(toa)
            else:
                matrix_ToA[x, y] = data[val][j][3]

    return matrix_E, matrix_ToA


def plot_single_cluster_ToT(output_path, clog_path, frame_number):
    clog = read_clog(clog_path)[2]
    tickfnt = 14
    margin = 5
    matrix = np.zeros([256, 256])

    i = 0
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
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(
        matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.clim(1, 1E3)
    cbar = plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='Energy [keV]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label='ToT Cluster #'+str(frame_number), fontsize=tickfnt)
    plt.xlim([min(x)-diff_x/2-margin, max(x)+diff_x/2+margin])
    plt.ylim([min(y)-diff_y/2-margin, max(y)+diff_y/2+margin])
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.savefig(output_path + '/ToT_cluster_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(output_path + '/ToT_cluster_' +
               str(frame_number) + '.txt', matrix)


def plot_single_cluster_ToA(output_path, clog_path, frame_number):
    clog = read_clog(clog_path)[2]
    tickfnt = 14
    margin = 5
    matrix = np.zeros([256, 256])

    i = 0
    x = []
    y = []
    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    i = 0
    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] += clog[frame_number][i][3]

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
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1, :])),
                origin='lower', cmap='modified_hot')
    plt.gca().xaxis.tick_bottom()
    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.clim(0, None)
    cbar = plt.colorbar(label='ToA [ns]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='ToA [ns]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label='ToA Cluster #'+str(frame_number), fontsize=tickfnt)
    plt.xlim([min(x)-diff_x/2-margin, max(x)+diff_x/2+margin])
    plt.ylim([min(y)-diff_y/2-margin, max(y)+diff_y/2+margin])
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.savefig(output_path + '/ToA_cluster_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(output_path + '/ToA_cluster_' +
               str(frame_number) + '.txt', matrix)


def plot_single_cluster_ToA_gaas(output_path, clog_path, frame_number, indicator, vmax):
    clog = read_clog(clog_path)[2]
    tickfnt = 14
    margin = 5
    matrix = np.zeros([256, 256])

    i = 0
    x = []
    y = []
    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    i = 0
    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] += clog[frame_number][i][3]

    if indicator == True:
        i = 0
        x_add = []
        y_add = []
        for i in range(len(clog[frame_number+1][:])):
            x_add.append(clog[frame_number][i][0])
            y_add.append(clog[frame_number][i][1])

        i = 0
        for i in range(len(clog[frame_number+1][:])):
            matrix[int(x_add[i]), int(y_add[i])] += clog[frame_number+1][i][3]
    else:
        pass

    if (max(x)-min(x)) < (max(y)-min(y)):
        diff_x = np.abs((max(x)-min(x))-(max(y)-min(y)))
    else:
        diff_x = 0
    if (max(y)-min(y)) < (max(x)-min(x)):
        diff_y = np.abs((max(y)-min(y))-(max(x)-min(x)))
    else:
        diff_y = 0

    # cmap = matplotlib.cm.get_cmap('modified_hot', 5)

    plt.close()
    plt.cla()
    plt.clf()
    plt.subplot()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    # 'modified_hot'
    plt.matshow(np.flip(np.rot90(matrix[::-1, :])),
                origin='lower', cmap='modified_hot')
    plt.gca().xaxis.tick_bottom()
    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.clim(0, vmax)
    cbar = plt.colorbar(label='ToA [ns]', shrink=0.8, aspect=20*0.8)
    cbar.set_label(label='ToA [ns]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label='ToA Cluster #'+str(frame_number), fontsize=tickfnt)
    plt.xlim([min(x)-diff_x/2-margin, max(x)+diff_x/2+margin])
    plt.ylim([min(y)-diff_y/2-margin, max(y)+diff_y/2+margin])
    plt.xlabel('X position [px]', fontsize=tickfnt)
    plt.ylabel('Y position [px]', fontsize=tickfnt)
    plt.savefig(output_path + '/ToA_cluster_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(output_path + '/ToA_cluster_' +
               str(frame_number) + '.txt', matrix)


def gaas_core_halo_study(FileInPath, FileInName, FileOutPath, FileOutName, angle, max_toa_diff, num_of_frames):
    all_unix_times = read_clog(FileInPath + FileInName)[0]
    all_frame_times = read_clog(FileInPath + FileInName)[1]
    all_data = read_clog(FileInPath + FileInName)[2]

    maximum_ToA_frame_difference = max_toa_diff     # in nanoseconds 5000

    ToA_values = list()
    ToA_values_halo = list()

    for i in range(len(all_data[:]) - 1):
        matrix_ToA = np.zeros([256, 256])

        x_list_first = list()
        y_list_first = list()

        x_list_second = list()
        y_list_second = list()

        first_unix = all_unix_times[i]
        first_meas = all_frame_times[i]

        second_unix = all_unix_times[i+1]
        second_meas = all_frame_times[i+1]

        unix_diff = second_unix - first_unix

        for j in range(len(all_data[i][:])):
            x_first = int(all_data[i][j][0])
            y_first = int(all_data[i][j][1])

            x_list_first.append(x_first)
            y_list_first.append(y_first)

            matrix_ToA[x_first, y_first] = all_data[i][j][3]

            ToA_values.append(str(all_data[i][j][3]))

            indicator = False

        if unix_diff < maximum_ToA_frame_difference and len(all_data[i+1][:]) < 10:
            for j in range(len(all_data[i+1][:])):
                x_second = int(all_data[i+1][j][0])
                y_second = int(all_data[i+1][j][1])

                x_list_second.append(x_second)
                y_list_second.append(y_second)

                if (x_second) in x_list_first or (x_second) in x_list_first or (x_second - 1) in x_list_first or (x_second + 1) in x_list_first and (y_second - 1) in y_list_first or (y_second + 1) in y_list_first or (y_second) in y_list_first or (y_second) in y_list_first:
                    matrix_ToA[x_second, y_second] = all_data[i +
                                                              1][j][3] + unix_diff
                    ToA_values.append(str(all_data[i+1][j][3] + unix_diff))
                    ToA_values_halo.append(
                        str(all_data[i+1][j][3] + unix_diff))
                    indicator = True

        else:
            indicator = False

        if i <= num_of_frames:
            print_fig_ToA(matrix_ToA, 100, 'test ToA frame #' +
                          str(i), FileOutPath, FileOutName + '_frame_'+str(i))
            plot_single_cluster_ToA_gaas(
                FileOutPath, FileInPath+FileInName, i, indicator)
        else:
            pass

    file = open(FileOutPath + 'ToA_values.txt', 'w')
    for item in ToA_values:
        file.write(item+"\n")
    file.close()

    file = open(FileOutPath + 'ToA_values_halo.txt', 'w')
    for item in ToA_values_halo:
        file.write(item+"\n")
    file.close()

    hist_data = np.loadtxt(FileOutPath + 'ToA_values.txt')
    hist_data_halo = np.loadtxt(FileOutPath + 'ToA_values_halo.txt')

    title = 'ToA histogram 31 MeV protons, ' + str(angle) + 'degrees'

    plt.close()
    plt.clf()
    plt.cla()
    tickfnt = 14
    a = plt.hist(hist_data[:], bins=512, histtype='step',
                 label=title, linewidth=1.75)
    ys = a[0]
    xs = a[1]
    plt.xlim(left=1, right=1E4)  # left=1E3
    # plt.ylim(bottom=1, top=1E5)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('ToA [ns]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(title)
    # plt.title(label_det[i]+' deposited energy distribution, '+str(label_energy[n])+' protons')
    plt.legend(loc='upper right')
    plt.savefig(FileOutPath + 'histogram_ToA_values.png', dpi=300,
                transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(FileOutPath + 'histogram_ToA_values.txt', np.c_[xs[1:], ys])

    plt.close()
    plt.clf()
    plt.cla()
    tickfnt = 14
    a = plt.hist(hist_data_halo[:], bins=128,
                 histtype='step', label=title, linewidth=1.75)
    ys = a[0]
    xs = a[1]
    plt.xlim(left=1, right=1E4)  # left=1E3
    # plt.ylim(bottom=1, top=1E5)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('ToA [ns]', fontsize=tickfnt)
    plt.ylabel('Particles [cnt]', fontsize=tickfnt)
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(title)
    # plt.title(label_det[i]+' deposited energy distribution, '+str(label_energy[n])+' protons')
    plt.legend(loc='upper left')
    plt.savefig(FileOutPath + 'histogram_ToA_values_halo.png', dpi=300,
                transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(FileOutPath + 'histogram_ToA_values_halo.txt',
               np.c_[xs[1:], ys])

    return


def frame_matrix_tpx3(clog_path, filename, frame_number):
    """
    Carlos, from Andrej's script, 4 Aug 2022'
    input is the clog calib file of output of DPE_CP
    it reads the clog calib file, finds one f, and makes it
    (it draws it and stores it - calling the print_fig_E funkce)
    the output is stored in a new automatic DIR within the Files DIR of DPE_CP output
    for TPX3 data in ToT+ToA
    """
    clog = read_clog(filename)[2]
    matrix_tot = np.zeros([256, 256])  # tot
    matrix_toa = np.zeros([256, 256])  # toa

    for j in range(len(clog[frame_number][:])):
        x = int(clog[frame_number][j][0])  # x coord
        y = int(clog[frame_number][j][1])  # y coord
        matrix_tot[x, y] = matrix_tot[x, y] + clog[frame_number][j][2]  # tot
        matrix_toa[x, y] = matrix_toa[x, y] + clog[frame_number][j][3]  # toa

    return matrix_tot, matrix_toa


def frame_matrix_tpx(clog_path, filename, frame_number):
    """
    Carlos, from Andrej's script, 4 Aug 2022'
    same as frame_matrix_tpx3
    for TPX data in ToT
    """
    clog = read_clog(filename)[2]
    matrix_tot = np.zeros([256, 256])  # tot
    # matrix_toa = np.zeros([256,256]) # toa

    for j in range(len(clog[frame_number][:])):
        x = int(clog[frame_number][j][0])  # x coord
        y = int(clog[frame_number][j][1])  # y coord
        matrix_tot[x, y] = matrix_tot[x, y] + clog[frame_number][j][2]  # tot
        # matrix_toa[x,y] = matrix_toa[x,y] + clog[frame_number][j][3] # toa

    return matrix_tot


"""
FUNCTIONS TO IMPLEMENT

1) single particle tracks with margin of given number of pixels to form a square

2) single particle tracks with a given number of pixel size matrix

3) single particle tracks with histograms on top and right side of the track to indicate the energy deposited in each row and column

4) 3D

5) next to single particle tracks draw 1D cuts along line

6) frame printing with a given number of clusters and fixed colorbar, for this frame, add two histograms on top of it
    - these histograms contain selected parameter, for example Cluster Height and the second Deposited Energy.
    - each part of the image can be also saved individually

7) create frame with counting data - similiar to deposited energy graph

8) create frame with clusters that were registered within some time - Elist in nanoseconds

9) Add calculation of a 


"""
