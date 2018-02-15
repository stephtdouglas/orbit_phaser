from __future__ import division, print_function, absolute_import

import os

import astropy.io.fits as fits
import numpy as np

def kepio(keplcfile):
    """Read in a Kepler LC file and return the time, flux, and error"""

    with fits.open(keplcfile) as hdu:
        print(hdu.info())

        t = hdu[1].data["TIME"]
        f = hdu[1].data["SAP_FLUX"]
        e = hdu[1].data["SAP_FLUX_ERR"]

        return t,f,e

if __name__=="__main__":
    t,f,e = kepio("kplr011517719-2013098041711_llc.fits.txt")
