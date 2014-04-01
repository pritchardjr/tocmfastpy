#!/usr/bin/python
#Jonathan Pritchard
"""
This code is designed to analyse statistics of a box produced by 21cmFast

Underlying this is the Box class, which should contain all relevant info
on the box itself and its parameters and data

"""
from Box import *
from PDF import *
import numpy as np
import os
import math
import string
import matplotlib.pyplot as plt

def boxMean(box):
    """simple mean of box"""
    mean=box.box_data.mean()
    return mean

def boxVar(box):
    """simple variance of box"""
    var=box.box_data.var()
    return var

def boxBasics(box):
    """basic statistics of box. Returns (mean,var)"""
    mean=box.box_data.mean()
    var=box.box_data.var()
    return (mean,var)

def boxPDF(box,NBIN=20):
    """get simple PDF of box as (xmin,xmax,pdf)
    hack here to ensure all data included in straightforward way
    bad since slightly distorts uniform distribution"""
    xmin=box.box_data.min()*0.99999  
    xmax=box.box_data.max()*1.00001

    delta=(xmax-xmin)/(NBIN)
    pdf=np.zeros(NBIN)
    xbin=np.zeros(NBIN)

    data=box.box_data
    pdfsum=0

    #number of elements which fall in to bin
    #trying to do this without a loop over the data elements
    for i in range(NBIN):
        binlow=i*delta+xmin
        binhigh=binlow+delta
        binmid=(binlow+binhigh)/2
        xbin[i]=binmid
        #next line a little convoluted and must be better way of
        #combining the two criterea into one evaluation over box
        nval=((data>=binlow)*(data<binhigh)).nonzero()[0].size
        pdfsum+=nval
        pdf[i]=float(nval)/float(data.size)/delta

    if not pdfsum==data.size:
        print 'Warning: pdf calculation has double counted elements'
        print 'counted=',pdfsum
        print 'expected=',data.size

    pdfV=PDF()
    pdfV.set(xmin,xmax,delta,xbin,pdf)
    #return (xmin,xmax,delta,xbin,pdf,pdfV)
    return pdfV

def boxMinkowski(box):
    """calculate Minkowksi functionals from box

    This is not straightforward...
    """
    mink=1
    return mink


def drawSkewer(box,startpos,direction,length):

    #find positions of skewer
    skewerpos=findSkewer(box,startpos,direction,length)
    skewer=np.zeros(len(skewerpos))
    
    #recover value of box at pixel positions along skewer
    for i in range(len(skewerpos)):
        skewer[i]=box.box_data[(skewerpos[i,0],skewerpos[i,1],skewerpos[i,2])]

    return skewer

def drawCleverSkewer(box,startpos,direction,length):

    #find positions of skewer
    skewerpos=findSkewer(box,startpos,direction,length)
    skewer=np.zeros(len(skewerpos))
    
    #recover value of box at pixel positions along skewer
    for i in range(len(skewerpos)):
        #consider each segment and work out which cells it intersects

        #sum the contributions to get the average element along the skewer
        skewer[i]=box.box_data[(skewerpos[i,0],skewerpos[i,1],skewerpos[i,2])]



    return skewer

def findSkewer(box,startpos,direction,length):
    """Draw a 1D skewer through the box and return an appropriately
    rebinned 1D array with the corresponding data values

    startpos=(x0,y0,z0)   initial position of skewer
    direction=(nx,ny,nz)  direction vector
    length: length of desired skewer in pixels

    Currently does lazy skewer of pixels along path without weighting
    by path length within pixels
    
    """

    dim=box.dim

    #validate parameter values
    if not len(startpos)==3:
        print "Expect startpos to be an array with (x0,y0,z0)"
        return

    startpos=startpos%dim #use periodic condition to map into box

    if not len(direction)==3:
        print "Expect direction to be an array with (nx,ny,nz)"
        return    

    directionnorm=math.sqrt((direction*direction).sum())
    direction=direction/directionnorm  #ensure direction is unit vector

    #now extract skewer
    skewer=np.zeros(int(length))

    #lazy skewer just takes cell value from central value
    #doesn't weight by path length, which would be better

    #first find position of pixels along the skewer
    indx=np.arange(int(length))
    skewerpos=np.zeros((int(length),3))
    for i in range(3):
        skewerpos[:,i]=(indx*direction[i]+startpos[i])%dim

    skewerpos=np.floor(skewerpos)


    return skewerpos


