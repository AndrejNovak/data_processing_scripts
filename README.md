# Data Processing Scripts

This library of scripts/methods is developed for post-processing of Timepix/Timepix3/Timepix4 detectors with different sensors and their data outputs acquired from the Data Processing Engine (DPE) in development at Advacam s.r.o. Some methods were developed in cooperation with Carlos Granja and Lukas Marek. Before using these scripts for your need, please contact authors. Please don't forget to mention or use co-author citation in your publication. Thank you!

The library contains methods that are capable of reading both Elist and clog files from DPE, add new cluster calculated parameters, write new elist, output coincidence clusters info, create matrices from clogs, print energy and ToA of individual clusters, print energy and ToA of multiple clusters, combination of particle filtration and printing into matrix.

# Methods to implement:
1) Single particle tracks with histograms on top and right side of the track to indicate the energy deposited in each row and column. (In progress)

2) Plot 3D particle tract. Define a method based on Bergmann's article and use it for plotting.

3) In single particle tracks, draw a line along the track. This is just a first step for length determination. Not necessary, just for me as a practise.

4) Frame printing with a given number of clusters and fixed colorbar. For this frame, add two histograms on top of it
    - these histograms contain selected parameter, for example Cluster Height and the second Deposited Energy.
    - each part of the image can be also saved individually.
    - this can be made such that the main image will always be the deposited energy. The other option is to draw each cluster with one specific value of the whole cluster - its height, roundness,...

5) Create a figure that shows recalculated total deposited energy to dose that was deposited in the sensor based on the sensor material (this value depends on material density - Si, SiC, CdTe, GaAs, Diamond).

6) Update method **read_elist_filter** so that it does not require printed elist (write_elist() method), read file and load it into the memory. Usually this information is already present in the memory. Also compare the classic append method with numpy append method.

7) Update method **read_elist_filter_parameters**, so that it does not require a loaded and printed elist (write_elist() method). The results it uses are already loaded in the memory. 


# Description of classes and methods that are included

At the beginning of the library, new *cmap* is registered called *modified_hot*. This color map is used in most of the figures where deposited energy is displayed and maps displayed colors from 0 (transparent) to maximum value (black).

## class Cluster_filter
Lukas+Carlos, ADV, Prague, 8 Aug 2022
Cluster_filter class is used to filter events in elist based on given criteria. The class takes  two inputs in its constructor, "edges" and "indeces". The "edges" is a list of border values for a given cluster analysis (CA) parameter (PAR) and "indeces" is a list of column numbers in the elist of the given cluster analysis parameter (CA PAR). 

The class has one method called "pass_filter" that takes a variable "cluster_var" as input.  The method iterates over the range of indeces, and for each index it defines a lower edge and an upper edge using the elements in the edges list. It also defines a variable "i_var" which is  the element of indeces list at the current index. The method then compares the "i_var"-th element of the cluster_var to the defined lower and upper edge and returns true if the element is within  the range, otherwise false.

edges = border values for the given CA PAR
indeces = COL in elist of the given CA PAR, e.g. 4 for Energy

## class Cluster_filter_one_parameter
The same as the Cluster_filter - need to resolve which one to keep and whether they are completely the same.

## class Cluster_filter_multiple_parameter
The same as the Cluster_filter - need to resolve which one to keep and whether they are completely the same.

## class Cluster_filter_multiple_parameter_ratios
From Lukas' cluster_filter class; Carlos modified/extended, Aug 2022
This class is similar to the "cluster_filter_MULTI_PAR_RATIOS" class, but with a more detailed description of the class and its methods. It is a class that is used to filter events in a list (elist) based on multiple criteria including ratios of different parameters. The class takes four inputs in its constructor, "edges", "indeces", "edges_ratio" and "ind_pair_ratio". "edges" is a list of border values for a given cluster analysis parameter (CA PAR), "indeces" is a list of column numbers in the elist of the given CA PAR. "edges_ratio" is a list of border values for the ratio(s) of pairs of CA PARs, and "ind_pair_ratio" is a list of column numbers in the elist of pair of CA PAR for ratio(s). 

The class has one method called "pass_filter" that takes a variable "cluster_var" as input. The method first iterates over the range of indeces and for each index it defines a lower edge and an upper edge using the elements in the edges list. It also defines a variable i_var which is the element of indeces list at the current index. The method then compares the i_var-th element of the cluster_var to the defined lower and upper edge. If the element is within the range, the ok counter is incremented by 1, if not the method returns false. 

