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
file rather than a normal FITS file. OIFITS is a standard for exchanging data for Optical (Visible/IR)
Interferometry, and is based on the FITS Standard. Since mm/sub-mm VLBI shares a
lot of similarities to optical interferometry, this format is better suited for 
mm/sub-mm measurements than UVFITS. Now as the Event Horizon Telescope team is already using it,
any person willing to conduct a research on the released data has to first go through the
data format and realise that there is no direct way of getting the data in a proper structure.
As the data preprocessing needs are huge, the accesibility of all the data within the 
OIFITS file is very important. Be it ground stations, phase data, errors etc. 

``oifits`` is a Python package for reading and analysing OIFITS Data. One can easily 
procure the interferometry data from the oifits file and store every thing in a numpy 
array for further analysis. 
There are specialised classes for storing the interferometry data, for example, 
class for storing visibility amplitude and differential phase data, a class for
storing squared visibility amplitude data. Another class for storing triple product 
and closure phase data. ``oifits`` later combines all the data into a class ``Data``.
which containes the wavelength, t3, vis and vis2 data of the experiment. And all these can
be extracted in one line of Python code.


``oifits`` also relies heavily on and interfaces well with the implementations of 
 fits module of ``Astropy`` package [@astropy] (``astropy.io.fits``).

``oifits`` is designed to be used by both researchers working on Optical Interferometry
and by researchers working on Event Horizon Telescope Data.

A research project is being worked upon by Shreyas Bapat[1] to reconstruct 
the VLBI Images which is highly dependent on this module.

# Acknowledgements

We acknowledge the support of Indian Institute of Technology Mandi, and 
Dr. Redouane Boumghar for supporting in writing this module.


# References