def plotSkewerPath(box,startpos,direction,length):
    """display projection of skewer onto coordinate axis

    """

    dim=box.dim
    skewerpos=findSkewer(box,startpos,direction,length)
    x=skewerpos[:,0]
    y=skewerpos[:,1]
    z=skewerpos[:,2]

    plt.figure(1)
    plt.subplot(1,3,1)
    plt.plot(x,y,marker='.',linestyle='')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis([0,dim,0,dim])
    plt.subplot(1,3,2)
    plt.plot(x,z,marker='.',linestyle='')
    plt.axis([0,dim,0,dim])
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.subplot(1,3,3)
    plt.plot(y,z,marker='.',linestyle='')
    plt.axis([0,dim,0,dim])
    plt.xlabel('Y')
    plt.ylabel('Z')
    plt.show()
    

    return 

def overplotSkewers(box,startpositions):
    #want to show 2D slice from box and draw skewer over it. Then plot the skewer
    indx=0
    box=myrun.slices[i].xH
    slice_data=(box.box_data)[:,:,indx]
    boxtype=1
    (cmap,norm)=tocmpy.boxvisuals.getColourMap(boxtype)
    plt.figure()

    for (k,startposition) in enumerate(startpositions):
        skewerpoints=tocmpy.boxstats.findSkewer(box,startposition,directions[k],length)
        plt.plot(skewerpoints[:,1],skewerpoints[:,0])
  
        plt.imshow(slice_data,cmap,norm=norm)
        plt.title('z=9.9, xH=0.504, 143Mpc box with 200 pixels/side')

        if figflag: plt.savefig('slice.png')

###########################################################################
# Box pdf and conditional pdfs
###########################################################################
def jointPDF(boxX,boxY,Nbins=20,xlimits=None,ylimits=None,normed=True):
    """ Given two boxes X and Y calculate joint p(X,Y) and 1D p(X), p(Y)
    These are essentially just histograms of the data, normalised appropriately
    """
    vecX=np.reshape(boxX,boxX.size)
    vecY=np.reshape(boxY,boxY.size)
    histX,binsX=np.histogram(vecX,Nbins,range=xlimits,density=normed)
    histY,binsY=np.histogram(vecY,Nbins,range=ylimits,density=normed)
    histXY,xedges,yedges=np.histogram2d(vecX,vecY,[binsX,binsY],normed=normed)
    return binsX,binsY,histX,histY,histXY

def conditionalPDF(boxX,boxY,Nbins=20,xlimits=None,ylimits=None,normed=True):
    """ Given two boxes X and Y calculate p(X|Y) and p(X), p(Y)

    Conditionals are given by p(X,Y)=p(X|Y)p(Y)=p(Y|X)p(X)
    so p(X|Y)=p(X,Y)/p(Y) and p(Y|X)=p(X,Y)/p(X)
    """

    NYbins=Nbins
    
    vecX=np.reshape(boxX,boxX.size)
    vecY=np.reshape(boxY,boxY.size)
    histX,binsX=np.histogram(vecX,Nbins,range=xlimits,density=normed)
    histY,binsY=np.histogram(vecY,NYbins,range=ylimits,density=normed)
    histXY,xedges,yedges=np.histogram2d(vecX,vecY,[binsX,binsY],normed=normed)

    histXcY=histXY/histY
    histYcX=(histXY.T/histX).T    
    
    return binsX,binsY,histX,histY,histXY,histXcY,histYcX