At the end of the loop, if the ok counter is equal to the length of indeces, it means that all the single CA PAR criteria passed. The method then iterates over the range of the ind_pair_ratio, for each index, it defines a lower edge and an upper edge for the ratio of the i_var-th element of the cluster_var to the defined lower and upper edge. If the ratio is within the range, the ok_rat counter is incremented by 1, if not the method returns false. 

edges = border values for the given CA PAR 
indeces = COL number in elist of the given CA PAR, e.g. 4 for Energy 
ind_pair_ratio = COL number in elist of pair of CA PAR for ratio(s)

## get_subdirectory_names(path_into_folder)
This method takes the full path to the directory for which you want the list of its subdirectories. It is a single line of code but one can use this method rather than always think of a way how to do this. This can be utilised for automation of data processing.

Example:
subdirectories = get_subdirectory_names('Q:/DPE_carlos_data_output/2022_12_VdG/2022_12_VdG_D05/')

## get_number_of_files(path_into_folder, file_extension)
This method returns the number of specific files in a given folder. Use for determination of the number of all clog or t3pa files. Can be extended to exclude MASK clogs from DPE output.

Example:
path = 'Q:/DPE_carlos_data_output/2022_12_VdG/2022_12_VdG_D05/00/Files/'
clog_count = get_number_of_files(path, 'clog')[0]
clog_names = get_number_of_files(path, 'clog')[1]

## print_out_elist(FileOutPath, filename, input_data)
**OLD METHOD, CURRENTLY NOT IN USE**
This is method that takes three inputs: FileOutPath, filename, and input_data. The method is used to print output data in a classic Elist format.

The method first checks if the FileOutPath directory exists, if it does not exist it creates the directory.  Then it opens a file with the specified filename in the FileOutPath directory and sets it as the standard output.  It then prints the input_data to the file and resets the standard output.

## print_out_mask(FilePath, filename)
You insert a matrix mask for a given detector and this method creates mask that can be used as a DPE input file mask. The mask can be exported from Pixet.

The other approach how to obtain simple input matrix can be achieved by acquiring 0.01s frame of a non-masked detector. The result of this acquisition is a matrix of zero values and non-zero values for noisy pixels. Then invert the frame (non-zero values -> 0, zero values -> 1) to obtain detector mask.

## read_clog(filename)
**WARNING** Use this method only for printing figures of total deposited energy. This clog accesses the data on a frame level and therefore is not suited for use in filtration results printing. The problem in this case is that when one of the coincidence clusters in the frame passes the filter, the whole frame is then passed to create_matrix method and disrupts the consecutive visual filter validation and verification. This is a huge problem mainly in TPX2 data acquired at simultaneous ToT & ToA operation mode (every event that is detected inherits the ToA value of the first registered event in the frame). **WARNING**

This method takes in the full filename of a .clog file as an input and is used to read through the file. The method opens the .clog file and reads all the lines of the file. It then uses a for loop to iterate through each line in the file. The method looks for lines that begin with "Frame" and extracts the Unix time and Acquisition time of each frame. These values are stored in lists called frames_unix_time and frame_times, respectively. The method also looks for lines that contain a specific pattern (using regular expressions) and extracts the x, y, ToT, and ToA values of each event in the frame. These values are stored in a nested list called all_values. The method returns three values: a list of Unix times of all frames, a list of Acquisition times of all frames, and a nested list of all the cluster data in the .clog file. You can access the Unix times of all frames by calling read_clog(filename)[0], the Acquisition times of all frames by calling read_clog(filename)[1], and the full cluster data by calling read_clog(filename)[2]. 

When using 'data = read_clog(FileInPath, filename)[2]', you can traverse the data on level of Frames, registered values (group of 4 values - [x, y, ToT, ToA]) and selected value from one of the four possible - x or y or ToT or ToA. 

To access first layer (selected frame) use: data[0] 
To access second layer (selected 4-group of selected frame) use: data[0][0] 
To access third layer (selected value from selected 4-group of selected frame) use: data[0][0][0]

## read_clog_clusters(filename)
**INFO** If you want to access data on a frame level and print total deposited energy, use read_clog() method. read_clog_testning method is designed for correlation with Elist and for correct printing of clusters that passed filtration parameters. Here, clusters are not divided into their respective frames but each individual cluster is separated. **INFO**

