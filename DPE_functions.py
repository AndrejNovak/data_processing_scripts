import re
import os
import os.path
import sys
import glob
import fnmatch
import itertools
import random
import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator
import json
from scipy.optimize import curve_fit
from scipy import stats
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import pandas as pd
from collections import Counter

from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
from skimage.util import invert


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


class Cluster_filter:
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

    def __init__(self, edges = [], indices = []):
        self.edges = edges
        self.indices = indices

    def pass_filter(self, cluster_var):
        for i in range(len(self.indices)):
            down_edge = self.edges[i]
            up_edge = self.edges[i + 1]
            i_var = self.indices[i]

            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                return True
            else:
                return False


class Cluster_filter_one_parameter:
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

    def __init__(self, edges = [], indices = []):
        self.edges = edges
        self.indices = indices

    def pass_filter(self, cluster_var):
        for i in range(len(self.indices)):
            down_edge = self.edges[i]
            up_edge = self.edges[i + 1]
            i_var = self.indices[i]

            if (cluster_var[i_var] >= down_edge and cluster_var[i_var] <= up_edge):
                return True
            else:
                return False


class Cluster_filter_multiple_parameter:
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

    At the end of the loop, if the ok counter is equal to the length of indeces, it means that all the criteria 
    passed, so the function returns True. This class is similar to the first two classes "cluster_filter" and 
    "cluster_filter_ONE_PAR" but it allows multiple criteria to be passed.

    edges = border values for the given CA PAR
    indeces = COL in elist of the given CA PAR, e.g. 4 for Energy
    """

    def __init__(self, edges = [], indices = []):
        self.edges = edges
        self.indices = indices

    def pass_filter(self, cluster_variable):
        ok = 0

        for i in range(len(self.indices)):
            down_edge = self.edges[i * 2]
            up_edge = self.edges[(i * 2) + 1]
            i_variables = self.indices[i]

            if (cluster_variable[i_variables] >= down_edge and cluster_variable[i_variables] <= up_edge):
                ok += 1
            else:
                return False

        if ok == len(self.indices):
            return True
        

class Cluster_filter_multiple_parameter_ratios:
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
    and upper edge. If the ratio is within the range, the ok_rat counter is incremented by 1, if not the function 
    returns false.

    edges = border values for the given CA PAR
    indeces = COL number in elist of the given CA PAR, e.g. 4 for Energy
    ind_pair_ratio = COL number in elist of pair of CA PAR for ratio(s)    
    """

    def __init__(self, edges = [], indices = [], edges_ratio = [], indices_pair_ratio = []):
        self.edges = edges
        self.indices = indices

        self.edges_ratio = edges_ratio
        self.indices_pair_ratio = indices_pair_ratio

    def pass_filter(self, cluster_variable):
        ok = 0
        ok_ratio = 0

        for i in range(len(self.indices)):
            down_edge = self.edges[i * 2]
            up_edge = self.edges[(i * 2) + 1]
            i_variable = self.indices[i]

            if (cluster_variable[i_variable] >= down_edge and cluster_variable[i_variable] <= up_edge):
                ok = ok + 1
            else:
                return False

        if ok == len(self.indices):
            number_ratio_filters = len(self.indices_pair_ratio) // 2

            for k in range(number_ratio_filters):
                down_edge_ratio = self.edges_ratio[k * 2]
                up_edge_ratio = self.edges_ratio[(k * 2) + 1]
                k_variable_ratio_top = self.indices_pair_ratio[k * 2]
                k_variable_ratio_bottom = self.indices_pair_ratio[(k * 2) + 1]

                ratio_cluster = (cluster_variable[k_variable_ratio_top] /
                             cluster_variable[k_variable_ratio_bottom])
                if (ratio_cluster >= down_edge_ratio and ratio_cluster <= up_edge_ratio):
                    ok_ratio = ok_ratio + 1
                else:
                    return False
            if ok_ratio == number_ratio_filters:
                return True


def get_subdirectory_names(path_into_folder):
    """
    This function takes the full path to the directory for which you want the list of its subdirectories.
    It is a single line of code but one can use this function rather than always think of a way how to do this. 

    Example:
    subdirectories = get_subdirectory_names('Q:/DPE_carlos_data_output/2022_12_VdG/2022_12_VdG_D05/')
    """
    return [ f.name for f in os.scandir(path_into_folder) if f.is_dir() ]


def get_number_of_files(path_into_folder, file_extension):
    """
    This function returns the number of specific files in a given folder.
    Use for determination of the number of all clog or t3pa files.

    Example:
    path = 'Q:/DPE_carlos_data_output/2022_12_VdG/2022_12_VdG_D05/00/Files/'
    clog_count = get_number_of_files(path, 'clog')[0]
    clog_names = get_number_of_files(path, 'clog')[1]
    """
    file_count = len(fnmatch.filter(os.listdir(path_into_folder), '*.' + file_extension))
    file_names = [ fnmatch.filter(os.listdir(path_into_folder), '*.' + file_extension) ]

    return file_count, file_names


def print_out_elist(FileOutPath, filename, input_data):
    """
    *** OLD FUNCTION, CURRENTLY NOT IN USE ***
    This is function that takes three inputs: FileOutPath, filename, and input_data. The function is used 
    to print output data in a classic Elist format.

    The function first checks if the FileOutPath directory exists, if it does not exist it creates the directory. 
    Then it opens a file with the specified filename in the FileOutPath directory and sets it as the standard output. 
    It then prints the input_data to the file and resets the standard output.
    """

    if not os.path.exists(FileOutPath):
        os.makedirs(FileOutPath)
    with open(FileOutPath + filename, 'w') as f:
        sys.stdout = f
        print(input_data)
        sys.stdout


def print_out_mask(FilePath, filename):
    """
    You insert matrix mask for a given detector and this function creates mask that
    can be used as a DPE input file mask.
    """
    mask = np.loadtxt(FilePath + filename)
    with open(FilePath + '\\DPE_mask_converted.txt', 'w') as f:
        for i, j in itertools.product(range(256), range(256)):
            if mask[i,j] == 0:
                f.write(f'[{str(j)},{str(i)}' + ']\n') 
       

def read_clog(filename):
    """ 
    *** WARNING *** Use this function only for printing figures of total deposited energy. This clog accesses
    the data on a frame level and therefore is not suited for use in filtration results printing. The problem
    in this case is that when one of the coincidence clusters in the frame passes the filter, the whole frame
    is then passed to create_matrix function and disrupts the consecutive visual filter validation and verification.
    This is a huge problem mainly in TPX2 data acquired at simultaneous ToT & ToA operation mode (every event
    that is detected inherits the ToA value of the first registered event in the frame).

    This function takes in the full filename of a .clog file as an input and is used to read through the file.
    The function opens the .clog file and reads all the lines of the file. It then uses a for loop to iterate 
    through each line in the file. The function looks for lines that begin with "Frame" and extracts the Unix 
    time and Acquisition time of each frame. These values are stored in lists called frames_unix_time and 
    frame_times, respectively. The function also looks for lines that contain a specific pattern (using regular 
    expressions) and extracts the x, y, ToT, and ToA values of each event in the frame. These values are stored 
    in a nested list called all_values. The function returns three values: a list of Unix times of all frames, 
    a list of Acquisition times of all frames, and a nested list of all the cluster data in the .clog file.
    You can access the Unix times of all frames by calling read_clog(filename)[0], the Acquisition times of all 
    frames by calling read_clog(filename)[1], and the full cluster data by calling read_clog(filename)[2].

    When using 'data = read_clog(FileInPath, filename)[2]', you can traverse the data on level of Frames, 
    registered values (group of 4 values - [x, y, ToT, ToA]) and selected value from one of the 
    four possible - x or y or ToT or ToA.
    To access first layer (selected frame) use: data[0]
    To access second layer (selected 4-group of selected frame) use: data[0][0]
    To access third layer (selected value from selected 4-group of selected frame) use: data[0][0][0] 
    """

    with open(filename) as inputFile:
        lines = inputFile.readlines()
    frame_unix_time = np.empty([0])
    frame_times = np.empty([0])

    current_cluster = []
    all_values = []

    a = []
    pattern_b = r"\[[^][]*]"

    for line in lines:
        if line != "\n":
            if (line.split()[0] == "Frame"):
                unixtime = float(line.split()[2].lstrip("(").rstrip(","))
                frame_unix_time = np.append(frame_unix_time, unixtime)
                measurement_time = float(line.split()[3].rstrip(","))
                frame_times = np.append(frame_times, measurement_time)

                all_values.append(current_cluster)
                current_cluster = []
                continue

            a = (re.findall(pattern_b, line))

            for element in a:
                b = ("".join(element)).rstrip("]").lstrip("[").split(",")
                b = [float(x) for x in b]
                current_cluster.append(b)

    # to fix problem with first list being empty, needs solution without copying for better performance
    return frame_unix_time, frame_times, all_values[1:].copy()


