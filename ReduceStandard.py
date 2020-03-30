# Reduces spectra for the standard star, calculates sensitivity function
# for flux calibration

__version__ = '1.0'
__author__ = 'Ingrid Pelisoli'

# Importing packages
from pyraf import iraf
from pyraf.iraf import gemini, gemtools, gmos, onedspec

print ("### Begin Processing GMOS/Longslit Images ###")
print ("###")

print ("=== Running gprepare ===")

# Runs gprepare to add mask definition
gmos.gprepare('*.fits', fl_addmdf='yes')

print ("=== gprepare finished ===")

print ("=== Pre-processing Flat ===")

# Prompts for flat file; format 'gFILE.fits'
flat = input('Flat file: ')

print ("Running gsreduce on the GCAL flats in order to:")
print ("- perform overscan subtraction;")
print ("- trim the frames;")
print ("- perform bias subtraction.")

# Set task parameters.
gmos.gsreduce.unlearn()
Flags = {'fl_over':'yes','fl_trim':'yes','fl_bias':'yes','fl_gscrrej':'no',
         'fl_crspec':'no', 'fl_dark':'no','fl_qecorr':'no',
         'fl_flat':'no','fl_gmosaic':'no','fl_fixpix':'no',
         'fl_gsappwave':'no','fl_scatsub':'no','fl_cut': 'no',
         'fl_title': 'no','fl_oversize':'yes','fl_vardq':'no',
         'fl_fulldq':'no','fl_inter':'no','verbose':'no'}
gmos.gsreduce(flat, bias='../Zero.fits', **Flags)

flat = 'gs' + flat
print ("=== gsreduce finished ===")

print ("=== Pre-processing Arcs ===")
print ("WARNING! Don't forget to implot your arcs to check instrument flexure.")

# Prompts for arc lamp file; format 'gFILE.fits'
arc = input('Arc file: ')

print ("Running gsreduce on the arc images in order to:")
print ("- perform overscan subtraction;")
print ("- trim the frames;")
print ("- perform bias subtraction;")
print ("- mosaic the science extensions.") 

# Set task parameters.
gmos.gsreduce.unlearn()
Flags = {'fl_over':'yes','fl_trim':'yes','fl_bias':'yes','fl_gscrrej':'no',
         'fl_crspec':'no', 'fl_dark':'no','fl_qecorr':'no',
         'fl_flat':'no','fl_gmosaic':'yes','fl_fixpix':'no',
         'fl_gsappwave':'yes','fl_scatsub':'no','fl_cut': 'no',
         'fl_title': 'no','fl_oversize':'yes','fl_vardq':'no',
         'fl_fulldq':'no','fl_inter':'no','verbose':'no'}
gmos.gsreduce(arc, bias='../Zero.fits', **Flags)

arc = 'gs' + arc

print ("=== gsreduce finished ===")

print ("Running gswavelength to obtain dispersion function")
gmos.gswavelength(arc)

print ("=== gswavelength finished ===")

print ("=== Running QE correction on Flat ===")

gmos.gqecorr.unlearn()
Flags = {'fl_correct':'yes','fl_keep':'yes','verbose':'no'}
gmos.gqecorr(flat, corrimages='QEcorr', refimages=arc, **Flags)

flat = 'q' + flat

print ("=== gqecorr finished ===")

print ("=== Mosaic Flat ===")

gmos.gmosaic.unlearn()
gmos.gmosaic(flat)

flat = 'm' + flat

print ("=== gmosaic finished ===")

print ("=== Creating Master Flat ===")

gmos.gsflat.unlearn()
Flags = {'fl_over':'no','fl_trim':'no','fl_bias':'no','fl_dark':'no',
         'fl_qecorr':'no','fl_fixpix':'no','fl_oversize':'yes','fl_vardq':'no',
         'fl_fulldq':'no','fl_inter':'no','verbose':'no'}

gmos.gsflat(flat, specflat='Flat.fits', **Flags)

print ("=== gsflat finished ===")

print ("=== Reducing Science Frames ===")

# Prompts for science files; format ['gFILE1.fits','gFILE2.fits',...]
science = input('Science files: ')

print ("Running gsreduce in order to:")
print ("- Perform overscan and bias subtractions;")
print ("- Trim the images;")
print ("- Remove cosmic rays with LAcos.")

# Set task parameters.
gmos.gsreduce.unlearn()
Flags = {'fl_over':'yes','fl_trim':'yes','fl_bias':'yes','fl_gscrrej':'no',
         'fl_crspec':'yes', 'fl_dark':'no','fl_qecorr':'no',
         'fl_flat':'no','fl_gmosaic':'no','fl_fixpix':'no',
         'fl_gsappwave':'no','fl_scatsub':'no','fl_cut': 'no',
         'fl_title': 'no','fl_oversize':'yes','fl_vardq':'no',
         'fl_fulldq':'no','fl_inter':'no','verbose':'no'}
gmos.gsreduce(','.join(str(x) for x in list(science)),
              bias='../Zero.fits', **Flags)

science = list('gs' + x for x in list(science))
    
print ("=== gsreduce finished ===")

print ("=== Running QE correction on Science images ===")

gmos.gqecorr.unlearn()
Flags = {'fl_correct':'yes','fl_keep':'no','verbose':'no'}
gmos.gqecorr(','.join(str(x) for x in list(science)),
             corrimages='QEcorr', refimages=arc, **Flags)

science = list('q' + x for x in list(science))

print ("=== gqecorr finished ===")

print ("Running gsreduce in order to:")
print ("- Flat field and mosaic images.")

gmos.gsreduce.unlearn()
Flags = {'fl_over':'no','fl_trim':'no','fl_bias':'no','fl_gscrrej':'no',
         'fl_crspec':'no', 'fl_dark':'no','fl_qecorr':'no',
         'fl_flat':'yes','fl_gmosaic':'yes','fl_fixpix':'yes',
         'fl_gsappwave':'no','fl_scatsub':'no','fl_cut': 'no',
         'fl_title': 'no','fl_oversize':'yes','fl_vardq':'no',
         'fl_fulldq':'no','fl_inter':'no','verbose':'no'}
gmos.gsreduce(','.join(str(x) for x in list(science)),
              flat='Flat.fits', bpm="../BPM.fits", **Flags)

science = list('gs' + x for x in list(science))

print ("=== gsreduce finished ===")

print ("=== Running wavelength calibration ===")

gmos.gstransform.unlearn()
gmos.gstransform(','.join(str(x) for x in list(science)), wavtran=arc)

science = list('t' + x for x in list(science))

print ("=== gstransform finished ===")

print ("=== Running background subtraction ===")

gmos.gsskysub.unlearn()
gmos.gsskysub(','.join(str(x) for x in list(science)))

science = list('s' + x for x in list(science))

print ("=== gsskysub finished ===")

print ("=== Extracting spectra ===")

gmos.gsextract.unlearn()
gmos.gsextract(','.join(str(x) for x in list(science)), fl_inter='yes')

science = list('e' + x for x in list(science))

print ("=== gsextract finished ===")

print ("=== Create sensitivity function ===")

caldir = input("Directory containing calibration data: ")
starname = input("Standard star name in calibration list: " )

gmos.gsstandard.unlearn()
gmos.gsstandard(','.join(str(x) for x in list(science)),
                fl_inter='yes', extinction='onedstds$ctioextinct.dat',
                starname=starname, caldir=caldir, sfunction="../sens")

print ("=== gsstandard finished ===")


print ("### DONE ###")