This method takes in the full filename of a .clog file as an input and is used to read through the file. The method opens the .clog file and reads all the lines of the file. It then uses a for loop to iterate through each line in the file. The method looks for lines that begin with "Frame" and extracts the Unix time and Acquisition time of each frame. These values are stored in lists called frames_unix_time and frame_times, respectively. The method also looks for lines that contain a specific pattern (using regular expressions) and extracts the x, y, ToT, and ToA values of each event in the frame. These values are stored in a nested list called all_values. The method returns three values: a list of Unix times of all frames, a list of Acquisition times of all frames, and a nested list of all the cluster data in the .clog file. You can access the Unix times of all frames by calling read_clog(filename)[0], the Acquisition times of all frames by calling read_clog(filename)[1], and the full cluster data by calling read_clog(filename)[2]. 

When using 'data = read_clog(FileInPath, filename)[2]', you can traverse the data on level of Frames, registered values (group of 4 values - [x, y, ToT, ToA]) and selected value from one of the four possible - x or y or ToT or ToA. 

To access first layer (selected frame) use: data[0] 
To access second layer (selected 4-group of selected frame) use: data[0][0] 
To access third layer (selected value from selected 4-group of selected frame) use: data[0][0][0]

## read_clog_multiple(FileInPath)
This method reads all clog files generated by the DPE excluding MASK clogs in the given directory. It utilizes the read_clog method that goes per cluster and reads Elist or ExtElist.txt.

Also contains commented method to write a Coincidence elist, a list which contains information about if and how many coincidence clusters each clog frame contains.

## get_elist_column(filename, col_name)
This method is used to extract a specific column from a file in Elist format, based on the exact name of the column. It takes in three inputs, the file path of the Elist, the name of the file, and the name of the column that needs to be extracted. It returns the data in the column in a python list format. The method first reads the first two lines of the file to get the names and units of all columns. It then iterates through the names of the columns and finds the column with the name that was passed as input. It then extracts the data in that column and returns it as a numpy array. 

From Elist extract a specific column based on the exact name of the column. Method returns a numpy array of data in python list format col_name = name of the variable from Elist 

Example, select column with Energy values: 
selected_column = get_column('path/to/Elist.txt', 'E')

## read_elist(filename):
**NOT NECESSARY - USE NUMPY LOADTXT** 
**np.loadtxt(filename, skiprows=2)** 

The read_elist method reads an Elist file and returns its data in the form of a list of lists, where the first list is the header, the second list is the units and the rest of the lists are the data. The user can then access the header and units by calling header, units, _ = read_elist('path/to/Elist.txt') or the data by calling 
data = read_elist('path/to/Elist.txt')[2]. 

Example - return header and units: 
header, units, _ = read_elist('path/to/Elist.txt') Example, 
return data only data = read_elist('path/to/Elist.txt')[2]

## read_elist_add_new_parameters(filename, column_number_pairs_for_ratios, header_text_new_columns, units_text_new_columns):
**PROBABLY UPDATED IN CARLOS read_elist_filter, check and delete if obsolete** 
Lukas 8 August 2022 

New version of read_elist to calculate new parameters and ratios old name "read_elist_make_ext_elist" 

This method reads an elist file, and calculates new columns which are the ratios of pairs of CA PAR (columns) specified in the col_num_pairs_for_ratios input. The new columns are added to the right of the original elist, and the new header and units for these new columns are specified in header_txt_new_cols and units_txt_new_cols inputs. The method returns the elist with the added columns, where the output is split into three objects: the header, the units, and the data. The method also prints the number of all clusters processed and the line number of the first and second row. 

Example: 
filename = elist_txt_name 
column_number_pairs_for_ratios = [4,7,9,7]    # Energy, Size, BorderPixel, Size 
header_text_new_columns = ['E/Size', 'BorderPixel/Size'] 
units_text_new_columns = ['keV/px', 'a.u.']

## read_elist_filter_parameters(filename, new_filter=None)
New read_elist method to include option to filter events (Lukas 8 August 22) 

This method reads an elist file (which is the calibrated output of DPE_CP) and applies a filter to the clusters based on certain CA PARs (cluster analysis parameters). The method takes in several arguments: 

