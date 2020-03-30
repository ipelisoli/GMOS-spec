# Create master bias from individial *.fits exposures

__version__ = '1.0'
__author__ = 'Ingrid Pelisoli'

# Importing packages
from pyraf import iraf
from pyraf.iraf import gemini, gemtools, gmos, onedspec

print ("### Begin Processing GMOS/Longslit Images ###")
print ("###")

# Runs gprepare to add mask definition
print ("=== Running gprepare ===")

gmos.gprepare('*.fits', fl_addmdf='yes')

print ("=== gprepare finished ===")

# Runs gbias
print ("=== Creating Master Bias ===")

gmos.gbias.unlearn()
gmos.gbias('g*.fits', outbias="../Zero.fits", fl_over='yes', fl_trim='yes')

print ("=== gbias finished ===")

print ("### DONE ###")


