# PeriCoupler
December 2025 
Nourhan Ahmed (namaahmed@mun.ca)
%____________________________________%
If you use this software in academic work, please cite:
Ahmed, Nourhan. (2026). *PeriCoupler* (Version 1.0) [Computer software].
https://github.com/Nourhan-Ahmed-M/PeriCoupler
%_____________________________________%

PeriCoupler is an open-source, user-friendly, Python-based tool designed to automate the generation of Peridynamic bonds and seamlessly integrate them into finite element models. The script enables efficient coupling between bond-based Peridynamics and conventional finite element analysis (FEA) within the ABAQUS framework.

This Python script for ABAQUS create a plug-in to the ABAQUS GUI to solve a 2D plane stress plate element using peridynamics mapping with finite element analysis introduced by Macek and Silling in{Peridynamics via finite element analysis 2007}.
%_____________________________________%

Add the plug-in to your plug-in menu as following:

1- copy the folder named PD_Comp_P to the abaqus_plugins folder in ABAQUS folder directory.
2- open the ABAQUS CAE.
3- Set your work directory.
4- From the plug-ins menu bar select (PD Plate Plugin).
5- In the "Path Directory" box paste the same path as in your work directory in step 3.
6- Specify your parameters and run.    