filename - name of the elist file, 
column_number_pairs_for_ratios - a list of column numbers of the CA PARs that are used to create new columns of ratios. For example, [4,7,9,7] would use the values in column 4, 7, 9 and 7 to calculate the ratios E/A, BordPx/A, etc.
header_text_new_columns - a list of headers for the new columns of ratios that are created, 
units_text_new_columns - a list of units for the new columns of ratios that are created, 
new_filter - an instance of the Cluster_filter_multiple_parameter class, which is used to filter the clusters based on certain CA PARs. If no filter is provided, the method will not filter the clusters and will only add new columns of ratios. 

The method reads the elist file line by line and processes each line accordingly. It first checks if the line is one of the first two rows (the header and units rows), in which case it adds the new column headers. For the rest of the lines, it checks if the new_filter is provided, and if it is, it applies the filter to the cluster variables. If the cluster passes the filter, it adds a value of 1 in the new column, otherwise it adds a value of 0. It also keeps track of the number of clusters, the number of clusters that pass the filter, and the number of clusters that fail the filter. Once all lines have been processed, the method returns the updated elist. 

A new column is appended to the Elist: 
Cluster passed the filter = 1 
Cluster failed the filter = 0 

Example: 
One filter for Height parameter - [100,500],[8] 
Two filters for Height and Size - [100,500,10,30], [8,7] 

The output is the same elist, with new column appended at the end + 1 column.

## read_elist_filter(filename, column_number_pairs_for_ratios, header_text_new_columns, units_text_new_columns, new_filter=None):
Carlos Granja, 23 August 2022 
old name "read_elist_make_ext_filter" 
**NOTE** this is probably updated version of read_elist_add_new_parameters, delete the old one if it is the case **NOTE**

This method reads an elist file (output from DPE_CP), calculates ratios of pairs of CA PAR and adds them as new columns to the elist. Then, it applies a filter to the clusters based on the CA PAR and the new ratios, and adds a new column indicating whether the cluster passed or failed the filter. The output is the same elist with the added new columns at the right. The method takes the following inputs: 

filename - path to the elist file 
column_number_pairs_for_ratios - a list of integers representing the column numbers of the CA PAR that will be used to calculate ratios. The list should contain pairs of integers, where the first integer of each pair is the numerator and the second integer is the denominator of the ratio. 
header_text_new_columns - a list of strings representing the names of the new columns with the ratios. The length of this list should be the same as the number of pairs in column_number_pairs_for_ratios. 
units_text_new_columns - a list of strings representing the units of the new columns with the ratios. The length of this list should be the same as the number of pairs in column_number_pairs_for_ratios. 
new_filter - an object of a class that defines the filter to be applied to the clusters. The class should have a method pass_filter(cluster_variable) that takes the list of variables of a cluster as input and returns a Boolean indicating whether the cluster passes or fails the filter. If no filter is desired, set new_filter to None. 
Cluster passed the filter = 1 
Cluster failed the filter = 0 

Example: 
filename = elist (output of DPE CP, stored in Files DIR output) 
column_number_pairs_for_ratios = [4, 7, 9, 7]  # Energy, Size, BorderPixel, Size 
header_text_new_columns = ['Energy/Size', 'BorderPixel/Size'] 
units_text_new_columns = ['keV/px', 'a.u.'] 
new_filter = [90, 5000, 4500, 5.E5, 0.9, 1.7, 4, 300, 30, 5000], [8, 4, 10, 7, 15]) # Height Energy Roundness Size, Energy/Size

## write_elist(filename, header, units, data)
This method writes a file in a specific Elist format. The method takes in four parameters: filename_out, header, units, and data. The filename_out is the name of the file to be written. The header and units are lists of strings that are written as the first two lines in the file. The data parameter is a 2D list, where each row represents a line in the file, and each element in the row represents a column. The method writes each row of data as a string, separated by semicolons, and ends each line with a newline character. The method uses the python built-in open method to open the file in write mode.

## write_coincidence_elist(filename, OutputPath, OutputName)
A list which contains information about if and how many coincidence clusters each clog frame contains. The output is divided into three columns of values: EventID, Count of coincidence events, Boolean value whether it is a Coincidence event.

## create_matrix_tpx3_t3pa(clog, number_of_clusters)
This method creates a 256x256 matrix from TPX3 format of data [X, Y, ToT, ToA] for the given number of clusters/frames depending on the used read_clog method. The output is a matrix with summed deposited energy.

**TO DO** 
Can be simply extended to ouput also ToA matrix:
matrix_energy = np.zeros([256, 256])
matrix_toa = np.zeros([256, 256])