def read_clog_clusters(filename):
    """ 
    *** INFO *** If you want to access data on a frame level and print total deposited energy, 
    use read_clog() function. read_clog_testning function is designed for correlation with Elist
    and for correct printing of clusters that passed filtration parameters. Here, clusters are not
    divided into their respective frames but each individual cluster is separated.

    This function takes in the full filename of a .clog file as an input and is used to read through the file.
    The function opens the .clog file and reads all the lines of the file. It then uses a for loop to iterate 
    through each line in the file. The function looks for lines that begin with "Frame" and extracts the Unix 
    time and Acquisition time of each frame. These values are stored in lists called frames_unix_time and 
    frame_times, respectively. The function also looks for lines that contain a specific pattern (using regular 
    expressions) and extracts the x, y, ToT, and ToA values of each event in the frame. These values are stored 
    in a nested list called all_values. The function returns three values: a list of Unix times of all frames, 
    a list of Acquisition times of all frames, and a nested list of all the cluster data in the .clog file.
    You can access the Unix times of all frames by calling read_clog(filename)[0], the Acquisition times of all 
    frames by calling read_clog(filename)[1], and the full cluster data by calling read_clog(filename)[2].

    When using 'data = read_clog(FileInPath, filename)[2]', you can traverse the data on level of Frames, 
    registered values (group of 4 values - [x, y, ToT, ToA]) and selected value from one of the 
    four possible - x or y or ToT or ToA.
    To access first layer (selected frame) use: data[0]
    To access second layer (selected 4-group of selected frame) use: data[0][0]
    To access third layer (selected value from selected 4-group of selected frame) use: data[0][0][0] 
    """

    with open(filename) as inputFile:
        lines = inputFile.readlines()
    frame_unix_time = np.empty([0])
    frame_times = np.empty([0])

    current_cluster = []
    all_values = []

    a = []
    pattern_b = r"\[[^][]*]"

    frame_counter = 0

    for line in lines:
        if line != "\n":
            current_cluster = []
            if (line.split()[0] == "Frame"):
                frame_counter += 1
                unixtime = float(line.split()[2].lstrip("(").rstrip(","))
                frame_unix_time = np.append(frame_unix_time, unixtime)
                measurement_time = float(line.split()[3].rstrip(","))
                frame_times = np.append(frame_times, measurement_time)

                continue

            a = (re.findall(pattern_b, line))
            #print(f'Frame {frame_counter} with {len(a)} events, specifically {a}')
            
            for element in a:
                b = ("".join(element)).rstrip("]").lstrip("[").split(",")
                b = [float(x) for x in b]
                current_cluster.append(b)
            all_values.append(current_cluster)

            
            #print(f'The current cluster is {current_cluster}\n')

    # to fix problem with first list being empty, needs solution without copying for better performance
    return frame_unix_time, frame_times, all_values


def read_clog_multiple(FileInPath):
    """
    This function reads all clog files generated by the DPE excluding MASK clogs
    in the given directory. It utilizes the read_clog function that goes per cluster.
    It reads Elist and writes a Coincidence elist, a list which contains information
    about if and how many coincidence clusters each frame contains.
    """
    
    OutputPath = FileInPath
    
    #elist_path = FileInPath + 'ExtElist.txt'
    #elist_data = read_elist(elist_path)[2]
    #OutputName = 'Coincidence_ExtElist'
    #write_coincidence_elist(elist_path, OutputPath, OutputName)

    full_clog_data = []

    for file in os.listdir(FileInPath):
        if file.endswith('.clog') and not file.startswith('MASK'):
            full_clog_data.extend(read_clog_clusters(os.path.join(FileInPath, file))[2])

    return full_clog_data


def get_elist_column(filename, col_name):
    """
    This function is used to extract a specific column from a file in Elist format, based on the exact name 
    of the column. It takes in three inputs, the file path of the Elist, the name of the file, and the name 
    of the column that needs to be extracted. It returns the data in the column in a python list format. 
    The function first reads the first two lines of the file to get the names and units of all columns. 
    It then iterates through the names of the columns and finds the column with the name that was passed 
    as input. It then extracts the data in that column and returns it as a numpy array.

    From Elist extract a specific column based on the exact name of the column
    Function returns a numpy array of data in python list format
    col_name = name of the variable from Elist

    Example, select column with Energy values:
    selected_column = get_column('path/to/Elist.txt', 'E') 
    """

    with open(filename, 'r') as inputFile:
        lines = inputFile.readlines()
    names = [lines[0].rstrip().split(';')]
    units = [lines[1].rstrip().split(';')]
    lines = lines[2:]
    for idx, val in enumerate(names[0][:]):
        if names[0][idx] == col_name:
            col_num = idx
    # print(f'From get_column() you are printing parameter {str(names[0][col_num])} in units {str(units[0][col_num])}\n'.)

    column_data = np.empty([0])

    for line in lines:
        column_data = np.append(column_data, line.rstrip().split(';')[col_num])

    return column_data


def read_elist(filename):
    """
    *** NOT NECESSARY - USE NUMPY LOADTXT ***
    *** np.loadtxt(filename, skiprows=2) ***
    The read_elist function reads an Elist file and returns its data in the form of a list of lists, 
    where the first list is the header, the second list is the units and the rest of the lists are 
    the data. The user can then access the header and units by calling 
    header, units, _ = read_elist('path/to/Elist.txt') or the data by calling 
    data = read_elist('path/to/Elist.txt')[2].

    Access full Elist data including header

    Example - return header and units:
    header, units, _ = read_elist('path/to/Elist.txt')

    Example, return data only
    data = read_elist('path/to/Elist.txt')[2]
    """

    with open(filename) as inputFile:
        lines = inputFile.readlines()
    inputFile.close()

    splitlines = [list(line.rstrip().split(";")) for line in lines]
    return splitlines[0], splitlines[1], splitlines[2:]


def read_elist_add_new_parameters(filename, column_number_pairs_for_ratios, header_text_new_columns, units_text_new_columns):
    """
    *** PROBABLY UPDATED IN CARLOS read_elist_filter, check and delete if obsolete ***
    Lukas 8 August 2022
    New version of read_elist to calculate new parameters and ratios
    old name "read_elist_make_ext_elist"

    This function reads an elist file, and calculates new columns which are the ratios of pairs of 
    CA PAR (columns) specified in the col_num_pairs_for_ratios input. The new columns are added to the right
    of the original elist, and the new header and units for these new columns are specified in 
    header_txt_new_cols and units_txt_new_cols inputs. The function returns the elist with the added columns, 
    where the output is split into three objects: the header, the units, and the data. The function also prints 
    the number of all clusters processed and the line number of the first and second row.

    How to use:
    filename = elist_txt_name
    column_number_pairs_for_ratios = [4,7,9,7]    # Energy, Size, BorderPixel, Size
    header_text_new_columns = ['E/Size', 'BorderPixel/Size']
    units_text_new_columns = ['keV/px', 'a.u.']
    """

    with open(filename, "r") as inputFile:
        lines = inputFile.readlines()
    splitlines = []

    #cluster_count_all = 0  # counter of all clusters, innitiate if you want to

    number_pairs_new_columns = len(column_number_pairs_for_ratios) // 2
    line_number = 0

    for line in lines:
        line_number += 1
        cluster_variable = list(line.rstrip().split(";"))
        # for the first heading 2 rows

        if line_number <= 2:
            if line_number == 1:
                for k in range(number_pairs_new_columns):
                    cluster_variable.append(header_text_new_columns[k])
                splitlines.append(cluster_variable)
            else:
                for k in range(number_pairs_new_columns):
                    cluster_variable.append(units_text_new_columns[k])
                splitlines.append(cluster_variable)

        else:
            cluster_variable = [float(i) for i in list(line.rstrip().split(";"))]
            #cluster_count_all += 1

            for i in range(number_pairs_new_columns):
                new_column_value = cluster_variable[column_number_pairs_for_ratios[i * 2]
                                            ] / cluster_variable[column_number_pairs_for_ratios[(i * 2) + 1]]
                cluster_variable.append(new_column_value)

            splitlines.append(cluster_variable)

    # print('Number of all clusters = ', cluster_count_all)

    # the full elist with extended col output as single object
    return splitlines[0], splitlines[1], splitlines[2:]


