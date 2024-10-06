import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from scipy.stats import gaussian_kde
from processing import process_data  
from cal_m import *


is_scatter = True


def create_star_map(ax, exoplanet_name, display_mode='scatter'):
    MAXNUM = 200
    
    ax.cla()

    stars, temperatures, magnitude, sun_coord, distance, sun_dist = process_data(MAXNUM, exoplanet_name)
    
    for i in range(0, MAXNUM):
        M = magnitude[i]
        magnitude[i] = cal_m(M, distance[i])
    
    sun_apparent_magnitude = cal_m(4.83, sun_dist)

    
    ra_list, dec_list = zip(*stars)
    
    
    ra_hours = (np.degrees(ra_list) / 15) % 24 
    dec_deg = np.degrees(dec_list)
      
    star_sizes = np.interp(magnitude, (min(magnitude), max(magnitude)), (5, 0.2))
    xy = np.vstack([ra_hours, dec_deg])
    kde = gaussian_kde(xy)
    
    ra_grid, dec_grid = np.meshgrid(np.linspace(0, 24, 100), np.linspace(-90, 90, 100))
    grid_coords = np.vstack([ra_grid.ravel(), dec_grid.ravel()])
    
    
    kde_values = kde(grid_coords).reshape(ra_grid.shape)
    
    
    normalized_temps = np.interp(temperatures, (min(temperatures), max(temperatures)), (0, 1))
    
    
    sun_ra_rad, sun_dec_rad = sun_coord
    sun_ra_hours = (np.degrees(sun_ra_rad) / 15) % 24
    sun_dec_deg = np.degrees(sun_dec_rad)
    
    
    if display_mode == 'scatter':
        
        
        ax.imshow(
            kde_values,
            extent=[0, 24, -90, 90], 
            cmap='coolwarm',
            alpha=0.5,
            origin='lower',
            aspect='auto'
        )
        
        
        halo_sizes = star_sizes * 2  
        ax.scatter(
            ra_hours, dec_deg,
            c='white',
            s=halo_sizes,
            edgecolor='none',
            alpha=0.3
        )
        
        
        ax.scatter(
            ra_hours, dec_deg,
            c='white',
            s=star_sizes,
            edgecolor='none',
            alpha=1.0
        )
    elif display_mode == 'heatmap':
        
        
        ax.scatter(
            ra_hours, dec_deg,
            c=temperatures,
            s=star_sizes,
            cmap='inferno',
            edgecolor='none',
            alpha=1.0
        )
        #plt.colorbar(ax.scatter(ra_hours, dec_deg, c=temperatures, cmap='inferno'), ax=ax, label='Star Temperature (K)')
        #the above causes duplication problems. i am currently working on a fix for that

    
    sun_size = np.interp(sun_apparent_magnitude, (min(magnitude), max(magnitude)), (5, 0.2))  
    ax.scatter(
        sun_ra_hours, sun_dec_deg,
        c='orange',
        s=sun_size,
        edgecolor='black',
        zorder=5,
        label='Sun'
    )
    
    
    ax.set_xlabel("Right Ascension (hours)")  
    ax.set_ylabel("Declination (degrees)")
    ax.grid(False)
    
    
    ax.set_facecolor('black')
    ax.set_title(f"Star Map for Exoplanet: {exoplanet_name} ({display_mode.capitalize()})")

    ax.legend(loc='upper right')
    
    plt.draw()

def submit_text(text):
    exoplanet_name = text.strip()
    if exoplanet_name:
        create_star_map(ax_main, exoplanet_name, 'scatter' if is_scatter else 'heatmap')


def save_graph(event):
    filename = f"star_map_{text_box.text.strip()}.png"
    plt.savefig(filename, dpi=300)
    print(f"Graph saved as {filename}")


def toggle_display(event):
    global is_scatter
    is_scatter = not is_scatter
    create_star_map(ax_main, text_box.text.strip(), 'scatter' if is_scatter else 'heatmap')


initial_exoplanet = "HD 1397 b"


fig, ax_main = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.25)  


create_star_map(ax_main, initial_exoplanet)


axbox = plt.axes([0.2, 0.1, 0.6, 0.075])  # [left, bottom, width, height] in fractions of figure size
text_box = TextBox(axbox, 'Enter Exoplanet Name: ', initial=initial_exoplanet)


save_button_ax = plt.axes([0.8, 0.025, 0.1, 0.05]) 
save_button = Button(save_button_ax, 'Save Graph')

toggle_button_ax = plt.axes([0.65, 0.025, 0.12, 0.05])  
toggle_button = Button(toggle_button_ax, 'Toggle Display')

text_box.on_submit(submit_text)
save_button.on_clicked(save_graph)
toggle_button.on_clicked(toggle_display)

plt.show()