for i in range(len(clog)):
    cluster_size_clog = len(clog[i][:])
    for j in range(cluster_size_clog):
          x, y = int(clog[i][j][0]), int(clog[i][j][1])
          matrix_energy[x, y] += clog[i][j][2]
          matrix_toa[x, y] += clog[i][j][3]

return matrix_energy, matrix_toa 
**TO DO**

## create_matrix_filter_tpx3_t3pa(filtered_elist, clog, number_column_filter, number_frames)
This method creates a filter for a 2D plot of a detector pixel matrix, specifically for TPX3 t3pa data and its clog output with short time frames (e.g. 100 ns). The method takes in three parameters: filtered_elist, clog, and number_frames. The filtered_elist is the output of a DPE_CP elist with an added column from a cluster filter. The clog is the output of a DPE_CP calibration. The number_frames is the number of frames to integrate, which is either the cluster number (for TPX3 t3pa data) or the frame number (for raw clog frame data). 

The method creates several matrices: matrix_energy_all, matrix_toa_all, matrix_energy_ok, matrix_toa_ok, matrix_energy_bad, and matrix_toa_bad. The method iterates over a list of random numbers and for each iteration, it retrieves the size of the cluster from the clog, and for each element in the cluster, it increments the corresponding element (Energy and ToA value) in the matrices. The method also keeps track of multiplets, which are clusters that have more than one pixel. The method returns the six matrices created. 

Description: 
elist_filtered - the DPE output elist with the added COL from cluster_filter, 
clog - clog output of DPE, 
number_frames - number of frames to integrate, to add to merged plot from the beginning, from frame number zero in the clog file output of DPE for TPX3 data a frame is created every 100 ns. For TPX3 t3pa data - input number_frames is the cluster - event number. For raw clog frame data - number_frames is the frame number.

## create_matrix_filter_tpx3_t3pa_for_filtering(filtered_elist, clog, number_of_particles)
This method creates a filter for a 2D plot of a detector pixel matrix, specifically for TPX3 t3pa data and its clog output with short time frames (e.g. 100 ns). The method takes in three parameters: filtered_elist, clog, and number_frames. The filtered_elist is the output of a DPE_CP elist with an added column from a cluster filter. The clog is the output of a DPE_CP calibration. The number_frames is the number of frames to integrate, which is either the cluster number (for TPX3 t3pa data) or the frame number (for raw clog frame data). 

The method creates several matrices: matrix_energy_all, matrix_toa_all, matrix_energy_ok, matrix_toa_ok, matrix_energy_bad, and matrix_toa_bad. The method iterates over a list of random numbers and for each iteration, it retrieves the size of the cluster from the clog, and for each element in the cluster, it increments the corresponding element (Energy and ToA value) in the matrices. The method also keeps track of multiplets, which are clusters that have more than one pixel. The method returns the six matrices created. 

Description: 
elist_filtered - the DPE output elist with the added COL from cluster_filter, 
clog - clog output of DPE, 
number_frames - number of frames to integrate, to add to merged plot from the beginning, from frame number zero in the clog file output of DPE for TPX3 data a frame is created every 100 ns. For TPX3 t3pa data - input number_frames is the cluster - event number. For raw clog frame data - number_frames is the frame number.

## create_matrix_filter_tpx_frame(filtered_elist, clog, number_column_filter, number_particles):
Carlos + Lukas + Andrej, 8 August 2022 
old name: create_matrix_filter_tpx_f 

This method creates a filter for a 2D plot of a detector pixel matrix, specifically for TPX frame data and its clog output with frames. The method takes in three parameters: filtered_elist, clog, and number_particles. The filtered_elist is the output of a DPE_CP elist with an added column from a filter. The clog is the output of a DPE_CP calibration. The number_particles is the number of events to integrate, which is either the cluster number (for TPX frame data) or the frame number (for raw clog frame data). 

The method creates several matrices: matrix_E_all, matrix_E_ok, and matrix_E_bad. The method iterates over a list of random numbers and for each iteration, it retrieves the size of the cluster from the clog, and for each element in the cluster, it increments the corresponding element in the matrices. The method also keeps track of multiplets, which are clusters that have more than one pixel fired. The method returns the three matrices created. 