def read_elist_filter_parameters(filename, new_filter=None):
    #testing 2023_03_23 def read_elist_filter_parameters(filename, column_number_pairs_for_ratios, header_text_new_columns, units_text_new_columns, new_filter=None):
    """
    # New read_elist function to include option to filter events (Lukas 8 August 22)

    This function reads an elist file (which is the calibrated output of DPE_CP) and applies a filter 
    to the clusters based on certain CA PARs (cluster analysis parameters). The function takes in 
    several arguments:

    filename - name of the elist file,

    column_number_pairs_for_ratios - a list of column numbers of the CA PARs that are used to create 
    new columns of ratios. For example, [4,7,9,7] would use the values in column 4, 7, 9 and 7 to 
    calculate the ratios E/A, BordPx/A, etc.

    header_text_new_columns - a list of headers for the new columns of ratios that are created,

    units_text_new_columns - a list of units for the new columns of ratios that are created,

    new_filter - an instance of the Cluster_filter_multiple_parameter class, which is used to filter 
    the clusters based on certain CA PARs. If no filter is provided, the function will not filter 
    the clusters and will only add new columns of ratios.

    The function reads the elist file line by line and processes each line accordingly. It first checks 
    if the line is one of the first two rows (the header and units rows), in which case it adds the new 
    column headers. For the rest of the lines, it checks if the new_filter is provided, and if it is, 
    it applies the filter to the cluster variables. If the cluster passes the filter, it adds a value 
    of 1 in the new column, otherwise it adds a value of 0. It also keeps track of the number of clusters, 
    the number of clusters that pass the filter, and the number of clusters that fail the filter. 
    Once all lines have been processed, the function returns the updated elist.
    
    A new columns is appended to the Elist:
    Cluster passed the filter = 1
    Cluster failed the filter = 0

    Example:
    One filter for Height parameter - [100,500],[8]
    Two filters for Height and Size - [100,500,10,30], [8,7]

    The output is the same elist, now with the added new column (column number = 16)
    """

    with open(filename, "r") as inputFile:
        lines = inputFile.readlines()

    # cluster_count_all = 0  # counter of all clusters
    # cluster_count_ok = 0  # counter of OK clu's
    # cluster_count_bad = 0  # counter of rejected clu's

    if new_filter is not None:
        splitlines = []

        for line_number, line in enumerate(lines, start=1):
            cluster_variable = list(line.rstrip().split(";"))

            if line_number <= 2:
                cluster_variable.append('Filter')
            else:
                cluster_variable = [float(i)
                               for i in list(line.rstrip().split(";"))]
                #cluster_count_all += 1

                if new_filter.pass_filter(cluster_variable):
                    #cluster_count_ok += 1
                    cluster_variable.append(1)
                else:
                    #cluster_count_bad += 1
                    cluster_variable.append(0)

            splitlines.append(cluster_variable)
        # print('Number of all clusters = ', cluster_count_all)
        # print('Number of OK clusters = ', cluster_count_ok)
        # print('Number of bad clusters = ', cluster_count_bad)

        return splitlines[0], splitlines[1], splitlines[2:]

    else:
        print('No filter was used, there is nothing to be processed')


def read_elist_filter(filename, column_number_pairs_for_ratios, header_text_new_columns, units_text_new_columns, new_filter=None):
    """
    Carlos Granja, 23 August 2022
    old name "read_elist_make_ext_filter"
    *** this is probably updated version of read_elist_add_new_parameters, delete the old one if it is the case ***

    This function reads an elist file (output from DPE_CP), calculates ratios of pairs of CA PAR and adds them 
    as new columns to the elist. Then, it applies a filter to the clusters based on the CA PAR and the new ratios, 
    and adds a new column indicating whether the cluster passed or failed the filter. The output is the same elist 
    with the added new columns at the right. The function takes the following inputs:

    filename - path to the elist file

    column_number_pairs_for_ratios - a list of integers representing the column numbers of the CA PAR that will be 
    used to calculate ratios. The list should contain pairs of integers, where the first integer of each pair is 
    the numerator and the second integer is the denominator of the ratio.

    header_text_new_columns - a list of strings representing the names of the new columns with the ratios. The length 
    of this list should be the same as the number of pairs in column_number_pairs_for_ratios.

    units_text_new_columns - a list of strings representing the units of the new columns with the ratios. The length 
    of this list should be the same as the number of pairs in column_number_pairs_for_ratios.

    new_filter - an object of a class that defines the filter to be applied to the clusters. The class should have 
    a function pass_filter(cluster_variable) that takes the list of variables of a cluster as input and returns 
    a Boolean indicating whether the cluster passes or fails the filter. If no filter is desired, set new_filter 
    to None.

    Cluster passed the filter = 1
    Cluster failed the filter = 0

    Example:
    filename = elist (output of DPE CP, stored in Files DIR output)
    column_number_pairs_for_ratios = [4, 7, 9, 7]  # Energy, Size, BorderPixel, Size
    header_text_new_columns = ['Energy/Size', 'BorderPixel/Size']
    units_text_new_columns = ['keV/px', 'a.u.']
    new_filter = [90, 5000, 4500, 5.E5, 0.9, 1.7, 4, 300, 30, 5000], [8, 4, 10, 7, 15]) # Height Energy Roundness Size, Energy/Size, 
    """

    with open(filename, "r") as inputFile:
        lines = inputFile.readlines()
        
    number_pairs_new_columns = len(column_number_pairs_for_ratios) // 2

    # cluster_count_all = 0  # counter of all clusters
    # cluster_count_ok = 0  # counter of OK clu's
    # cluster_count_bad = 0  # counter of rejected clu's

    if new_filter is not None:
        splitlines = []

        for line_number, line in enumerate(lines, start=1):
            cluster_variable = list(line.rstrip().split(";"))

            if line_number <= 2:
                if line_number == 1:
                    cluster_variable.extend(
                        header_text_new_columns[k]
                        for k in range(number_pairs_new_columns)
                    )
                    cluster_variable.append('Applied_filter')
                else:
                    cluster_variable.extend(
                        units_text_new_columns[k]
                        for k in range(number_pairs_new_columns)
                    )
                    cluster_variable.append('1 = ok')
            else:
                cluster_variable = [float(i)
                               for i in list(line.rstrip().split(";"))]

                # cluster_count_all += 1

                for i in range(number_pairs_new_columns):
                    new_column_value = round(
                        cluster_variable[column_number_pairs_for_ratios[i * 2]] / cluster_variable[column_number_pairs_for_ratios[(i * 2) + 1]], 3)

                    cluster_variable.append(new_column_value)

                if new_filter.pass_filter(cluster_variable):
                    # cluster_count_ok += 1
                    cluster_variable.append(1)
                else:
                    # cluster_count_bad += 1
                    cluster_variable.append(0)

            splitlines.append(cluster_variable)
        # print('Number of all clusters = ', cluster_count_all)
        # print('Number of OK clusters = ', cluster_count_ok)
        # print('Number of bad clusters = ', cluster_count_bad)

        # print('--- read elist ext filt done ---')

        return splitlines[0], splitlines[1], splitlines[2:]

    else:
        print('No filter was used, there is nothing to be processed')


def write_elist(filename, header, units, data):
    """
    This function writes a file in a specific Elist format. The function takes in four parameters: filename_out, 
    header, units, and data. The filename_out is the name of the file to be written. The header and units are lists 
    of strings that are written as the first two lines in the file. The data parameter is a 2D list, where each row 
    represents a line in the file, and each element in the row represents a column. The function writes each row of 
    data as a string, separated by semicolons, and ends each line with a newline character. The function uses the 
    python built-in open function to open the file in write mode.
    """
    with open(filename, 'w') as f:
        f.write(';'.join(map(str, header))+'\n')
        f.write(';'.join(map(str, units))+'\n')
        
        for row in data:
            s = ';'.join(map(str, row))
            f.write(s+'\n')


def write_coincidence_elist(filename, OutputPath, OutputName):
    #def write_elist_add_coincidence(filename, header, units, data, OutputPath, OutputName):
    print('Printing cluster coincidence')
    #data = np.loadtxt(filename, skiprows=2, delimiter=';')
    eventid = np.loadtxt(filename, skiprows=2, delimiter=';', usecols=1, dtype='int')
    count = np.bincount(eventid)
    events = np.arange(0, len(count), 1)

    bool_value = np.array([])
    for number in range(len(count)-1):
        if count[number] > 1:
            bool_value = np.append(bool_value, 1)
        else:
            bool_value = np.append(bool_value, 0)

    out_values = np.column_stack((events[:-1], count[:-1], bool_value))
    np.savetxt(OutputPath + OutputName + '.txt', out_values, delimiter=',', header='Event, Count, Is_Coincidence', fmt="%i", comments='')


def create_matrix_tpx3_t3pa(clog, number_of_clusters):
    """
    Only matrix creation without selection of filtration pass filter
    """
    matrix_energy = np.zeros([256, 256])

    counter = 0

    for i in range(len(clog)):
        cluster_size_clog = len(clog[i][:])
        
        # TOTO PO IWORID ABSTRAKTE VYMAZAT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if cluster_size_clog > 4 and counter < number_of_clusters:
            counter += 1
            for j in range(cluster_size_clog):
                x, y = int(clog[i][j][0]), int(clog[i][j][1])
                matrix_energy[x, y] += clog[i][j][2]

    print(f'VYMAZAT!!! - pocet eventov ktore presli v experimente je: {counter}')
    return matrix_energy


