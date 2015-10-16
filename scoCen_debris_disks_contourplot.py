import numpy as np
import sys
import matplotlib # necessary to save plots remotely; comment out if local
matplotlib.use('Agg') # comment out if local
import matplotlib.pyplot as plt
import pyfits
import pylab
from matplotlib.patches import Ellipse
from matplotlib.ticker import AutoMinorLocator,LinearLocator,NullLocator
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(7,9.5)) ## will probably need to scale down by ~20%
outer_grid = gridspec.GridSpec(6, 4, wspace = 0.0, hspace = 0.0)
pylab.xticks([])
pylab.yticks([])

def make_cmap(colors, position=None, bit=False): # tools to make the custom color map that is continuous in both rgb, cmyk, and greyscale
    import matplotlib as mpl
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit('position must start with 0 and end with 1')
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],                                                 bit_rgb[colors[i][1]],                                                 bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))
    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap

colors = [(255,255,255),(248,255,255),(240,255,255),(210,253,255),(184,252,255),(192,244,204),(155,255,145),(210,200,12),(230,180,7),(236,124,13),(233,100,25),(228,30,45),(198,0,46),(103,0,51)] 
my_cmap = make_cmap(colors,bit=True)

diskName = ['HIP63439','HD110058','HD113766','HIP62657','HIP73145','HIP74959','HIP74499','HIP72070','HIP78043','HIP79516','HIP84881','HIP82747','HIP79742','HIP76310','HIP80088','HIP77911','HIP79977','HIP79288','HD117214','HD115600','HD106906','HD114082','HIP63886','HIP62482']

beamA, beamB, beamC, beamD, beamE = [1.38,.83], [1.36,1.16], [1.25,0.82], [1.02,0.67], [1.32,.9] # determined from imaging with robust = 2

dist = [141.27,107.41,122.55,108.58,112.7,113.16,89.93,132.63,144.3,133.69,118.34,142,146.2,150.83,139.08,147.71,122.7,149.93,110.25,110.5,85.47,92.08,106.72,112.7] # in pc

noiselev = np.array([4.43,4.11,4.54,4.26,8.95,5.,6.63,6.2,6.86,4.48,3.98,24.2,5.11,5.07,5.16,4.66,5.79,6.13,4.78,4.54,4.38,5.42,5.68,4.40])*1e-5 # for all images created with robust = 2

def plotcmd(ax, levels):
    dat = diskName[i]+'/vis/'+diskName[i]+'spw123_nat.fits'
    if i == 3 :
        dat = 'HIP62657/vis/HIP62657spw123natOffset.fits'
    if i == 8 :
        dat = 'HIP78043/vis/HIP78043spw123natOffset.fits'
    if i == 9 :
        dat = 'HIP79516/vis/HIP79516spw123natOffset.fits'
    if i == 12 :
        dat = 'HIP79742/vis/HIP79742spw123natOffset.fits'
    if i == 13 :
        dat = 'HIP76310/vis/HIP76310spw123567natOffset.fits'
    if i == 16 :
        dat = 'HIP79977/vis/HIP79977spw123567natOffset.fits'
    hdulist = pyfits.open(dat)
    pixel_data = hdulist[0].data.squeeze()[:-1,:]
    ax.text(60,900,diskName[i],fontsize=8)
    #ax.text(448,480,r'$\star$',fontsize=12) # could put a star cartoon in center of image but it didn't really add much
    linewidth = (100*1024)/(6.4*dist[i]) # scale bar adjusted for each image
        # specifics for inset images with various robust levels
    if i <= 3:
        beam = Ellipse(xy=(150,105),height=beamA[0]/.00625,width=beamA[1]/.00625,angle=-79,facecolor='none',edgecolor='k',hatch='//')
    if i > 3 and i <= 8:
        beam = Ellipse(xy=(130,130),height=beamB[0]/.00625,width=beamB[1]/.00625,angle=26,facecolor='none',edgecolor='k',hatch='//')
    if i > 8 and i <= 12:
        beam = Ellipse(xy=(130,105),height=beamC[0]/.00625,width=beamC[1]/.00625,angle=89,facecolor='none',edgecolor='k',hatch='//')
    if i > 12 and i <= 17:
        beam = Ellipse(xy=(130,100),height=beamD[0]/.00625,width=beamD[1]/.00625,angle=79,facecolor='none',edgecolor='k',hatch='//')
    if i > 17 and i <= 23:
        beam = Ellipse(xy=(140,105),height=beamE[0]/.00625,width=beamE[1]/.00625,angle=-70,facecolor='none',edgecolor='k',hatch='//')
    line = pylab.Line2D((640,640+linewidth),(100,100),lw=2.5,color='k')
    ax.add_line(line)
    ax.add_patch(beam)
    ax.pcolormesh(pixel_data,cmap=my_cmap,vmin=0,vmax=np.max(pixel_data)) # this is how I decided to scale this image (0 is bottom of colormap, max is the deep red)
    ax.contour(pixel_data, levels=levels, colors='k')
    ax.contour(pixel_data, -levels, colors='k') 
    ax.set_xticks([192,512,832])
    ax.set_yticks([192,512,832])
    ax.xaxis.set_minor_locator(LinearLocator(33))
    ax.yaxis.set_minor_locator(LinearLocator(33))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    if ax.is_first_col() and ax.is_last_row(): # goodies for the bottom left
        ax.set_xlabel(r'$\Delta \alpha$ (")')
        ax.set_ylabel(r'$\Delta \delta$ (")')
        x = [-2,0,2]
        ax.set_xticks([192,512,832])
        ax.set_xticklabels(x)
        ax.set_yticks([192,512,832])
        ax.set_yticklabels(x)
        ax.text(595,135,'100 AU',fontsize=7)
        ax.xaxis.set_minor_locator(LinearLocator(33))
        ax.yaxis.set_minor_locator(LinearLocator(33))

