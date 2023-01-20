# -*- coding: utf-8 -*-
"""
@author: Carlos+Lukas+Andrej, ADV, Prague, 9 Aug 2022
stored in C:\Carlos\data\python\36 carlos finds single f in clog and draws it 4aug22
reads the elist and clog files (both output DPE_CP)
applies a cluster filter (according CA PAR) and finds
which clusters are OK and which BAD
and creates 2D sq matrices and draws them (output png + txt files):
    - all particles
    - filter OK
    - filter bad
this script calls and uses defined functions and newly also classes
read_clog, read_elist_filter, cluster_filter, create_matrix_filter, print_fig_E, print_fig_ToA
from Andrej corr_elist_clog.py july2022 + edited/modified/expanded Carlos+Lukas
- input values are
    - # of f's to integrate clusters, starts from the beginning i.e. f = 0
    - filter CA PARs (for now just 1 CA PAR filter)
- input data are
    - clog calib file of output of DPE_CP
    - elist file of output of DPE_CP
- output are
    - 3x sq matrices ToT [calib]: all part, filter ok, filter bad [png + txt]
    - 3x sq matrices ToA: all part, filter ok, filter bad
the output are stored in a new automatic DIR "DPE_figures" within the Files DIR of DPE_CP output
works for TPX3 data in ToT+ToA --> clog f's of 100 ns'
potize for TPX data in ToT
"""
# ---------- input par's of Andrej's python with the needed functions -------
# path of Andrej's python script with embedded funkce
#dir_andrej = "c:/Carlos/data/python/33 andrej new script 22july2022"
dir_functions = "C:/Users/andrej/Documents/FEI/Vyskum/Data_Processing_Engine/"

# ----------------------- add other folder -------------------
# importing sys
import sys
# ---------------- importing a function from a file------------
sys.path.insert(1, dir_functions)   # use /   not  \
#sys.path.insert(1, dir_andrej)   # use /   not  \
    
    
#sys.path.insert(1, 'c:/Carlos/data/python/33 andrej new script 22july2022')   # use /   not  \
#sys.path.append('c:\Carlos\data\python\31 andrej new script july2022')

from corr_elist_clog import read_clog,read_elist_make_ext_filter,read_elist_make_ext_elist,read_elist_filter,cluster_filter_MULTI_PAR,cluster_filter_MULTI_PAR_RATIOS,write_elist, create_matrix_filter_tpx3_t3pa, create_matrix_filter_tpx_f, print_fig_E, print_fig_ToA
#from corr_elist_clog import read_clog, read_elist_filter, cluster_filter_ONE_PAR, cluster_filter_MULTI_PAR, write_elist, create_matrix_filter_tpx3_t3pa, create_matrix_filter_tpx_f, print_fig_E, print_fig_ToA
#from corr_elist_clog import read_clog, read_elist_filter, cluster_filter, create_matrix_filter_tpx3_t3pa, create_matrix_filter_tpx_f, print_fig_E, print_fig_ToA
#from corr_elist_clog import read_clog, read_elist, parameter_filter, get_column, plot_single_cluster, frame_matrix_tpx3, print_fig_E, print_fig_ToA
#from corr_elist_clog import read_clog, frame_matrix_tpx3, print_fig_E, print_fig_ToA
#from corr_elist_clog import *   # nepomohlo, jinde dle Pavel

# -- new COL's
col_num_pairs_for_ratios_input = [4,7,9,7] # E,A,  BordPx,A
header_txt_new_cols_input = ['E/A','BordPx/A']
units_txt_new_cols_input = ['keV/px','a.u.']

# -- num of COL of the filter in the here extended elist
num_col_filter = 17