def create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_frames):
    """
    Carlos + Lukas + Andrej, 8 August 2022

    This function creates a filter for a 2D plot of a detector pixel matrix, specifically for TPX3 t3pa data 
    and its clog output with short time frames (e.g. 100 ns). The function takes in three parameters: 
    filtered_elist, clog, and number_frames. The filtered_elist is the output of a DPE_CP elist with an added 
    column from a cluster filter. The clog is the output of a DPE_CP calibration. The number_frames is the number 
    of frames to integrate, which is either the cluster number (for TPX3 t3pa data) or the frame number (for raw 
    clog frame data).

    The function creates several matrices: matrix_energy_all, matrix_toa_all, matrix_energy_ok, matrix_toa_ok, 
    matrix_energy_bad, and matrix_toa_bad. The function iterates over a list of random numbers and for each 
    iteration, it retrieves the size of the cluster from the clog, and for each element in the cluster, it 
    increments the corresponding element (Energy and ToA value) in the matrices. The function also keeps track 
    of multiplets, which are clusters that have more than one pixel. The function returns the six matrices created.

    Description:

    elist_filtered - the DPE output elist with the added COL from cluster_filter,

    clog - clog output of DPE,

    number_frames - number of frames to integrate, to add to merged plot from the beginning, from frame number zero in the 
    clog file output of DPE for TPX3 data a frame is created every 100 ns. For TPX3 t3pa data - input number_frames 
    is the cluster - event number. For raw clog frame data - number_frames is the frame number.
    """

    random_numbers = list(range(0, number_frames))

    matrix_energy_all = np.zeros([256, 256])
    matrix_toa_all = np.zeros([256, 256])

    matrix_energy_ok = np.zeros([256, 256])
    matrix_toa_ok = np.zeros([256, 256])

    matrix_energy_bad = np.zeros([256, 256])
    matrix_toa_bad = np.zeros([256, 256])

    jump = 0
    frame_jump = 0
    multiplet_number = 0  # to keep record of multiplet occurrence

    for idx, var in enumerate(random_numbers):
        cluster_size_clog = len(clog[var][:])
        cluster_size_elist = filtered_elist[2][var][7]

        for j in range(cluster_size_clog):
            x, y = int(clog[var][j][0]), int(clog[var][j][1])

            matrix_energy_all[x, y] += clog[var][j][2]
            matrix_toa_all[x, y] = clog[var][j][3]

        if filtered_elist[2][var][number_column_filter] == 1:
            # to take into account multiplets, these can be resolved in elist, but not in clog

            for j in range(cluster_size_clog):
                x, y = int(clog[var][j][0]), int(clog[var][j][1])

                matrix_energy_ok[x, y] += clog[var][j][2]
                matrix_toa_ok[x, y] = clog[var][j][3]

        else:
            if jump == 1:
                for j in range(cluster_size_clog):
                    x, y = int(clog[var][j][0]), int(clog[var][j][1])

                    matrix_energy_bad[x, y] += clog[i][j][2]
                    matrix_toa_bad[x, y] = clog[var][j][3]

    return matrix_energy_all, matrix_toa_all, matrix_energy_ok, matrix_toa_ok, matrix_energy_bad, matrix_toa_bad


def create_matrix_filter_tpx3_t3pa_for_filtering(filtered_elist, clog, number_of_particles):
    """
    2023_03_28 - 
    This function creates a filter for a 2D plot of a detector pixel matrix, specifically for TPX3 t3pa data 
    and its clog output with short time frames (e.g. 100 ns). The function takes in three parameters: 
    filtered_elist, clog, and number_frames. The filtered_elist is the output of a DPE_CP elist with an added 
    column from a cluster filter. The clog is the output of a DPE_CP calibration. The number_frames is the number 
    of frames to integrate, which is either the cluster number (for TPX3 t3pa data) or the frame number (for raw 
    clog frame data).

    The function creates several matrices: matrix_energy_all, matrix_toa_all, matrix_energy_ok, matrix_toa_ok, 
    matrix_energy_bad, and matrix_toa_bad. The function iterates over a list of random numbers and for each 
    iteration, it retrieves the size of the cluster from the clog, and for each element in the cluster, it 
    increments the corresponding element (Energy and ToA value) in the matrices. The function also keeps track 
    of multiplets, which are clusters that have more than one pixel. The function returns the six matrices created.

    Description:

    elist_filtered - the DPE output elist with the added COL from cluster_filter,

    clog - clog output of DPE,

    number_frames - number of frames to integrate, to add to merged plot from the beginning, from frame number zero in the 
    clog file output of DPE for TPX3 data a frame is created every 100 ns. For TPX3 t3pa data - input number_frames 
    is the cluster - event number. For raw clog frame data - number_frames is the frame number.
    """
    matrix_energy_all = np.zeros([256, 256])
    matrix_toa_all = np.zeros([256, 256])

    matrix_energy_ok = np.zeros([256, 256])
    matrix_toa_ok = np.zeros([256, 256])

    matrix_energy_bad = np.zeros([256, 256])
    matrix_toa_bad = np.zeros([256, 256])

    for i in range(number_of_particles):
        cluster_size_clog = len(clog[i][:])
        #print(f'The number of events in frame {i} are {len(clog[0])} the total number of pixels is {cluster_size_clog}')
        for j in range(cluster_size_clog):
            x, y = int(clog[i][j][0]), int(clog[i][j][1])

            matrix_energy_all[x, y] += clog[i][j][2]
            matrix_toa_all[x, y] = clog[i][j][3]

        if filtered_elist[2][i][-1] == 1:
            for j in range(cluster_size_clog):
                x, y = int(clog[i][j][0]), int(clog[i][j][1])

                matrix_energy_ok[x, y] += clog[i][j][2]
                matrix_toa_ok[x, y] = clog[i][j][3]
        else:
            for j in range(cluster_size_clog):
                x, y = int(clog[i][j][0]), int(clog[i][j][1])
                
                matrix_energy_bad[x, y] += clog[i][j][2]
                matrix_toa_bad[x, y] = clog[i][j][3]

    return matrix_energy_all, matrix_toa_all, matrix_energy_ok, matrix_toa_ok, matrix_energy_bad, matrix_toa_bad


def create_matrix_filter_tpx_frame(filtered_elist, clog, number_column_filter, number_particles):
    """
    Carlos + Lukas + Andrej, 8 August 2022
    old name: create_matrix_filter_tpx_f

    This function creates a filter for a 2D plot of a detector pixel matrix, specifically for TPX frame data and its 
    clog output with frames. The function takes in three parameters: filtered_elist, clog, and number_particles. 
    The filtered_elist is the output of a DPE_CP elist with an added column from a filter. The clog is the output 
    of a DPE_CP calibration. The number_particles is the number of events to integrate, which is either the cluster 
    number (for TPX frame data) or the frame number (for raw clog frame data).

    The function creates several matrices: matrix_E_all, matrix_E_ok, and matrix_E_bad. The function iterates over 
    a list of random numbers and for each iteration, it retrieves the size of the cluster from the clog, and for each 
    element in the cluster, it increments the corresponding element in the matrices. The function also keeps track 
    of multiplets, which are clusters that have more than one pixel fired. The function returns the three matrices 
    created.

    Example:

    filtered_elist -  the DPE output elist with additional column from filter,

    clog - the clog output of DPE,

    number_particles - number of events to integrate, to add to merged plot from beginning, from frame number zero 
    in the clog file output of DPE for TPX data frames. For TPX frame data ToT - input number_particles is the 
    cluster i.e. event number. For raw clog frame data - number_particles is the frame number.
    """

    random_numbers = list(range(0, number_particles))

    matrix_all = np.zeros([256, 256])
    matrix_ok = np.zeros([256, 256])
    matrix_bad = np.zeros([256, 256])

    # cluster_count_all = 0
    # cluster_count_ok = 0
    # cluster_count_bad = 0

    jump = 0
    # f_jump = 0
    # multiplet_num = 0 # to keep record of multiplet occurrence

    for idx, var in enumerate(random_numbers):
        cluster_size_clog = len(clog[var][:])
        
        # cluster_count_all += 1

        for j in range(cluster_size_clog):
            x, y = int(clog[var][j][0]), int(clog[var][j][1])
            matrix_all[x, y] += clog[var][j][2]

        if filtered_elist[2][var][number_column_filter] == 1:
            # cluster_count_ok += 1

            for j in range(cluster_size_clog):
                x, y = int(clog[var][j][0]), int(clog[var][j][1])
                matrix_ok[x, y] += clog[var][j][2]

        else:
            if jump < 1:
                # cluster_count_bad += 1

                for j in range(cluster_size_clog):
                    x, y = int(clog[var][j][0]), int(clog[var][j][1])
                    matrix_bad[x, y] += clog[var][j][2]


    # print('all clu = ', cluster_count_all)
    # print('all ok = ', cluster_count_ok)
    # print('all bad = ', cluster_count_bad)

    # return matrix_all, matrix_ok, matrix_bad, cluster_count_all, cluster_count_ok, cluster_count_bad

    return matrix_all, matrix_ok, matrix_bad