for i in range(24): # all the images excluding insets are plotted here
    levels = np.array([j*noiselev[i] for j in range(3,28,3)]) # 3 sigma contours for every image except for HIP82747, which was bright enough that it needed its own contour scaling (directly below)
    if i == 11:
        levels = np.array([j*noiselev[i] for j in range(5,136,20)])
    inner_grid = gridspec.GridSpecFromSubplotSpec(6, 4, subplot_spec=outer_grid[i], wspace=0.0, hspace=0.0)
    ax = plt.Subplot(fig, outer_grid[i])
    plotcmd(ax, levels)
    fig.add_subplot(ax)

#all inset plots are done manually instead of with a plotcmd below

dat = 'HIP79516/vis/HIP79516spw123rob05_5zoom.fits'
levels = np.array([j*4.8e-5 for j in range(3,28,3)])
hdulist = pyfits.open(dat)
pixel_data = hdulist[0].data.squeeze()[:-1,:]
inset_ax = fig.add_axes([0.41, .565,.77*(1./8), .77*(1./12)])
inset_ax.pcolormesh(pixel_data,cmap=my_cmap,vmin=0,vmax=np.max(pixel_data))
inset_ax.contour(pixel_data, levels=levels, colors='k')
inset_ax.contour(pixel_data, -levels, colors='k') 
beam = Ellipse(xy=(235,155),height=1.12/.003125,width=0.71/.003125,angle=89.1,facecolor='none',edgecolor='k',hatch='//')
inset_ax.add_patch(beam)
inset_ax.set_xticklabels([])
inset_ax.set_yticklabels([])
inset_ax.set_xticks([])
inset_ax.set_yticks([])

dat = 'HIP79742/vis/HIP79742spw123rob0_zoom.fits' # images were created "zoomed" by a factor of 2 such that they would appear the same size when scaled down by a factor of two in this inset
levels = np.array([j*4.5e-5 for j in range(3,28,3)])
hdulist = pyfits.open(dat)
pixel_data = hdulist[0].data.squeeze()[:-1,:]
inset_ax = fig.add_axes([0.216, .4315,.77*(1./8), .77*(1./12)]) # manually found the location that worked
inset_ax.pcolormesh(pixel_data,cmap=my_cmap,vmin=0,vmax=np.max(pixel_data))
inset_ax.contour(pixel_data, levels=levels, colors='k')
inset_ax.contour(pixel_data, -levels, colors='k') 
beam = Ellipse(xy=(225,135),height=0.95/.003125,width=0.56/.003125,angle=87.9,facecolor='none',edgecolor='k',hatch='//')
inset_ax.add_patch(beam)
inset_ax.set_xticklabels([])
inset_ax.set_yticklabels([])
inset_ax.set_xticks([])
inset_ax.set_yticks([])

