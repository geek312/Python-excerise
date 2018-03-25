import pynamical
from pynamical import simulate, phase_diagram_3d
import pandas as pd, numpy as np, matplotlib.pyplot as plt, random, glob, os, IPython.display as IPdisplay
from PIL import Image
#matplotlib inline

title_font = pynamical.get_title_font()
label_font = pynamical.get_label_font()
save_folder = 'images/phase-animate'

# set a filename, run the logistic model, and create the plot
gif_filename = '01-pan-rotate-zoom-demo'
working_folder = '{}/{}'.format(save_folder, gif_filename)
if not os.path.exists(working_folder):
    os.makedirs(working_folder)

pops = simulate(num_gens=1000, rate_min=3.99, num_rates=1)
fig, ax = phase_diagram_3d(pops, remove_ticks=False, show=False, save=False)

# create 36 frames for the animated gif
steps = 36

# a viewing perspective is composed of an elevation, distance, and azimuth
# define the range of values we'll cycle through for the distance of the viewing perspective
min_dist = 7.
max_dist = 10.
dist_range = np.arange(min_dist, max_dist, (max_dist - min_dist) / steps)

# define the range of values we'll cycle through for the elevation of the viewing perspective
min_elev = 10.
max_elev = 60.
elev_range = np.arange(max_elev, min_elev, (min_elev - max_elev) / steps)

# now create the individual frames that will be combined later into the animation
for azimuth in range(0, 360, int(360 / steps)):
    # pan down, rotate around, and zoom out
    ax.azim = float(azimuth / 3.)
    ax.elev = elev_range[int(azimuth / (360. / steps))]
    ax.dist = dist_range[int(azimuth / (360. / steps))]

    # set the figure title to the viewing perspective, and save each figure as a .png
    fig.suptitle('elev={:.1f}, azim={:.1f}, dist={:.1f}'.format(ax.elev, ax.azim, ax.dist))
    plt.savefig('{}/{}/img{:03d}.png'.format(save_folder, gif_filename, azimuth))

# don't display the static plot...
plt.close()

# load all the static images into a list then save as an animated gif
gif_filepath = '{}/{}.gif'.format(save_folder, gif_filename)
images = [Image.open(image) for image in glob.glob('{}/*.png'.format(working_folder))]
gif = images[0]
gif.info['duration'] = 75  # milliseconds per frame
gif.info['loop'] = 0  # how many times to loop (0=infinite)
gif.save(fp=gif_filepath, format='gif', save_all=True, append_images=images[1:])
IPdisplay.Image(url=gif_filepath)

# set a filename, run the logistic model, and create the plot
gif_filename = '02-pan-rotate-logistic-phase-diagram'
working_folder = '{}/{}'.format(save_folder, gif_filename)
if not os.path.exists(working_folder):
    os.makedirs(working_folder)

pops = simulate(num_gens=1000, rate_min=3.99, num_rates=1)
fig, ax = phase_diagram_3d(pops, color='#003399', xlabel='Population (t)', ylabel='Population (t + 1)', zlabel='',
                           show=False, save=False)

# look straight down at the x-y plane to start off
ax.elev = 89.9
ax.azim = 270.1
ax.dist = 11.0

# sweep the perspective down and rotate to reveal the 3-D structure of the strange attractor
for n in range(0, 100):
    if n > 19 and n < 23:
        ax.set_xlabel('')
        ax.set_ylabel('')  # don't show axis labels while we move around, it looks weird
        ax.elev = ax.elev - 0.5  # start by panning down slowly
    if n > 22 and n < 37:
        ax.elev = ax.elev - 1.0  # pan down faster
    if n > 36 and n < 61:
        ax.elev = ax.elev - 1.5
        ax.azim = ax.azim + 1.1  # pan down faster and start to rotate
    if n > 60 and n < 65:
        ax.elev = ax.elev - 1.0
        ax.azim = ax.azim + 1.1  # pan down slower and rotate same speed
    if n > 64 and n < 74:
        ax.elev = ax.elev - 0.5
        ax.azim = ax.azim + 1.1  # pan down slowly and rotate same speed
    if n > 73 and n < 77:
        ax.elev = ax.elev - 0.2
        ax.azim = ax.azim + 0.5  # end by panning/rotating slowly to stopping position
    if n > 76:  # add axis labels at the end, when the plot isn't moving around
        ax.set_xlabel('Population (t)')
        ax.set_ylabel('Population (t + 1)')
        ax.set_zlabel('Population (t + 2)')

    # add a figure title to each plot then save the figure to the disk
    fig.suptitle('Logistic Map, r=3.99', fontsize=16, x=0.5, y=0.85)
    plt.savefig('{}/{}/img{:03d}.png'.format(save_folder, gif_filename, n), bbox_inches='tight')

# don't display the static plot
plt.close()

# load all the static images into a list then save as an animated gif
gif_filepath = '{}/{}.gif'.format(save_folder, gif_filename)
images = [Image.open(image) for image in glob.glob('{}/*.png'.format(working_folder))]
gif = images[0]
gif.info['duration'] = 10  # milliseconds per frame
gif.info['loop'] = 0  # how many times to loop (0=infinite)
gif.save(fp=gif_filepath, format='gif', save_all=True, append_images=images[1:])
IPdisplay.Image(url=gif_filepath)