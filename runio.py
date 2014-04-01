#!/usr/bin/python
#Jonathan Pritchard
""" Class for handling a 21cmfast data run
maintain list of run data and location of boxes

interfaces with the Run class to store data in Slice objects

organisation is a little strange here. In some ways should be associated
with Run class directly, but python makes that harder than I'd like
therefore arrange as helper functions

"""

from Run import *
import boxio
import numpy
import os.path
import sys
import re

def loadslices(base,dim,boxsize):
    """from specified directory base find all 21cm boxes with
    pixel dimensions dim and boxlength boxsize and sort them
    into a list of Slices"""

    #first identify relevant files
    filenames=findrun(base,dim,boxsize)

    #now sort them into redshift collections
    filedict=dictByRedshift(filenames)

    print filedict

    myrun=Run()
    myrun.setFromDict(filedict)

    return myrun


def findrun(base,dim,boxsize):
    """ find all files associated with run given base directory
    and the resolution size and box length """

    if not os.path.isdir(base):
        print base, 'is not a valid directory'
        sys.exit(1)

    #retreive all files that match tag and box size
    #note this will include the initialisation boxes, which
    #are independent of redshift
    searchstr='_'+str(dim)+'_'+str(boxsize)+'Mpc'
    filenames=os.listdir(base)

    box_files=[]
    for filename in filenames:
        if filename.find(searchstr)>=0:
            box_files.append(os.path.join(base,filename))

    return box_files


def locateboxes(filenames,prefix):
    """ from a prefix locate all of the relevant boxes in the run"""
    boxes=[]
    if self.init:
        for filename in filenames:
            (base,fname)=os.path.split(filename)
            if fname.find(prefix)==0:
                boxes.append(filename)

    if len(boxes)==0:
        print 'prefix was not found in run'

    return sorted(boxes)


def dictByRedshift(filenames):
    """reorder the files by redshift and return a dictionary
    {z,filenames}
    """

    #shortdict=[]
    longdict={}
    for filename in filenames:
        match=re.search('_z([0-9.]+)',filename)
        if match:
            z=float(match.group(1))
        else:
            #initialisation boxes are labelled with z=0.0 in 21cmFast
            #standard output or without a redshift label
            z=0.0

        #shortdict.append((z,filename))
        if z in longdict.keys():
            longdict[z].append(filename)
        else:
            longdict[z]=[filename]

    return longdict
    #return shortdict


def listWithRedshift(filenames):
    """reorder the files by redshift and return a dictionary
    {z,filenames}
    """

    shortdict=[]
    longdict={}
    for filename in filenames:
        match=re.search('_z([0-9.]+)',filename)
        if match:
            z=float(match.group(1))
        else:
            #initialisation boxes are labelled with z=0.0 in 21cmFast
            #standard output or without a redshift label
            z=0.0

        shortdict.append((z,filename))
        if z in longdict.keys():
            longdict[z].append(filename)
        else:
            longdict[z]=[filename]

    return longdict
    return shortdict


def filesByRedshift(filenames):
    """return filenames ordered by redshift"""
    shortdict=listWithRedshift(filenames)
    #need to sort on float(z) since str(z) doesn't order properly
    new_filenames=[]
    for tuple in sorted(shortdict):
        new_filenames.append(tuple[1])

    return new_filenames


def getRedshiftList(filenames):
    """ from Run filenames get the redshifts"""

    redshifts=[]
    for filename in filenames:
        param_dict=boxio.parse_filename(filename)
        redshifts.append(param_dict['z'])

    return redshifts