dat = 'HIP76310/vis/HIP76310spw123567_2zoom.fits'
levels = np.array([j*5.3e-5 for j in range(3,28,3)])
hdulist = pyfits.open(dat)
pixel_data = hdulist[0].data.squeeze()[:-1,:]
inset_ax = fig.add_axes([0.41, .4315,.77*(1./8), .77*(1./12)])
inset_ax.pcolormesh(pixel_data,cmap=my_cmap,vmin=0,vmax=np.max(pixel_data))
inset_ax.contour(pixel_data, levels=levels, colors='k')
inset_ax.contour(pixel_data, -levels, colors='k') 
beam = Ellipse(xy=(185,130),height=0.85/.003125,width=0.59/.003125,angle=81.5,facecolor='none',edgecolor='k',hatch='//')
inset_ax.add_patch(beam)
inset_ax.set_xticklabels([])
inset_ax.set_yticklabels([])
inset_ax.set_xticks([])
inset_ax.set_yticks([])

dat = 'HIP79977/vis/HIP79977spw123567_2zoom.fits'
levels = np.array([j*6.5e-5 for j in range(3,28,3)])
hdulist = pyfits.open(dat)
pixel_data = hdulist[0].data.squeeze()[:-1,:]
inset_ax = fig.add_axes([0.216, .298,.77*(1./8), .77*(1./12)])
inset_ax.pcolormesh(pixel_data,cmap=my_cmap,vmin=0,vmax=np.max(pixel_data))
inset_ax.contour(pixel_data, levels=levels, colors='k')
inset_ax.contour(pixel_data, -levels, colors='k') 
beam = Ellipse(xy=(170,125),height=0.75/.003125,width=0.48/.003125,angle=77.8,facecolor='none',edgecolor='k',hatch='//')
inset_ax.add_patch(beam)
inset_ax.set_xticklabels([])
inset_ax.set_yticklabels([])
inset_ax.set_xticks([])
inset_ax.set_yticks([])

dat = 'HIP78043/vis/HIP78043spw123_rob0zoom.fits'
levels = np.array([j*6.86e-5 for j in range(3,28,3)])
hdulist = pyfits.open(dat)
pixel_data = hdulist[0].data.squeeze()[:-1,:]
inset_ax = fig.add_axes([0.216, .565,.77*(1./8), .77*(1./12)])
inset_ax.pcolormesh(pixel_data,cmap=my_cmap,vmin=0,vmax=np.max(pixel_data))
inset_ax.contour(pixel_data, levels=levels, colors='k')
inset_ax.contour(pixel_data, -levels, colors='k') 
beam = Ellipse(xy=(205,210),height=1.11/.003125,width=0.88/.003125,angle=23.0,facecolor='none',edgecolor='k',hatch='//')
inset_ax.add_patch(beam)
inset_ax.set_xticklabels([])
inset_ax.set_yticklabels([])
inset_ax.set_xticks([])
inset_ax.set_yticks([])

dat = 'HIP62657/vis/HIP62657spw123_rob0zoom.fits'
levels = np.array([j*6.8e-5 for j in range(3,28,3)])
hdulist = pyfits.open(dat)
pixel_data = hdulist[0].data.squeeze()[:-1,:]
inset_ax = fig.add_axes([0.797, .8315,.77*(1./8), .77*(1./12)])
inset_ax.pcolormesh(pixel_data,cmap=my_cmap,vmin=0,vmax=np.max(pixel_data))
inset_ax.contour(pixel_data, levels=levels, colors='k')
inset_ax.contour(pixel_data, -levels, colors='k') 
beam = Ellipse(xy=(210,140),height=1.06/.003125,width=0.6/.003125,angle=-79.2,facecolor='none',edgecolor='k',hatch='//')
inset_ax.add_patch(beam)
inset_ax.set_xticklabels([])
inset_ax.set_yticklabels([])
inset_ax.set_xticks([])
inset_ax.set_yticks([])

plt.savefig('/home/jliemansifry/Desktop/scoCen_debris_disks_family_portrait.png',dpi=400)
plt.show()
