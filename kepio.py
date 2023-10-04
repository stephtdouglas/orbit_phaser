from __future__ import division, print_function, absolute_import

import os

import lightkurve as lk
import astropy.io.fits as fits
import numpy as np

def kepio(keplcfile):
    """Read in a Kepler LC file and return the time, flux, and error"""

    # print(keplcfile)
    # print(os.path.exists(keplcfile))

    with fits.open(keplcfile) as hdu:
        # print(hdu.info())

        t = hdu[1].data["TIME"]
        f = hdu[1].data["SAP_FLUX"]
        e = hdu[1].data["SAP_FLUX_ERR"]

        return t,f,e
    # return 0,0,0

def search_mast(target,**kwargs):

    search_result = lk.search_lightcurve(target, **kwargs)
    lc = search_result.download()

    t = lc.time.value
    f = lc.flux.value
    e = lc.flux_err.value

    return t,f,e

if __name__=="__main__":
    # t,f,e = kepio("kplr011517719-2013098041711_llc.fits")
    t,f,e = search_mast("KIC 6922244",author="Kepler",quarter=2)
    print(t,f,e)