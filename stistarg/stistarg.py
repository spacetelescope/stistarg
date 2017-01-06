#! /usr/bin/env python

'''
HST/STIS Target Acquisition Simulator                 29-Dec-2016
Created 27 July 2016 by Bralen Berry & Sean Lockwood
Algorithm adapted from Solaris C "tas" code.
'''

from __future__ import division, print_function
import os
import sys
import numpy as np
from astropy.io import fits

__author__  = 'Berry & Lockwood'
__version__ = '2.1a1'
__all__ = ['stistarg', 'findcheckbox', 'calculate_flux_centroid', 'display_results']

# For compatibility between Python 2/3:
if sys.version_info.major == 2:
    WAIT = raw_input
    INTEGER_TYPES = (int, long,)
elif sys.version_info.major == 3:
    WAIT = input
    INTEGER_TYPES = (int,)
else:
    raise Exception('Version of Python not supported:  {}'.format(sys.version_info.major))


def findcheckbox(inarray, checkboxsize):
    '''
    INPUTS:
        inarray            pointer to the input array
        checkboxsize       size of the (square) checkbox
    
    RETURNS:
        maxFluxRow         x location of brightest checkbox
        maxFluxCol         y location of brightest checkbox
        maxFlux column     the max flux's value
        
    DESCRIPTION: This function finds the brightest checkboxes within the 
        input image sub-array, and returns their locations and fluxes.  
        A checkbox of specified size is scanned over the
        collected image, moving 1 pixel at a time over cols then
        rows of the collected image, always staying wholly within the
        collected image. At each position of the checkbox, the
        sum of flux counts in the checkbox is accumulated.  This sum is 
        compared against the running maximum, and the global max and 
        the upper-left corner indices of the checkbox relative to the 
        collected image are updated when a new max is found.
    '''
    shape = np.shape(inarray)
    nRows = shape[0]    # row indices for input array
    nCols = shape[1]    # col indices for input array
    
    # Initialize max counts & location for all checkboxes in input array
    maxFlux    =  0.
    maxFluxRow = -1
    maxFluxCol = -1
    
    # Compute the number of rows and cols of checkboxes
    ncbRows = nRows - checkboxsize + 1
    ncbCols = nCols - checkboxsize + 1
    
    # Step through the rows and columns of checkboxes:
    for cbrow in range(ncbRows):
        for cbCol in range(ncbCols):
            #Accumulate flux within checkbox:
            checkboxsum = np.sum(inarray[cbrow:cbrow+checkboxsize, cbCol:cbCol+checkboxsize])
            
            # Update new flux maximum and location within the subarray:
            if (checkboxsum > maxFlux):
                maxFlux    = checkboxsum
                maxFluxRow = cbrow
                maxFluxCol = cbCol
    
    return maxFluxRow, maxFluxCol, maxFlux


def calculate_flux_centroid(inarray, x, y, checkboxsize, centroidmode='flux'):
    '''
    calculate_flux_centroid
    
    INPUTS:
        inarray               pointer to the input array
        maxfluxrow            x location of brightest checkbox
        maxfluxcol            y location of brightest checkbox
        checkboxsize          size of the (square) checkbox
        centroid mode         flux or geometric centroid method
        
    RETURNS:
        rowcentroid           x location of centroid using flux centroid method
        colcentroid           y location of centroid using flux centroid method
        georowcentroid        x location of centroid using Geometric centroid method
        geocolocentroid       y location of centroid using Geometric centroid method
        
        
    DESCRIPTION: This function calculates a flux-weighted centroid
        within a given checkbox within a collected image. 
        
        Before computing the flux-weighted centroid, this function
        checks the total flux within the checkbox. If it does not exceed 
        a scaled box-flux threshold, there is not enough flux in the 
        checkbox to perform a meaningful flux-weighted centroid, and the 
        geometric center of the checkbox is computed instead.
    '''
    subarr = inarray[x:x+checkboxsize, y:y+checkboxsize]
    
     # total counts in checkbox
    totalmass = np.sum(subarr, dtype=np.float32)       
    
    if centroidmode == 'flux':
        # calculates the flux-weighted centroid
        
        #compute row and column centroids
        rowcentroid = x + np.sum(np.sum(subarr, axis=1) * range(checkboxsize)) / totalmass
        colcentroid = y + np.sum(np.sum(subarr, axis=0) * range(checkboxsize)) / totalmass
        return rowcentroid, colcentroid
        
    elif centroidmode == 'geometric':
        # calculates the geometric centroid
        
        #compute the geometric row and column centroids
        georowcentroid = x + (checkboxsize - 1) / 2.0
        geocolcentroid = y + (checkboxsize - 1) / 2.0
        return georowcentroid, geocolcentroid
        
    else:
        raise Exception('Centroid mode must be "flux" or "geometric".')


