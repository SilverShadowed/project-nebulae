import numpy as np

def cal_m(M, d):
	m = M + 5 * np.log10(d / 10)
	return m 
