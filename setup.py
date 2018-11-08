#!/usr/bin/env python

from setuptools import setup
import os
import yaml

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

# These get saved into version.py for use in the package:
with open('setup.yaml') as f:
    cfg = yaml.load(f)

# Write a "version.py" file containing version and author info:
with open(os.path.join('stistarg', 'version.py'), 'w') as f:
    for key in cfg:
        f.write('__{}__ = "{}"\n'.format(key, cfg[key]))

setup(
    name = 'stistarg',
    url = cfg['docs_url'],
    version = cfg['version'],
    description = 'HST/STIS Target Acquisition Simulator',
    long_description = long_description,
    author = cfg['author'],
    author_email = 'help@stsci.edu',
    maintainer = 'Sean Lockwood',
    maintainer_email = 'lockwood@stsci.edu',
    license = 'BSD-new',
    keywords = ['astronomy'],
    classifiers = ['Programming Language :: Python',
                   #'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Development Status :: 5 - Production/Stable',
                   'Operating System :: OS Independent',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
    packages = ['stistarg'],
    install_requires = ['setuptools', 'numpy', 'astropy>=1.3', 'matplotlib'],
    entry_points={
          'console_scripts': ['stistarg = stistarg.stistarg:parse']},
    )