# ---------------------------------------------------------------------
# ---------------------- << ENTER fill-in >> --------------------------
# ---------------------------------------------------------------------
#
# ----- input data DIR and file to be processed = from clog output from DPE_CP ----
#
# ---------------------------------------------------------------
# ----------------- TPX3 D05 500 um filters, Carlos ADV, 23 Aug 2022 ------------
# ---------------------------------------------------------------
# 
# --- particle-type groups:
# ----------------------- << p's + HCPs nPPs >> ------------------------- 
# --- A: LE protons nPP + fast n's  << paired with B + E + I >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,6000,150,5000,0.0,0.9,4,400,30,30000,0,0.85],[8,4,10,7,15,16]) # H E R A, E/A, Bord/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,6000,150,5000,0.0,0.9,4,400,30,3000],[8,4,10,7,15]) # H E R A, E/A, 
#filter_RAN_COL_RAT = cluster_filter_MULTI_PAR_RATIOS([90,6000,800,90000,0.0,0.9,4,400],[8,4,10,7,12],[50,3000,0.0,0.95],[4,7,9,7]) # H E R A, E/A, BordPx/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([10,6000,100,90000,0.0,0.9,4,400,5,30,0.0,0.95],[8,4,10,7,12,15,16]) # H E R A E/A BordPx/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,6000,800,5000,0.0,0.9,4,400],[8,4,10,7]) # H E R A
# --- B: LE protons nPP + fast n's  << paired with A + D >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,6000,5.E3,3.E5,0.0,0.9,12,400,30,3000],[8,4,10,7,15]) # H E R A, E/A, 
#filter_RAN_COL = cluster_filter_MULTI_PAR([130,5000,5000,90000,0.0,0.9,12,400],[8,4,10,7]) # H E R A
# --- C: HE HCPs MIPs + VHE p's nPP = straight thin tracks mid H << paired with J >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([50,400,80,5000,0.0,0.8,6,400,0.6,1.0,4,300,30,1000,0.8,1.0],[8,4,10,7,12,13,15,16]) # H E R A LIN LEN, E/A, Bord/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,300,5,2000,4,300,0.94,1.0,4,50,0.8,1.0],[8,4,7,12,15,16]) # H E A LIN, E/A, BordPx/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([10,90,15,800,0.0,0.9,4,400,10,50,0.9,1.0],[8,4,10,7,15,16]) # H E R A, E/A, BordPx/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,5000,50,800,0.0,0.9,4,400],[8,4,10,7]) # H E R A
# ----------------------- << p's + HCPs PPs >> ------------------------- 
# --- D: LE protons PP = round blobs << paired with E + B + F >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,5000,1500,4500,0.9,1.7,4,300,30,5000],[8,4,10,7,15]) # H E R A, E/A, 
#filter_RAN_COL = cluster_filter_MULTI_PAR([130,5000,1500,90000,0.9,1.7,4,200],[8,4,10,7]) # H E R A
# --- E: HE protons PP + VLE p + fast n? << paired with D + A >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,5000,150,1500,0.85,1.7,4,200,0.0,0.8,30,5000],[8,4,10,7,12,15]) # H E R A LIN, E/A, 
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,5000,250,1500,0.5,1.7,4,200,0.0,0.4],[8,4,10,7,12]) # H E R A LIN
# --- F: ions + LE protons PP + n's = round blobs << paired with E + B + D >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,5000,4500,5.E5,0.9,1.7,4,300,30,5000],[8,4,10,7,15]) # H E R A, E/A, 
# ----------------------- << e + LCPs + g's + X rays + small clu n's >> ------------------------- 
# --- J: HE e's + g's straight + VHE rel p's << paired with C + H >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([10,90,5,5000,4,300,0.7,1.0,4,30],[8,4,7,12,15]) # H E A LIN, E/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,90,4,400,3,30,0.8,1.0],[7,8,15,16]) # H A, E/A, BordPx/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([4,400,0,90],[7,8]) # A H
# --- G: ME e's + g's = low H twisted curly thin tracks << paired with F >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,90,5,9000,4,300,0.0,0.9,4,50,0.8,1.0],[8,4,7,12,15,16]) # H E A LIN, E/A, BordPx/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,90,5,9000,4,300,0.0,0.9,4,50],[8,4,7,12,15]) # H E A LIN, E/A, 
#filter_RAN_COL_RAT = cluster_filter_MULTI_PAR_RATIOS([0,300,10,3000,0,0.7,4,300,0.25,1.0],[8,4,10,7,12],[0,50,0.95,1.0],[4,7,9,7]) # H E R A LIN, E/A, BordPx/A
#filter_RAN_COL_RAT = cluster_filter_MULTI_PAR_RATIOS([0,300,10,3000,0,0.7,4,300,0.25,1.0],[8,4,10,7,12],[0,50],[4,7]) # H E R A LIN, 
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,300,10,3000,0,0.7,4,300,0.25,1.0],[8,4,10,7,12]) # H E R A LIN
# ----------------------- << small clu + fast n's? >> ------------------------- 
# --- H: X rays + fast n's? = small clu's A <= 3
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,3,3,500],[7,15]) # A, E/A
# ----------------------- << LE e's + g's curly >> ------------------------- 
# --- I: mid H + BordPx/A > 0.8  << paired with A + J >>
#filter_RAN_COL = cluster_filter_MULTI_PAR([10,90,80,5000,0.0,0.85,4,400,0.0,0.7,5,30,0.85,1.0],[8,4,10,7,12,15,16]) # H E R A LIN, E/A, Bord/A
# ----------------------- << noisy clu >> ------------------------- 
# --- K: noisy px's = small A < 3 + H too high
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,3,500,1.E6,0,1.0],[7,15,16]) # A, E/A, BordPx/A
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,3],[7]) # A
# ----------------------- << testing checking >> ------------------------- 
# --- X: for testing, checking
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,5.E5],[8]) # H
#filter_RAN_COL = cluster_filter_MULTI_PAR([500,1.E5,1,3],[8,7]) # H A
#filter_RAN_COL = cluster_filter_MULTI_PAR([3,90,75,100],[8,15]) # H Epx
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,1.E3,4,200,75,100],[8,7,15]) # H A Epx
#filter_RAN_COL = cluster_filter_MULTI_PAR([5.E3,5.E6],[4]) # E
#filter_RAN_COL = cluster_filter_MULTI_PAR([0,0.9],[10]) # R
#filter_RAN_COL = cluster_filter_MULTI_PAR([75,100],[15]) # Epx
#filter_RAN_COL = cluster_filter_MULTI_PAR([4,2.E2],[13]) # LEN_2D_px
# ----------------- << for Andrej work >> -------------------
#filter_RAN_COL = cluster_filter_MULTI_PAR([90,5.E5,0.9,1.0,5,7],[8,12,13]) # H LIN LEN


