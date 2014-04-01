#!/usr/bin/python
#Jonathan Pritchard
"""
This code provides options for visualising a 21cmFast box.
"""

import os
import re
import sys
import math
import string
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import mayavi.mlab as mlab
import time
import commands
import numpy
import Image
import Box
from matplotlib import mpl,pyplot

def lutForTBMap():
  """ produce a look up table for a red-black-blue colormap"""
  cmap=mpl.colors.LinearSegmentedColormap.from_list('my_colormap',
                                           ['blue','black','red'],
                                           256)
  lut=[]
  for i in range(256):
    lut.append(cmap.__call__(i,bytes=True))
               
  return lut

def show_slice(box_data,indx):
  """from box_data produce a slice and display it"""
  slice_data=box_data[:,indx,:]

  #print slice_data
  img=plt.imshow(slice_data,cmap=cm.Greys_r)

  
  #plt.show(img)
  
  filename='slice.png'
  plt.savefig(filename,format='png')
  
  return

def show_box(box_data):
  """from box_data produce a 3D image of surfaces and display it"""

  use_color_flag=True
  reverse_redshift_flag=True

  (dimx,dimy,dimz)=box_data.shape
  print box_data.shape

  mycolor='black-white'

  if use_color_flag:
      mycolor='blue-red'
      mycolor='RdBu'
      #need to set color scale to be symmetric around zero

  if reverse_redshift_flag:
    print 'want to be able to reseverse long axis ordering'
    box_data=numpy.flipud(box_data)
    #box_data=box_data[:,::-1,:]

  print box_data.min(), box_data.max()
  #clip_data
  clip=30.0
  vmax=clip
  vmin= -clip
  box_data[box_data>vmax]=vmax
  box_data[box_data<vmin]=vmin
  
  print box_data.min(), box_data.max()
  c_black=(0.0,0.0,0.0)
  c_white=(1.0,1.0,1.0)

  #s=box_data
  mlab.figure(1,bgcolor=c_white,fgcolor=c_black)
  planex=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(box_data),
                            plane_orientation='x_axes',
                            slice_index=dimx-1,colormap=mycolor
                        )
  planey=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(box_data),
                            plane_orientation='y_axes',
                            slice_index=dimy-1,colormap=mycolor
                        )

  planez=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(box_data),
                            plane_orientation='z_axes',
                            slice_index=dimz-1,colormap=mycolor
                        )

  # colormap='blue-red' may be useful for 21 cm brightness maps
  # although it passes through white not black
  


  #now try to invert the color scheme

  lut=planez.module_manager.scalar_lut_manager.lut.table.to_array()
  lut=numpy.flipud(lut)
  #lut=lutForTBMap()
  #print help(lut)
  planex.module_manager.scalar_lut_manager.lut.table = lut
  planey.module_manager.scalar_lut_manager.lut.table = lut
  planez.module_manager.scalar_lut_manager.lut.table = lut

  mlab.draw()  #force update of figure

  mlab.colorbar()
  mlab.outline(color=c_black)
  
  #mlab.show()

  filename='volume_slice.png'
  figsave=mlab.gcf()
  #mlab.savefig(filename,figure=figsave,magnification=4.)
  mlab.savefig(filename,size=(1800,800),figure=figsave,magnification=4)
  mlab.close()

  #Can't get MayaVi to output a good eps, so use PIL to convert
  im = Image.open(filename)
  im.save("volume_slice.eps")
  
  return

def parse_box(box_data,indx):
  """
  from box_data produce a 3D image of surfaces and display it using an
  animation of a slice moving back and forth through the box
  NOT FUNCTIONAL AT PRESENT - NEED TO WORK OUT THE MAYAVI SYNTAX
  -can't get different slices to display in a nice fashion
  """

  s=box_data
  sp=1-box_data

  mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                            plane_orientation='z_axes',
                            slice_index=0,colormap='black-white'
                        )
  mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                            plane_orientation='x_axes',
                            slice_index=0,colormap='black-white'
                        )
  l=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                            plane_orientation='y_axes',
                            slice_index=0,colormap='black-white'
                        )


  #s=sp

  fig=mlab.gcf()
  ms=l.mlab_source
  print 'indx=',dir(ms)
  for i in range(90):
    #l=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
    #                        plane_orientation='y_axes',
    #                        slice_index=i,colormap='black-white'
    #                    )
    if(i%2):
      ms.reset(scalars=sp)
    else:
      ms.reset(scalars=s)
      
    #print dir(ms)
    #print ms
    #camera=fig.scene.camera
    #camera.yaw(i)
    fig.scene.reset_zoom()
    mlab.draw()
    filename='volume_slice_frame'+str(i)+'.png'
    print filename
    #mlab.savefig(filename)
    
  mlab.show()
    
  return


def parse_boxes(filenames, dim):
  """from a list of filenames to 21cmFast output order them and make a movie
  using ffmpeg"""

  savedir='./slice_temp'
  if not os.path.isdir(savedir):
    os.mkdir(savedir)
  boxes=[]
  redshifts=[]
  for filename in sorted(filenames,reverse=True):
    param_dict=parse_filename(filename)
    box_data=open_box(filename,dim)
    boxes.append(box_data)
    redshifts.append(param_dict['z'])

  s=boxes[0]
  indx=dim-1
  lz=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                            plane_orientation='z_axes',
                            slice_index=indx,colormap='black-white'
                        )
  lx=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                            plane_orientation='x_axes',
                            slice_index=indx,colormap='black-white'
                        )
  ly=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                            plane_orientation='y_axes',
                            slice_index=indx,colormap='black-white'
                        )

  titlestr='z=%3.2d' % redshifts[0]
  tit=mlab.text(0.1,0.9,titlestr,width=0.1)
  #s=sp

  fig=mlab.gcf()
  msx=lx.mlab_source
  msy=ly.mlab_source
  msz=lz.mlab_source
  
  for i in range(1,len(boxes)):
    #l=mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
    #                        plane_orientation='y_axes',
    #                        slice_index=i,colormap='black-white'
    #                    )
    msx.reset(scalars=boxes[i])
    msy.reset(scalars=boxes[i])
    msz.reset(scalars=boxes[i])
    
    #print dir(ms)
    #print ms
    #camera=fig.scene.camera
    #camera.yaw(i)
    titlestr='z=%3.2d' % redshifts[i]
    mlab.text(0.1,0.9,titlestr,width=0.1)
    #fig.reset(text=titlestr)
    fig.scene.reset_zoom()
    mlab.draw()
    #time.sleep(1)
    fname='volume_slice_frame%03d.png' % i
    filename=os.path.join(savedir,fname)
    print filename
    mlab.savefig(filename)

  mlab.close()
  #mlab.show()
  #call ffmpeg to make a movie
  # -r controls the framerate in frames/second
  #needs better handling in case ffmpeg asks for user response
  cmd='ffmpeg -f image2 -r 5 -i ./slice_temp/volume_slice_frame%03d.png -sameq ./slice_temp/anim.mov -pass 2'
  (status,output)=commands.getstatusoutput(cmd)
  print status
  
  return
