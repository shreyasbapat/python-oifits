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
    orcid: 0000-0003-2849-4375
    affiliation: 1
  - name: Ananya Shukla
    affiliation: 1
affiliations:
 - name: School of Computing and Electrical Engineering, Indian Institute of Technology Mandi
   index: 1

date: 05 September 2019
bibliography: paper.bib
---

# Background

The problem of understanding the open data that is provided by Event Horizon Telescope team on [VLBI Reconstruction Portal](http://vlbiimaging.csail.mit.edu) is complicated. Rather than using the FITS image file format that is used primarily as a method of exchanging bitmap data between different hardware platforms and software applications that do not support the common image file format, the radio interferometry data is stored in OIFITS file. OIFITS [@1510.04556] is a standard for exchanging calibrated, time-averaged data from astronomical optical interferometers, based on the FITS Standard. OIFITS may be used to combine data from multiple interferometer arrays for joint analysis and/or image reconstruction. Since mm/sub-mm VLBI shares a lot of similarities to optical interferometry, this format is better suited for mm/sub-mm measurements than UVFITS. The OIFITS files are complex since they have several headers, tables and irrelevant information for image reconstruction. A person willing to work on the released data  needs to go through the data format. There is no direct way to parse OIFITS data easily which further adds to the complexity.  As the data preprocessing requirements are huge, the accessibility of all the data including ground stations, phase data, errors within the OIFITS file is very important. Since OIFITS files are of great significance to the astronomers working on interferometers, there is a need for  an OIFITS file parser which is Python3 compliant, with easy installation and proper documentation.

# Summary

``oifits`` is a Python package for reading and analysing OIFITS Data. One can easily procure the interferometry data from the OIFITS file and store it in a numpy array for further analysis. There are specialised classes for storing the interferometry data some of which are mentioned below:

* Class to store visibility amplitude and differential phase data.
* Class to store squared visibility amplitude data
* Class to store triple product and closure phase data.

And many more such classes. These classes hold all the details of the experiment and no data is lost.

``oifits`` later combines all the data into a class ``Data`` which contains wavelength, t3, vis and vis2 data of the experiment. All the details can be extracted with a single line of Python code.

``oifits`` also relies heavily on and interfaces well with the implementations of
 fits module of ``Astropy`` package [@astropy] (``astropy.io.fits``). It also relies on the routines provided by ``Numpy`` package [@oliphant2006guide]. 

``oifits`` is designed to be used by both researchers working on Optical Interferometry
and by researchers working on Event Horizon Telescope Data.

An example of how easy ``oifits`` make it to read the files is :

```python
from oifits.read import OIParser

a = OIParser.read("test.oifits")

t3data = a.export_to_ascii()
```

# Acknowledgements

We acknowledge the support of Indian Institute of Technology Mandi, and
Dr. Redouane Boumghar for supporting in writing this module.


# References