def calibrate_frame(a_path, b_path, c_path, t_path, matrix):
    """
    *** REWRITEN FROM CARLOS' MATLAB SCRIPT ***

    This function calibrates an uncalibrated matrix to energy using input calibration matrices. The function takes in 
    five parameters: a_path, b_path, c_path, t_path and matrix for the calibration. The a_path, b_path, c_path and 
    t_path are the names or full paths of the respective calibration matrices. The matrix is the uncalibrated input.

    The function loads the calibration matrices from the provided paths using the numpy np.loadtxt(). It then creates 
    a new matrix called tot, which is the calibrated energy matrix. It iterates over the elements of the input matrix, 
    and for each element, if the value of matrix[i, j] > 0.8, it uses the calibration matrices to recalculate the 
    corresponding element in the matrix. Otherwise, it sets the corresponding element of the tot matrix to 0. It then 
    returns the tot matrix.
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
                             t[i, j] + b[i, j] - matrix[i, j]) ** 2 + 4 * a[i, j] * c[i, j]))) / (2 * a[i, j])
            else:
                tot[i, j] = 0

    return tot


def print_figure_energy(matrix, vmax, title, OutputPath, OutputName):
    """
    Old name: print_fig_E

    Function to print a figure of deposited energy in logarithmic colorbar scale.
    """

    mydpi = 300
    tickfnt = 16

    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)

    plt.close()
    plt.cla()
    plt.clf()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(
        matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    cbar = plt.colorbar(label='Energy [keV]', aspect=20*0.8, shrink=0.8) # shrink=0.8
    cbar.set_label(label='Energy [keV]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.clim(1, vmax)
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '.png', dpi=mydpi,
                transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '.txt', matrix, fmt="%.3f")


def print_figure_energy_iworid_2023(matrix, vmax, title, OutputPath, OutputName):
    """
    Old name: print_fig_E

    Function to print a figure of deposited energy in logarithmic colorbar scale.
    """

    mydpi = 300
    tickfnt = 16

    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)

    plt.close()
    plt.cla()
    plt.clf()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(
        matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    plt.gca().xaxis.tick_bottom()
    cbar = plt.colorbar(label='Deposited energy per-pixel [keV/px]', aspect=20*0.8, shrink=0.8) # shrink=0.8
    cbar.set_label(label='Deposited energy per-pixel [keV/px]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    # plt.clim(vmin,vmax) - set your own range using vmin, vmax
    plt.clim(1, vmax)
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.xlim([0,100])
    plt.ylim([0,100])
    #plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    #plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '.png', dpi=mydpi,
                transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '.txt', matrix, fmt="%.3f")


def print_figure_toa(matrix, vmax, title, OutputPath, OutputName):
    """
    Old name: print_fig_ToA

    Function to print a figure of ToA values in linear scale.
    """
    
    tickfnt = 14
    mydpi = 300

    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)

    plt.close()
    plt.cla()
    plt.clf()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot')
    # If the orientation of matrix doesnt fit, use this instead
    plt.matshow(np.flip(np.rot90(matrix[::-1, :])),
                origin='lower', cmap='modified_hot')    # cmap='modified_hot' 'viridis'
    plt.gca().xaxis.tick_bottom()
    cbar = plt.colorbar(label='ToA [ns]', aspect=20*0.8)
    cbar.set_label(label='ToA [ns]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.clim(0, vmax)
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
    plt.tick_params(axis='x', labelsize=tickfnt)
    plt.tick_params(axis='y', labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.savefig(OutputPath + OutputName + '.png', dpi=mydpi,
                transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '.txt', matrix, fmt="%.3f")


def parameter_filter(data_column, min_value, max_value):
    """

    This function is used to filter data based on a specific column's value. The function takes in three parameters: 
    data_column, min_value, and max_value. The data_column parameter is a list of values for a specific column of 
    data, min_value is the minimum acceptable value for the column's data, and max_value is the maximum acceptable 
    value for the column's data.

    The function first creates two empty lists passed and bad, which will be used to store the line numbers of the data 
    that pass the filter and those that don't pass the filter, respectively. Then it iterates over the data_column 
    and compares each value to the min_value and max_value. If the value is greater than or equal to min_value and 
    less than or equal to max_value, the function appends the index of that value to the passed list. If the value 
    is not within the acceptable range, the function appends the index of that value to the bad list. It then returns 
    the passed and bad lists.

    Example: 
    
    For data_column use function get_column(filename, col_name)

    parameter_filter(get_column('Elist.txt', 'E'), 1, 1E3)
    """

    passed = []
    bad = []

    for idx, val in enumerate(data_column):
        if float(val) >= min_value and float(val) <= max_value:
            passed.append(idx)
        else:
            bad.append(idx)

    return passed, bad


def create_matrix_tpx3_old(data, number_frames, random):
    """
    Old name: create_matrix

    This function creates a 2D plot of a detector pixel matrix using the data input, and a number of frames to 
    integrate. The function takes three parameters: data, number_frames, and random. The data parameter is the clog 
    calibration output of DPE_CP, number_frames is the number of frames to integrate from the beginning, and random 
    is a string that determines whether or not random numbers are chosen.

    The function first creates a list of random numbers, either by using the random.sample() function or by creating 
    a range of numbers based on the number_frames parameter. It then creates two matrices, matrix_energy and 
    matrix_toa, that are initially filled with zeroes.

    The function then iterates over the random_numbers list, and for each iteration, it retrieves the size of the 
    cluster from the data, and for each element in the cluster, it increments the corresponding element in the 
    matrices. The function also keeps track of multiplets, which are clusters that have more than one pixel fired. 
    The function returns the two matrices created.

    The matrix_energy is the sum of energies in each pixel, and matrix_toa is the ratio of ToA of each pixel to the 
    maximum ToA in the cluster.

    Description:

    data - the clog output of DPE,

    number_frames - number of frames to integrate, to add to merged plot from beginning, from frame number zero in 
    the clog file output of DPE. For TPX3 data a frame is created every 100 ns. For TPX3 t3pa data - input 
    number_frames is the cluster - event number. For raw clog frame data - number_frames is the frame number.

    random - determines whether random frames are chosen or not.
    """

    if random == 'True':
        random_numbers = sorted(random.sample(
            range(0, len(data[:])), len(number_frames)))
    else:
        random_numbers = list(range(0, number_frames))

    matrix_energy = np.zeros([256, 256])
    matrix_toa = np.zeros([256, 256])

    for idx, val in enumerate(random_numbers):
        for j in range(len(data[val][:])):
            x, y = int(data[val][j][0]), int(data[val][j][1])

            toa = []
            
            for i in range(len(data[val][:])):
                toa.append(data[val][i][3])
                matrix_energy[x, y] += data[val][j][2]
            else:
                pass

            if max(toa) != 0:
                matrix_toa[x, y] = (data[val][j][3]) / max(toa)
            else:
                matrix_toa[x, y] = data[val][j][3]

    return matrix_energy, matrix_toa


def print_figure_single_cluster_energy(clog_path, frame_number, vmax, title, OutputPath, OutputName):
    """
    Old name: plot_single_cluster_ToT   
    """
    tickfnt = 16
    margin = 5

    clog = read_clog(clog_path)[2]
    matrix = np.zeros([256, 256])

    x = []
    y = []

    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] += clog[frame_number][i][2]

    if (max(x) - min(x)) < (max(y) - min(y)):
        difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
    else:
        difference_position_x = 0
    if (max(y) - min(y)) < (max(x) - min(x)):
        difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
    else:
        difference_position_y = 0

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
    plt.clim(1, vmax)
    cbar = plt.colorbar(label='Energy [keV]', aspect=20*0.8) # shrink=0.8
    cbar.set_label(label='Energy [keV]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    plt.ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '_' +
               str(frame_number) + '.txt', matrix, fmt="%.3f")


def print_figure_single_cluster_energy_smooth(clog_path, frame_number, vmax, title, OutputPath, OutputName):
    """
    The same function as print_figure_single_cluster_energy with smoothened scale
    """
    tickfnt = 14
    margin = 5

    clog = read_clog_clusters(clog_path)[2]
    matrix = np.zeros([256, 256])

    x = []
    y = []
    print(len(clog))
    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] += clog[frame_number][i][2]

    if (max(x) - min(x)) < (max(y) - min(y)):
        difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
    else:
        difference_position_x = 0
    if (max(y) - min(y)) < (max(x) - min(x)):
        difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
    else:
        difference_position_y = 0

    plt.close()
    plt.cla()
    plt.clf()
    plt.subplot()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.imshow(np.flip(np.rot90(
        matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm(), interpolation='gaussian')
    plt.gca().xaxis.tick_bottom()
    plt.clim(1, vmax)
    cbar = plt.colorbar(label='Energy [keV]', aspect=20*0.8) # shrink=0.8
    cbar.set_label(label='Energy [keV]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    plt.ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '_' + str(frame_number) + '_smooth.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '_' +
               str(frame_number) + '_smooth.txt', matrix, fmt="%.3f")

    plt.close()
    plt.cla()
    plt.clf()
    plt.subplot()
    plt.rcParams["figure.figsize"] = (11.7, 8.3)
    # plt.matshow(matrix[:,:], origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    # If the orientation of matrix doesnt fit, use this instead
    plt.imshow(np.flip(np.rot90(
        matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm(), interpolation='None')
    plt.gca().xaxis.tick_bottom()
    plt.clim(1, vmax)
    cbar = plt.colorbar(label='Energy [keV]', aspect=20*0.8) # shrink=0.8
    cbar.set_label(label='Energy [keV]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    plt.ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '_' +
               str(frame_number) + '.txt', matrix, fmt="%.3f")


def print_figure_single_cluster_energy_histograms(clog_path, frame_number, vmax, title, OutputPath, OutputName):
    """
    The same function as print_figure_single_cluster_energy but with histograms.
    """
    tickfnt = 9

    clog = read_clog(clog_path)[2]
    matrix = np.zeros([256, 256])

    x = []
    y = []

    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] += clog[frame_number][i][2]

    x_column_values = np.empty([0])
    y_row_values = np.empty([0])

    for i in range(len(x)):
        x_column_values = np.append(x_column_values, np.sum(matrix[int(x[i]),:]))

    for i in range(len(y)):
        y_row_values = np.append(y_row_values, np.sum(matrix[:,int(y[i])]))
    
    if (max(x) - min(x)) < (max(y) - min(y)):
        difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
    else:
        difference_position_x = 0
    if (max(y) - min(y)) < (max(x) - min(x)):
        difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
    else:
        difference_position_y = 0

    margin = 0.5
    plt.close()
    plt.cla()
    plt.clf()
    matplotlib.rc('xtick', labelsize=tickfnt) 
    matplotlib.rc('ytick', labelsize=tickfnt)
    fig, axs = plt.subplots(2, 2)
    fig.tight_layout(pad=1)
    axs[0, 0].bar(x, x_column_values, linewidth=0)
    axs[0, 0].set_xlim([min(x) - int(difference_position_x) / 2 - margin, max(x) + int(difference_position_x) + margin])
    axs[0, 0].set_ylim([1,1E3])
    axs[0, 0].set_title('Energy values in x direction', fontsize=tickfnt)
    axs[0, 0].set_yscale('log')
    axs[0, 1].axis('off')
    aa = axs[1, 0].matshow(np.flip(np.rot90(
        matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
    axs[1, 0].xaxis.tick_bottom()
    cbar = fig.colorbar(aa)
    #axs[1, 0].set_clim(1, vmax)
    #cbar = axs[1, 0].plt.colorbar(label='Energy [keV]', shrink=0.8, aspect=20*0.8)
    #cbar.set_label(label='Energy [keV]', size=tickfnt, weight='regular')   # format="%.1E"
    #cbar.ax.tick_params(labelsize=tickfnt)
    axs[1, 0].set_xlim([min(x) - int(difference_position_x) / 2 - margin, max(x) + int(difference_position_x) / 2 + margin])
    axs[1, 0].set_ylim([min(y) - int(difference_position_y) / 2 - margin, max(y) + int(difference_position_y) / 2 + margin])
    #axs[1, 0].set_title('Axis [1, 0]', fontsize=tickfnt)
    axs[1, 1].barh(y, y_row_values)
    axs[1, 1].set_xlim([1,1E3])
    axs[1, 1].set_ylim([min(y) - int(difference_position_y) / 2 - margin, max(y) + int(difference_position_y) / 2 + margin])
    #axs[1, 1].set_ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y + margin])
    axs[1, 1].set_title('Energy values in x direction', fontsize=tickfnt)
    axs[1, 1].set_xscale('log')
    plt.savefig(OutputPath + OutputName + '_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '_' +
               str(frame_number) + '.txt', matrix, fmt="%.3f")


def print_figure_single_cluster_toa_tpx3(clog_path, frame_number, vmax, title, OutputPath, OutputName):
    """
    Old name: plot_single_cluster_ToA
    
    For Timepix3 and Timepix2 detectors.
    """
    tickfnt = 16
    margin = 5

    clog = read_clog(clog_path)[2]
    matrix = np.zeros([256, 256])

    x = []
    y = []

    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] += clog[frame_number][i][3]

    if (max(x) - min(x)) < (max(y) - min(y)):
        difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
    else:
        difference_position_x = 0
    if (max(y) - min(y)) < (max(x) - min(x)):
        difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
    else:
        difference_position_y = 0

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
    plt.clim(0, vmax)
    cbar = plt.colorbar(label='ToA [ns]', aspect=20*0.8) # shrink=0.8
    cbar.set_label(label='ToA [ns]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    plt.ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '_' +
               str(frame_number) + '.txt', matrix, fmt="%.3f")


def print_figure_single_cluster_toa_tpx(clog_path, frame_number, vmax, title, OutputPath, OutputName):
    """
    Old name: plot_single_cluster_ToA
    
    For Timepix detectors.
    """
    tickfnt = 16
    margin = 5

    clog = read_clog(clog_path)[2]
    matrix = np.zeros([256, 256])

    x = []
    y = []

    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] = clog[frame_number][i][2]

    if (max(x) - min(x)) < (max(y) - min(y)):
        difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
    else:
        difference_position_x = 0
    if (max(y) - min(y)) < (max(x) - min(x)):
        difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
    else:
        difference_position_y = 0

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
    plt.clim(0, vmax)
    cbar = plt.colorbar(label='ToA [ns]', aspect=20*0.8) # shrink=0.8
    cbar.set_label(label='ToA [ns]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label=title, fontsize=tickfnt+4)
    plt.xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    plt.ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.savefig(OutputPath + OutputName + '_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + OutputName + '_' +
               str(frame_number) + '.txt', matrix, fmt="%.3f")


def plot_single_cluster_toa_gaas(OutputPath, clog_path, frame_number, indicator, vmax):
    """
    This is a plot function that I used for Elitech 2023 school article, it is not really published.
    """
    tickfnt = 16
    margin = 5

    clog = read_clog(clog_path)[2]
    matrix = np.zeros([256, 256])

    x = []
    y = []

    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    for i in range(len(clog[frame_number][:])):
        matrix[int(x[i]), int(y[i])] = clog[frame_number][i][3]

    if indicator == True:
        x_add = []
        y_add = []

        for i in range(len(clog[frame_number + 1][:])):
            x_add.append(clog[frame_number][i][0])
            y_add.append(clog[frame_number][i][1])

        for i in range(len(clog[frame_number + 1][:])):
            matrix[int(x_add[i]), int(y_add[i])] = clog[frame_number + 1][i][3]
    else:
        pass

    if (max(x) - min(x)) < (max(y) - min(y)):
        difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
    else:
        difference_position_x = 0
    if (max(y) - min(y)) < (max(x) - min(x)):
        difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
    else:
        difference_position_y = 0

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
    plt.clim(0, vmax)
    cbar = plt.colorbar(label='ToA [ns]', aspect=20*0.8) # shrink=0.8
    cbar.set_label(label='ToA [ns]', size=tickfnt,
                   weight='regular')   # format="%.1E"
    cbar.ax.tick_params(labelsize=tickfnt)
    plt.title(label='ToA Cluster #'+str(frame_number), fontsize=tickfnt)
    plt.xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    plt.ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    plt.xlabel('X position [pixel]', fontsize=tickfnt)
    plt.ylabel('Y position [pixel]', fontsize=tickfnt)
    plt.savefig(OutputPath + '/ToA_cluster_' + str(frame_number) + '.png',
                dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)
    np.savetxt(OutputPath + '/ToA_cluster_' +
               str(frame_number) + '.txt', matrix, fmt="%.3f")


def gaas_core_halo_study(FileInPath, FileInName, FileOutPath, FileOutName, angle, max_toa_diff, num_of_frames):
    """
    This is a plot function that I used for Elitech 2023 school article, it is not really published.
    """

    all_unix_times = read_clog(FileInPath + FileInName)[0]
    all_frame_times = read_clog(FileInPath + FileInName)[1]
    all_data = read_clog(FileInPath + FileInName)[2]

    maximum_ToA_frame_difference = max_toa_diff     # in nanoseconds 5000

    ToA_values = list()
    ToA_values_halo = list()

    for i in range(len(all_data[:]) - 1):
        matrix_toa = np.zeros([256, 256])

        x_list_first = list()
        y_list_first = list()

        x_list_second = list()
        y_list_second = list()

        first_unix = all_unix_times[i]
        first_meas = all_frame_times[i]

        second_unix = all_unix_times[i + 1]
        second_meas = all_frame_times[i + 1]

        unix_diff = second_unix - first_unix

        for j in range(len(all_data[i][:])):
            x_first, y_first = int(all_data[i][j][0]), int(all_data[i][j][1])

            x_list_first.append(x_first)
            y_list_first.append(y_first)

            matrix_toa[x_first, y_first] = all_data[i][j][3]

            ToA_values.append(str(all_data[i][j][3]))

            indicator = False

        if unix_diff < maximum_ToA_frame_difference and len(all_data[i + 1][:]) < 10:
            for j in range(len(all_data[i + 1][:])):
                x_second, y_second = int(all_data[i + 1][j][0]), int(all_data[i + 1][j][1])

                x_list_second.append(x_second)
                y_list_second.append(y_second)

                if (x_second) in x_list_first or (x_second) in x_list_first or (x_second - 1) in x_list_first or (x_second + 1) in x_list_first and (y_second - 1) in y_list_first or (y_second + 1) in y_list_first or (y_second) in y_list_first or (y_second) in y_list_first:
                    matrix_toa[x_second, y_second] = all_data[i +
                                                              1][j][3] + unix_diff
                    ToA_values.append(str(all_data[i + 1][j][3] + unix_diff))
                    ToA_values_halo.append(
                        str(all_data[i + 1][j][3] + unix_diff))
                    indicator = True

        else:
            indicator = False

        if i <= num_of_frames:
            print_figure_toa(matrix_toa, 100, 'test ToA frame #' +
                          str(i), FileOutPath, FileOutName + '_frame_'+str(i))
            plot_single_cluster_toa_gaas(
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
    tickfnt = 16
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
    tickfnt = 16
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


def create_matrix_tpx3(filename, frame_number):
    """
    4 August 2022

    This function creates a 2D plot of a detector pixel matrix for Timepix3 and Timepix2 detectors using the data 
    in a clog file and a specific frame number. The function takes two parameters: filename and frame_number. The 
    filename parameter is the path to the clog file, and the frame_number parameter is the specific frame from which 
    to draw data from the clog file.

    The function first reads the clog file using the read_clog() function and assigns the data to the variable clog. 
    Then it creates two matrices, matrix_tot and matrix_toa, that are initially filled with zeroes.

    The function then iterates over the data in the clog file, and for each iteration, it retrieves the x and y 
    coordinates and the ToT and ToA values of the pixel. It then increments the corresponding element in the 
    matrix_tot and assigns the ToA value to the corresponding element in the matrix_toa. The function returns the 
    two matrices created, matrix_tot and matrix_toa.

    Description:

    filename - clog file of the DPE output,

    frame_number - frame to be drawn from the clog file.
    """

    clog = read_clog(filename)[2]
    matrix_tot = np.zeros([256, 256])
    matrix_toa = np.zeros([256, 256])
    matrix_counts = np.zeros([256, 256])

    for i in range(len(clog[frame_number][:])):
        x, y = int(clog[frame_number][i][0]), int(clog[frame_number][i][1])
    
        matrix_tot[x, y] += clog[frame_number][i][2]
        matrix_toa[x, y] = clog[frame_number][i][3]
        matrix_counts[x, y] += 1

    return matrix_tot, matrix_toa, matrix_counts


def create_matrix_tpx(filename, frame_number, what_type):
    """
    4 August 2022

    This function creates a 2D plot of a detector pixel matrix for Timepix detectors using the data in a clog file 
    and a specific frame number. The function takes three parameters: filename, frame_number, and what_type. 
    The filename parameter is the path to the clog file, the frame_number parameter is the specific frame from which 
    to draw data from the clog file, and the what_type parameter is a string that indicates whether to create 
    a matrix of "ToT" or "ToA" values.

    The function first reads the clog file using the read_clog() function and assigns the data to the variable clog. 
    Then it creates a matrix, matrix, that is initially filled with zeroes.

    The function then iterates over the data in the clog file, and for each iteration, it retrieves the x and y 
    coordinates and the ToT and ToA values of the pixel. It then increments the corresponding element in the matrix 
    with the value of ToT or assigns the ToA value to the corresponding element in the matrix depending on the value 
    of what_type. The function returns the matrix created.

    Description:

    filename - clog file of the DPE output,

    frame_number - frame to be drawn from the clog file,

    what_type - to get info whether ToT or ToA is being processed, input either 'ToT' or 'ToA'.
    """

    clog = read_clog(filename)[2]
    matrix = np.zeros([256, 256])
    matrix_counts = np.zeros([256, 256])

    if what_type == 'ToT':
        for j in range(len(clog[frame_number][:])):
            x, y = int(clog[frame_number][j][0]), int(clog[frame_number][j][1])
            matrix[x, y] += clog[frame_number][j][2]
    else:
        for j in range(len(clog[frame_number][:])):
            x, y = int(clog[frame_number][j][0]), int(clog[frame_number][j][1])
            matrix[x, y] += clog[frame_number][j][2]
            matrix_counts[x, y] += 1

    return matrix, matrix_counts


def scatter_histogram_for_function(clog_path, frame_number, x, y, ax, ax_histx, ax_histy):
    # no labels
    fig, axs = plt.subplots()
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    clog = read_clog(clog_path)[2]
    area = np.empty([0])

    x = []
    y = []

    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])
        area = np.append(area, clog[frame_number][i][2])

    xbin_value = Counter(x)
    ybin_value = Counter(y)

    #colours = cm.hot_r(np.linspace(0, 1, len(area)))

    # the scatter plot:
    
    image = ax.scatter(x, y, s=area, c=area, cmap='viridis', marker='s')
    ax.set(xlabel='X position [pixel]', ylabel='Y position [pixel]')
    #divider = make_axes_locatable(ax)
    #cax = divider.new_vertical(size = '5%', pad = 0.5)
    #fig.add_axes(cax)
    fig.colorbar(image, norm=colors.LogNorm())
    
    #divider = make_axes_locatable(ax)
    #cbar.ax.set_ylabel('z data', labelpad=5)
    #cbar.ax.yaxis.set_ticks_position("right")
    #cbar.set_clim(1, 1E3)

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    #lim = (int(xymax/binwidth) + 1) * binwidth

    #bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=len(xbin_value))
    ax_histx.set(xlabel='X position [pixel]', ylabel='Count [-]')
    ax_histy.hist(y, bins=len(ybin_value), orientation='horizontal')
    ax_histy.set(xlabel='Count [-]', ylabel='Y position [pixel]')


def print_figure_single_cluster_count_histograms(clog_path, frame_number, OutputPath, OutputName):
    """
    The same function as print_figure_single_cluster_energy but with histograms.
    """
    tickfnt = 16

    clog = read_clog(clog_path)[2]
    matrix = np.zeros([256, 256])

    x = []
    y = []

    for i in range(len(clog[frame_number][:])):
        x.append(clog[frame_number][i][0])
        y.append(clog[frame_number][i][1])

    x_column_values = np.empty([0])
    y_row_values = np.empty([0])

    for i in range(len(x)):
        x_column_values = np.append(x_column_values, x[i])

    for i in range(len(y)):
        y_row_values = np.append(y_row_values, y[i])

    plt.close()
    plt.cla()
    plt.clf()
    plt.xlim([min(x_column_values), max(x_column_values)])
    plt.ylim([min(y_row_values), max(y_row_values)])
    fig = plt.figure(figsize=(6, 6))
    # Add a gridspec with two rows and two columns and a ratio of 1 to 4 between
    # the size of the marginal axes and the main axes in both directions.
    # Also adjust the subplot parameters for a square plot.
    gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(1, 4),
                        left=0.1, right=0.9, bottom=0.1, top=0.9,
                        wspace=0.15, hspace=0.15)
    # Create the Axes.
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
    # Draw the scatter plot and marginals.
    scatter_histogram_for_function(clog_path, frame_number, x_column_values, y_row_values, ax, ax_histx, ax_histy)


def mm_to_px(value_in_mm):
    """ This function is designed to simply convert mm values of cluster position X and Y
    from old Elist format to px values. The output of the newest clusterer is already given
    in px values so use this for DPE version 1.0.5 and lower."""
    return (value_in_mm) / 0.055


def check_if_position_is_in_mask(mask, x_value, y_value):
    """
    This function checks whether the given X or Y position is in mask. It can be used only for 1 px clusters only.
    Insert mask matrix with 256x256 dimension
    """
    if mask[int(mm_to_px(x_value)), int(mm_to_px(y_value))] == 0:
        return True
    else:
        return False


def gauss_fitting(X,C,X_mean,sigma):
    return C*exp(-(X-X_mean)**2/(2*sigma**2))


def smooth(x,window_len,window):
    """
    This function was made using a cookbook available here:
    https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html

    Smooth the data using a window with requested size
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    #if x.ndim != 1:
    #    raise ValueError, print("smooth only accepts 1 dimension arrays.")

    #if x.size < window_len:
    #    raise ValueError, print("Input vector needs to be bigger than window size.")

    #if window_len<3:
    #    return x


    #if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
    #    raise ValueError, print("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]

    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(),s,mode='valid')

    return y[(int(window_len/2)+1):-(int(window_len/2)-1)]


