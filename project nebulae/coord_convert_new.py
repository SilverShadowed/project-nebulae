import numpy as np

def convert_from_celestial_to_cartesian(ra, dec, distance): #ra and dec are taken as degrees
	ra = np.radians(ra)
	dec = np.radians(dec)
	x = distance * np.cos(dec) * np.cos(ra)
	y = distance * np.cos(dec) * np.sin(ra)
	z = distance * np.sin(dec)
	return x, y, z

def convert_cartesian_from_earth_to_exo(earth_cartesian, exo_cartesian): #taken both as tuples
	#earth_cartesian: the coordinate of the star if earth is the origin
	new_coordinates = (earth_cartesian[0] - exo_cartesian[0], earth_cartesian[1] - exo_cartesian[1], earth_cartesian[2] - exo_cartesian[2])
	return new_coordinates

def convert_from_cartesian_to_celestial(x, y, z):
	dec = np.arcsin(z / ((x**2 + y**2 + z**2)**(1/2)))
	ra = np.arctan2(y, x)
	return ra, dec

