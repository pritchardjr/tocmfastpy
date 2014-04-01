""" Class for handling a single redshift entry from 21cmFast

Held as relevant boxes as either a string filename or a Box instance.
This allows Slice to know if existence of relevant boxes even if they
are not currently loaded into memory

Individual boxes can then be accessed directly or via wrapper routines

TO DO:
1) enable access to boxes via name e.g. "XH", "VX" and so on. Maybe via
dictionary or something


"""

from Box import *
import numpy as np
import os.path
import boxio

class Slice:
    """This is the Slice class"""
    boxtypedict={'density':0,'xh':1,'vx':2,'vy':3,'vz':4,'deltaT':5}
    
    def __init__(self):
        self.init=False
        #storage of data relating to boxes
        self.density=False   #overdensity
        self.xH=False        #neutral fraction
        self.vx=False        #velocity x
        self.vy=False        #velocity y
        self.vz=False        #velocity z
        self.deltaT=False    #21cm brightness
        self.fdensity=''   #overdensity file
        self.fxH=''        #neutral fraction file
        self.fvx=''        #velocity x file
        self.fvy=''        #velocity y file
        self.fvz=''        #velocity z file
        self.fdeltaT=''    #21cm brightness file
        return


    def info(self):
        """print information on the Slice instance and return list of
        filenames

        """
        print "this Slice instance has the following filenames"
        print self.fdensity
        print self.fxH
        print self.fvx
        print self.fvy
        print self.fvz
        print self.fdeltaT
        print "\n"

        files=[]
        files.append(self.fdensity)
        files.append(self.fxH)
        files.append(self.fvx)
        files.append(self.fvy)
        files.append(self.fvz)
        files.append(self.fdeltaT)
        
        return files
    

    def assignFiles(self,files):
        """from list of files work out which are which and assign Slice

        Also basic checking that all correspond to same redshift
        """

        #default to no file present
        fdensity=''
        fxH=''
        fvx=''
        fvy=''
        fvz=''
        fdeltaT=''

        for file in files:
            param_dict=boxio.parse_filename(file)
            
            if (param_dict['type'] =='density'):
                fdensity=file
            elif  (param_dict['type'] =='xh'):
                fxH=file
            elif  (param_dict['type'] =='vx'):     
                fvx=file
            elif  (param_dict['type'] =='vy'):     
                fvy=file
            elif  (param_dict['type'] =='vz'):     
                fvz=file
            elif  (param_dict['type'] =='deltaT'):     
                fdeltaT=file
                
        self.setFiles(fdensity,fxH,fvx,fvy,fvz,fdeltaT)
        return
    

    def setFiles(self,fdensity,fxH='',fvx='',fvy='',fvz='',fdeltaT=''):
        """provide paths to the files containing the individual boxes
        output by 21cmFast

        Error checking limited to making sure file exists. User responsible
        for making sure they correspond to the same box!
        Order: (density,xH,vx,vy,vz,deltaT).
        """
        if(os.path.exists(fdensity)):
            print 'set density'
            self.fdensity=fdensity
        if(os.path.exists(fxH)):
            print 'set xH'
            self.fxH=fxH
        if(os.path.exists(fvx)):
            print 'set vx'
            self.fvx=fvx
        if(os.path.exists(fvy)):
            print 'set vy'
            self.fvy=fvy
        if(os.path.exists(fvz)):
            print 'set vz'
            self.fvz=fvz
        if(os.path.exists(fdeltaT)):
            print 'set deltaT'
            self.fdeltaT=fdeltaT

        if self.fdensity or self.fxH or self.vx or self.vy or self.vz or self.deltaT:
            self.init=True
            
        return

    def loaddataS(self,labels):
        """ Load data using string labels

        Could do with some error handling if labels aren't valid options
        """
        filter=[False,False,False,False,False,False]

        for label in labels:
            print label
            if label in self.boxtypedict:
                filter[self.boxtypedict[label]]=True
        loaddata(filter)
        return

    def loaddata(self,filter=[True,True,True,True,True,True]):
        """Using filenames load data into memory

        filter is an optional tuple of booleans specifying which data should
        be loaded (density,xH,vx,vy,vz,deltaT). Default is load all
        """
        
        if(os.path.exists(self.fdensity) and filter[0]):
           print "loading...",self.fdensity
           self.density=boxio.readbox(self.fdensity)
        if(os.path.exists(self.fxH) and filter[1]):
           print "loading...",self.fxH
           self.xH=boxio.readbox(self.fxH)
        if(os.path.exists(self.fvx) and filter[2]):
           print "loading...",self.fvx
           self.vx=boxio.readbox(self.fvx)
        if(os.path.exists(self.fvy) and filter[3]):
           print "loading...",self.fvy
           self.vy=boxio.readbox(self.fvy)
        if(os.path.exists(self.fvz) and filter[4]):
           print "loading...",self.fvz
           self.vz=boxio.readbox(self.fvz)
        if(os.path.exists(self.fdeltaT) and filter[5]):
           print "loading...",self.fdeltaT
           self.deltaT=boxio.readbox(self.fdeltaT)
           
        return

    def forgetdata(self):
        """remove data on boxes from memory"""
        print "Forgetting data in Slice"
        self.density=False   #overdensity
        self.xH=False        #neutral fraction
        self.vx=False        #velocity x
        self.vy=False        #velocity y
        self.vz=False        #velocity z
        self.deltaT=False    #21cm brightness
        return

    def pixel(self,inpos):
        """from tuple (x,y,z) return tuple of pixel values
        Order: (density,xH,vx,vy,vz,deltaT)

        Error checks that data is stored in Box class before trying to
        obtain value

        I'd love to vectorise this routinue so that is would work for
        an array of position values! i.e. an N by 3 array
        
        """
        pos=tuple(inpos)  #little annoying, but this helps pass a numpy array

        #set default values
        density=0
        xH=0
        vx=vy=vz=0
        deltaT=0
        self.init=True
        #get value from boxes if they exist
        if isinstance(self.density,Box):
            density=self.density.box_data[pos]
        if isinstance(self.xH,Box):
            xH=self.xH.box_data[pos]
        if isinstance(self.vx,Box):
            vx=self.vx.box_data[pos]
        if isinstance(self.vy,Box):
            vy=self.vy.box_data[pos]
        if isinstance(self.vz,Box):
            vy=self.vz.box_data[pos]
        if isinstance(self.deltaT,Box):
            deltaT=self.deltaT.box_data[pos]
            
        return (density,xH,vx,vy,vz,deltaT)
