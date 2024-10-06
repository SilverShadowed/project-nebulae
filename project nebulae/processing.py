from convert_exo_to_host import *
from coord_convert_new import *
from sun_coord import *
from get_gaia import *

def process_data(max_star_limit, exoplanet_name):


	#max_star_limit = 100
	gaia_id = get_exoplanet_host_star_gaia_id(exoplanet_name)


	#exoplanet_name = "HD 1397 b"

	star_coords, star_temps, star_magnitude, star_parallax = get_star_coordinates_and_temperatures(max_star_limit, gaia_id)

	new_star_coords = []

	exoplanet_coord, exoplanet_parallax = convert_REAL(exoplanet_name) #coords of host star

	#print(exoplanet_coord[0])


	distance_between_2 = []

	for i in range(0, max_star_limit):
		exoplanet_ra, exoplanet_dec = exoplanet_coord[0]
		star_ra, star_dec = star_coords[i]
		star_current_parallax = star_parallax[i]
		star_distance = 1 / star_current_parallax
		star_coord1 = convert_from_celestial_to_cartesian(star_ra, star_dec, star_distance)



		exo_distance = 1 / exoplanet_parallax[0]
		exo_coord1 = convert_from_celestial_to_cartesian(exoplanet_ra, exoplanet_dec, exo_distance)
		
		x1, y1, z1 = exo_coord1
		xx, yy, zz = star_coord1
		distance_between_2.append(((xx - x1)**2 + (yy - y1)**2 + (zz - z1)**2)**(1/2))

		sun_coord, sun_dist = find_coord_of_sun(x1,y1,z1)


		x, y, z = convert_cartesian_from_earth_to_exo(star_coord1, exo_coord1)
		coords = convert_from_cartesian_to_celestial(x,y,z)
		new_star_coords.append(coords)


	return(new_star_coords, star_temps, star_magnitude, sun_coord, distance_between_2, sun_dist)

	#print(new_star_coords)
