# GMOS-spec
## Reduce GMOS spectra

This repository contains three scripts to perform data reduction of GMOS spectra.
The steps to be run are:
1. Download data from the Gemini archive.
2. Organize your directory. Put bias files in a separate director, and preferably do the same for files concerning the
standard star.
3. In the Bias directory, run MakeBias.py (it will usee *all* .fits files in that directory).
4. In the Standard directory, run ReduceStandard.py. This script is interactive. It will first prompt for the flat file. One
single file is expected, which should be input as 'gFILE.fits' (*with* the quotes). Next it will ask for an arc lamp file,
which should be input with the same format. The wavelength calibration runs interactively by default. The code will finally
prompt for a list of science spectra, which should be input as ['gFILE1.fits','gFILE2.fits',...]. The extraction of 1D spectra
will also run interactively. Last the code will prompt for the directory containing the calibration data, and the name of the
star in the calibration files. Extinction is currently set to ctioextinct.dat, change that if data comes from GMOS-N. The last
interactive step is the sensitivity function fitting.
5. In the directory containing science data, run ReduceSpec.py. The steps are the same as for the standard star, except that
of course it will not request data on the calibration directory, but instead it will apply the sens.fits function generated
in the previous step to flux calibrate the science spectra.

The steps followed by these scripts are described here: http://drforum.gemini.edu/topic/gmos-mos-guidelines-part-1/
(skipping MOS specific stuff)\
Big thanks to user mangelo who suggested the above recipe.
