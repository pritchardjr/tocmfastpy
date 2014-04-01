#!/usr/bin/python
#Jonathan Pritchard
"""
Class: PDF

This class is designed to hold a statistical 1D PDF with details on the
value in different bins and the minimum and maximum values

Data is held as a histogram of points with midpoints in the array xbin
and pdf in the array pdf.


"""

import numpy as np
import os
import math

class PDF:
    """Define PDF class for holding a box PDF"""
    def __init__(self):
        self.init=False
        self.delta=0  #bin width
        self.xmin=0   #lowest x value
        self.xmax=0   #highest x value
        self.nbin=0   #number of bins
        self.xbin=0   #midpoints of bins
        self.pdf=0    #value of PDF in each bin
        return

    def set(self,xmin,xmax,delta,xbin,pdf):
        """set PDF from array of data
        (xmin,xmax) are limits of PDF
        delta is the bin size
        xbin is array of midpoints
        pdf is the normalised pdf so that sum(pdf*delta)=1
        """
        self.init=True
        self.xmin=xmin
        self.xmax=xmax
        self.nbin=xbin.size
        self.delta=delta
        self.xbin=xbin
        self.pdf=pdf
        return

    def setFromFreq(self,xmin,xmax,delta,xbin,freq):
        """set PDF from histogram of frequencies
        pdf=freq/sum(freq)/delta with delta the bin size
        """
        self.init=True
        self.xmin=xmin
        self.xmax=xmax
        self.nbin=xbin.size
        self.delta=delta
        self.xbin=xbin
        self.pdf=freq/freq.sum()/delta
        return

    def getIndx(self,x):
        """get position in PDF array of value x"""
        #error check on bounds
        if (x<self.xmin or x>self.xmax):
            print "Value x=",x," is out of range"
            return -1

        #get index of bin
        indx=int((x-self.xmin)/self.delta)
        return indx

    def getValue(self,x):
        """get value of PDF at specified point"""
        if not self.init:
            print "PDF not initialised"
            return 0.0
        
        indx=self.getIndx(x)
        if indx<0:
            return -1
        
        val=self.pdf[indx]
        return val

    def getMean(self):
        """integrate over PDF to get the mean of the distribution
        Since midpoints are stored in xbin, this is the integral using
        those midpoints.

        integrating against the weights w(x) gives
        W(x)=\int delta*pdf*w(xbin)

        for mean: w(x)=x

        """
        kernel=self.pdf*self.xbin
        mean=kernel.sum()*self.delta

        return mean

    def getVar(self):
        """integrate over PDF to get the variance of the distribution
        Since midpoints are stored in xbin, this is the integral using
        those midpoints.

        integrating against the weights w(x) gives
        W(x)=\int delta*pdf*w(xbin)

        For var: w(xbin)=(xbin-mean)**2

        """
        mean=self.getMean()
        kernel=self.pdf*(self.xbin-mean)**2
        mean=kernel.sum()*self.delta

        return mean

    def getNMoment(self,Nmom):
        """integrate over PDF to get the Nth moment of the distribution
        Since midpoints are stored in xbin, this is the integral using
        those midpoints.

        integrating against the weights w(x) gives
        W(x)=\int delta*pdf*w(xbin)

        For Nth moment: w(xbin)=(xbin-mean)**N
        Note N=0: should check normalisation of pdf
             N=1: should give zero
             N=2: gives variance
             N=3: gives skew
             N=4: gives kertosis

        Discretisation error should be expected
        """
        mean=self.getMean()
        kernel=self.pdf*(self.xbin-mean)**Nmom
        mean=kernel.sum()*self.delta

        return mean