Example: 
filtered_elist -  the DPE output elist with additional column from filter, 
clog - the clog output of DPE, 
number_particles - number of events to integrate, to add to merged plot from beginning, from frame number zero in the clog file output of DPE for TPX data frames. For TPX frame data ToT - input number_particles is the cluster i.e. event number. For raw clog frame data - number_particles is the frame number.

## calibrate_frame(a_path, b_path, c_path, t_path, matrix)
**REWRITEN FROM CARLOS' MATLAB SCRIPT** 

This method calibrates an uncalibrated matrix to energy using input calibration matrices. The method takes in five parameters: a_path, b_path, c_path, t_path and matrix for the calibration. The a_path, b_path, c_path and t_path are the names or full paths of the respective calibration matrices. The matrix is the uncalibrated input. 

The method loads the calibration matrices from the provided paths using the numpy np.loadtxt(). It then creates a new matrix called tot, which is the calibrated energy matrix. It iterates over the elements of the input matrix, and for each element, if the value of matrix[i, j] > 0.8 (??why??), it uses the calibration matrices to recalculate the corresponding element in the matrix. Otherwise, it sets the corresponding element of the tot matrix to 0. It then returns the tot matrix.

## print_figure_energy(matrix, vmax, title, OutputPath, OutputName)
Old name: print_fig_E

Method to print a figure of deposited energy in logarithmic colorbar scale.

## print_figure_energy_iworid_2023(matrix, vmax, title, OutputPath, OutputName)
**WARNING** DELETE THIS METHOD **WARNING**

## print_figure_toa(matrix, vmax, title, OutputPath, OutputName)
Old name: print_fig_ToA

Method to print a figure of ToA values in linear scale.

## parameter_filter(data_column, min_value, max_value)
This method is used to filter data based on a specific column's value. The method takes in three parameters: data_column, min_value, and max_value. The data_column parameter is a list of values for a specific column of data, min_value is the minimum acceptable value for the column's data, and max_value is the maximum acceptable value for the column's data. 

The method first creates two empty lists passed and bad, which will be used to store the line numbers of the data that pass the filter and those that don't pass the filter, respectively. Then it iterates over the data_column and compares each value to the min_value and max_value. If the value is greater than or equal to min_value and less than or equal to max_value, the method appends the index of that value to the passed list. If the value is not within the acceptable range, the method appends the index of that value to the bad list. It then returns the passed and bad lists. 

Example: 
For data_column use method get_column(filename, col_name) 
parameter_filter(get_column('Elist.txt', 'E'), 1, 1E3)

## create_matrix_tpx3_old(data, number_frames, random)
Old name: create_matrix 

This method creates a 2D plot of a detector pixel matrix using the data input, and a number of frames to integrate. The method takes three parameters: data, number_frames, and random. The data parameter is the clog calibration output of DPE_CP, number_frames is the number of frames to integrate from the beginning, and random is a string that determines whether or not random numbers are chosen. 

The method first creates a list of random numbers, either by using the random.sample() method or by creating a range of numbers based on the number_frames parameter. It then creates two matrices, matrix_energy and matrix_toa, that are initially filled with zeroes. 

The method then iterates over the random_numbers list, and for each iteration, it retrieves the size of the cluster from the data, and for each element in the cluster, it increments the corresponding element in the matrices. The method also keeps track of multiplets, which are clusters that have more than one pixel fired. The method returns the two matrices created. 

The matrix_energy is the sum of energies in each pixel, and matrix_toa is the ratio of ToA of each pixel to the maximum ToA in the cluster. 

Description:
data - the clog output of DPE, 
number_frames - number of frames to integrate, to add to merged plot from beginning, from frame number zero in the clog file output of DPE. For TPX3 data a frame is created every 100 ns. For TPX3 t3pa data - input number_frames is the cluster - event number. For raw clog frame data - number_frames is the frame number. 
random - boolean that determines whether random frames are chosen or not.

## print_figure_single_cluster_energy(clog_path, frame_number, vmax, title, OutputPath, OutputName)
Old name: plot_single_cluster_ToT

**WARNING** Uses read_clog method that returns coincidences or frames in case of TPX2 data processing. **WARNING**

Method that is used to print single frame/cluster (depending on the read_clog method that is used). The frame is centered for the displayed data in a square format.

## print_figure_single_cluster_energy_smooth(clog_path, frame_number, vmax, title, OutputPath, OutputName)
Method that takes single cluster and returns a figure of deposited energy that is smoothened by the Gaussian interpolation method.

