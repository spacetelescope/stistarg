.. stistarg documentation master file, created by
   sphinx-quickstart on Fri Jan  6 17:04:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

  git clone https://github.com/spacetelescope/stistarg.git
  cd stistarg
  python setup.py install

(`stistarg` will be added to conda soon.)


Command Line Interface
----------------------

For more information, type ``stistarg --help``::
  
  usage: stistarg [-h] [--ext EXT] [--point | --diffuse CHECKBOXSIZE] [--display]
                  FILENAME
  
  Simulate HST/STIS onboard target acquisition algorithm on user data.
  
  positional argument:
    FILENAME              Input file
  
  optional arguments:
    -h, --help            show this help message and exit
    --ext EXT             Input FITS extension [default=0]
    --point               Point-source algorithm [default]
    --diffuse CHECKBOXSIZE
                          Diffuse-source algorithm. Specify checkboxsize
                          [odd integer 3-101]
    --display, -d         Display results with matplotlib.pyplot
  
  Version 2.1a1; Written by Berry & Lockwood


Python API
----------

.. autofunction:: stistarg.stistarg


Optional Functions
------------------

.. autofunction:: stistarg.findcheckbox
.. autofunction:: stistarg.calculate_flux_centroid
.. autofunction:: stistarg.display_results


Limitations
-----------

This alpha release currently supports only the STIS detector format and scale.  The 
capability to use non-STIS data will be added in a future release.


Support
-------

For support, please contact the STScI help desk at help<at>stsci<dot>edu.
