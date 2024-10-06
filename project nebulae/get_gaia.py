from astroquery.gaia import Gaia

def get_star_coordinates_and_temperatures(limit, exoplanet_host_gaia_id):

    exoplanet_host_gaia_id = exoplanet_host_gaia_id[9:]
    query = f"""
    SELECT TOP {limit} ra, dec, teff_gspphot, phot_g_mean_mag, parallax
    FROM gaiadr3.gaia_source
    WHERE teff_gspphot IS NOT NULL AND phot_g_mean_mag IS NOT NULL AND source_id != {exoplanet_host_gaia_id} 
    ORDER BY random_index
    """
    
    job = Gaia.launch_job(query)
    result = job.get_results()
    
    # Extract RA, DEC, and temperature
    coordinates = [(row['ra'], row['dec']) for row in result]
    temperatures = [row['teff_gspphot'] for row in result]
    magnitude = [row['phot_g_mean_mag'] for row in result]
    parallax = [row['parallax'] for row in result]
    

    return coordinates, temperatures, magnitude, parallax
