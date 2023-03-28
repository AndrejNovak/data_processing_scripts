from DPE_functions import *

FileInPath = r'Q:\DPE_carlos_data_output\2022_06_krakow\B3\H09_TPX3_Si500\07\Files\\'

read_clog_multiple(FileInPath)

#FilePath = r'Q:\timepix_config_calib_files\minipix_tpx2\X00-W1698 500 um Si\\'
#filename = 'X00_mask.txt'

#print(check_if_position_is_in_mask(FilePath, filename, 12, 12))

####### TEST OF NEW CLOG READING #########
vmax = 1E3
title = 'Test'
OutputName = 'test_figure'
OutputPath = r'C:/Users/andrej/Documents/FEI/'

clog_path = r'C:\Users\andrej\Documents\FEI\ClusterLog_smooth_cluster.clog'
print_figure_single_cluster_energy_smooth(clog_path, 0, vmax, title, OutputPath, OutputName)

clog_path = r'C:\Users\andrej\Documents\FEI\ClusterLog_test.clog'
vmax = 1E3
title = 'Test'
OutputName = 'test_figure'
OutputPath = r'C:/Users/andrej/Documents/FEI/'

####### TEST OF NEW CLOG READING #########

"""
clog_path = r'Q:\DPE_carlos_data_output\2021_10_krakow\Si500um\06\10\Files\ClusterLog.clog'
elist_path = r'Q:\DPE_carlos_data_output\2021_10_krakow\Si500um\06\10\Files\ExtElist.txt'
vmax = 1E3
title = 'Test'
OutputPath = r'C:/Users/andrej/Documents/FEI/'
OutputName = 'test_figure'
OutputNameElist = 'Elist_coincidence.txt'

#print_figure_single_cluster_energy_histograms(clog_path, 1, vmax, title, OutputPath, OutputName)
#print_figure_single_cluster_count_histograms(clog_path, 9, OutputPath, OutputName)

#write_elist_add_coincidence(elist_path, OutputPath, OutputNameElist)


am_elist_data = np.loadtxt('E:\\DPE_andrej_data_output\\2023_02_24_Am241_time_spectra\\X00_tpx2\\000\\Files\\ExtElist.txt', skiprows=2, delimiter=';')

filtered_data = np.empty([0])

for i in range(1000000):
    if am_elist_data[i,7] == 1:
        filtered_data = np.append(filtered_data, am_elist_data[i,4])

tickfnt=12

plt.close()
plt.clf()
plt.cla()
plt.hist(filtered_data[:,4], bins=2048, histtype = 'step', linewidth=1.75)
plt.xlim(left=0, right=200)
plt.ylim(bottom=1, top=1E6)
plt.yscale('log')
plt.xlabel('Energy [keV]', fontsize=tickfnt)
plt.ylabel('Particles [cnt]', fontsize=tickfnt)
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.legend(loc='upper right')
plt.show()
#plt.savefig('X00_Am241_1ps_clusters.png', dpi=300, transparent=True, bbox_inches="tight", pad_inches=0.01)






#---------------------------------
#Input
#---------------------------------

file_hist_path = "../devel/in/hist/"
file_hist_base_name = "Hist1D_E_EqBin_Total"

#---------------------------------
#Functions 
#---------------------------------

#Load data from file with name and path file_in_pathName -> returns two lists with X and y positions of points
def load_hist(file_in_path, file_in_base_name, fill_sparse_export=True, file_in_end_data = ".hist", file_in_end_info = ".hist_info"):

     bin_conts=[]
     low_edges=[]
     
     if path.exists(file_in_path + file_in_base_name + file_in_end_data):
          file_in = open(file_in_path + file_in_base_name + file_in_end_data)
          line_num = 0
          bin_width = 0
          curr_low_edge = 0
          pre_low_edge = 0

          for line in file_in:
               line_num += 1

               line = line.replace('\n', '')
               line = line.replace('\r', '') 
               if(len(line) == 0): continue
               line_list = re.split("\t", line)

               if(len(line_list)<2): continue

               curr_low_edge = float(line_list[0])
               curr_bin_conts = float(line_list[1])

               if line_num == 2: bin_width = curr_low_edge - pre_low_edge

               #If there is a gap in the data -> fill it with 0
               if(bin_width != 0 and fill_sparse_export):
                    while (curr_low_edge - pre_low_edge)/bin_width > 1:
                         pre_low_edge += bin_width
                         bin_conts.append(0)
                         low_edges.append(pre_low_edge)

               bin_conts.append(curr_bin_conts)
               low_edges.append(curr_low_edge)

               pre_low_edge = curr_low_edge

          file_in.close()

     else: 
          print("Could not open data file!", file_in_path + file_in_base_name)
          return ([-1],[-1])    

     return (low_edges, bin_conts)

#Plot hist 1D and save it
def plot_hist1d(low_edges,bin_conts, legend_data="", color="C0"):

     plt.hist(low_edges, low_edges, weights=bin_conts, color=color, histtype='step',label=legend_data, linewidth=0.8)


#---------------------------------
#Main processing part
#---------------------------------

if __name__ == '__main__':

     bin_conts, low_edges = load_hist(file_hist_path, file_hist_base_name, True)
     plot_hist1d(bin_conts, low_edges, "data", "C0")

     # plt.ylim(ymin=1, ymax = 2) #Set image range to nicely fit also the legend
     plt.xlim(xmin=-1e2, xmax = 1.5e4) #Set image range to nicely fit also the legend
     plt.legend(title="Legend") #Add legend into plot
     plt.grid(visible = True, color ='grey',  linestyle ='-.', linewidth = 0.5,  alpha = 0.6) #Grid on background
     plt.xlabel("X", fontsize=12)  #Set label of X axis
     plt.ylabel("Y", fontsize=12)  #Set label of Y axis
     plt.title("Title")    #Set title
     plt.yscale('log')
     # plt.xscale('log') 

     plt.show()





     # ELIST PY

     #---------------------------------
#Input variables
#---------------------------------

file_in_path_name = "./output/p_70MeV_60deg/extelist.txt"             #File with input data
file_out_path_name = "./output/p_70MeV_60deg/hist1D_LET.png"        #File for output image

label_x = "Count [-]"				#Label on X axis
label_y = "Time [ns]"					#Label on Y axis
title = "Time evolution"     			#title of the graph
legen_data = "Time from elist"			#Label in the legend for the data

sens_thick = 	500
part_dir = 		60
E_dep_mean = 	1960

#---------------------------------
#Functions 
#---------------------------------

#Load data from file with name and path file_in_path_name -> returns two lists with X and y positions of points
def load_file_column(file_in_path_name, index, minimum = 0, maximum = 0):
	list_column=[]
	line_num = 0

	mean = 0
	std = 0
	n = 0

	do_range = True
	if minimum == maximum: do_range = False

	if path.exists(file_in_path_name):

		file_in = open(file_in_path_name)

		for line in file_in:

			line_num += 1
			if(line_num <= 2): continue

			line = line.replace('\n', '')
			line_list = re.split(";", line)

			if len(line_list) >= index:
				num = float(line_list[index])

				if do_range and (num > maximum or num < minimum):
					continue
			
				n += 1
				mean += num
				std += num*num
				list_column.append(num)

		file_in.close()

	else: print("File " + file_in_path_name + " does not exits.")

	mean = mean/float(n)

	if n > 1:
		std = math.sqrt((std - mean*mean*float(n))/float(n - 1));
	else:
		std = 0

	print("--------------------")
	print("Column:\t", index)
	print("N:\t", n)
	print("Mean:\t", mean)
	print("Std:\t", std)

	return (list_column, mean, std)

#Minimum and maximum value in list
def GetMinMaxListVal(List, Min = 666, Max = -666):
	if(len(List) == 0):
		return (666,-666) 

	if Min >= Max:
		Min = List[0]
		Max = List[0]

	for i in range(len(List)):
		if List[i] > Max:
			Max = List[i]
		if List[i] < Min:
			Min = List[i]
	return (Min,Max)

#Plot 1D graph with linear fuction defined with A_Slope and B_Shift
def PlotGraph1D(file_out_path_name, ListX, ListY, title, label_x, label_y):
	#Main plot function
	plt.plot(ListX,ListY, color='gainsboro', linewidth=0,
		marker='o', markerfacecolor='dodgerblue', markeredgewidth=0,
		markersize=1,label=legen_data)

     #Additional settings 
	plt.xlabel(label_x)
	plt.ylabel(label_y)
	plt.title(title)
	#plt.text(10, 144, r'an equation: $E=mc^2$', fontsize=15)
	(Ymin,Ymax) = GetMinMaxListVal(ListY)
	plt.ylim(ymin=Ymin-(Ymax-Ymin)*0.2, ymax = Ymax+(Ymax-Ymin)*0.4)
	#plt.legend(bbox_to_anchor=(0.01,0.9), loc="center left", borderaxespad=1, frameon=False)
	plt.legend(fontsize=10)
	plt.grid(visible = True, color ='grey',  linestyle ='-.', linewidth = 0.5,  alpha = 0.6)

	#fig = plt.gcf()
	#fig.set_size_inches(14.5, 8.5)

	#Save and close file
	plt.savefig(file_out_path_name, dpi=600)
	#plt.close()
	plt.show()

#Plto 1D histogram from data
def plot_1Dhist(elist, n_bins, x_range):
	
	if len(elist) <=- 0: return 1
	plt.hist(elist,bins=n_bins, range=x_range, histtype='step', linewidth=0.8)


	#plt.ylim(ymin=1e-4, ymax = BinContMax*3) #Set image range to nicely fit also the legend
	#plt.xlim(xmin=4, xmax = 1.2e4) #Set image range to nicely fit also the legend
	plt.grid(visible = True, color ='grey',  linestyle ='-.', linewidth = 0.5,  alpha = 0.6) #Grid on background
	#plt.xlabel(label_x, fontsize=12)  #Set label of X axis
	plt.ylabel("N [-]", fontsize=12)  #Set label of Y axis
	#plt.title(title)    #Set title
	#plt.yscale('log')
	#plt.xscale('log')


	plt.show() 
	return 0

def plot_hist1d_auto(elist, mean, std, factor = 3):
	plot_1Dhist(elist, 200, [mean - factor*std,mean + factor*std])

#---------------------------------
#Main processing part
#---------------------------------

# (ListComulmTime) = load_file_column(file_in_path_name,5)
# (ListComulmE) = load_file_column(file_in_path_name,4)
# (ListComulmX) = load_file_column(file_in_path_name,2)

# print(GetMinMaxListVal(ListComulmE))

# ListX = []

# FirstTime = ListComulmTime[0]

# for x in range(len(ListComulmTime)):
# 	ListX.append(x);
# 	ListComulmTime[x] -= FirstTime
# 	print(x,"\t",ListComulmTime[x])

# PlotGraph1D(file_out_path_name, ListX,ListComulmTime, title, label_x, label_y);

list_LET, LET_mean, LET_std = load_file_column(file_in_path_name, 26, 1.3, 3.5)
list_E, E_mean, E_std = load_file_column(file_in_path_name, 4, 1300, 3000)
list_L3D, L3D_mean, L3D_std = load_file_column(file_in_path_name,24, 800, 1200)
list_L2D_corr, L2D_corr_mean, L2D_corr_std = load_file_column(file_in_path_name,23, 10, 20)

# plot_hist1d_auto(list_LET, LET_mean, LET_std)
# plot_1Dhist(list_E, 200, [E_mean - 3*E_std,E_mean + 3*E_std])
# plot_1Dhist(list_L3D, 200, [L3D_mean - 3*L3D_std,L3D_mean + 3*L3D_std])
# plot_1Dhist(list_L2D_corr, 200, [L2D_corr_mean - 3*L2D_corr_std,L2D_corr_mean + 3*L2D_corr_std])

L2D_est = (sens_thick/55.)/math.tan( (90-part_dir)*math.pi/180.)
L3D_est = math.sqrt(L2D_est*L2D_est*55.*55. + sens_thick*sens_thick) 

print("============================================")
print("Sensor thickness:\t" , sens_thick , "um")
print("Particle direction:\t" , part_dir , "deg")
print("Lenght 2D estimated:\t" , L2D_est , "px")
print("Lenght 3D estimated:\t" , L3D_est , "um")
print("LET estimated:\t\t" , E_dep_mean/L3D_est , "keV/um")
print("============================================")
print("Lenght 2D estimated:\t" , L2D_est , "px")
print("Lenght 2D from clust:\t" , L2D_corr_mean , "px")
print("============================================")
print("Mean LET form E_mean/L3D_mean:\t", E_mean/L3D_mean)
print("Mean LET form E_mean/pythL2D:\t", E_mean/math.sqrt(L2D_corr_mean*L2D_corr_mean*55.*55. + sens_thick*sens_thick))
print("Mean LET from clusterer:\t", LET_mean)
print("Mean LET from estimated:\t", E_dep_mean/L3D_est)
print("============================================")



plot_hist1d_auto( *load_file_column(file_in_path_name, 22) )
plot_hist1d_auto( *load_file_column(file_in_path_name, 21) )
plot_hist1d_auto( *load_file_column(file_in_path_name, 20) )
plot_hist1d_auto( *load_file_column(file_in_path_name, 19) )
plot_hist1d_auto( *load_file_column(file_in_path_name, 18) )
plot_hist1d_auto( *load_file_column(file_in_path_name, 17) )
plot_hist1d_auto( *load_file_column(file_in_path_name, 16) )
plot_hist1d_auto( *load_file_column(file_in_path_name, 15) )


# RUN DPE

import multiprocessing
import subprocess


dpe = "/mnt/MainDisk/Soubory/Programy/Vlastni/c++/aplikace/DataProcessing/Processing/DPE/Release/Linux/dpe.sh"

param_file_paths = ["/run/media/lukasm/10ABE5A17D6AED39/Work/Data/Single/MixedFields/RadiationSources/133Ba_Source/B_MiniTPX3_H09_2mmCdTe_n450V/",
					"/run/media/lukasm/10ABE5A17D6AED39/Work/Data/Single/MixedFields/RadiationSources/137Cs_Source/C_MiniTPX3_H09_2mmCdTe_n450V/",
					"/run/media/lukasm/10ABE5A17D6AED39/Work/Data/Single/MixedFields/RadiationSources/152Eu_Source/B_MiniTPX3_H09_2mmCdTe_n450V/",
					"/run/media/lukasm/10ABE5A17D6AED39/Work/Data/Single/MixedFields/RadiationSources/22Na_Source/B_MiniTPX3_H09_2mmCdTe_n450V/",
					"/run/media/lukasm/10ABE5A17D6AED39/Work/Data/Single/MixedFields/RadiationSources/241Am_Source/I_MiniTPX3_H09_2mmCdTe_n450V/",
					"/run/media/lukasm/10ABE5A17D6AED39/Work/Data/Single/MixedFields/RadiationSources/60Co_Source/D_MiniTPX3_H09_2mmCdTe_n450V/"]

param_file_name = "ParametersFile.txt"

do_multi_process = True

def cmd_dpe(dpe, param_file_path, param_file_name):

	cmd = dpe + " " + param_file_path + param_file_name
	os.system(cmd)

def run_dpe():
	if do_multi_process:

		processes = []
		for n in range(len(param_file_paths)):
			print("Process num: ", n )
			process = multiprocessing.Process(target=cmd_dpe, args=(dpe,param_file_paths[n],param_file_name,))
			processes.append(process)
			process.start()

		for process in processes:
			process.join()
	else:

		cmd = dpe + " " + param_file_paths[0] + param_file_name
	os.system(cmd)


if __name__ == '__main__':
    run_dpe()
	

# RUN CLUSTERER


def run_clusterer(clusterer, file_in_path_name, file_out_path = "./", calib_dir = "", 
					clog_name = "", elist2_name = "", sens_thick = 500):
	rc = 0

	if len(clusterer) == 0 or len(file_in_path_name) == 0:
		return -1

	cmd = clusterer + " "
	if len(calib_dir) != 0:
		cmd += " -c " + calib_dir	
	if len(clog_name) != 0:
		cmd += " -l " + file_out_path + clog_name		
	if len(elist2_name) != 0:
		cmd += " --extendedevlist --evlist2 " + file_out_path + elist2_name
	cmd += " --el-thickness " + str(sens_thick)
	cmd += " " + file_in_path_name

	print(cmd)

	rc = os.system(cmd)

	return rc



if __name__ == '__main__':
	clusterer = "/mnt/MainDisk/Soubory/Programy/Vlastni/c++/aplikace/DataProcessing/PreProcessing/clusterer/out/clusterer"
	file_in_path_name = "/mnt/MainDisk/Soubory/Programy/Vlastni/python/aplikace/advacam/dpe/devel/test/run_clusterer/in/tot_toa.t3pa"
	file_out_path = "/mnt/MainDisk/Soubory/Programy/Vlastni/python/aplikace/advacam/dpe/devel/test/run_clusterer/out/"
	calib_dir = ""
	elist2_name = "Elist"
	clog_name = "ClusterLog"

	run_clusterer(clusterer, file_in_path_name, file_out_path, calib_dir, clog_name, elist2_name)

	
"""