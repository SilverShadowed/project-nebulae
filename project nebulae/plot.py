import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from scipy.stats import gaussian_kde
from processing import process_data  # Ensure that 'processing.py' contains the 'process_data' function
from cal_m import *

# Flag to track display mode (scatter or heatmap)
is_scatter = True

# Function to create and update the plot based on the exoplanet name and display mode
def create_star_map(ax, exoplanet_name, display_mode='scatter'):
    MAXNUM = 200
    # Clear the previous plot
    ax.cla()
    
    # Process data for the given exoplanet
    stars, temperatures, magnitude, sun_coord, distance, sun_dist = process_data(MAXNUM, exoplanet_name)
    
    for i in range(0, MAXNUM):
        M = magnitude[i]
        magnitude[i] = cal_m(M, distance[i])
    
    sun_apparent_magnitude = cal_m(4.83, sun_dist)

    # Unpack RA and Dec into separate lists
    ra_list, dec_list = zip(*stars)
    
    # Convert RA from radians to hours
    ra_hours = (np.degrees(ra_list) / 15) % 24  # Normalize to [0, 24] hours
    dec_deg = np.degrees(dec_list)
    
    # Star sizes based on apparent magnitude (brighter stars are bigger)
    star_sizes = np.interp(magnitude, (min(magnitude), max(magnitude)), (5, 0.2))
    
    # Create a 2D Gaussian KDE (Kernel Density Estimate) to model star density
    xy = np.vstack([ra_hours, dec_deg])
    kde = gaussian_kde(xy)
    
    # Generate a grid over which to evaluate KDE
    ra_grid, dec_grid = np.meshgrid(np.linspace(0, 24, 100), np.linspace(-90, 90, 100))
    grid_coords = np.vstack([ra_grid.ravel(), dec_grid.ravel()])
    
    # Evaluate KDE on the grid
    kde_values = kde(grid_coords).reshape(ra_grid.shape)
    
    # Normalize temperatures to use in color for heatmap
    normalized_temps = np.interp(temperatures, (min(temperatures), max(temperatures)), (0, 1))
    
    # Convert Sun's RA and Dec from radians to hours and degrees
    sun_ra_rad, sun_dec_rad = sun_coord
    sun_ra_hours = (np.degrees(sun_ra_rad) / 15) % 24
    sun_dec_deg = np.degrees(sun_dec_rad)
    
    # Plot based on the selected display mode
    if display_mode == 'scatter':
        
        # Plot the density background based on KDE (clustering)
        ax.imshow(
            kde_values,
            extent=[0, 24, -90, 90],  # [0, 24, -90, 90] for hours and degrees
            cmap='coolwarm',
            alpha=0.5,
            origin='lower',
            aspect='auto'
        )
        
        # Plot halos around stars based on temperature (larger, more translucent markers)
        halo_sizes = star_sizes * 2  # Halos twice the size of stars
        ax.scatter(
            ra_hours, dec_deg,
            c='white',
            s=halo_sizes,
            edgecolor='none',
            alpha=0.3
        )
        
        # Plot the stars themselves, all white
        ax.scatter(
            ra_hours, dec_deg,
            c='white',
            s=star_sizes,
            edgecolor='none',
            alpha=1.0
        )
    elif display_mode == 'heatmap':
        
        # Plot a heatmap using star temperatures
        ax.scatter(
            ra_hours, dec_deg,
            c=temperatures,
            s=star_sizes,
            cmap='inferno',
            edgecolor='none',
            alpha=1.0
        )
        #plt.colorbar(ax.scatter(ra_hours, dec_deg, c=temperatures, cmap='inferno'), ax=ax, label='Star Temperature (K)')

    # Plot the Sun as an orange dot
    sun_size = np.interp(sun_apparent_magnitude, (min(magnitude), max(magnitude)), (5, 0.2))  # Adjust size as needed
    ax.scatter(
        sun_ra_hours, sun_dec_deg,
        c='orange',
        s=sun_size,
        edgecolor='black',
        zorder=5,
        label='Sun'
    )
    
    # Add labels and grid
    ax.set_xlabel("Right Ascension (hours)")  # Changed from degrees to hours
    ax.set_ylabel("Declination (degrees)")
    ax.grid(False)
    
    # Set a dark background to mimic the night sky
    ax.set_facecolor('black')
    ax.set_title(f"Star Map for Exoplanet: {exoplanet_name} ({display_mode.capitalize()})")
    
    # Add a legend
    ax.legend(loc='upper right')
    
    # Redraw the canvas
    plt.draw()

# Callback function for the TextBox submission
def submit_text(text):
    exoplanet_name = text.strip()
    if exoplanet_name:
        create_star_map(ax_main, exoplanet_name, 'scatter' if is_scatter else 'heatmap')

# Callback function for the Save button
def save_graph(event):
    filename = f"star_map_{text_box.text.strip()}.png"
    plt.savefig(filename, dpi=300)
    print(f"Graph saved as {filename}")

# Callback function for the Toggle button
def toggle_display(event):
    global is_scatter
    is_scatter = not is_scatter
    create_star_map(ax_main, text_box.text.strip(), 'scatter' if is_scatter else 'heatmap')

# Initial exoplanet name
initial_exoplanet = "HD 1397 b"

# Create the main figure and axis
fig, ax_main = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.25)  # Make space for the TextBox and Buttons

# Create the initial plot
create_star_map(ax_main, initial_exoplanet)

# Create an axis for the TextBox
axbox = plt.axes([0.2, 0.1, 0.6, 0.075])  # [left, bottom, width, height] in fractions of figure size
text_box = TextBox(axbox, 'Enter Exoplanet Name: ', initial=initial_exoplanet)

# Create an axis for the Save button
save_button_ax = plt.axes([0.8, 0.025, 0.1, 0.05])  # Adjust position for the button
save_button = Button(save_button_ax, 'Save Graph')

# Create an axis for the Toggle Display button
toggle_button_ax = plt.axes([0.65, 0.025, 0.12, 0.05])  # Adjust position for the toggle button
toggle_button = Button(toggle_button_ax, 'Toggle Display')

# Connect the submit event to the callback function for the TextBox
text_box.on_submit(submit_text)

# Connect the buttons to their callback functions
save_button.on_clicked(save_graph)
toggle_button.on_clicked(toggle_display)

# Show the plot with the TextBox and Buttons
plt.show()