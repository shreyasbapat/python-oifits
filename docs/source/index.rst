oifits - A Tool which makes understanding EHT Data Easy
=======================================================

**oifits** is an open source pure Python package dedicated to problems arising
in Interferometry data parsing.
The problem of understanding the open data that is provided by Event Horizon
Telescope team on VLBI Reconstruction Portal (http://vlbiimaging.csail.mit.edu)
is complicated. All the radio interferometry data is generally stored in OIFITS
file rather than a normal FITS file. There is a lot of Radio Astronomy specific
data that has to be taken out and understood before working on the acquired data
and analysing it. OIFITS is a standard for exchanging data for Optical (Visible/IR)
Interferometry, and is based on the FITS Standard. Since mm/sub-mm VLBI shares a
lot of similarities to optical interferometry, this format is better suited for
mm/sub-mm measurements than UVFITS.


View `source code`_ of oifits!

.. _`source code`: https://github.com/shreyasbapat/python-oifits


oifits is developed by an open community. Release
announcements and general discussion take place on our `mailing list`_
and `chat`_.

.. _`mailing list`: https://groups.io/g/oifits-dev
.. _`chat`: https://riot.im/app/#/room/#oifits:matrix.org

.. include:: form.rst


The `source code`_, `issue tracker`_ and `wiki`_ are hosted on GitHub, and all
contributions and feedback are more than welcome. You can test oifits in your
browser using binder, a cloud Jupyter notebook server:

.. image:: https://img.shields.io/badge/launch-binder-e66581.svg?style=flat-square
   :target: https://beta.mybinder.org/v2/gh/shreyasbapat/python-oifits/master?filepath=index.ipynb

.. _`source code`: https://github.com/shreyasbapat/python-oifits
.. _`issue tracker`: https://github.com/shreyasbapat/python-oifits/issues
.. _`wiki`: https://github.com/shreyasbapat/python-oifits/wiki/


Contents
--------

.. toctree::
    :maxdepth: 2

    getting_started
    jupyter
    changelog
    dev_guide
    api/index
