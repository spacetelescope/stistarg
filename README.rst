HST/STIS Target Acquisition Simulator
=====================================

See documentation at http://stistarg.readthedocs.io/en/latest/

Utility to simulate HST/STIS target acquisitions with various "optional parameters" 
available in the Astronomer's Proposal Tool (APT) on a user-supplied FITS image.

|build-status| |coverage| |docs| |conda|


Command Line Interface
----------------------

For more information, type ``stistarg --help``::
  
  usage: stistarg [-h] [--ext EXT] [--point | --diffuse CHECKBOXSIZE] [--display]
                  FILENAME
  
  Simulate HST/STIS onboard target acquisition algorithm on user data.
  
  positional argument:
    FILENAME              Input FITS file
  
  optional arguments:
    -h, --help            show this help message and exit
    --ext EXT             Input FITS extension [default=0]
    --point               Point-source algorithm [default]
    --diffuse CHECKBOXSIZE
                          Diffuse-source algorithm. Specify checkboxsize [odd integer 3-101]
    --display, -d         Display results with matplotlib.pyplot
  
  Version 2.4; Written by Berry & Lockwood


Python API
----------

.. code-block:: python

  import stistarg
  stistarg.stistarg(filename, ext=0, source='point', checkboxsize=3, display=False)


Limitations
-----------

This release currently supports only the STIS detector format and scale.  The 
capability to use non--STIS data will be added in a future release.  Users wishing to 
use data from other sources must trim and rescale their input data accordingly.  The 
STIS CCD plate scale is `0.05078 arcsec/pix`_.

.. _`0.05078 arcsec/pix`: http://www.stsci.edu/hst/stis/documents/handbooks/currentIHB/c13_specref03.html#922126

Furthermore, `stistarg` assumes the use of STIS acquisition image data and trims out the 
last five columns from the input array before performing calculations (these are normally 
hot).  To skip this behavior, users should pad their data accordingly.


Contact
-------

For support, please contact the STScI help desk at help<at>stsci<dot>edu.


.. |build-status| image:: https://travis-ci.org/spacetelescope/stistarg.svg?branch=master
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/spacetelescope/stistarg

.. |coverage| image:: https://coveralls.io/repos/github/spacetelescope/stistarg/badge.svg?branch=master
    :alt: code coverage
    :scale: 100%
    :target: https://coveralls.io/github/spacetelescope/stistarg?branch=master

.. |docs| image:: https://readthedocs.org/projects/stistarg/badge/
    :alt: Documentation Status
    :scale: 100%
    :target: http://stistarg.readthedocs.io/en/latest/?badge=latest

.. |conda| image:: https://anaconda.org/sean-lockwood/stistarg/badges/installer/conda.svg
    :alt: conda install
    :target: https://anaconda.org/sean-lockwood/stistarg
