#!/bin/python3

from physdata.xray import *  # pip install physdata
import numpy as np

for element in fetch_elements():
	if element.z not in [85, 87]:  # Skip those with arbitrary density
		a=np.asarray(element.get_coefficients(use_density=True))
		np.savetxt(str(element.z)+".csv",np.transpose(a[:,0:2]*[1000,1]), fmt="%.8G",delimiter=",")
