.. python-oifits

.. |astropy| image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat-square
   :target: http://www.astropy.org/

.. |mailing| image:: https://img.shields.io/badge/mailing%20list-groups.io-8cbcd1.svg?style=flat-square
   :target: https://groups.io/g/oifits-dev

.. |doi| image:: https://zenodo.org/badge/168302584.svg?style=flat-square
   :target: https://zenodo.org/badge/latestdoi/168302584

.. |riotchat| image:: https://img.shields.io/matrix/oiifts:matrix.org.svg?logo=riot&style=flat-square
   :target: https://riot.im/app/#/room/#oifits:matrix.org

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
   :target: https://github.com/shreyasbapat/python-oifits/raw/master/COPYING

.. |docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat-square
   :target: http://oifits.vlbi.software/en/latest/?badge=latest

.. |orcid-shreyas| image:: https://img.shields.io/badge/id-0000--0002--0870--4665-a6ce39.svg
   :target: https://orcid.org/0000-0002-0870-4665

:Name: python-oifits
:Author: Shreyas Bapat |orcid-shreyas|
:Website: http://vlbi.software/
:Version: 0.1.0

|astropy| |mailing|  |riotchat| |license| |docs|


Documentation
=============

|docs|

Complete documentation, including a user guide and an API reference, can be read on
the wonderful `Read the Docs`_.

http://oifits.vlbi.software/

.. _`Read the Docs`: https://readthedocs.org/


Requirements
============

EinsteinPy requires the following Python packages:

* NumPy, for basic numerical routines
* Astropy, for physical units and time handling

oifits is usually tested on Linux on Python
3.6 and 3.7 against latest NumPy.

Installation
============

The easiest and fastest way to get the package up and running is to
install python-oifits using `conda <http://conda.io>`_::

  $ conda install oifits --channel conda-forge

Or for Debian/Ubuntu/Mint users, the package is installable from `apt <https://packages.debian.org/sid/python3-einsteinpy>`_::

  $ pip install oifits

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

Developers Documentation can be found here.

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

 Shreyas Bapat et al.. (2019). oifits: oifits 0.1.0. Zenodo. 10.5281/zenodo.2582388


What's the future of the project?
---------------------------------

oifits is a part of my Major Technicsl Project.
The best way to get an idea of the roadmap is to see the `Milestones`_ of
the project.

.. _`Milestones`: https://github.com/shreyasbapat/python-oifits/milestones