def straighten_single_cluster_rows(cluster_data, cluster_number, centroid_x, centroid_y, line_max, vmax, OutputPath, OutputName):
    #elist_cluster = np.loadtxt(elist_path, skiprows=2, delimiter=';')

    #centroid_x = mm_to_px(elist_cluster[cluster_number, 2])
    #centroid_y = mm_to_px(elist_cluster[cluster_number, 3])

    matrix = np.zeros([256, 256])

    x = [item[0] for item in cluster_data[:]]
    y = [item[1] for item in cluster_data[:]]
    energy = [item[2] for item in cluster_data[:]]

    new_x = x.copy()
    new_y = y.copy()

    row_centroid = []
    count = 0

    total_energy_row_values = []

    if (int(max(y)) - int(min(y))) > 20:
        print(f'Y max min difference is: {int(max(y)) - int(min(y))}')
        for i in range(int(min(y)), int(max(y))+1):
            indices = []
            x_row_values = []
            energy_row_values = []
            energy_position_nasobok_values = []

            indices.extend(idx for idx, value in enumerate(y) if int(value) == i)

            for indice in indices:
                x_row_values.append(x[indice])
                energy_row_values.append(energy[indice])
                energy_position_nasobok_values.append(x[indice] * energy[indice])
            
            row_centroid.append(sum(energy_position_nasobok_values) / sum(energy_row_values))

            for indice in indices:
                new_value = np.round_(new_x[indice] - (row_centroid[count] - centroid_x), decimals=0)
                if new_value < 0:
                    new_x[indice] = 0
                if new_value > 255:
                    new_x[indice] = 255
                else:
                    new_x[indice] = new_value
                #print(x[indice], new_x[indice], centroid_x, row_centroid[count], row_centroid[count] - centroid_x, np.round_(row_centroid[count] - centroid_x, decimals=0))
            count += 1

            total_energy_row_values.append(sum(energy_row_values))
    
        energy_sample = []
        sampling_length = 5

        #for i in range(int(sampling_length/2)):
        #    total_energy_row_values.append(0)
        #    total_energy_row_values.insert(0, 0)

        for i in range(len(total_energy_row_values) - sampling_length):
            energy_sample.append(sum(total_energy_row_values[i:i+sampling_length])/sampling_length)

        plot_x_data = np.linspace(0, int((len(total_energy_row_values) - sampling_length +1)), int(len(total_energy_row_values) - sampling_length), endpoint=True)

        for i in range(len(cluster_data[:])):
            matrix[int(new_x[i]), int(y[i])] += cluster_data[i][2]

        if (max(new_x) - min(new_x)) < (max(y) - min(y)):
            difference_position_x = np.abs((max(new_x) - min(new_x)) - (max(y) - min(y)))
        else:
            difference_position_x = 0
        if (max(y) - min(y)) < (max(new_x) - min(new_x)):
            difference_position_y = np.abs((max(y) - min(y)) - (max(new_x) - min(new_x)))
        else:
            difference_position_y = 0

        tickfnt = 16
        margin = 5

        plt.close()
        plt.cla()
        plt.clf()
        fig = plt.figure(constrained_layout=True, figsize=(10, 10))
        fig.suptitle('Cluster ' + str(cluster_number), fontsize=20)
        gs = fig.add_gridspec(2, 2)
        fig_ax1 = fig.add_subplot(gs[0,0])
        fig_ax1.set_title('Straightening test')
        fig_ax1.set_xlabel('X position [pixel]')
        fig_ax1.set_ylabel('Y position [pixel]')
        fig_ax1.set_xlim([min(new_x) - difference_position_x / 2 - margin, max(new_x) + difference_position_x / 2 + margin])
        fig_ax1.set_ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
        # Display image, `aspect='auto'` makes it fill the whole `axes` (ax3)
        im2 = fig_ax1.imshow(np.flip(np.rot90(matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=LogNorm(vmin=1, vmax=max(matrix.flatten())))
        # Create divider for existing axes instance
        divider2 = make_axes_locatable(fig_ax1)
        # Append axes to the right of ax3, with 20% width of ax3
        cax2 = divider2.append_axes("right", size="20%", pad=0.05)
        # Create colorbar in the appended axes
        # Tick locations can be set with the kwarg `ticks`
        # and the format of the ticklabels with kwarg `format`
        cbar2 = plt.colorbar(im2, cax=cax2, format="%.2f") #ticks=MultipleLocator(0.2)
        # Remove xticks from ax3
        #ax2.xaxis.set_visible(False)
        # Manually set ticklocations
        #ax2.set_yticks([0.0, 2.5, 3.14, 4.0, 5.2, 7.0])

        matrix = np.zeros([256, 256])

        for i in range(len(cluster_data[:])):
            matrix[int(x[i]), int(y[i])] += cluster_data[i][2]

        if (max(x) - min(x)) < (max(y) - min(y)):
            difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
        else:
            difference_position_x = 0
        if (max(y) - min(y)) < (max(x) - min(x)):
            difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
        else:
            difference_position_y = 0

        fig_ax2 = fig.add_subplot(gs[0,1])
        fig_ax2.set_title('Before straightening')
        fig_ax2.set_xlabel('X position [pixel]')
        fig_ax2.set_ylabel('Y position [pixel]')
        fig_ax2.set_xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
        fig_ax2.set_ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
        # Display image, `aspect='auto'` makes it fill the whole `axes` (ax3)
        im3 = fig_ax2.imshow(np.flip(np.rot90(matrix[::-1, :])), origin='lower', cmap='modified_hot', norm=LogNorm(vmin=1, vmax=max(matrix.flatten())))
        # Create divider for existing axes instance
        divider3 = make_axes_locatable(fig_ax2)
        # Append axes to the right of ax3, with 20% width of ax3
        cax3 = divider3.append_axes("right", size="20%", pad=0.05)
        # Create colorbar in the appended axes
        # Tick locations can be set with the kwarg `ticks`
        # and the format of the ticklabels with kwarg `format`
        cbar3 = plt.colorbar(im3, cax=cax3, format="%.2f") #ticks=MultipleLocator(0.2)
        # Remove xticks from ax3
        #ax2.xaxis.set_visible(False)
        # Manually set ticklocations
        #ax2.set_yticks([0.0, 2.5, 3.14, 4.0, 5.2, 7.0])

        #fig_ax3 = fig.add_subplot(gs[1, :])
        #fig_ax3.set_title(f'Averaged over {sampling_length * 55} $\mu$m, total E: {int(sum(total_energy_row_values))} keV')
        #fig_ax3.plot(plot_x_data, energy_sample[::-1])
        #fig_ax3.set_xlabel('Sample number [-]')
        #fig_ax3.set_ylabel('Mean energy in sample [keV]')
        #fig_ax3.set_ylim([0,vmax])

        windows=['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
        legend=['original signal']
        legend.extend(windows)

        fig_ax4 = fig.add_subplot(gs[1, :])
        fig_ax4.set_title(f'Averaged over {sampling_length * 55} $\mu$m, total E: {int(sum(total_energy_row_values))} keV')
        fig_ax4.plot(plot_x_data, energy_sample[::-1])
        fig_ax4.set_xlabel('Sample number [-]')
        fig_ax4.set_ylabel('Mean energy in sample [keV]')
        fig_ax4.set_ylim([0,max(energy_sample[::-1]) + 100])
        fig_ax4.legend(legend)

        for w in windows:
            smooth_value = smooth(total_energy_row_values[::-1],sampling_length,w)
            plot_x_data_smooth = np.linspace(0, len(smooth_value), len(smooth_value), endpoint=True)
            fig_ax4.plot(plot_x_data_smooth, smooth_value)

        plt.savefig(OutputPath + 'all_in_one_' + str(cluster_number) + '.png',
                    dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)

    return 1


def cluster_skeleton(cluster_data, cluster_number, OutputPath, OutputName):
    """
    Zhang’s method vs Lee’s method

    skeletonize [Zha84] works by making successive passes of the image, removing pixels on object borders. 
    This continues until no more pixels can be removed. The image is correlated with a mask that assigns each 
    pixel a number in the range [0…255] corresponding to each possible pattern of its 8 neighboring pixels. 
    A look up table is then used to assign the pixels a value of 0, 1, 2 or 3, which are selectively removed 
    during the iterations.

    skeletonize(..., method='lee') [Lee94] uses an octree data structure to examine a 3x3x3 neighborhood of a pixel. 
    The algorithm proceeds by iteratively sweeping over the image, and removing pixels at each iteration until 
    the image stops changing. Each iteration consists of two steps: first, a list of candidates for removal is assembled; 
    then pixels from this list are rechecked sequentially, to better preserve connectivity of the image.

    Note that Lee’s method [Lee94] is designed to be used on 3-D images, and is selected automatically for those. 
    For illustrative purposes, we apply this algorithm to a 2-D image.

    [Zha84] A fast parallel algorithm for thinning digital patterns, T. Y. Zhang and C. Y. Suen, Communications of the ACM, 
    March 1984, Volume 27, Number 3.
    [Lee94] (1,2) T.-C. Lee, R.L. Kashyap and C.-N. Chu, Building skeleton models via 3-D medial surface/axis thinning algorithms. 
    Computer Vision, Graphics, and Image Processing, 56(6):462-478, 1994.
    """
    matrix = np.zeros([256, 256])

    x = [item[0] for item in cluster_data[:]]
    y = [item[1] for item in cluster_data[:]]
    energy = [item[2] for item in cluster_data[:]]

    for i in range(len(cluster_data[:])):
        matrix[int(x[i]), int(y[i])] += cluster_data[i][2]

    if (max(x) - min(x)) < (max(y) - min(y)):
        difference_position_x = np.abs((max(x) - min(x)) - (max(y) - min(y)))
    else:
        difference_position_x = 0
    if (max(y) - min(y)) < (max(x) - min(x)):
        difference_position_y = np.abs((max(y) - min(y)) - (max(x) - min(x)))
    else:
        difference_position_y = 0

    margin = 5

    matrix = np.flip(np.rot90(matrix[::-1, :]))
    matrix = matrix.copy(order='C')

    skeleton = skeletonize(matrix)

    matrix_lee = np.where(matrix > 0, 1, matrix)
    skeleton_lee = skeletonize(matrix_lee, method='lee')

    plt.close()
    plt.cla()
    plt.clf()
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(14, 10),
                         sharex=True, sharey=True)

    ax = axes.ravel()
    ax[0].imshow(matrix, origin='lower', cmap='modified_hot')
    ax[0].set_xlabel('X position [pixel]')
    ax[0].set_ylabel('Y position [pixel]')
    ax[0].set_xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    ax[0].set_ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    ax[0].set_title('original', fontsize=20)

    ax[1].imshow(skeleton, origin='lower', cmap='modified_hot')
    ax[1].set_xlabel('X position [pixel]')
    ax[1].set_ylabel('Y position [pixel]')
    ax[1].set_xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    ax[1].set_ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    ax[1].set_title('skeleton', fontsize=20)

    ax[2].imshow(skeleton_lee, origin='lower', cmap='modified_hot')
    ax[2].set_xlabel('X position [pixel]')
    ax[2].set_ylabel('Y position [pixel]')
    ax[2].set_xlim([min(x) - difference_position_x / 2 - margin, max(x) + difference_position_x / 2 + margin])
    ax[2].set_ylim([min(y) - difference_position_y / 2 - margin, max(y) + difference_position_y / 2 + margin])
    ax[2].set_title('skeleton Lee', fontsize=20)

    fig.tight_layout()

    plt.savefig(OutputPath + OutputName + '_' + str(cluster_number) + '.png',
                    dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.1)