def validate_inputs(filename, ext, checkboxsize, source):
    if not os.access(filename, os.F_OK):
        raise IOError('Cannot access FITS file:  {:s}'.format(filename))
    if (ext < 0) or not isinstance(ext, INTEGER_TYPES):
        raise IOError('FITS file extension not a valid positive integer.')
    if checkboxsize not in range(3, 101+1, 2):
        raise IOError('checkbox size is not an odd integer in 3-101:  {}'.format(checkboxsize))
    if source not in ['point', 'diffuse']:
        raise IOError('Source-finding algorithm must be either "point" or "diffuse":  {}'.format(source))
    if source == 'point' and checkboxsize != 3:
        raise IOError('Checkbox size must be 3 pixels for point-source finding algorithm.')


def display_results(arr, flux_x, flux_y, chkx, chky, checkboxsize, geo_x=None, geo_y=None, 
    filename=None, ext=None):
    '''
    Display input array marked with brightest checkbox and flux/geometric positions.
    '''
    from matplotlib import pyplot as plt
    plt.ion()
    
    # Determine inner-98% flux range:
    sorted_arr = arr.flatten()
    sorted_arr.sort()
    vmin = sorted_arr[int(round(len(sorted_arr)*.01))]  #  1% flux level
    vmax = sorted_arr[int(round(len(sorted_arr)*.99))]  # 99% flux level
    if vmin >= vmax:
        vmin = np.min(sorted_arr)  #   0% flux level
        vmax = np.max(sorted_arr)  # 100% flux level
    
    fig, ax = plt.subplots()
    # Display data:
    img = ax.imshow(arr, origin='lower', aspect='auto', interpolation='nearest', cmap='viridis', 
        vmin=vmin, vmax=vmax)
    if filename is not None:
        ax.set_title('{:s}[{:.0f}]'.format(filename, ext))
    ax.set_xlabel('X [pix]')
    ax.set_ylabel('Y [pix]')
    cb = fig.colorbar(img)
    cb.set_label('Flux')
    # Plot grey X at flux centroid coordinate:
    ax.plot(flux_x, flux_y, 'x', color='0.40', markersize=12, mew=2, alpha=0.8)
    if geo_x is not None and geo_y is not None:
        # Plot orange X at geometric centroid coordinate:
        ax.plot(geo_x, geo_y, 'x', color='#FFA500', markersize=12, mew=2, alpha=0.8)
    # Plot checkbox boundaries:
    ax.plot(
        [chkx - 0.5, chkx - 0.5, chkx + checkboxsize - 0.5, chkx + checkboxsize - 0.5, chkx - 0.5], 
        [chky - 0.5, chky + checkboxsize - 0.5, chky + checkboxsize - 0.5, chky - 0.5, chky - 0.5], 
        'w')
    
    # Explicitly set plotting boundaries:
    ax.set_xlim(0, np.shape(arr)[0]-1)
    ax.set_ylim(0, np.shape(arr)[1]-1)
    
    fig.show()
    tmp = WAIT('Press ENTER to exit... ')


