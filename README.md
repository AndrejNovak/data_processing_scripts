# Data Processing Scripts

This library of scripts/functions is developed for post-processing of Timepix/Timepix3/Timepix4 detectors with different sensors and their data outputs acquired from the Data Processing Engine (DPE) in development at Advacam s.r.o. Some functions were developed in cooperation with Carlos Granja and Lukas Marek. Before using these scripts for your need, please contact authors. Please don't forget to mention or use co-author citation in your publication. Thank you!

The library contains functions that are capable of reading both Elist and clog files from DPE, add new cluster calculated parameters, write new elist, output coincidence clusters info, create matrices from clogs, print energy and ToA of individual clusters, print energy and ToA of multiple clusters, combination of particle filtration and printing into matrix.

# Functions to implement:
1) Single particle tracks with histograms on top and right side of the track to indicate the energy deposited in each row and column. (In progress)

2) Plot 3D particle tract. Define a function based on Bergmann's article and use it for plotting.

3) In single particle tracks, draw a line along the track. This is just a first step for length determination. Not necessary, just for me as a practise.

4) Frame printing with a given number of clusters and fixed colorbar. For this frame, add two histograms on top of it
    - these histograms contain selected parameter, for example Cluster Height and the second Deposited Energy.
    - each part of the image can be also saved individually.
    - this can be made such that the main image will always be the deposited energy. The other option is to draw each cluster with one specific value of the whole cluster - its height, roundness,...

5) Create a figure that shows recalculated total deposited energy to dose that was deposited in the sensor based on the sensor material (this value depends on material density - Si, SiC, CdTe, GaAs, Diamond).