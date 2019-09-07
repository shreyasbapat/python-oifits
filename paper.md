---
title: 'oifits : Python Module for Processing EHT Data'
tags:
  - Python
  - astronomy
  - interferometry
  - Radio-Astronomy
  - oifits
authors:
  - name: Shreyas Bapat
    orcid: 0000-0002-0870-4665
    affiliation: 1
  - name: Arnav Bhavsar
    affiliation: 1
affiliations:
 - name: Indian Institute of Technology Mandi
   index: 1
   
date: 05 September 2019
bibliography: paper.bib
---

# Summary

The problem of understanding the open data that is provided by Event Horizon 
Telescope team on VLBI Reconstruction Portal (http://vlbiimaging.csail.mit.edu)
is complicated. All the radio interferometry data is generally stored in OIFITS
file rather than a normal FITS file. There is a lot of Radio Astronomy specific 
data that has to be taken out and understood before working on the acquired data 
and analysing it. OIFITS is a standard for exchanging data for Optical (Visible/IR)
Interferometry, and is based on the FITS Standard. Since mm/sub-mm VLBI shares a
lot of similarities to optical interferometry, this format is better suited for 
mm/sub-mm measurements than UVFITS.

``oifits`` is a Python package for reading and analysing OIFITS Data. One can easily 
procure the interferometry data from the oifits file and store every thing in a numpy 
array for further analysis. 
``oifits`` also relies heavily on and interfaces well with the implementations of 
 fits module of ``Astropy`` package [@astropy] (``astropy.io.fits``).

``oifits`` is designed to be used by both researchers working on Optical Interferometry
and by researchers working on Event Horizon Telescope Data.

# Acknowledgements

We acknowledge the contributions of Dr. Redouane Boumghar for helping in writing the module.


# References