# ---------------------------------------------------------------
# ----------------- TPX3 D05 500 um cyklotron CCB Krakow june 2022 ------------
# ---------------------------------------------------------------
#det_name = ['CdTe_2000um', 'GaAs_500um', 'Si_100um', 'Si_300um', 'Si_500um']
#e_name = ['31_MeV', '22_MeV']

#det = det_name[1]
#energy = e_name[0]

#folder_data = 'C:/Users/andrej/Documents/FEI/Vyskum/Data_Processing_Engine/DPE_carlos_data_output/2018_08_01_protons/' + det + '/' + energy + '/50_angle/Files/'
slab = 3
slab_name = ['a', 'd', 'e', 'Pb']
#folder_data = "C:/Users/andrej/Documents/FEI/2022_IEEE_prispevok/data/output/C2/16/Files/"
#folder_data = "C:/Users/andrej/Documents/FEI/2022_IEEE_prispevok/data/output/C2/28/Files/"
#folder_data = "C:/Users/andrej/Documents/FEI/2022_IEEE_prispevok/data/output/C2/36/Files/"
folder_data = "C:/Users/andrej/Documents/FEI/2022_IEEE_prispevok/data/output/C2/75/Files/"
print(folder_data)
#folder_data = r'c:/Carlos/data/cyclotron krakow CCB/2022 06 04 - INSPIRE/32 TPX3 D05/C1/04 70MeV spot a/D05 4.5ms 80V/DPE_CP 251/Files'
#folder_data = r'c:/Carlos/data/cyclotron krakow CCB/2022 06 04 - INSPIRE/32 TPX3 D05/C2/38 150MeV  slab f/D05 4.5ms 80V/DPE_CP 251/Files'
filename_clog = 'ClusterLog.clog'   # clog file name
#filename_clog = 'ClusterLog_itot_cnt_.clog'   # clog file name
filename_elist = 'Elist.txt'  # elist file name INPUT
filename_out_txt = 'Elist_filt.txt' # elist filtered name OUTPUT
# of particles starting from the 1st, for TPX3 data, DPE CP output
num_particles = 500
# ---------------------------------------------------------------------
# ------------------- << END of ENTER fill-in >> ----------------------
# ---------------------------------------------------------------------

print('Script running, Carlos, ADV, Prague, July 2022')
print(folder_data+filename_clog)

clog = read_clog(folder_data,filename_clog)[2]
#num_particles = len(clog[:])
#sys.exit(0)  # break stop (for debugging)
# ---------------- load the elist output of DPE_CP --------------
# preferred way/Lukas
#new_filter = filter([100,300], [5])
'''
# alternative way, not chosen
# new_filter = filter()
#new_filter.edges = [100,300]
#new_filter.indeces = [4]
'''

# ------------------ read elist, make/add new cols --------
#elist_ext = read_elist_make_ext_elist(filename_elist,col_num_pairs_for_ratios_input,header_txt_new_cols_input,units_txt_new_cols_input)

# ----------------------- write out ext elist -----------
#write_elist(filename_out_txt,elist_ext[0],elist_ext[1],elist_ext[2])

# ------------------ apply filter to elist, and label the OK's in a new last col = 16 --------
#elist_filtered = read_elist_filter(filename_elist) # without filter
#elist_filtered = read_elist_filter(filename_elist, filter_H)

#elist_filtered = read_elist_filter(filename_out_txt, filter_RAN_COL)
#elist_filtered = read_elist_filter(filename_elist,filter_RAN_COL)

#CdTe 2000 um 31 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([2E4,4E4,300,700,370,700,0.8,0.95,50,60,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#CdTe 2000 um 22 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([1.5E4,4E4,200,600,200,700,0.75,0.95,30,60,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#GaAs 500 um 31 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([2E3,3E4,20,50,300,600,0.8,0.9,8,12,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y
#filter_RAN_COL = cluster_filter_MULTI_PAR([2E3,1E5,1E2,1E5],[4,8]) # E S H LIN LEN X Y

