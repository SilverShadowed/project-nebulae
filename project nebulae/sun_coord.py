from coord_convert_new import *
def find_coord_of_sun(x,y,z): #in cartesian
	x2,y2,z2 = convert_cartesian_from_earth_to_exo((0, 0, 0), (x,y,z))
	distance = ((x2 - x)**2 + (y2 - y)**2 + (z2 - z)**2)**(1/2)
	ra,dec = convert_from_cartesian_to_celestial(x2,y2,z2)
	return (ra,dec), distance
