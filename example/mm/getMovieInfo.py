import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from twmovieapi import mm

# get mirama movie screenings info
info = mm.MovieInfo()

for m, d, t in info.get('MM'):
    print(m, d, t)
    break
