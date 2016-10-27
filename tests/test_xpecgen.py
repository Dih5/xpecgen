#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_xpecgen.py: Tests for  the `xpecgen` package.
"""

import unittest
from numpy.testing import *


from xpecgen import xpecgen as xg

def L1(y1,y2):
    """Distance in the sense of the 1-norm"""
    return sum(abs(y2-y1))
        


class xpecgen_test(unittest.TestCase):
    
    def test_clone(self):
        """Test the Spectrum clone method"""
        s=xg.calculate_spectrum(100,12,3,10,epsrel=0.5,monitor=None)
        s2=s.clone()
        #Check same values
        self.assertListEqual(list(s.x),list(s2.x))
        self.assertListEqual(list(s.y),list(s2.y))
        self.assertListEqual(list(s.discrete),list(s2.discrete))
        #Check alteration does not alter both instances
        s.x[0]=10
        s.y[0]=10
        s.discrete[0][0]=10
        self.assertNotEqual(s.x[0],s2.x[0])
        self.assertNotEqual(s.y[0],s2.y[0])
        self.assertNotEqual(s.discrete[0][0],s2.discrete[0][0])
    
    def test_HVL_values(self):
        """Test to reproduce the values in Table III of Med. Phys. 43, 4655 (2016)"""
        

        #Calculate the emission spectra
        num_div=20 #Points in each spectrum (quick calculation)
        s50=xg.calculate_spectrum(50,12,3,num_div,epsrel=0.5,monitor=None)
        s80=xg.calculate_spectrum(80,12,3,num_div,epsrel=0.5,monitor=None)
        s100=xg.calculate_spectrum(100,12,3,num_div,epsrel=0.5,monitor=None)

        #Attenuate them
        s50.attenuate(0.12,xg.get_mu(13)) #1.2 mm of Al
        s50.attenuate(100,xg.get_mu("air")) #100 cm of Air
        s80.attenuate(0.12,xg.get_mu(13)) #1.2 mm of Al
        s80.attenuate(100,xg.get_mu("air")) #100 cm of Air
        s100.attenuate(0.12,xg.get_mu(13)) #1.2 mm of Al
        s100.attenuate(100,xg.get_mu("air")) #100 cm of Air

        #Functions to calculate HVL in the sense of dose in Al
        fluence_to_dose=xg.get_fluence_to_dose()
        mu_Al=xg.get_mu(13)
        
        #HVL in mm
        hvl50=10 * s50.hvl(0.5,fluence_to_dose,mu_Al)
        hvl80=10 * s80.hvl(0.5,fluence_to_dose,mu_Al)
        hvl100=10 * s100.hvl(0.5,fluence_to_dose,mu_Al)

        self.assertAlmostEqual(hvl100,2.37,places=1)
        self.assertAlmostEqual(hvl80,1.85,places=1)
        self.assertAlmostEqual(hvl50,1.20,places=1)

        
                
                
                
    
                
        
    
    
if __name__ == "__main__":
    unittest.main()
