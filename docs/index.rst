HST/STIS Target Acquisition Simulator
=====================================

Utility to simulate HST/STIS target acquisitions with various "optional parameters" 
available in the Astronomer's Proposal Tool (APT) on a user-supplied FITS image.

.. warning::

  This is a pre-release.  The results have not yet been extensively tested and not all 
  features are included.  Use at your own risk!

.. toctree::
   :maxdepth: 2


Installation
------------

`stistarg` is designed to run in the AstroConda_ environment.  After installing it, 
launch the AstroConda environment::

  source activate astroconda

.. _Astroconda: http://astroconda.readthedocs.io

Then, install the `stistarg` script::

  conda install -c sean-lockwood stistarg


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
                          Diffuse-source algorithm. Specify checkboxsize
                          [odd integer 3-101]
    --display, -d         Display results with matplotlib.pyplot
  
  Version 2.1a2; Written by Berry & Lockwood


Python API
----------

.. autofunction:: stistarg.stistarg


Auxiliary Functions
-------------------

.. autofunction:: stistarg.findcheckbox
.. autofunction:: stistarg.calculate_flux_centroid
.. autofunction:: stistarg.display_results


Limitations
-----------

This alpha release currently supports only the STIS detector format and scale.  The 
capability to use non--STIS data will be added in a future release.  Users wishing to 
use data from other sources must trim and rescale their input data accordingly.  The 
STIS CCD plate scale is `0.05078 arcsec/pix`_.

.. _`0.05078 arcsec/pix`: http://www.stsci.edu/hst/stis/documents/handbooks/currentIHB/c13_specref03.html#922126

Furthermore, `stistarg` assumes the use of STIS acquisition image data and trims out the 
last five columns from the input array before performing calculations (these are normally 
hot).  To skip this behavior, users should pad their data accordingly.


Support
-------

For support, please contact the STScI help desk at help<at>stsci<dot>edu.
