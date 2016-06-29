#!/usr/bin/env python3
import cProfile
import xpecgen as xg

#Example to profile the time spent in a calculation
cProfile.run('xg.calculate_spectrum(100,12,3,50)')
