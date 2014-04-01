#!/usr/bin/python
#Jonathan Pritchard
"""
This code provides options for visualising a 21cmFast box.

Unclear whether plotting delta or 1+delta is better. If I plot 1+delta then
its possible to plot on a log scale, which amplifies the contrast for overdense
regions

"""

mayaviflag=True

import os
import re
import sys
import math
import string
import matplotlib as mlab
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
#Mayavi not available in 64bit EPD distribution, so catch the exception
try:
  import mayavi.mlab as mlab
except:
  print "mayavi module not available, so disabling 3D plotting"
  mayaviflag=False
  
import time
import commands
import numpy
import Image
import Box
import Run
from matplotlib import mpl,pyplot

def lutForTBMap():
  """ produce a look up table for a red-black-blue colormap"""
  cmap=mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['blue','black','red'],
                                           256)
  #I'm not entirely sure what this lower is for. Its used with mayavi
  lut=[]
  for i in range(256):
    lut.append(cmap.__call__(i,bytes=True))
               
  return cmap


def getColourMap(boxtype):
  """ Work out which colourmap is needed for the specified boxtype and
  return the colourmap and normalisation bounds

  returns (cmap,norm)
  """
  if boxtype ==0:
    cmap=lutForTBMap()
    cmap=cm.Greys_r
    norm = mpl.colors.Normalize(vmin = 0.0, vmax = 10.0, clip = True)
  elif boxtype==1:
    cmap=cm.Greys_r
    norm=None   
  else:
    cmap=lutForTBMap()
    norm = mpl.colors.Normalize(vmin = -100.0, vmax = 100.0, clip = True)

  return (cmap,norm)


def show_slice(box,indx,boxtype):
  """from Box object produce a slice and display it"""
  slice_data=box.box_data[:,indx,:]

  if boxtype==0:
    print "plotting delta+1"
    slice_data=(box.box_data+1)[:,indx,:]

  #print slice_data
  (cmap,norm)=getColourMap(boxtype)
  
  img=plt.imshow(slice_data,cmap,norm=norm)

  #label image with redshift
  txt='z=%3f' % box.z
  xpos=box.dim/2
  ypos=0
  plt.text(xpos,ypos,txt)

  #display image to screen
  plt.show(img)
  
  #filename='slice.png'
  #plt.savefig(filename,format='png')
  
  return img

def movie(myrun,boxtype):
  """ Make a movie from a Run object. This makes individual frames as png
  files and then uses an external call to ffmpeg to make a mov file that
  combines the individual frames.

  TO DO: options for colour map, selecting which 21cmFast box to use, and
  which index position to use

  Parameters:
  boxtype - determine which of the six available boxes to use
  0:density 1:xH 2:vx 3:vy 4:vz 5:deltaT
  currently handles boxtype<1: xH otherwise deltaT
  
  """

  makeframes(myrun,boxtype)
  makemovie()
  return

def makeframes(myrun,boxtype):
  """ make a set of sequentially numbered frames from a Run object for
  use in making a movie from the simulation

  WARNING: there seems to be some memory lekage somewhere. Increase in memory
  used by python with each iteration
  
  """

  savedir='./'

  indx=0

  #set colour map for figures
  (cmap,norm)=getColourMap(boxtype)

  #make individual frames
  for j in range(1,len(myrun.slices)):
    #run through slices from high-redshift to low
    i=len(myrun.slices)-j
    
    #from the box data make a slice
    myrun.slices[i].loaddata()
    if boxtype==0:
      #slice_data=myrun.slices[i].density.box_data[:,indx,:] #delta
      slice_data=(myrun.slices[i].density.box_data+1)[:,indx,:] #delta+1
    elif boxtype==1:
      slice_data=myrun.slices[i].xH.box_data[:,indx,:]
    else:
      slice_data=myrun.slices[i].deltaT.box_data[:,indx,:]
      
    img=plt.imshow(slice_data,cmap,norm=norm)
    
    fname='volume_slice_frame%03d.png' % j
    filename=os.path.join(savedir,fname)
    print filename
    #plt.show()
    plt.savefig(filename,format='png')
    myrun.slices[i].forgetdata()

  print 'frames made'
  return
  
def makemovie():
  """ From a set of sequentially ordered frames use ffmpeg to make a
  movie
  """
  #call ffmpeg to make a movie
  # -r controls the framerate in frames/second

  #TO DO LIST:
  #1) needs better handling in case ffmpeg asks for user response
  #2) needs to handle overwriting anim.mov if that exists
  #3) should be able to handle an input ordered list of arbitrarily named files
  # i.e. by copying files to temporary sequentially numbered files, making
  # movie and then deleting the files
  #4) needs to handle input directories for input files and output movie

  #obsolete version of the command -sameq key. but depreciated
  #cmd='ffmpeg -f image2 -r 5 -i ./volume_slice_frame%03d.png -sameq ./anim.mov -pass 2'

  #new version. -pix_fmt yuv420p needed to get more than blank output.
  cmd="ffmpeg -f image2 -r 5 -c:v png -i ./volume_slice_frame%03d.png -pix_fmt yuv420p ./anim.mov"
  (status,output)=commands.getstatusoutput(cmd)
  print status
  return