#GaAs 500 um 22 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([2E3,3E4,10,50,150,700,0.77,0.9,7,15,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#Si 100 um 31 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([275,1E3,5,45,50,450,0.65,0.95,2,8,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#Si 100 um 22 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([275,1E3,4,60,25,450,0.6,0.95,1,8,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#Si 300 um 31 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([1E3,4E3,25,100,100,500,0.75,0.9,8,15,2,12,2,12],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#Si 300 um 22 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([1E3,5E3,20,100,200,500,0.7,0.9,5,20,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#Si 500 um 31 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([2E3,4E3,45,70,150,500,0.8,0.9,11,15,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y

#Si 500 um 22 MeV filter
#filter_RAN_COL = cluster_filter_MULTI_PAR([2E3,8E3,40,200,200,500,0.8,0.9,10,30,0.55,13.53,0.55,13.53],[4,7,8,12,13,2,3]) # E S H LIN LEN X Y


#IEEE processing Slab a d e Pb
filter_RAN_COL = cluster_filter_MULTI_PAR([1,200,1,4,1,100],[4,7,8]) # E S H

elist_filtered = read_elist_make_ext_filter(folder_data+filename_elist,col_num_pairs_for_ratios_input,header_txt_new_cols_input,units_txt_new_cols_input,filter_RAN_COL)

#elist_filtered = read_elist_filter(filename_elist, filter_RAN_COL)
#elist_filtered = read_elist_filter(filename_elist, filter_E)
#elist_filtered = read_elist_filter(filename_elist, filter_Lin)
#elist_filtered = read_elist_filter(filename_elist, filter_R_E)
#elist_filtered = read_elist_filter(filename_elist, filter_A_H)
print("elist extension + filtering done")
# extracts the selected col from the elist
#column_sel = get_column(filename_elist, col_sel_name)

# ----------------------- folder to write out data -----------
write_elist(folder_data+filename_out_txt,elist_filtered[0],elist_filtered[1],elist_filtered[2])
#FileOut_Path = 'Clog_output/'       # Output file folder location 
#FileOut_Name = 'clog_read_output.txt'   # Output file name



# -------------- for TPX3 t3pa data -----------------
#sq_matrices = create_matrix_filter_tpx3_t3pa(elist_filtered,filename_clog,num_col_filter,num_particles)

# -------------- for TPX frame ToT data -----------------
print("start create matrix")
sq_matrices = create_matrix_filter_tpx3_t3pa(elist_filtered,clog,num_col_filter,num_particles)

print("create matrix processing done")

'''
# -------------- TPX3 t3pa print out (png, txt) the sq matrices of filter OK and BAD clusters -----------------
print_fig_E(sq_matrices[0],'sq_matrix_E_all')
print_fig_ToA(sq_matrices[1],'sq_matrix_ToA_all')
print_fig_E(sq_matrices[2],'sq_matrix_E_ok')
print_fig_ToA(sq_matrices[3],'sq_matrix_ToA_ok')
print_fig_E(sq_matrices[4],'sq_matrix_E_bad')
print_fig_ToA(sq_matrices[5],'sq_matrix_ToA_bad')
'''

# -------------- TPX frames print out (png, txt) the sq matrices of filter OK and BAD clusters -----------------

all_name = slab_name[slab] + '_E_all_' + str(num_particles)
ok_name = slab_name[slab] + '_E_ok_' + str(num_particles)
bad_name = slab_name[slab] + '_E_bad_' + str(num_particles)

print(all_name, ok_name, bad_name)
print(type(all_name))

filter_path = dir_functions + '/ieee/'

print_fig_E(sq_matrices[0], 1E5, 'All particles', filter_path, all_name)
print_fig_E(sq_matrices[2], 1E5, 'OK particles', filter_path, ok_name)
print_fig_E(sq_matrices[4], 1E5, 'BAD particles', filter_path, bad_name)

print("print sq 2D matrices done")


'''
# -------------- write out to disk the output/generated f's in txt and png ----------------
print_fig_E(matice[0], "matice_sq_E")
print_fig_ToA(matice[1], "matice_sq_ToA")

print('End of processing, Done')

# -------------- call and use the funkce -----------------
#matice = create_matrix(data, num_frames, rand)
# -------------- reads the clog file, finds a single frame in it -----------------
# syntax:   def frame_matrix(clog_path, filename, frame_number):
matice = frame_matrix_tpx3(folder_data,filename,frame_number)


# -------------- write out to disk the output/generated f's in txt and png ----------------
print_fig_E(matice[0], "matice_sq_E")
print_fig_ToA(matice[1], "matice_sq_ToA")
'''

print('End of processing, Done')