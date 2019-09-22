Getting started
===============

Overview
--------

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

Installation
------------

It’s as easy as running one command!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stable Versions:
~~~~~~~~~~~~~~~~

For installation of the latest ``stable`` version of EinsteinPy:

- Using pip:

  .. code-block:: sh

       $ pip install oifits

- Using conda:

  .. code-block:: sh

       $ conda install -c conda-forge oifits

Latest Versions
~~~~~~~~~~~~~~~

For installing the development version, you can do two things:

- Installation from clone:

  .. code-block:: sh

       $ git clone https://github.com/shreyasbapat/python-oifits.git
       $ cd python-oifits/
       $ python setup.py install

- Install using pip:

  .. code-block:: sh

       $ pip install git+https://github.com/einsteinpy/einsteinpy.git

Development Version
~~~~~~~~~~~~~~~~~~~

  .. code-block:: sh

       $ git clone your_account/python-oifits.git
       $ pip install --editable /path/to/python-oifits[dev]

Please open an issue `here`_ if you feel any
difficulty in installation!

.. _`here` : https://github.com/shreyasbapat/python-oifits/issues


Running your first code using the library
-----------------------------------------

An example can be found in the `examples`_ folder.

.. _`examples` : https://oifits.readthedocs.io/en/latest/jupyter.html

Contribute
----------

oifits is an open source library which is under heavy development.
To contribute kindly do visit :

https://github.com/shreyasbapat/python-oifits

and also check out current posted issues and help us expand this
awesome library.
