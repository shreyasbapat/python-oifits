.. python-oifits

.. image:: http://vlbi.software/logo.png
   :target: http://vlbi.software/
   :alt: python-oifits logo
   :width: 50px
   :align: center

.. |astropy| image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat-square
   :target: http://www.astropy.org/

.. |mailing| image:: https://img.shields.io/badge/mailing%20list-groups.io-8cbcd1.svg?style=flat-square
   :target: https://groups.io/g/oifits-dev

.. |doi| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3402135.svg
   :target: https://doi.org/10.5281/zenodo.3402135

.. |riotchat| image:: https://img.shields.io/matrix/oifits:matrix.org.svg?logo=riot&style=flat-square
   :target: https://riot.im/app/#/room/#oifits:matrix.org

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://github.com/shreyasbapat/python-oifits/raw/master/COPYING

.. |docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat-square
   :target: http://oifits.vlbi.software/en/latest/?badge=latest

.. |orcid-shreyas| image:: https://img.shields.io/badge/id-0000--0002--0870--4665-a6ce39.svg
   :target: https://orcid.org/0000-0002-0870-4665

:Name: python-oifits
:Author: Shreyas Bapat |orcid-shreyas|
:Website: http://oifits.vlbi.software/
:Version: 1.0.dev0

|astropy| |mailing|  |riotchat| |license| |docs| |doi|

**python-oifits** is the python package for dealing with Event Horizons Telescope Data. The Data
is in infamous OIFITS format. Which is too complex to parse everytime when applying any machine learning
or deep learning model on the VLBI Data. The module provides easy access to all the data that is in the
OIFITS file. And provides a easy function to export all the data to a numpy array for making computer
scientists later spending time on the application of data science models rather than understanding the data.

Documentation
=============

|docs|

Complete documentation, including a user guide and an API reference, can be read on
the given link:

http://oifits.vlbi.software/


Requirements
============

oifits requires the following Python packages:

* NumPy, for basic numerical routines
* Astropy, for fits handling

oifits is usually tested on Linux on Python
3.6 and 3.7 against latest NumPy.

Installation
============

The easiest and fastest way to get the package up and running is to
install python-oifits using pip or conda by simply running::

  $ pip install oifits
  $ conda install -c conda-forge oifits

And it's done!

Testing
=======

If installed correctly, the tests can be run using pytest::

  $ pytest -vv
  ============================= test session starts ==============================
  platform linux -- Python 3.7.1, pytest-4.3.1, py-1.8.0, pluggy-0.9.0
  rootdir: /home/shreyas/Local Forks/python-oifits, inifile: setup.cfg
  plugins: remotedata-0.3.1, openfiles-0.3.1, doctestplus-0.3.0, cov-2.5.1, arraydiff-0.3
  collected 1 items
  [...]
  ==================== 1 passed, 1 warnings in 28.19 seconds ====================
  $

Problems
========

If the installation fails or you find something that doesn't work as expected,
please open an issue in the `issue tracker`_.

.. _`issue tracker`: https://github.com/shreyasbapat/python-oifits/issues

Contributing
============

oifits is a community project, hence all contributions are more than
welcome! For more information, head to `CONTRIBUTING.rst`_.

.. _`CONTRIBUTING.rst`: https://github.com/shreyasbapat/python-oifits/blob/master/CONTRIBUTING.rst


Support
=======

|mailing|

Release announcements and general discussion take place on our `mailing list`_.
Feel free to join!

.. _`mailing list`: https://groups.io/g/oifits-dev

https://groups.io/g/oifits-dev

Please join our `[matrix]`_ channel for further queries.

.. _`[matrix]`: https://matrix.to/#/#oifits:matrix.org


If you still have a doubt, write a mail directly to `shreyas@einsteinpy.org <mailto:shreyas@einsteinpy.org>`_.

Citing
======

If you use oifits on your project, please
`drop us a line <mailto:shreyas@einsteinpy.org>`_.

You can also use the DOI to cite it in your publications. This is the latest
one:

|doi|

And this is an example citation format::

 Shreyas Bapat et al.. (2019). oifits: oifits 0.1.1. Zenodo. 10.5281/zenodo.3402135


Why care for the OIFITS now?
----------------------------

oifits is a part of my Major Technical Project of my B.Tech. Degree. I faced the issue of not understanding
exactly what the data was, and there was NO PYTHON MODULE which can tell me what's inside the data file.
So I spent a significant amount of my research in understanding the data. And I don't want this to happen to
anyone who wants to do their research using the world's largest telescope ;)