![test_figure_0|320x271,50%](https://github.com/AndrejNovak/data_processing_scripts/assets/20739208/6055887a-1af3-4f33-9922-20a3e1dbc6ed)
![test_figure_0_smooth|320x271,50%](https://github.com/AndrejNovak/data_processing_scripts/assets/20739208/ea0447b3-6831-42cb-8b91-cf8b880300d5)

## print_figure_single_cluster_energy_histograms(clog_path, frame_number, vmax, title, OutputPath, OutputName)
**WARNING** Uses read_clog method that returns coincidences or frames in case of TPX2 data processing. **WARNING**

Method that is used to print single frame/cluster (depending on the read_clog method that is used). The frame is centered for the displayed data in a square format and two histogramns of deposited energy for each row/column is on its right side/top.

## print_figure_single_cluster_toa_tpx3(clog_path, frame_number, vmax, title, OutputPath, OutputName)
Old name: plot_single_cluster_ToA
**WARNING** This method is probably no longer necessary. **WARNING**

Method used for Timepix3 and Timepix2 detectors (mode of operation with both ToT and ToA). Returns a figure of ToA values for a given frame/cluster.

## print_figure_single_cluster_toa_tpx(clog_path, frame_number, vmax, title, OutputPath, OutputName)
Old name: plot_single_cluster_ToA
    
For Timepix and Timepix2 detectors operated in ToA mode. Returns a figure of ToA values for a given frame/cluster.

## plot_single_cluster_toa_gaas(OutputPath, clog_path, frame_number, indicator, vmax)
**WARNING** This is a plot method that I used for Elitech 2023 school article, it is not really published and this method serves no other method, delete this. **WARNING**

## gaas_core_halo_study(FileInPath, FileInName, FileOutPath, FileOutName, angle, max_toa_diff, num_of_frames)
**WARNING** This is a plot method that I used for Elitech 2023 school article, it is not really published and this method serves no other method, delete this. **WARNING**

## create_matrix_tpx3(filename, frame_number)
This method creates a 2D plot of a detector pixel matrix for Timepix3 and Timepix2 detectors using the data in a clog file and a specific frame number. The method takes two parameters: filename and frame_number. The filename parameter is the path to the clog file, and the frame_number parameter is the specific frame from which to draw data from the clog file. 

The method first reads the clog file using the read_clog() method and assigns the data to the variable clog. Then it creates two matrices, matrix_tot, matrix_toa, matrix_counts that are initially filled with zeroes. 

The method then iterates over the data in the clog file, and for each iteration, it retrieves the x and y coordinates and the ToT and ToA values of the pixel. It then increments the corresponding element in the matrix_tot and assigns the ToA value to the corresponding element in the matrix_toa. The method returns the three matrices created, matrix_tot, matrix_toa and matrix_counts. 

Description: 
filename - clog file of the DPE output, 
frame_number - frame to be drawn from the clog file.

## create_matrix_tpx(filename, frame_number, what_type)
**NOTE** Get rid of "what_type" and update this method to return both matrices. **NOTE**

This method creates a 2D plot of a detector pixel matrix for Timepix detectors using the data in a clog file and a specific frame number. The method takes three parameters: filename, frame_number, and what_type. The filename parameter is the path to the clog file, the frame_number parameter is the specific frame from which to draw data from the clog file, and the what_type parameter is a string that indicates whether to create a matrix of "ToT" or "ToA" values. 

The method first reads the clog file using the read_clog() method and assigns the data to the variable clog. Then it creates a matrix, matrix, that is initially filled with zeroes. 

The method then iterates over the data in the clog file, and for each iteration, it retrieves the x and y coordinates and the ToT and ToA values of the pixel. It then increments the corresponding element in the matrix with the value of ToT or assigns the ToA value to the corresponding element in the matrix depending on the value of what_type. The method returns the matrix created. 

Description: 
filename - clog file of the DPE output, 
frame_number - frame to be drawn from the clog file, what_type - to get info whether ToT or ToA is being processed, input either 'ToT' or 'ToA'.

## scatter_histogram_for_function(clog_path, frame_number, x, y, ax, ax_histx, ax_histy)
**NOTE** Return to this method to revise, whether it is needed to be included here. It is used in method **print_figure_single_cluster_count_histograms** that aims to print single histogram and on its sides the histograms with respect to the deposited energy in rows/columns. **NOTE**

## mm_to_px(value_in_mm)
Simple method used to convert values from milimeters to pixels. The DPE v1.0.5 returns X and Y vylues in milimeter format, while in DPE v1.0.6 I expect that these position values will be in pixels (my assumption is based on the latest version of Clusterer).

## check_if_position_is_in_mask(mask, x_value, y_value)
This method checks whether the given X or Y position is in mask. It can be used only for 1 px clusters only. Insert mask matrix with 256x256 dimension.

## gauss_fitting(X,C,X_mean,sigma)
**NOTE** Find where it is used and whether it is still necessary. Probably used in measurements of Temporal stability and position of 59.6 keV peak in acquired data from C05, L06 and FitPIX detector (measured some time at the beginning of the 2023 year). **NOTE**

## smooth(x,window_len,window)
This method was made using a cookbook available here: 
https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html 

Smooth the data using a window with requested size This method is based on the convolution of a scaled window with the signal. The signal is prepared by introducing reflected copies of the signal (with the window size) in both ends so that transient parts are minimized in the begining and end part of the output signal. 

input: 
x: the input signal 
window_len: the dimension of the smoothing 
window; should be an odd integer window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman' flat window will produce a moving average smoothing. 

output: the smoothed signal 

Example: 
t=linspace(-2,2,0.1) 
x=sin(t)+randn(len(t))*0.1 
y=smooth(x) 

TODO: the window parameter could be the window itself if an array instead of a string 
NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.

## straighten_single_cluster_rows(cluster_data, cluster_number, centroid_x, centroid_y, line_max, vmax, OutputPath, OutputName):
**WARNING** Contains a constraint on the minimal Y difference between the max Y and min Y values (to pre-select events with larger path in the detector, presumably protons). **WARNING**

This is a simple method that takes a single cluster, its centroid, then for each row of the cluster, row centroid is calculated. For each row its position is then changed based on the difference between the total centroid and row centroid. As a result, the particle cluster is then straightened. This can be used for protons or other particles with low curvature of the track; however, it can not be used for events on the sensor border, fragmentation events or high curvature events such as electrons.

Returns a figure with cluster before straightening, after and the smoothened energy deposited in rows with sampling length of 5 values.

## cluster_skeleton(cluster_data, cluster_number, OutputPath, OutputName)
Zhang’s method vs Lee’s method 

skeletonize [Zha84] works by making successive passes of the image, removing pixels on object borders. This continues until no more pixels can be removed. The image is correlated with a mask that assigns each pixel a number in the range [0…255] corresponding to each possible pattern of its 8 neighboring pixels. A look up table is then used to assign the pixels a value of 0, 1, 2 or 3, which are selectively removed during the iterations. 

skeletonize(..., method='lee') [Lee94] uses an octree data structure to examine a 3x3x3 neighborhood of a pixel. The algorithm proceeds by iteratively sweeping over the image, and removing pixels at each iteration until the image stops changing. Each iteration consists of two steps: first, a list of candidates for removal is assembled; then pixels from this list are rechecked sequentially, to better preserve connectivity of the image. 

Note that Lee’s method [Lee94] is designed to be used on 3-D images, and is selected automatically for those. For illustrative purposes, we apply this algorithm to a 2-D image. 

[Zha84] A fast parallel algorithm for thinning digital patterns, T. Y. Zhang and C. Y. Suen, Communications of the ACM, March 1984, Volume 27, Number 3. 
[Lee94] (1,2) T.-C. Lee, R.L. Kashyap and C.-N. Chu, Building skeleton models via 3-D medial surface/axis thinning algorithms. Computer Vision, Graphics, and Image Processing, 56(6):462-478, 1994.

**WARNING** Contains a constraint on the minimal Y difference between the max Y and min Y values (to pre-select events with larger path in the detector, presumably protons). **WARNING**

For a given cluster returns figure of original cluster, its skeleton using Zha84 and Lee94 method.

## get_neighbors_of_matrix_element(cluster_matrix, radius, row_number, column_number)
Given matrix coordinate X Y, the method returns its neighbour values, a matrix of 3x3 dimension when distance of 1 pixel is investigated. The distance from point is given by the radius (cuboid mask).

## cluster_skeleton_ends_joints(cluster_data, cluster_number, OutputPath, OutputName)
Method that utilizes get_neighbors_of_matrix_element() method to investigate particle skeleton in order to determine the end/entry and joint points of the cluster skeleton.
