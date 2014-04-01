""" Class for handling a 21cmfast data run
maintain list of run data and location of boxes
if boxes read in to memory then remember that too"""

import numpy

class Box:
    def __init__(self):
        self.name='my name'
        self.box_data=[]
        self.dim=[]
        self.param_dict={}
        self.init=False
        self.z= -1
        return

    def info(self):
        #report info on box
        print 'initialised=',self.init
        print 'dim=',self.dim
        return

    def setBox(self,box_data,param_dict):
        #initialise Box from box_data and param_dict
        self.box_data=box_data
        self.param_dict=param_dict
        self.dim=param_dict['dim']
        self.init=True
        self.z=param_dict['z']
        return

    def getBoxStats(self):
        if self.init:
            print 'box_data exists'
            self.mean=self.box_data.mean()
            self.var=self.box_data.var()
        else:
            print 'box_data has not been initialised'
            self.mean=0.0
            self.var=0.0

        print 'mean=',self.mean, ' var=',self.var
        return
    
    def boxToOverdensity(self):
        """Renormalise the box to scaled variable delta=(x-xmean)/xmean"""
        if self.init:
            self.getBoxStats()
            self.box_data=(self.box_data-self.mean)/self.mean

        else:
            print 'box_data has not been initialised'

        self.getBoxStats()
        return

    def boxFromThreshold(self,crit_delta):
        #produce new box with all zeros
        newbox=numpy.zeros(self.box_data.shape)
        newbox[self.box_data<=crit_delta]=1
        return newbox

    def thresholdFromVolume(self,vol_frac):
        """given a volume fraction find the threshold delta_crit that
        divides box values below that from box values above that. """

        #work in terms of number of pixels that need to be below threshold
        count_frac=int(vol_frac*self.box_data.size)
        #use ordered list of all box elements
        indx=self.box_data.copy()   #this is memory inefficient
        indx=indx.reshape((indx.size))
        indx.sort()
        #find threshold value
        crit_delta=indx[count_frac]
        
        return crit_delta
