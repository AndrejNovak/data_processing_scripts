# Data Processing Scripts

These scripts are developed for post-processing of Timepix/3 detectors with different sensors and their data outputs from the Data Processing Engine (DPE). Some functions were developed in cooperation with Carlos Granja and Lukas Marek. Before utilising these scripts for your results, please contact authors or use co-author citation. Thank you!

As of 2023-02-01 I began the process of coincidence analysis and improvement of coindicende event filtration for displaying in figures.


# Functions to implement:
1) Single particle tracks with histograms on top and right side of the track to indicate the energy deposited in each row and column. (In progress)

2) Plot 3D particle tract. Define a function based on Bergmann's article and use it for plotting.

3) In single particle tracks, draw a line along the track. This is just a first step for length determination. Not necessary, just for me as a practise.

4) Frame printing with a given number of clusters and fixed colorbar. For this frame, add two histograms on top of it
    - these histograms contain selected parameter, for example Cluster Height and the second Deposited Energy.
    - each part of the image can be also saved individually.
    - this can be made such that the main image will always be the deposited energy. The other option is to draw each cluster with one specific value of the whole cluster - its height, roundness,...

7) Create a plot of single frames representing counts - similiar to plot of total deposited energy.

8) Create a plot with clusters that were registered by the detector within time set on input - Elist from DPE gives a time value in nanoseconds.

9) Create a figure that shows recalculated total deposited energy to dose that was deposited in the sensor based on the sensor material (this value depends on material density - Si, SiC, CdTe, GaAs, Diamond).

10) Update read_clog function so that it is able to load multiple clog files in a given directory. This needs to be implemented since the number of clogs created by DPE is the same as the number of input clogs to DPE; however, the Elist gives only one list with all the processed events and therefore the event correlation has to be updated.