def stistarg(filename, ext=0, source='point', checkboxsize=3, display=False):
    '''
    HST/STIS Target Acquisition Simulator
    
    '''
    from datetime import datetime
    
    source = source.lower()
    
    # Check user inputs:
    validate_inputs(filename, ext, checkboxsize, source)
    
    with fits.open(filename) as f:
        # Set data extension:
        inarray = f[ext].data.transpose()
        
        # Error check on extension:
        if inarray is None:
            raise Exception ('No data found:  Try a different extension.')
        
        # Use findcheckbox function:
        x, y, maxFlux = findcheckbox(inarray, checkboxsize)
        
        if source == 'point':
             # use function calculate_flux_centroid for Point source
             # returns flux weighted centroid
            rowcentroid, colcentroid= calculate_flux_centroid(inarray, x, y, checkboxsize, 'flux')
            georowcentroid, geocolcentroid = None, None
        elif source == 'diffuse':
            # use function calculate_flux_centroid for Diffuse source
            # returns geometric and flux weighted centroids 
            georowcentroid, geocolcentroid = \
                calculate_flux_centroid(inarray, x, y, checkboxsize, 'geometric')
            rowcentroid, colcentroid = \
                calculate_flux_centroid(inarray, x, y, checkboxsize, 'flux')
        else:
            raise Exception('Source type must be "point" or "diffuse".')
        
        # Program/system info:
        print('-'*80)
        print('STIS Target Acquisition Simulator')
        print('{:s} v{:s}'.format(os.path.basename(__file__), __version__))
        print('Python v{:s}'.format(sys.version.split(' ')[0]))
        print('Run time:  {:s}\n'.format(datetime.now().isoformat(' ').rsplit('.',1)[0]))
        
        # User inputs:
        print('Input File:      {:s}[{:.0f}]'.format(filename, ext))
        print('Input Options:   {:s} source, checkbox size = {:.0f}'.format(
            source, checkboxsize))
        print('Image Subarray:  {}\n'.format(np.shape(inarray)))
        
        # Outputs:
        print('Brightest checkbox flux:  {}'.format(maxFlux))
        if display:
            flux_plotnote = '  [Grey X]'
            geo_plotnote  = '  [Orange X]'
        else:
            flux_plotnote = ''
            geo_plotnote  = ''
        
        print('Flux center:              x = {:.1f} ; y = {:.1f}{:s}'.format(
            rowcentroid, colcentroid, flux_plotnote))
        if source == 'diffuse':
            print('Geometric center:         x = {:.1f} ; y = {:.1f}{:s}'.format(
                georowcentroid, geocolcentroid, geo_plotnote))
        
        print('\n(All coordinates are zero-indexed.)')
        print('-'*80 + '\n')
        
        if display:
            display_results(f[ext].data, rowcentroid, colcentroid, x, y, checkboxsize, 
                georowcentroid, geocolcentroid, filename, ext)
        
    return (rowcentroid, colcentroid, maxFlux)


def parse():
    '''
    Command line script interface to parse user inputs and call stistarg().
    '''
    import argparse
    
    parser = argparse.ArgumentParser( \
        description='Simulate HST/STIS onboard target acquisition algorithm on user data.', 
        epilog='Version {:s}; Written by {:s}'.format(__version__, __author__))
    
    # .fits file that will be analyzed
    parser.add_argument('filename', metavar='FILENAME', help='Input file', type=str)
    
    # Data are in extension:
    parser.add_argument('--ext', help='Input FITS extension [default=0]', dest='ext', type=int, default=0)
    
    # Set 'point' or 'diffuse' source-finding algorithm:
    algorithm_group = parser.add_mutually_exclusive_group()
    algorithm_group.add_argument('--point', action='store_true', help='Point-source algorithm [default]')
    algorithm_group.add_argument('--diffuse', dest='checkboxsize', default=None, type=int, \
        help='Diffuse-source algorithm. Specify checkboxsize [odd integer 3-101]')
    
    parser.add_argument('--display', '-d', dest='display', action='store_true', 
        help='Display results with matplotlib.pyplot')
    
    args = parser.parse_args()
    
    if args.checkboxsize is not None:
        source = 'diffuse'
    else:
        source = 'point'
        args.checkboxsize = 3
    
    # Call stistarg main function:
    values = stistarg(args.filename, args.ext, source, args.checkboxsize, args.display)


if __name__ == '__main__':
    parse()
