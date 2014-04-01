""" Class for handling a 21cmfast data run
maintain list of run data and location of boxes


Updated version will hold files in Slice classes to impose some
structure on the data set and allow for better recall.

Run contains an individual Slice for each redshift. Each Slice contains a Box
for each of the 21cmFast output files for a single redshift. The individual
box contains a filename initially, but data can be loaded in to memory or
removed from memory easily within the wrapper the Box provides.

EXAMPLE USAGE:
     import tocmfastpy as TOCM
     basedir='../../../catherine/21cmStatistics/code/21cmFAST/Boxes/'
     myrun=TOCM.runio.loadslices(basedir,200,143)
     myrun.info()

     will find all files associated with a HIIDIM=200, 143 Mpc box output
     from 21cmFast into Boxes/

     Cn then access Box data using something like
     myrun.slices[3].loaddata()
     myrun.slices[3].xH.box_data[1][1][2]
     myrun.slices[3].xH.getBoxStats()
     myrun.slices[3].forgetdata()

BUG: Currently doesn't store the full resolution boxes from the initialisation
     in the file structure. These are the deltak_ and deltax_ boxes, which
     are unusual filenames and should be handled differently by the Slice.

Last modified: 2 Jan 2012
"""

from Slice import *
import boxio
import numpy
import os.path
import sys
import re


class Run:
    def __init__(self):
        self.name=''
        self.dir=''
        self.filenames=[]
        self.slices=[]
        self.redshifts=[]
        self.dim=0
        self.boxsize=0
        self.init=False
        return

    def len(self):
        """return the number of slices"""
        return len(self.slices)

    def info(self):
        """summarise the contents of the Run instance"""
        count=0
        for slice in self.slices:
            if slice.init:
                count+=1
                slice.info()

        print "Run contains", len(self.slices), "Slices with ", count," containing files"
        print "Nominal redshifts are:\n"
        print self.redshifts
            
        return


    def listfiles(self):
        """rebuild dict of all files contained within Run instance"""
        filedict={}
        for (indx,slice) in enumerate(self.slices):
            filedict[self.redshifts[indx]]=slice.info()

        return filedict


    def setFromDict(self,filedict):
        """given dictionary of form {z,filenames} set up Run as a
        collection of Slices
        """
        
        for z in sorted(filedict.keys()):
            slice=Slice()
            files=filedict[z]
            slice.assignFiles(files)
            self.slices.append(slice)
            self.redshifts.append(z)

        return
