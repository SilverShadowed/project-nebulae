from astroquery.gaia import Gaia
import requests
import time

def get_exoplanet_host_star_gaia_id(exoplanet_name):
	tap_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

	query = f"""
	SELECT gaia_id
	FROM ps
	WHERE pl_name = '{exoplanet_name}'
	"""

	params = {
        'REQUEST': 'doQuery',
        'LANG': 'ADQL',
        'QUERY': query,
        'FORMAT': 'json'
    }

	response = requests.get(tap_url, params=params)
	
	if response.status_code == 200:
		data = response.json()
		if len(data) > 0:
			exoplanet = data[0]
			gaia_id = exoplanet.get('gaia_id')
			print(gaia_id)
			return gaia_id
		else:
			return None
	else:
		raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

def get_specific_gaia_star_coords(gaia_star_name):

 	query = f"""
 	SELECT TOP 1 ra, dec, parallax
 	FROM gaiadr3.gaia_source
 	WHERE source_id = {gaia_star_name}
 	"""


 	job = Gaia.launch_job(query)
 	result = job.get_results()



 	coordinates = [(row['ra'], row['dec']) for row in result]
 	parallax = [row['parallax'] for row in result]

 	return coordinates, parallax



def convert_REAL(exoplanet_name):
	get_gaia_id = get_exoplanet_host_star_gaia_id(exoplanet_name)
	get_gaia_id = get_gaia_id[9:]
	coordinates, parallax = get_specific_gaia_star_coords(get_gaia_id)
	return coordinates, parallax

'''
get_gaia_id = get_exoplanet_host_star_gaia_id("AU Mic b")

get_gaia_id = get_gaia_id[9:]

coordinates, parallax = get_specific_gaia_star_coords(get_gaia_id)




print(coordinates, parallax)
'''