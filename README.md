# Data Processing Scripts

These scripts are developed for post-processing of Timepix/3 detectors with different sensors and their data outputs from the Data Processing Engine (DPE). Some functions were developed in cooperation with Carlos Granja and Lukas Marek. Before utilising these scripts for your results, please contact authors or use co-author citation. Thank you!

As of 2023-02-01 I began the process of coincidence analysis and improvement of coindicende event filtration for displaying in figures.


# Functions to implement:
1) Single particle tracks with histograms on top and right side of the track to indicate the energy deposited in each row and column.

2) 3D particle track imaging.

3) In single particle tracs, draw a line along the track.

4) Frame printing with a given number of clusters and fixed colorbar, for this frame, add two histograms on top of it
    - these histograms contain selected parameter, for example Cluster Height and the second Deposited Energy.
    - each part of the image can be also saved individually

7) create frame with counting data - similiar to deposited energy graph

8) create frame with clusters that were registered within some time - Elist in nanoseconds

9) Add calculation of a 

10) Make a new figure for energy with two histograms on top and on the right.

11) New figure that recalculates total deposited energy to dose that was deposited in the sensor material
(depends on material density - Si, SiC, CdTe, GaAs)

12) Make print figure energy for multiple clog files present in the directory.