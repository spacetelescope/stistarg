HST/STIS Target Acquisition Simulator
=====================================

See documentation (to be posted) at http://stistarg.readthedocs.io/en/latest/

Utility to simulate HST/STIS target acquisitions with various "optional parameters" 
available in the Astronomer's Proposal Tool (APT) on a user-supplied FITS image.

|build-status| |docs|


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
                          Diffuse-source algorithm. Specify checkboxsize [odd integer 
                          3-101]
    --display, -d         Display results with matplotlib.pyplot
  
  Version 2.1a1; Written by Berry & Lockwood


Python API
----------

.. code-block:: python

  import stistarg
  stistarg.stistarg(filename, ext=0, source='point', checkboxsize=3, display=False)


Limitation
----------

Currently only supports STIS detector format and scale.  The capability to use non-STIS 
data will be added in a future release.


Contact
-------

For support, please contact the STScI help desk at help<at>stsci<dot>edu.


.. |build-status| image:: https://travis-ci.org/spacetelescope/stistarg.svg?branch=master
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/spacetelescope/stistarg

.. |docs| image:: https://readthedocs.org/projects/stistarg/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: http://stistarg.readthedocs.io/en/latest/?badge=latest
