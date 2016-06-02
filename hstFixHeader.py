#!/usr/bin/env python

import numpy as np
from astropy.io import fits
from astropy.time import Time


def fixHeader(filename):

    h = fits.open(filename, mode='update')

    prihdr = h[0].header

    # DELETING ALL COMMENT/HISTORY KEYWORDS
    del prihdr["COMMENT"]
    del prihdr["HISTORY"]

    # UPDATING/CREATING COORDINATES KEYWORD
    prihdr["OBJECT"] = "eta Car"
    prihdr["BSCALE"] = (1.00E+00, "REAL = TAPE * BSCALE + BZERO")
    prihdr["BZERO"] = 0.00E+00
    prihdr["BUNIT"] = "erg/s/cm2/Ang"
    prihdr["BTYPE"] = "flux"
    prihdr["CTYPE1"] = "RA"
    prihdr["CTYPE2"] = "DEC"
    prihdr["CTYPE3"] = "VEL"
    prihdr["CUNIT1"] = "deg"
    prihdr["CUNIT2"] = "deg"
    prihdr["CUNIT3"] = "km/s"
    prihdr["CROTA1"] = 0.0E+00
    prihdr["CROTA2"] = 0.0E+00
    prihdr["CROTA3"] = 0.0E+00
    prihdr["CRPIX3"] = 1
    prihdr["CRVAL3"] = h[0].header["VMIN"]
    prihdr["CDELT3"] = h[0].header["DELV"]

    # CORRECTING DATE-OBS KEYWORD AND ADDING JD
    prihdr["DATE-OBS"] = prihdr["DATEOBS"]
    prihdr["JD"] = ((Time(prihdr["DATE-OBS"], scale="utc")).jd, "Julian Day of observation")
    prihdr["DECYEAR"] = ((Time(prihdr["DATE-OBS"], scale="utc")).decimalyear, "Decimal year of observation")

    # INFO ABOUT CYCLE AND PHASE
    jd0, period = 2456874.4, 2022.7
    prihdr["PHI"] = (((Time(prihdr.get("DATEOBS"), scale="utc")).jd - jd0) / period + 13, "Cycle+orbital phase of obs.")
    prihdr.set("COMMENT", "PHI=(JD-{:.1f})/{:.1f}+13".format(jd0, period))

    # UPDATING HISTORY
    datetime = Time.now()
    prihdr.set("HISTORY", "Last update on {}".format(datetime.isot))

    h.flush()
    h.close()


def fix(fitsList):

    """
    \n
    \t Updates a list of HST/STIS data cube files with standard FITS header keywords.\n
    \t N.B.: The changes are performed on the fly.

    \t Calling sequence:

    \t\t import hstFixHeader
    \t\t hstFixHeader.fix('list_of_fits_files.txt')

    \t The format of the input file must be as follows.

    \t\t /PATH/TO/THE/FOLDER/CONTAINING/THE/DATA/
    \t\t file_0.fits
    \t\t file_1.fits
    \t\t [...]
    \t\t file_n.fits

    \t N.B.: The full path must be given with a forward slash at the end.\n
    \n
    """
    # GET THE LIST WITH THE PATH TO THE DATA
    # AND THE NAME OF THE FILES
    fits_list = np.loadtxt(fitsList, dtype=np.str)
    data_dir = ''

    for index, item in enumerate(fits_list):
        if index == 0:
            # GET THE PATH TO THE DATA
            data_dir = item
        else:
            # FIX HEADER (ADD IMPORTANT KEYWORDS)
            fixHeader(data_dir+item)


if __name__ == "__main__":
    fix(fitsList)
